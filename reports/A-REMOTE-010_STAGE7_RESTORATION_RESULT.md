# A-REMOTE-010 Stage 7 restoration result

Recorded UTC: 2026-10-13T15:19:11Z. Input commit `55c13231afc802dee825d6952e6cbc34a1db5ff4`; [owner confirmation](../references/A010_STAGE7_OWNER_CONFIRMATION_2026-10-13.md); [sanitized evidence](../references/device_evidence/remote/A-REMOTE-010/STAGE7_RESULT.json).

**PASS / OWNER ACCEPTED — PRIOR FIRMWARE RESTORED AND FUNCTIONAL.**

After revalidating the private restore span and recovery backup, exactly one write supplied only the 2,506,752-byte prior-byte span at `0x10000`. Esptool reported successful data-hash verification. A complete readback of `0x10000–0x273FFF` was 2,506,752 bytes and matched SHA-256 `57736494ea726600c68e25ae6a8f5b3bd109f5e5c1d5d858a05afd7ee8603aca` exactly.

The first attempted normal reset did not start REMOTE. The owner disconnected and reconnected USB, after which normal operation returned. The owner confirmed the original firmware boots and the UI and existing configuration are functional. At the approved practical hobby/public-beta level, the owner accepted Stage 7 PASS and directed that this bounded USB reconnection observation be preserved without opening another investigation.

No bootloader, partition table, OTA metadata, default NVS or `remote_ctl` image was supplied. `remote_ctl` was neither erased nor written during restoration; its last verified state remains generation 2 with the two controlled test records. No source or private artifact was published.
