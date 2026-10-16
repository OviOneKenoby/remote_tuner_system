# A-REMOTE-011 Stage 5 brightness restoration and admission diagnostics

Date: 2026-10-15  
Status: IMPLEMENTED / FOCUSED TESTS PASS / PRODUCTION BUILD FAIL / STOPPED

## Implemented private changes

The incorrect CCM binding was removed from the generated brightness slider. Its original `setUpduty` callback, generated label, 0–255 range and touch behavior were restored. Brightness and CCM volume are again independent.

The existing HOME numeric volume label and non-interactive bar remain unchanged. They continue to update only from copied, authoritative CCM snapshots on the LVGL timer; no widget, layout or optimistic update was added.

The existing volume admission decision was decomposed into named read-only outcomes without bypassing or changing a gate: disconnected, missing session, missing capability revision, unknown volume, unavailable `volume.set`, minimum, maximum, in-flight, token limit, queue full or accepted. Bounded counters record raw encoder transitions, complete cycles, last delta, attempted/accepted volume intents, the latest admission outcome and the relevant copied snapshot flags. Single-in-flight, session binding and no-retry behavior remain intact.

Focused verification passed:

- brightness/HOME UI ownership: 1/1, 8 assertions;
- exact admission diagnostics: 2/2, 20 assertions;
- affected encoder routing: 5/5, 25 assertions.

Previously passing unrelated suites were not repeated.

## Production build stop

The one authorized `remote01` build failed at the first compiler error. The extended diagnostics implementation supplies 40 Core values and 40 JSON field names, but `diagnostics::Core::values` was declared with length 39. Template deduction therefore reported conflicting sizes 39 and 40, and assignment of the 40-value initializer to the 39-element array also failed.

This is a demonstrated compile-time metadata-count defect. No firmware binary, size, SHA-256, OTA-headroom or static-RAM result exists for this candidate. Per the stop condition, the array length was not corrected and no second build was attempted.

No hardware access, flash operation, live command, TUNER change, GPIO/NVS/pairing/protocol change, private publication or PR merge occurred.

The minimum next action is to authorize changing only the Core diagnostics array length from 39 to 40 and running one production build. Hardware installation remains separately gated.

