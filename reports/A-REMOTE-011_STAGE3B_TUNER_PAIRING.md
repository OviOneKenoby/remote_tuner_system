# A-REMOTE-011 Stage 3B: TUNER-only pairing provisioning

## Result

**STOPPED — THE SINGLE AUTHORIZED CAPSULE TRANSMISSION RETURNED `storage_error`; TUNER PAIRING WAS NOT COMPLETED.** No automatic retry, REMOTE provisioning, production-firmware restoration or RTCP command followed.

## Preconditions

- The retained Stage 1 TUNER rollback set was present and every manifest-listed file matched its recorded byte length and SHA-256. The accepted five-entry installed partition layout remained the layout authority.
- Accepted A-010/A-011 evidence records the current REMOTE active persistence generation as 2. No later `remote_ctl` mutation was authorized or recorded.
- The TUNER's current LAN IPv4 address was obtained privately from its own successful `STA_GOT_IP` boot event. The address and device identifier are omitted from public evidence.
- One matching two-capsule set was generated once with the operating-system CSPRNG. Both 112-byte capsules remain private; no pairing identifier, PSK, capsule bytes or secret-derived value was printed or published.

## Helper installation

The TUNER commissioning application was 2,026,864 bytes (`0x1EED70`) with SHA-256 `8b239db4d8cdee712341a68fa12fb6ea521bc4c6b8eed62020832517d8c5d111`, matching the accepted Stage 3A artifact.

The TUNER was positively identified through its classic ESP32 ROM interface with 4 MiB flash. One application-only write was made at `0x10000` using 921600-baud esptool communication and `keep` flash mode/frequency/size. Esptool erased the covering application sectors `0x10000–0x1FEFFF`, wrote the authorized image through `0x1FED6F`, and verified its write-time hash. No bootloader, partition-table, OTA-metadata or explicit NVS image write was issued.

An independent readback of exactly `0x10000–0x1FED6F` was 2,026,864 bytes and matched the candidate SHA-256 above.

## Single provisioning attempt

The commissioning identity `target=tuner` and normal setup completion were observed before transmission. The private TUNER capsule was transmitted exactly once. The helper returned the sanitized result:

`A011_PAIR result=storage_error secret_output=0`

Source review localizes this result to the helper's initial read-only `Preferences.begin("remote_pair", true)` check. On an absent namespace, that call can fail instead of representing an empty namespace. The helper returns `storage_error` immediately from that branch, before opening the namespace read-write or calling either `putBytes`; therefore this attempt did not execute a pairing-data write. This exposes a concrete Stage 3A helper defect: its empty-store detection does not match the real ESP32 Preferences behavior even though the host policy tests passed.

## Scope and next gate

The helper firmware remains installed and both original capsules remain private. TUNER pairing is incomplete; REMOTE is unprovisioned and untouched. No retry, recovery capsule, restore, erase, RTCP command or PR merge occurred.

The minimum next action is a private helper correction that treats a genuinely absent `remote_pair` namespace as empty while continuing to fail closed for other storage errors, followed by focused test/build verification. A second TUNER provisioning transmission requires separate owner authorization after review of that exact corrected image and confirmation that the retained original capsules will be reused.
