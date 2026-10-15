# REMOTE//01 handoff

## Metadata

- Handoff ID: REMOTE-A-REMOTE-011-STAGE5-EC11-INSTALL-20261015
- Updated (UTC): 2026-10-15
- Task ID: A-REMOTE-011
- Status: STAGE 5 APPLICATION INSTALLED -- CONTROL TEST NOT STARTED
- Coordination branch: `remote/a-remote-011-kickoff-20261013`, PR #17
- Input head: `c5db0de3f5cff915b86ebb904fad179e5f05c561`

## Result

The owner confirmed the EC11 is connected to the approved GPIO2/GPIO5/GPIO38 wiring. The accepted 2,518,896-byte application was installed once at `0x10000` using 921600-baud esptool communication. Exact readback matched SHA-256 `6aca8931fcd08b91fcf489bd6d77212cbb0d4c762e70a657d7abec6911ab8e95`; no retry or unrelated flash operation occurred.

Two read-only post-boot snapshots showed connected stored networking, ready storage, valid main and external voltage sensing, a ready IMU, an active authenticated session with advancing capability revisions, and zero control dispatches or applied results.

## Scope guard

No intentional encoder rotation, KEY press, `volume.set`, pairing/NVS change, TUNER modification, private binary/source publication or PR merge occurred. Encoder direction and detent convention remain physically unverified. The KEY has no application action and its logical event is not exposed by current diagnostics. BUTTON_1 through BUTTON_3 remain unconnected and untested.

## Next owner checkpoint

Confirm the normal UI and retained configuration. If those checks pass, separately authorize one controlled adjacent encoder detent test on HOME, with the TUNER at a safe audible volume. That test may transmit exactly one `volume.set`; it must stop on the first unexpected direction, detent count, session or result behavior.

## Evidence

- `reports/A-REMOTE-011_STAGE5_EC11_COMMISSIONING.md`
- `references/device_evidence/remote/A-REMOTE-011/STAGE5_EC11_COMMISSIONING.json`
- Previous implementation: `reports/A-REMOTE-011_STAGE5_BUTTON_INPUT_IMPLEMENTATION.md`
- GPIO record: `docs/REMOTE_GPIO_MAP.md`
