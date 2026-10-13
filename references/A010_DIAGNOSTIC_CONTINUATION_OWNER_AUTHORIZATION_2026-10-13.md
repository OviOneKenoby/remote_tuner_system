Owner decision: accept the A-REMOTE-010 host phase and authorize a scoped continuation for diagnostic activation design, implementation, review and clean build.

Do not access hardware, flash firmware, erase or write NVS in this phase. Stop before the first hardware operation and request separate explicit approval.

Keep PR #16 OPEN and UNMERGED. Continue A-REMOTE-010; do not create or start A-REMOTE-011.

Goal:

Add the smallest narrowly gated diagnostic path required to exercise the private remote_persistence backend on physical hardware later, without activating persistence during ordinary boot and without implementing the common API.

Requirements:

1. Diagnostic activation must be explicitly build-gated:
   - disabled in normal production/default configuration;
   - enabled only in the A-010 validation candidate;
   - clearly visible in the boot/build identity.

2. No automatic persistence activity:
   - no remote_ctl initialization merely because firmware boots;
   - no record creation, authority update, erase or migration at startup;
   - ordinary UI/application behavior must remain unchanged until an explicit diagnostic command is received.

3. Provide a minimal UART diagnostic interface with separate read-only and mutating operations.

Required read-only operations:

- report whether partition label remote_ctl exists;
- report partition type/subtype, offset and size;
- report backend/schema status;
- report whether the partition is erased, initialized, valid, empty, recoverable, corrupt or ambiguous;
- report selected generation and record metadata without printing payload contents or secrets;
- report capacity/free-space information available safely.

Required mutating operations for later authorized testing:

- initialize the erased remote_ctl partition;
- commit one known non-secret diagnostic payload;
- commit a successor diagnostic payload;
- reopen/recover after reboot;
- cleanly erase only remote_ctl for controlled rollback, but only as an explicitly separate command.

4. Every mutating command must require:
   - the diagnostic build;
   - an exact deliberate confirmation token;
   - explicit serial invocation;
   - clear before/after result reporting;
   - rejection if the selected partition is not exactly remote_ctl at 0xE20000 with size 0x10000.

5. The diagnostic must never:
   - open or write the default NVS partition;
   - modify Wi-Fi/UI/device configuration;
   - log payload contents;
   - accept arbitrary partition labels, offsets or raw flash addresses;
   - erase automatically after failure;
   - retry mutations indefinitely.

6. Add focused tests for:
   - diagnostic disabled state;
   - command parsing;
   - confirmation-token rejection;
   - exact partition-identity guard;
   - read-only status on erased/valid/corrupt/ambiguous models;
   - correct sequencing of init/first commit/successor commit;
   - rejection of unsafe erase or wrong partition;
   - no payload logging.

7. Review the ESP-IDF adapter path specifically:
   - custom NVS partition initialization by label;
   - NVS handle lifecycle;
   - commit semantics;
   - error mapping;
   - iterator/resource cleanup;
   - NVS full/no-free-pages/new-version handling;
   - ensure no automatic erase is hidden inside adapter error handling.

8. Perform one clean serial build of the diagnostic candidate.
9. Record:
   - exact private source changes;
   - build configuration/diagnostic flag;
   - firmware/ELF/map/partitions/bootloader hashes;
   - firmware size and OTA headroom;
   - proof that partitions.bin remains byte-identical to A-009;
   - proof that the diagnostic entry points and backend are reachable in the ELF;
   - proof that ordinary boot does not invoke them.

10. Prepare one complete later hardware protocol covering:
    - retained A-009 backup verification;
    - exact diagnostic firmware flash region(s);
    - post-flash normal boot/UI/configuration check before any remote_ctl mutation;
    - initial read-only status;
    - separately staged init, first commit, reboot recovery, successor commit and reboot recovery;
    - capacity/free-space observation;
    - bounded failure handling;
    - restoration of the previous firmware;
    - optional remote_ctl erase only under separate explicit authorization.

11. Keep the practical hobby/public-beta scope:
    - no exhaustive power-cut campaign;
    - no thousands of generated scenarios;
    - no industrial endurance qualification;
    - investigate further only for a concrete functional, corruption, security or bricking defect.

12. Do not:
    - access hardware;
    - flash anything;
    - mutate remote_ctl;
    - modify TUNER;
    - implement the common API, MQTT, SmartThings or UI;
    - change the partition layout;
    - publish private REMOTE source, credentials or payloads;
    - merge PR #16.

Return:

- continuation commit and PR head;
- diagnostic design and exact command set;
- private source files changed;
- new test totals and verdict;
- ESP-IDF adapter review verdict;
- clean-build result;
- candidate hashes, size and OTA headroom;
- partitions.bin identity result;
- proof of no boot-time persistence activity;
- complete hardware protocol path;
- exact first hardware operation proposed but not executed;
- explicit confirmation that zero hardware operations occurred.