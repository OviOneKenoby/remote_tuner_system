# Source evidence (read-only)
Paths/lines below refer to exact hashes in SOURCE_SDK_SHA256.json. This is source evidence, not execution of SDK code.

## components/control/core.cpp
- L255: `bool Core::persist() {`
- L262: `bool Core::begin(U64 now) {`

## components/control/include/control/core.hpp
- L143: `class Journal {`
- L148: `virtual bool commit(const Store &) = 0;`

## components/control/include/control/mock_adapter.hpp
- L5: `class MockJournal final : public Journal {`
- L9: `bool commit(const Store &) override {`

## components/network_manager/runtime.cpp
- L44: `return handle && nvs_set_blob(handle, key, data, n) == ESP_OK && nvs_commit(handle) == ESP_OK;`
- L48: `auto e = nvs_erase_key(handle, key);`
- L49: `return (e == ESP_OK || e == ESP_ERR_NVS_NOT_FOUND) && nvs_commit(handle) == ESP_OK;`
- L166: `if (nvs_flash_init() == ESP_OK && nvs_open("remote_wifi", NVS_READWRITE, &storage.handle) == ESP_OK) {`
- L178: `wifi_init_config_t c = WIFI_INIT_CONFIG_DEFAULT(); c.nvs_enable = 0;`

## components/network_manager/include/network_manager/model.hpp
- L11: `using Blob = std::array<unsigned char, 108>;`

## SDK5.5.3/src/nvs_api.cpp
- L66: `Lock lock;`
- L100: `Lock lock;`
- L130: `Lock lock;`
- L171: `Lock lock;`
- L188: `Lock lock;`
- L215: `Lock lock;`
- L246: `Lock lock;`
- L274: `Lock lock;`
- L300: `Lock lock;`
- L314: `Lock lock;`
- L333: `Lock lock;`
- L346: `Lock lock;`
- L360: `Lock lock;`
- L411: `extern "C" esp_err_t nvs_commit(nvs_handle_t c_handle)`
- L413: `Lock lock;`
- L425: `Lock lock;`
- L435: `extern "C" esp_err_t nvs_set_blob(nvs_handle_t c_handle, const char* key, const void* value, size_t length)`
- L437: `Lock lock;`
- L451: `Lock lock;`
- L503: `Lock lock;`
- L536: `extern "C" esp_err_t nvs_get_blob(nvs_handle_t c_handle, const char* key, void* out_value, size_t* length)`
- L543: `Lock lock;`
- L569: `Lock lock;`
- L785: `Lock lock;`
- L823: `Lock lock;`
- L857: `Lock lock;`

## SDK5.5.3/src/nvs_handle_simple.cpp
- L39: `esp_err_t NVSHandleSimple::set_blob(const char *key, const void* blob, size_t len)`
- L101: `esp_err_t NVSHandleSimple::commit()`
- L105: `return ESP_OK;`

## SDK5.5.3/src/nvs_storage.cpp
- L63: `while(p.findItem(Page::NS_ANY, ItemType::BLOB_IDX, nullptr, itemIndex, item) == ESP_OK) {`
- L135: `if(p.eraseItem(iter->nsIndex, nvs::ItemType::BLOB_IDX, iter->key, 255, iter->chunkStart) == ESP_OK){`
- L273: `esp_err_t Storage::writeMultiPageBlob(uint8_t nsIndex, const char* key, const void* data, size_t dataSize, VerOffset chunkStart)`
- L282: `uint32_t max_pages = mPageManager.getPageCount() - 1;`
- L284: `if(max_pages > (Page::CHUNK_ANY-1)/2) {`
- L285: `max_pages = (Page::CHUNK_ANY-1)/2;`
- L288: `if(dataSize > max_pages * Page::CHUNK_MAX_SIZE) {`
- L361: `err = getCurrentPage().writeItem(nsIndex, ItemType::BLOB_IDX, key, item.data, sizeof(item.data));`
- L406: `err = findItem(nsIndex, ItemType::BLOB_IDX, key, findPage, item, Page::CHUNK_ANY, VerOffset::VER_ANY, &itemIndex);`
- L472: `VerOffset prevStart,  nextStart;`
- L473: `prevStart = nextStart = VerOffset::VER_0_OFFSET;`
- L487: `nextStart`
- L491: `err = writeMultiPageBlob(nsIndex, key, data, dataSize, nextStart);`
- L534: `// Delete previous value`
- L542: `if(item.datatype == ItemType::BLOB_IDX) {`
- L543: `// If the item found was BLOB_INDEX, the eraseMultiPageBlob is used to erase the whole multi-page blob.`
- L546: `err = eraseMultiPageBlob(nsIndex, key, prevStart);`
- L659: `auto err = findItem(nsIndex, ItemType::BLOB_IDX, key, findPage, item);`
- L699: `eraseMultiPageBlob(nsIndex, key);`
- L714: `auto err = findItem(nsIndex, ItemType::BLOB_IDX, key, findPage, item);`
- L786: `esp_err_t Storage::eraseMultiPageBlob(uint8_t nsIndex, const char* key, VerOffset chunkStart)`
- L796: `auto err = findItem(nsIndex, ItemType::BLOB_IDX, key, findPage, item, Page::CHUNK_ANY, chunkStart, &itemIndex);`
- L816: `// If there exists another BLOB_IDX with the same key and namespace index, delete it`
- L818: `err = findItem(nsIndex, ItemType::BLOB_IDX, key, findPage, item, Page::CHUNK_ANY, chunkStart, &itemIndex);`
- L856: `// The caller has specified the chunk version, delete all chunks within the chunk index range indicated by the BLOB_IDX entry`
- L902: `// If the item found is BLOB_IDX, the eraseMultiPageBlob is used to erase the whole multi-page blob.`
- L903: `if (item.datatype == ItemType::BLOB_IDX) {`
- L904: `return eraseMultiPageBlob(nsIndex, key, item.blobIndex.chunkStart);`
- L961: `// If requested datatype is BLOB, first try to find the item with datatype BLOB_IDX - new format`
- L964: `err = findItem(nsIndex, ItemType::BLOB_IDX, key, findPage, item);`
- L1090: `item.datatype != ItemType::BLOB_IDX);`

## SDK5.5.3/src/nvs_pagemanager.cpp
- L100: `auto err = newPage->erase();`
- L113: `err = it->copyItems(*newPage);`
- L118: `err = it->erase();`
- L132: `return ESP_ERR_NVS_NO_FREE_PAGES;`
- L139: `esp_err_t PageManager::requestNewPage()`
- L163: `return ESP_ERR_NVS_NOT_ENOUGH_SPACE;`
- L171: `esp_err_t err = erasedPage->markFreeing();`
- L176: `// Activating a new page first when markFreeing is done. The data recovery from power loss will be`
- L185: `err = erasedPage->copyItems(*newPage);`
- L190: `err = erasedPage->erase();`
- L208: `return ESP_ERR_NVS_NOT_ENOUGH_SPACE;`
- L212: `auto err = p->erase();`
- L228: `nvsStats.available_entries = 0;`
- L245: `// avoid overflow of size_t declared available_entries in case of free_entries being too low`
- L246: `nvsStats.available_entries = (nvsStats.free_entries >= Page::ENTRY_COUNT) ? nvsStats.free_entries - Page::ENTRY_COUNT : 0;`

## SDK5.5.3/src/nvs_page.hpp
- L39: `static const size_t ENTRY_SIZE  = NVS_CONST_ENTRY_SIZE;`
- L40: `static const size_t ENTRY_COUNT = NVS_CONST_ENTRY_COUNT;`
- L43: `static const size_t CHUNK_MAX_SIZE = ENTRY_SIZE * (ENTRY_COUNT - 1);`
- L204: `NVS_ASSERT_OR_RETURN(entry < ENTRY_COUNT, ESP_FAIL);`
- L205: `*address =  mBaseAddress + ENTRY_DATA_OFFSET + static_cast<uint32_t>(entry) * ENTRY_SIZE;`
- L217: `typedef CompressedEnumTable<EntryState, 2, ENTRY_COUNT> TEntryTable;`
