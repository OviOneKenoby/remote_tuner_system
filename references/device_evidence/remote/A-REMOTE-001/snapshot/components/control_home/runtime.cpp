#include "diagnostics/api.hpp"
#include "control_home/development.hpp"
#include "control_home/power_suspend.hpp"
#include "network_manager/api.hpp"
#include "power_management/api.hpp"
#include "driver/usb_serial_jtag.h"
#include "driver/usb_serial_jtag_vfs.h"
#include "esp_heap_caps.h"
#include "esp_log.h"
#include "esp_memory_utils.h"
#include "esp_random.h"
#include "esp_timer.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include <cstdio>

namespace control_home {
namespace {
Channel channel;
portMUX_TYPE mux = portMUX_INITIALIZER_UNLOCKED;
TaskHandle_t owner = nullptr;
bool started = false;
std::size_t live = 0, allocations = 0, frees = 0, failures = 0;
bool corrupt = false;
void observer(void *p, std::size_t bytes, bool allocated) {
  if (xTaskGetCurrentTaskHandle() != owner)
    corrupt = true;
  if (!p) {
    ++failures;
    return;
  }
  if (allocated) {
    ++allocations;
    live += bytes;
  } else {
    ++frees;
    if (live < bytes)
      corrupt = true;
    else
      live -= bytes;
  }
}
void telemetry(const char *stage) {
  multi_heap_info_t internal{}, external{};
  heap_caps_get_info(&internal, MALLOC_CAP_INTERNAL | MALLOC_CAP_8BIT);
  heap_caps_get_info(&external, MALLOC_CAP_SPIRAM | MALLOC_CAP_8BIT);
  ESP_LOGI(
      "UC_RUNTIME",
      "stage=%s INT free=%u min=%u largest=%u PSRAM free=%u min=%u largest=%u",
      stage, unsigned(internal.total_free_bytes),
      unsigned(internal.minimum_free_bytes),
      unsigned(internal.largest_free_block),
      unsigned(external.total_free_bytes),
      unsigned(external.minimum_free_bytes),
      unsigned(external.largest_free_block));
  unsigned rejected;
  portENTER_CRITICAL(&mux);
  rejected = unsigned(channel.rejected);
  portEXIT_CRITICAL(&mux);
  ESP_LOGI(
      "UC_RUNTIME",
      "stage=%s payload=%u allocations=%u frees=%u failed_allocations=%u "
      "accounting_corrupt=%u stack_min_bytes=%u owner_ok=%u queue_rejected=%u",
      stage, unsigned(control::Memory::used), unsigned(allocations),
      unsigned(frees), unsigned(failures),
      unsigned(corrupt || live != control::Memory::used),
      unsigned(uxTaskGetStackHighWaterMark(nullptr)),
      unsigned(xTaskGetCurrentTaskHandle() == owner), rejected);
}
bool is_owner(void *) { return xTaskGetCurrentTaskHandle() == owner; }
void task(void *) {
  owner = xTaskGetCurrentTaskHandle();
  vTaskDelay(pdMS_TO_TICKS(5000)); // unchanged factory startup finishes first
  ESP_LOGI("UC_RUNTIME",
           "BEGIN synthetic_only=1 profile=0 owner_cpu=%d stack_bytes=24576",
           int(xPortGetCoreID()));
  if (control::Memory::used || control::Memory::observer) {
    ESP_LOGE("UC_RUNTIME", "FAIL allocator ownership");
    vTaskDelete(nullptr);
    return;
  }
  control::Memory::observer = observer;
  void *block = heap_caps_malloc(sizeof(development::Session),
                                 MALLOC_CAP_SPIRAM | MALLOC_CAP_8BIT);
  if (!block) {
    control::Memory::observer = nullptr;
    ESP_LOGE("UC_RUNTIME", "FAIL runtime allocation");
    vTaskDelete(nullptr);
    return;
  }
  char epoch[64];
  std::snprintf(epoch, sizeof epoch, "home.synthetic.boot:%08lx",
                static_cast<unsigned long>(esp_random()));
  auto *s = new (block) development::Session(control::Id(epoch), is_owner, nullptr);
  auto now = [] { return control::U64(esp_timer_get_time() / 1000); };
  if (!s->initialize(now())) {
    s->~Session();
    heap_caps_free(block);
    control::Memory::observer = nullptr;
    ESP_LOGE("UC_RUNTIME", "FAIL initialization");
    vTaskDelete(nullptr);
    return;
  }
  ESP_LOGI("UC_RUNTIME", "wrapper_bytes=%u wrapper_psram=%u",
           unsigned(sizeof(*s)), unsigned(esp_ptr_external_ram(s)));
  // IDF 5.5.3's nonblocking no-driver VFS read sees only driver-buffered
  // availability, so opening /dev/secondary alone never receives a byte.
  // Install the bounded RX/TX driver; keep logs on the same USB interface.
  usb_serial_jtag_driver_config_t input_config =
      USB_SERIAL_JTAG_DRIVER_CONFIG_DEFAULT();
  const esp_err_t input_status =
      usb_serial_jtag_is_driver_installed()
          ? ESP_OK
          : usb_serial_jtag_driver_install(&input_config);
  if (input_status == ESP_OK)
    usb_serial_jtag_vfs_use_driver();
  ESP_LOGI("UC_MOCK",
           "DEVELOPMENT_ONLY MOCK_ONLY input=%s init=%s keys=p a u 0 1 v d r - "
           "+ o c s "
           "l n f m",
           input_status == ESP_OK ? "USB_SERIAL_JTAG_DRIVER" : "UNAVAILABLE",
           esp_err_to_name(input_status));
  telemetry("initialized");
  development::PowerSuspend suspension;
  bool power_attempted = false, resume_warned = false;
  auto publish = [&] {
    auto snapshot = s->snapshot();
    portENTER_CRITICAL(&mux); channel.publish(snapshot); portEXIT_CRITICAL(&mux);
  };
  auto drain_input = [&] {
    char discarded[256];
    if (input_status == ESP_OK) (void)usb_serial_jtag_read_bytes(discarded, sizeof discarded, 0);
  };
  control::U64 acquisition = now(), diagnostic_time=0, diagnostic_session=0, diagnostic_revision=0;
  while (true) {
    const auto time = now();
    const auto ds=s->snapshot();
    if(time-diagnostic_time>=1000 || ds.session!=diagnostic_session || ds.capability_revision!=diagnostic_revision) {
      diagnostics::Core d{}; d.time=time; multi_heap_info_t internal{},external{};
      heap_caps_get_info(&internal,MALLOC_CAP_INTERNAL|MALLOC_CAP_8BIT);heap_caps_get_info(&external,MALLOC_CAP_SPIRAM|MALLOC_CAP_8BIT);
      unsigned qr;portENTER_CRITICAL(&mux);qr=unsigned(channel.rejected);portEXIT_CRITICAL(&mux);
      auto q=s->boundary.inbox.counts();const auto &c=s->boundary.counts;
      d.values={ds.session,ds.capability_revision,s->device.mock.dispatches,control::Memory::used,allocations,frees,failures,corrupt||live!=control::Memory::used,xTaskGetCurrentTaskHandle()==owner,qr,uxTaskGetStackHighWaterMark(nullptr),internal.total_free_bytes,internal.minimum_free_bytes,internal.largest_free_block,external.total_free_bytes,external.minimum_free_bytes,external.largest_free_block,q.posted,q.rejected,q.overflow,q.busy,c.applied,c.stale,c.invalid,c.refused,c.lifecycle,c.discarded};
      diagnostics::publish(d);
      if(ds.session!=diagnostic_session || ds.capability_revision!=diagnostic_revision)diagnostics::event(time,diagnostics::Event::CORE,unsigned(ds.session));
      diagnostic_time=time;diagnostic_session=ds.session;diagnostic_revision=ds.capability_revision;
    }
    if (power_management::owner_request() != power_management::Request::NONE) {
      if (!power_attempted) {
        power_attempted = true;
        bool ok = suspension.park(*s, time, power_management::owner_request() == power_management::Request::SHUTDOWN);
        if (ok) { drain_input(); publish(); }
        power_management::owner_ack(ok, !ok);
        ESP_LOGI("POWER", "owner_parked=%u refused=%u pending=%u", unsigned(ok), unsigned(!ok), unsigned(s->device.pending));
      }
      vTaskDelay(pdMS_TO_TICKS(20)); continue;
    }
    power_attempted = false;
    if (suspension.parked) {
      if (!suspension.resume(*s, time)) {
        if (!resume_warned) ESP_LOGE("POWER", "owner_resume=FAILED controls_unavailable=1");
        resume_warned = true;
        vTaskDelay(pdMS_TO_TICKS(1000)); continue;
      }
      resume_warned = false; drain_input(); publish(); acquisition = time;
      power_management::owner_ack(false);
      ESP_LOGI("POWER", "owner_resume=READY session=%llu buffered_input_discarded=1",
               static_cast<unsigned long long>(s->snapshot().session));
    }
    s->core.tick(time);
    // At most one external inbox event per turn, on the same Core owner.
    s->boundary.process_one(time);
    // Fixed budget: at most eight serial bytes and one HOME intent per turn.
    char keys[8];
    const int bytes = input_status == ESP_OK
                          ? usb_serial_jtag_read_bytes(keys, sizeof keys, 0)
                          : 0;
    for (int i = 0; i < bytes; ++i) {
      if (network_manager::development_key(static_cast<unsigned char>(keys[i]))) {
        const bool queued = network_manager::development_command(static_cast<unsigned char>(keys[i]));
        ESP_LOGI("NETWORK_DEV", "key=%c queued=%u DEVELOPMENT_ONLY", keys[i], unsigned(queued));
        continue;
      }
      if (power_management::development_key(static_cast<unsigned char>(keys[i]))) {
        bool queued = power_management::development_command(static_cast<unsigned char>(keys[i]));
        ESP_LOGI("POWER_DEV", "key=%c queued=%u DEVELOPMENT_ONLY owner_path=1", keys[i], unsigned(queued));
        continue;
      }
      const bool is_owner = xTaskGetCurrentTaskHandle() == owner;
      const auto reply = development::input(
          *s, static_cast<unsigned char>(keys[i]), time, is_owner);
      if (reply.kind == development::InputKind::IGNORE)
        continue;
      if (reply.kind == development::InputKind::UNKNOWN) {
        ESP_LOGI("UC_MOCK", "key=%c recognized=0 accepted=0 owner_ok=%u",
                 keys[i], unsigned(is_owner));
      } else {
        if(!reply.accepted)diagnostics::event(time,diagnostics::Event::CORE_REFUSED,unsigned(static_cast<unsigned char>(keys[i])));
        const auto state = s->snapshot();
        ESP_LOGI("UC_MOCK",
                 "key=%c recognized=1 accepted=%u owner_ok=%u session=%llu "
                 "capability_revision=%llu "
                 "dispatches=%u",
                 keys[i], unsigned(reply.accepted), unsigned(is_owner),
                 static_cast<unsigned long long>(state.session),
                 static_cast<unsigned long long>(state.capability_revision),
                 s->device.mock.dispatches);
        if (reply.kind == development::InputKind::TELEMETRY && reply.accepted)
          {
            telemetry("requested");
            auto q = s->boundary.inbox.counts();
            const auto &c = s->boundary.counts;
            ESP_LOGI("UC_INGRESS", "posted=%u rejected=%u overflow=%u busy=%u applied=%llu stale=%llu invalid=%llu refused=%llu lifecycle=%llu discarded=%llu",
              unsigned(q.posted), unsigned(q.rejected), unsigned(q.overflow), unsigned(q.busy),
              (unsigned long long)c.applied, (unsigned long long)c.stale, (unsigned long long)c.invalid,
              (unsigned long long)c.refused, (unsigned long long)c.lifecycle, (unsigned long long)c.discarded);
          }
      }
    }
    Intent intent;
    bool present;
    portENTER_CRITICAL(&mux);
    present = channel.pop(intent);
    portEXIT_CRITICAL(&mux);
    if (present) {
      bool accepted = s->handle(intent, time);
      if(!accepted)diagnostics::event(time,diagnostics::Event::CORE_REFUSED,unsigned(intent.action));
      ESP_LOGI("UC_RUNTIME", "intent=%llu action=%u accepted=%u dispatches=%u",
               static_cast<unsigned long long>(intent.token),
               unsigned(intent.action), unsigned(accepted),
               s->device.mock.dispatches);
    }
    if (time - acquisition >= 1000) {
      s->device.acquire(time);
      acquisition = time;
    }
    auto snapshot = s->snapshot();
    portENTER_CRITICAL(&mux);
    channel.publish(snapshot);
    portEXIT_CRITICAL(&mux);
    vTaskDelay(pdMS_TO_TICKS(50));
  }
}
} // namespace
bool request(Action action) {
  if (!power_management::commands_allowed()) return false;
  portENTER_CRITICAL(&mux);
  bool accepted = channel.request(action);
  portEXIT_CRITICAL(&mux);
  return accepted;
}
bool read(Snapshot &snapshot, std::uint64_t &generation) {
  portENTER_CRITICAL(&mux);
  bool changed = channel.generation != generation;
  if (changed) {
    snapshot = channel.latest;
    generation = channel.generation;
  }
  portEXIT_CRITICAL(&mux);
  return changed;
}
void start() {
  if (started)
    return;
  started = true;
  if (xTaskCreatePinnedToCore(task, "UC_owner", 24576, nullptr, 2, nullptr,
                              1) != pdPASS)
    ESP_LOGE("UC_RUNTIME", "FAIL owner creation");
}
} // namespace control_home
