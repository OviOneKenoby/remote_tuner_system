# A-REMOTE-010 final closure report

Recorded UTC: 2026-10-13T15:19:11Z.

## Final verdict

**DONE / OWNER ACCEPTED at the practical hobby/public-beta assurance level.**

A-REMOTE-010 delivered the minimum private persistence backend for the dedicated 64 KiB `remote_ctl` NVS partition without implementing the REMOTE–TUNER common API. Host validation passed 28 focused tests and clean private builds. Hardware validation confirmed exact partition selection, erased initialization, first and successor commits, monotonic generations 0→1→2, reboot recovery, no incomplete transaction, bounded capacity behavior, retained default configuration and no payload disclosure. The diagnostic firmware was then replaced with the exact accepted prior firmware span, verified by full readback.

The installed final application is the accepted original factory firmware. The partition table remains the accepted seven-entry A-REMOTE-009 layout. `remote_ctl` remains present at `0xE20000`, size `0x10000`, unerased, with last verified generation 2 and controlled non-secret test records; the restored firmware ignores this dedicated partition. The first post-restoration normal-reset attempt did not start REMOTE, but one owner-performed USB disconnect/reconnect restored normal operation. The owner confirmed original firmware boot, functional UI and retained configuration and accepted this observation without further investigation.

Private source, firmware, complete flash backups, UART captures and device-specific data remain private. The verified primary 16 MiB backup, separate-storage copy, original partition-table sector and restore span must be retained with their recorded hashes. No `remote_ctl` erase, common API, TUNER change, MQTT, SmartThings or UI feature was included. A-REMOTE-011 remains not started.

## Merge recommendation

PR #16 is ready for owner-authorized normal merge. It contains sanitized coordination records, hashes, protocols, limitations and the complete historical investigation. It publishes no private REMOTE source or binary. Merge only after a separate explicit owner instruction; no additional test or task should start automatically.
