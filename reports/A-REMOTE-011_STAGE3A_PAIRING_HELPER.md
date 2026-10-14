# A-REMOTE-011 Stage 3A: private one-shot pairing helper

## Verdict

**PASS — IMPLEMENTED AND BUILD VERIFIED; NOT EXECUTED ON HARDWARE.** Two private commissioning-only firmware variants and private offline tooling now implement the minimum storage writes required by the existing production pairing readers. No operational pairing identifier or PSK was generated. No device was accessed, flashed, paired or sent an RTCP command.

## Stored fields and isolation

The TUNER helper writes only the existing `remote_pair` Preferences namespace keys `pair_id` (16 bytes) and `psk` (32 bytes). It leaves every other default-NVS namespace and key untouched. While this helper build is active, the RTCP listener is compile-time disabled.

The REMOTE helper converts the same pair material plus the privately selected TUNER IPv4 address and fixed RTCP/1 port 46411 into the existing 68-byte A-011 association envelope. It commits that envelope only through the accepted A-010 `remote_ctl` backend, using the backend's recovered `next_generation`; existing generation history is preserved and an uncommitted generation is never reused. It requires the privately recorded current active generation and initial association session generation 1.

Both helpers accept one fixed 112-byte binary capsule with a target discriminator, bounded fields and SHA-256 integrity check. They never print the pairing identifier, PSK, address, capsule bytes or complete stored payload. Results use a small fixed set of sanitized status codes. Pairing is unavailable in normal production builds because `A011_PAIRING_COMMISSIONING` defaults to zero.

## One-shot and recovery behavior

- An already complete TUNER pairing or decodable REMOTE association is refused.
- TUNER provisioning is allowed only from an empty `remote_pair` state. A one-key partial state is refused until an explicit recovery capsule removes only `pair_id` and `psk`, verifies empty state and then provisions the same capsule.
- REMOTE provisioning is allowed only from an exact healthy recovered generation. A backend incomplete-transaction indication is refused until an explicit recovery capsule commits at the new `next_generation`. Corrupt, ambiguous, schema-mismatched, capacity-exhausted, storage-error and unexpected-generation states fail closed.
- If TUNER reports complete and REMOTE does not, retain the capsules and use the REMOTE recovery procedure; do not regenerate credentials. If REMOTE is complete and TUNER is not, use the TUNER partial-state procedure. If either store is unsafe rather than specifically recoverable, stop and restore only from the retained device-specific backup under separate authorization.

## Verification

- Private capsule and policy tests: **16/16 PASS**.
- REMOTE commissioning build: PASS; firmware 2,517,136 bytes; SHA-256 `a55ef1b54818821089956f0bec17f37df5c88087dcdb1407bb65c64db21091d4`; static RAM 47,196 bytes; 628,592 bytes remain in its 3 MiB application slot.
- TUNER commissioning build: PASS; firmware 2,026,800 bytes; SHA-256 `94955b3445ea832139704798a9cc3f5e6db2cce2d20671cd6b26f94b8ec7771b`; static RAM 86,032 bytes; 1,118,928 bytes remain in its 3 MiB application slot.
- Normal REMOTE production build: PASS with commissioning disabled; static RAM 47,084 bytes.
- Normal TUNER production build: PASS with commissioning disabled; static RAM 85,912 bytes.
- Focused scan of all new helper/tool files found no embedded credential, token or private-key material.

## Exact later provisioning sequence

This sequence is prepared and **not authorized for execution**:

1. Reverify the retained Stage 1 rollback files and the exact private helper image hashes above.
2. Privately determine the TUNER IPv4 address that REMOTE must use. Offline, run the private capsule generator once with that address and the verified current REMOTE active generation. It creates one TUNER capsule and one REMOTE capsule containing the same freshly generated 16-byte identifier and 32-byte PSK; the tool prints only `created=2 secret_output=0`.
3. Preserve both capsules in owner-controlled private storage. Do not copy them to the coordination or TUNER repositories.
4. Under separate owner authorization, flash only the TUNER helper application range, boot it, and send the TUNER capsule exactly once with the private runner. Require `result=complete`.
5. Under separate owner authorization, flash only the REMOTE helper application range, boot it, and send the REMOTE capsule exactly once. Require `result=complete`.
6. If and only if a helper reports its specific partial-state code after an interrupted attempt, derive a recovery capsule from the same original capsule offline and send it once under new owner authorization. Any other error stops the procedure.
7. Restore the accepted Phase 3 production application to each device, without changing bootloader, partition table, OTA metadata, default NVS outside the two approved TUNER keys, or REMOTE storage outside the A-010 commit.
8. Verify normal UI/configuration first, then begin the separately authorized read-only identity/capability/state commissioning stage. No `volume.set` belongs to pairing provisioning.

The private implementation and binaries remain outside GitHub. PR #17 remains open and unmerged. The next owner decision is whether to authorize the first operation of this sequence: application-only installation of the TUNER commissioning helper after private capsule generation and pre-write hash verification.
