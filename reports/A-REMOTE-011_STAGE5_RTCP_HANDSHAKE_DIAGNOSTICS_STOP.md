# A-REMOTE-011 Stage 5 bounded RTCP handshake diagnostics

Date: 2026-10-15  
Status: DIAGNOSTIC MODEL TEST PASS / STATUS-SCHEMA SIZE BOUND FAILURE

The private REMOTE implementation adds fixed-size, read-only RTCP handshake diagnostics without changing transport framing, cryptography, timeouts, reconnect policy or CCM behavior. It records only sanitized stage and failure enums, a signed platform error code, bounded saturating counters and the server-hello byte count. It does not record endpoints, identifiers, keys, nonces, proofs, messages or payloads.

Covered stages are TCP connection, completed client hello, server-hello receipt and length, framing validation, proof validation, completed client finish, completed encrypted identity request, identity response receipt and identity acceptance. Failure categories distinguish connect failure, timeout, EOF, short read, invalid frame, proof failure, send failure, receive failure, cryptographic failure and identity rejection where the existing control flow provides that distinction. Evidence survives reconnect attempts in fixed storage and creates no network traffic.

The first focused host-test compilation exited with code 1, emitted no compiler diagnostic and produced no executable. The mandatory first-failure stop applied: the test was not retried and the production build was not started. Test totals, firmware size, artifact SHA-256, OTA headroom and static RAM therefore remain unavailable. No hardware, flash, pairing/NVS, TUNER, encoder or control operation occurred.

The owner subsequently authorized exactly one unchanged retry. Before execution, the compiler executable, working directory, test source, include root, diagnostic header and writable output directory were all verified; no prior executable existed. The retry again exited with code 1, produced zero bytes on stdout and stderr, and created no executable. No test process or production build was started. The reproducible immediate host compiler-process failure is the first available diagnostic; there is no compiler message identifying a source error. No further retry or source change occurred.

The owner then supplied and validated the host root cause: the MSYS2 UCRT64 runtime directory was absent from the process PATH. With only `C:\msys64\ucrt64\bin` prepended to the temporary test process PATH, the focused RTCP diagnostic model compiled and passed 6/6 assertions.

The next affected status-schema compilation stopped at the first actionable source diagnostic: the 14 added Core fields increase `diagnostics::Snapshots` to 1,120 bytes, violating its existing `sizeof(Snapshots) <= 1024` static bound. No source correction was authorized or attempted. The production build was not started, so firmware size, SHA-256, OTA headroom and static RAM remain unavailable. No hardware or device state changed.

