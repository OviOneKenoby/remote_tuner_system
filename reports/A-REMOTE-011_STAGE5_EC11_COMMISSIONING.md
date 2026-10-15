# A-REMOTE-011 Stage 5 EC11 commissioning

Date: 2026-10-15  
Status: INSTALLATION PASS / CONTROL TEST NOT STARTED

## Result

The owner confirmed the EC11 is physically connected to the approved pins: GPIO2/J6-3 (S1), GPIO5/J6-6 (S2), GPIO38/J3-8 (KEY), 3V3/J6-8 and GND/J6-9. GPIO1 and GPIO4 remain dedicated to voltage sensing; the three additional button inputs remain unconnected and microSD remains excluded.

The accepted 2,518,896-byte application matched SHA-256 `6aca8931fcd08b91fcf489bd6d77212cbb0d4c762e70a657d7abec6911ab8e95`. The retained private rollback evidence was present and its candidate-range image reverified against its private manifest before the operation.

The application was written once at `0x10000` using 921600-baud esptool communication. Esptool wrote only the application range and completed its data-hash verification. An independent readback of exactly 2,518,896 bytes matched the accepted SHA-256. No fallback or write retry occurred.

Two read-only LAN snapshots after boot showed the accepted application identity, connected stored networking, ready storage, a live authenticated session, advancing capability revisions, valid main and external voltage observations, a ready IMU, zero failed allocations, and zero command dispatches or applied control results. This establishes boot, network, voltage-sensing and RTCP/CCM readiness without exercising the encoder.

## Deliberate stop

No intentional encoder rotation, KEY press, `volume.set`, pairing/NVS change, TUNER modification or other persistent operation was performed after installation. Encoder direction and physical detent convention therefore remain unverified. The KEY input has no application action and the installed diagnostics do not expose its logical event, so its physical event was not claimed. BUTTON_1 through BUTTON_3 remain unconnected and were not tested.

Owner visual confirmation of the normal UI and retained configuration, followed by separate authorization, is required before one controlled encoder detent test that may transmit `volume.set`. PR #17 remains open and unmerged.

