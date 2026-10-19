# A-REMOTE-013 resource and risk assessment

No build or device measurement was performed in Phase 1. Values below are accepted prior measurements; estimates are labeled.

## Baseline budgets

| Device | Application | Slot headroom | Static RAM | Relevant runtime evidence |
| --- | ---: | ---: | ---: | --- |
| TUNER v1.1.12 | 2,037,632 bytes | 1,108,096 bytes in the 3 MiB slot | 87,512 / 327,680 bytes | During validated A2DP coexistence: minimum internal free heap 22,468 bytes; minimum largest internal block 16,372 bytes |
| REMOTE installed | 2,526,848 bytes | 618,880 bytes in the 3 MiB slot | 47,388 / 327,680 bytes | Existing fixed RTCP, diagnostics, UI, persistence and sleep/wake operation accepted at hobby/public-beta level |

Flash is not the immediate blocker. TUNER internal heap fragmentation during Classic Bluetooth, long main-loop work, and bounded wire/UI storage are the material constraints.

## Concrete constraints

- TUNER `MAX_STATIONS=15`, `MAX_FAVORITES=10`, `MAX_RECENT=5`, `MAX_BROWSE_RESULTS=20`, `MAX_BROWSE_TAGS=40`, and about 250 countries. Names are bounded to 64 bytes and URLs to 256 bytes.
- TUNER browser arrays are lazily allocated and released; HTTPS/JSON work is synchronous. It must not be moved into the RTCP service path or kept alive during audio without measurement.
- The A2DP fix deliberately releases unused BLE controller memory and initializes Classic-only mode. A-REMOTE-013 must not re-enable BLE or add large long-lived internal allocations.
- RTCP plaintext is limited to 512 bytes. Twenty station items cannot fit in one response with names and identity metadata, so catalogs need explicit paging/chunking.
- REMOTE Core foundations currently bound resources to 16 per relevant fixed collection. A 20-result Radio Browser page cannot be assumed to fit without an approved bound or smaller wire page.
- `remote_ctl` is a 64 KiB NVS partition with an A-010 bounded record envelope used for association/control durability. It is not approved as a station/logo cache and must not be consumed implicitly.
- LVGL widgets must be updated by the UI task. Network callbacks must publish bounded copied state rather than call LVGL directly.

## Risk register

| Risk | Evidence | Required control |
| --- | --- | --- |
| A2DP internal-memory regression | Prior unused BLE allocation caused network outage; v1.1.12 correction is hardware validated | Preserve Classic-only setup; measure free heap, largest block and allocation failures for each TUNER slice |
| RTCP/web starvation | TUNER main loop owns audio, RTCP, web and synchronous e-paper/browser work | Keep requests bounded; cooperatively service RTCP during approved long display work; never run Radio Browser HTTPS in an RTCP handler |
| Catalog overflow | 512-byte records, 16-resource REMOTE bound, up to 20 search results | Approve page/item/string limits and deterministic continuation; reject oversized data |
| Mutable station identity | Current arrays shift on deletion and use names/URLs/indices | Add durable opaque ID plus catalog revision before remote selection |
| Stale media metadata | ICY/AVRCP callbacks can outlive display state transitions | Bind metadata to source/media generation; clear on transition and reconnect |
| Command ambiguity | Disconnect after send can leave effect uncertain | Retain single-in-flight, correlation, no automatic retry and session fencing |
| Artwork memory/network pressure | No current pipeline; images could be large or hostile | Fixed byte/dimension/format bounds, timeout, one transfer, decode outside hot path, placeholder on failure |
| Artwork privacy/security | Raw stream/logo URLs can reveal third-party or private endpoints | Approve locator policy; prefer a sanitized station-logo locator tied to durable station identity |
| Persistent wear/corruption | Catalog/logo churn does not belong in association storage | Start with volatile bounded cache; any durable cache needs a separate layout and recovery decision |
| UI truth drift | Provisional control and authoritative state may differ | Preserve visual distinction and update authority only from admitted observations |
| Motion-wake confusion | QMI8658 initialization can be intermittent | Track separately; buttons do not need to wake the device in this milestone |

## Expected implementation cost

Playback command additions should be small in flash and fixed RAM, but exact deltas are UNKNOWN until each production build. Station catalogs and artwork are materially larger. The implementation plan therefore gates them behind measured production builds and hardware coexistence checks rather than reserving speculative memory.

PSRAM is available in the selected TUNER profile and REMOTE hardware, but DMA, lwIP, Bluetooth and some TLS allocations still require internal memory. Merely placing application buffers in PSRAM does not remove the need to measure internal free heap and largest block.
