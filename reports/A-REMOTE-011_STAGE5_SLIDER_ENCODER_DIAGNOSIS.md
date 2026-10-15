# A-REMOTE-011 Stage 5 wrong-slider and encoder diagnosis

Date: 2026-10-15  
Status: HARDWARE VALIDATION FAIL / DIAGNOSIS COMPLETE / CORRECTION NOT STARTED

## Demonstrated UI binding mistake

The generated mock-up contains exactly one LVGL slider: `screen_slider_1`, a child of generated carousel element 2. Its generated range is 0–255, its label says that it controls the backlight, and the production application originally attached its click callback to `setUpduty`. It is therefore conclusively the brightness slider.

The incorrect implementation selected it because it was the only object with LVGL slider type and treated the owner request for the existing mock-up volume slider as confirmation of its semantic role. The existing label, 0–255 backlight range and callback were contrary evidence and should have stopped the implementation.

There is no separate LVGL volume slider in the actual hierarchy. The custom HOME page has an authoritative volume presentation composed of `home.volume`, an LVGL label, and `home.level`, a plain non-interactive `lv_obj` bar inside `volume_track`. The HOME timer already updates both from the copied CCM snapshot. This is the intended existing volume widget, but it is not an LVGL slider.

The minimum UI correction is to remove the new volume binding from `screen_slider_1` and restore its original clickability, label and `setUpduty` callback. Brightness and CCM volume must remain independent. No replacement slider or layout change is authorized. Any further use of the existing HOME label/bar requires an explicit owner decision, although it already displays authoritative volume without optimistic encoder movement.

## Encoder path diagnosis

Source inspection confirms the production path:

1. GPIO2 and GPIO5 are configured as input-only with internal pull-ups.
2. A fixed task samples both pins every 2 ms.
3. The bounded quadrature model emits only complete valid cycles.
4. The router emits volume intent only while the custom HOME page is active.
5. `control_home::request` enforces connected session, current capability revision, authoritative volume, `volume.set` availability, bounds and one-in-flight admission.
6. The serialized Core owner builds and dispatches the CCM request through RTCP/1.

After the owner's physical rotation, one read-only diagnostic snapshot showed an active session and advancing capability revision, 59 rejected HOME-channel requests, zero posted Core ingress events, zero dispatches and zero applied/refused results. The only production entry points to that channel are HOME controls and the encoder route. Together with the owner's rotation observation, this demonstrates that physical sampling, complete-cycle decoding and HOME gating reached `control_home::request`; execution stopped before Core/RTCP dispatch.

The current diagnostics aggregate all local request rejections and do not expose the copied snapshot's `volume_known`, `volume_set`, current value, boundary position, outstanding flag or per-reason rejection. The exact admission condition therefore cannot be distinguished from current evidence. Direction and detent convention also remain unverified because no command was admitted.

## Minimum next actions

1. Apply only the demonstrated brightness restoration.
2. Add bounded read-only diagnostics for the encoder cycle count/last delta and the HOME channel's current connection, volume-known, volume-set, bounds, outstanding state and rejection reason. Do not add a command path.
3. Build and install that corrected diagnostic candidate only after separate owner authorization, then observe one controlled detent. The test must stop before any retry if admission or direction is unexpected.

No source edit, build, flash, persistent mutation, intentional command, TUNER change or PR merge occurred during this diagnosis.

