# A-REMOTE-011 Stage 5: REMOTE encoder volume-control routing review

## Result

**BLOCKED BEFORE SOURCE EDIT — NO PRODUCTION ENCODER ROUTE OR GPIO IDENTITY EXISTS IN THE ACCEPTED PRIVATE SOURCE.**

The active private REMOTE workspace and the preserved A-010/A-011 source copies were inspected before editing, as required. They agree on the following facts:

- `physical_input::Model` provides a bounded, host-tested quadrature decoder and emits signed `ENCODER_CYCLE` events;
- that model is used only by host tests;
- no production source instantiates the model, samples encoder A/B lines, defines encoder GPIOs, or consumes `ENCODER_CYCLE` events;
- no LVGL encoder input device is registered;
- the production UI currently routes HOME touch buttons only to previous/toggle/next intents;
- no existing UI-context router distinguishes HOME volume control from encoder navigation in other pages.

The accepted source therefore does not provide the unambiguous encoder routing required to implement “one physical detent equals one supported volume step” while preserving navigation elsewhere. Adding GPIO assignments or a second handler would require guessing and would violate the owner’s constraints. Treating all rotation as HOME volume would also change undefined navigation behavior outside the HOME context.

No private source file was changed. No test or production build was run because there was no valid implementation input to verify. No firmware, hardware, pairing, NVS, CCM or RTCP operation occurred, and zero `volume.set` commands were sent.

## Minimum owner input required

Provide the existing encoder’s accepted hardware and routing identity:

1. the two already-wired GPIO assignments and electrical polarity/pull configuration, or the exact existing driver/API that owns them;
2. the current detent convention if it differs from the preserved quadrature model;
3. the UI rule that identifies the volume-control context while preserving encoder navigation in every other context.

With those facts, the narrow implementation can reuse the existing model, add clockwise/counterclockwise volume intents to `control_home`, use the latest fresh observed value and 1/100 grid, and retain the existing single-in-flight/no-retry/session invalidation behavior.
