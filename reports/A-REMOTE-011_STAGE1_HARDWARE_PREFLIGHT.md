# A-REMOTE-011 Stage 1: read-only hardware identification and rollback capture

## Result

**PASS for REMOTE//01. PASS for TUNER//01. STAGE 1 COMPLETE; NO PERSISTENT WRITE OR ERASE.**

Stage 1 was executed against the published procedure at `f0d4eced37ddaa5e05566b0b7c77a23a87d67665`. Each device was connected and inspected separately. Identity was established through the chip ROM interface rather than inferred from a COM-port name. All raw captures, device identifiers and private paths remain outside the public repository.

## REMOTE//01

- ROM identity: ESP32-S3, revision 0.2; native USB Serial/JTAG; physical flash 16 MiB.
- Installed table: the expected seven entries decoded successfully. Its 3,072-byte table prefix is byte-identical to accepted partition artifact SHA-256 `a144343580dbdadace66fccc5969d7557de3d4c4f15a61e76db205cc26348184`; the remainder of the 4 KiB table sector is erased padding.
- Full backup: 16,777,216 bytes, SHA-256 `31fd537c4bf534b101e74ed582bf0aa909235686207da29ad61413f21688b43d`.
- Complete factory partition backup: 8,388,608 bytes, SHA-256 `a2cdad46d173856a051bcf143a148d730f4ce9d47a17446411c2475b2383efea`.
- Current candidate-range rollback bytes (`0x10000–0x27627F`): 2,515,584 bytes, SHA-256 `0f89125f8dd7833920c3bb35aa83961286ac21cf13fceec59f20c456f6cf2ffa`.
- `remote_ctl` rollback: 65,536 bytes, SHA-256 `6bb3aa0c903d59ee1b341a828b61424be73327b270bd0fd662a4c2cb891db1e0`. It is non-erased, as expected for the preserved generation-2 A-010 records. Its contents were not decoded or published.
- Installed application image is structurally valid. Its first 2,506,752 bytes match the retained A-010 Stage 7 restore identity exactly: SHA-256 `57736494ea726600c68e25ae6a8f5b3bd109f5e5c1d5d858a05afd7ee8603aca`.
- Independent direct reads of the table sector, `remote_ctl`, and full proposed candidate range are byte-identical to the corresponding full-backup slices.
- The full flash and rollback-critical regions are neither all-`0xFF` nor all-`0x00`. Primary and second private copies have matching hashes.
- ROM/USB recovery access: available and exercised read-only through a successfully loaded RAM stub. No recovery write was attempted.

## TUNER//01

- ROM identity: ESP32-D0WDQ6-V3, revision 3.1; physical flash 4 MiB; CH340 USB serial interface.
- Installed table: the expected five entries decoded successfully. Its 3,072-byte table prefix is byte-identical to accepted partition artifact SHA-256 `aaae2888c5a6a348004b5b436f47abb25ae32e72d9003902955a998eda723edd`; the remainder of the 4 KiB table sector is erased padding.
- Full backup: 4,194,304 bytes, SHA-256 `4a980e0887fab052389c233429d9cdf398720e119f2b51141a4fcfb8aa5914f6`.
- Complete `app0` partition backup: 3,145,728 bytes, SHA-256 `3ce83b7a6f9e9132b34df5dd8168e6874932bb74618457584c8337967911a6c1`.
- Current candidate-range rollback bytes (`0x10000–0x200C6F`): 2,034,800 bytes, SHA-256 `4dc7347191a38a18fe76b1635b446a485443ac6d06406bb6f53d303cd105b88a`.
- Default-NVS rollback: 20,480 bytes, SHA-256 `d01056d8fa27b70070f410018fb98b1195694ec40927aa32ab2dab7b0736c61f`. It was preserved as opaque private data and was not decoded or published.
- Installed application image is structurally valid. It is not byte-identical to the prior historical v1.1.11 artifact over that artifact's recorded length. Stage 1 makes no source-equivalence claim; the fresh installed bytes are now the authoritative rollback input.
- Independent direct reads of the table sector, default NVS, and full proposed candidate range are byte-identical to the corresponding full-backup slices.
- The full flash and rollback-critical regions are neither all-`0xFF` nor all-`0x00`. Primary and second private copies have matching hashes.
- ROM/USB recovery access: available and exercised read-only through a successfully loaded RAM stub. No recovery write was attempted.

## Scope and disposition

The only device interactions were ROM identity queries, flash identity queries, RAM-stub loading, read-only flash capture, and the tool's normal volatile reset. There was no flash write, erase, firmware installation, partition update, pairing, PSK generation, NVS mutation, `remote_ctl` mutation, RTCP command, or PR merge.

Stage 1 is complete at the approved practical hobby/public-beta level. Both devices have a verified primary capture and a separately hashed local copy. Before Stage 2, the copies required by the published protocol must also be placed on owner-controlled separate storage and reverified there.

Stage 2 remains unauthorized. Its next proposed operation is application-only installation, beginning with revalidation of candidates and rollback material. Separate owner authorization is required before any firmware write.
