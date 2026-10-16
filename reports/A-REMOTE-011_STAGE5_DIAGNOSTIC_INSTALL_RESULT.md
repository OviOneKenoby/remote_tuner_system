# A-REMOTE-011 Stage 5 diagnostic installation result

Date: 2026-10-15  
Status: APPLICATION INSTALLATION PASS / CONTROL TEST BLOCKED

After the owner restored the USB connection, Windows reported the currently enumerated Espressif USB serial/JTAG interface healthy. A read-only esptool ROM connection identified the expected ESP32-S3 and 16 MiB physical flash. The accepted private candidate and retained 16 MiB rollback image were reverified before the write.

The accepted 2,520,640-byte application was written once at `0x10000` using stable 921600-baud esptool communication. No retry or fallback occurred. An independent exact-length readback matched candidate SHA-256 `9edbfc968dbfe3dea66ab4d8932bb2e9389df670874510264b99fc9b5b51f98a`.

Read-only post-boot diagnostics showed the application running, connected through stored Wi-Fi configuration, valid main/external voltage observations, no allocation errors, and zero encoder transitions, detents, volume intents or command dispatches. The later baseline still reported the volume channel disconnected, with no authoritative volume observation and no `volume.set` capability. Authenticated RTCP volume synchronization is therefore not confirmed, and the controlled encoder test remains blocked. No encoder rotation or control command was attempted.

Owner visual confirmation of the normal UI, retained settings, restored brightness behavior and existing HOME volume presentation remains pending. PR #17 remains open and unmerged.

