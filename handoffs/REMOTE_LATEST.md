# REMOTE//01 handoff

## Metadata

- Handoff ID: REMOTE-A-REMOTE-011-STAGE5-INCLUDE-PATH-RESULT-20261014
- Updated (UTC): 2026-10-14
- Task ID: A-REMOTE-011
- Status: STAGE 5 INCLUDE-PATH CORRECTION FAILED WITH ORIGINAL ERROR
- Coordination branch: `remote/a-remote-011-kickoff-20261013`, PR #17
- Input head: `13d3b5f27500904b7a78173a2011edd3255f83b7`

## Result

The owner approved encoder A on GPIO2/J6-3, B on GPIO5/J6-6 and common on J6-9 GND, using input-only GPIOs with internal pull-ups. The assignment is documented as owner-approved but physically unverified. GPIO1 external-power sensing and GPIO4 `BAT_ADC` remain unchanged.

The private HOME-only encoder-to-volume path was implemented with the existing quadrature decoder, CCM admission and RTCP/1 adapter. Focused encoder/admission tests passed 5/5 with 25 assertions; the existing quadrature tests passed 19/19 with 21,621 assertions and 1,000 randomized cycles.

The authorized correction registered the existing shared include tree as a header-only ESP-IDF component and added `physical_input` to `user_app` private requirements. Exactly one production build was run. It retained the original `fatal error: physical_input/model.hpp: No such file or directory` diagnostic while compiling `user_app`; no distinct error appeared. Work stopped without another correction, build or test. No firmware artifact, size, hash or OTA-headroom result exists.

## Scope guard

No hardware access, flash operation, live `volume.set`, pairing/NVS mutation or TUNER change occurred. Private source and binaries remain private. PR #17 remains open and unmerged.

## Next owner decision

Authorize or reject a further bounded investigation of ESP-IDF/PlatformIO component discovery and one subsequent production build. Hardware commissioning remains a later, separate decision after a successful build.

## Evidence

- `docs/REMOTE_GPIO_MAP.md`
- `reports/A-REMOTE-011_STAGE5_ENCODER_IMPLEMENTATION_STOP.md`
- `references/device_evidence/remote/A-REMOTE-011/STAGE5_ENCODER_IMPLEMENTATION_STOP.json`
- `reports/A-REMOTE-011_STAGE5_INCLUDE_PATH_RESULT.md`
- `references/device_evidence/remote/A-REMOTE-011/STAGE5_INCLUDE_PATH_RESULT.json`
- Prior GPIO resolution: `reports/A-REMOTE-011_STAGE5_GPIO_RESOLUTION.md`
- Stage 4 completion: `reports/A-REMOTE-011_STAGE4_COMPLETE.md`
