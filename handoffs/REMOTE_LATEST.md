# REMOTE//01 handoff

## Metadata

- Handoff ID: REMOTE-A-REMOTE-011-STAGE5-BUILD-PASS-20261014
- Updated (UTC): 2026-10-14
- Task ID: A-REMOTE-011
- Status: STAGE 5 PRIVATE IMPLEMENTATION AND PRODUCTION BUILD PASS -- HARDWARE COMMISSIONING NOT STARTED
- Coordination branch: `remote/a-remote-011-kickoff-20261013`, PR #17
- Input head: `847d9c83ee7cb778e57451f7fe7d80faa0495cf6`

## Result

The owner approved encoder A on GPIO2/J6-3, B on GPIO5/J6-6 and common on J6-9 GND, using input-only GPIOs with internal pull-ups. The assignment is documented as owner-approved but physically unverified. GPIO1 external-power sensing and GPIO4 `BAT_ADC` remain unchanged.

The private HOME-only encoder-to-volume path was implemented with the existing quadrature decoder, CCM admission and RTCP/1 adapter. Focused encoder/admission tests passed 5/5 with 25 assertions; the existing quadrature tests passed 19/19 with 21,621 assertions and 1,000 randomized cycles.

Generated metadata demonstrated that the failed build tree predated the new header-only component: it contained neither `physical_input` nor the shared include directory in the `user_app` compile group. The generated tree was preserved under a private sibling name, forcing fresh discovery. The regenerated graph contains both entries, and exactly one subsequent production build passed.

The private application is 2,518,496 bytes with SHA-256 `58d09a4d7b39a287d80b48270b5236986657f27fb716692b77ff4af3e573cab7`; it has 627,232 bytes of headroom in either unchanged 3 MiB OTA slot. PlatformIO reported 47,172 bytes static RAM use and 2,517,997 bytes flash use. Previously passing tests were not repeated because no relevant source changed.

## Scope guard

No hardware access, flash operation, live `volume.set`, pairing/NVS mutation or TUNER change occurred. Private source and binaries remain private. PR #17 remains open and unmerged.

## Next owner decision

Authorize or reject the separately gated, reversible REMOTE hardware commissioning step: verify the private candidate and rollback image, install only the application, confirm normal behavior, observe encoder direction/detents, and permit at most one controlled volume change.

## Evidence

- `docs/REMOTE_GPIO_MAP.md`
- `reports/A-REMOTE-011_STAGE5_ENCODER_IMPLEMENTATION_STOP.md`
- `references/device_evidence/remote/A-REMOTE-011/STAGE5_ENCODER_IMPLEMENTATION_STOP.json`
- `reports/A-REMOTE-011_STAGE5_INCLUDE_PATH_RESULT.md`
- `references/device_evidence/remote/A-REMOTE-011/STAGE5_INCLUDE_PATH_RESULT.json`
- `reports/A-REMOTE-011_STAGE5_COMPONENT_DISCOVERY_RESOLVED.md`
- `references/device_evidence/remote/A-REMOTE-011/STAGE5_COMPONENT_DISCOVERY_RESULT.json`
- Prior GPIO resolution: `reports/A-REMOTE-011_STAGE5_GPIO_RESOLUTION.md`
- Stage 4 completion: `reports/A-REMOTE-011_STAGE4_COMPLETE.md`
