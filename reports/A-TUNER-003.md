# A-TUNER-003 — final integration and identified-artifact regression preparation

Date (UTC): 2026-10-08T17:53:04Z
Coordination execution input: `531aa8cd0435ed9813ab39664888992583df0d28`
Status: READY FOR REVIEW — software integration and artifact preparation PASS;
physical hardware PENDING / NOT RUN.

## Outcome

Firmware PR #2 remained exactly at reviewed commit
`8fac1da6ccd749a47843d99dc746fc3d6e4bf19b`, based on prior `main`
`371cdebce7ba2648ea71636d5bdb5d738b42e680`. Final call-path review found no
substantive difference or new defect in the authorized four corrections. The
PR was merged ordinarily as `d1e51765179f99567df3b5d18a451152adac514c`.
Its Git tree `01a23382bf54be3e1a04fa992984e62c4570be8d` exactly equals the reviewed
head tree.

A documentation-only artifact/changelog PR #3 was then merged as firmware
`main` `cb17e945b9c0e086a03e7176d9ad442a8c78d89b`. The final `main` adds only
the artifact manifest/checklist documentation and CHANGELOG entry after the
software merge; executable/configuration paths are unchanged.

## Integration disposition

| Item | Software review/integration | Physical status |
| --- | --- | --- |
| B01 strict DELETE parsing/no mutation | PASS; both real handlers validate full decimal/range before remove call | PENDING |
| B03 discovered codec through Favorite/NVS/reload | PASS; value-owned codec reaches add/save/load and decoder selection | PENDING |
| B04 zero/stale saved traversal only | PASS; both directions no-op before unsafe arithmetic/play | PENDING |
| B06 saturating radio/BT Down | PASS; shared volume path reaches and remains zero | PENDING |
| Prior decoder/Recent/metadata/BT/HTTPS fixes | No conflicting executable change found | Representative regression PENDING |

Full B04 identity semantics and B02/B05/B07–B11 remain outside this task.
There is no Native/API/transport/security/discovery/pairing, dependency,
platform, partition, GPIO, version or contract change.

## Exact artifact

The original reported binary was still available in the unchanged isolated
build and was recovered, not rebuilt:

- Source commit: `8fac1da6ccd749a47843d99dc746fc3d6e4bf19b`
- Embedded build ID: `8fac1da6ccd7`
- File: `firmware.bin`
- Size: 1,999,408 bytes
- SHA-256: `AF066BA215F863A7D2583A6313ACEE00020CCFAD4F8F8C3168DEDA76BCD6F5D4`
- Public non-production prerelease: https://github.com/OviOneKenoby/ESP32-WROVER-Internet-radio/releases/tag/a-tuner-003-regression-8fac1da
- Direct binary: https://github.com/OviOneKenoby/ESP32-WROVER-Internet-radio/releases/download/a-tuner-003-regression-8fac1da/firmware.bin
- Manifest: https://github.com/OviOneKenoby/ESP32-WROVER-Internet-radio/blob/cb17e945b9c0e086a03e7176d9ad442a8c78d89b/artifacts/A-TUNER-003/SHA256SUMS.txt

Public download readback reproduced the exact size/hash. The prerelease tag
resolves to the tested source commit. This is deliberately not a production
release.

## Verification basis

The executable source and artifact did not change, so the task-directed reuse
of prior evidence applies:

- A-TUNER-002 MSYS2 GCC 16.2.0 deterministic suite: PASS, 249 checks.
- Independent PM Ubuntu GCC 13.3.0 suite: PASS, 249 checks.
- Original isolated clean PlatformIO build: PASS; RAM 83,056 / 327,680
  (25.3%), flash 1,992,833 / 3,145,728 (63.4%).
- Final merge/tree and scoped executable-diff checks: PASS.
- Original artifact hash and public release readback: PASS.
- Physical upload/regression: NOT RUN / PENDING.

Complete commands, versions, identities, hashes and the non-verdict optional
rerun note are in
[integration evidence](../references/device_evidence/tuner/A-TUNER-003/INTEGRATION_AND_ARTIFACT.md).

## Owner-assisted regression package

The exact owner checklist is versioned at
[OWNER_REGRESSION_CHECKLIST.md](https://github.com/OviOneKenoby/ESP32-WROVER-Internet-radio/blob/cb17e945b9c0e086a03e7176d9ad442a8c78d89b/artifacts/A-TUNER-003/OWNER_REGRESSION_CHECKLIST.md)
and also attached to the prerelease. It requires:

1. Hash/size/build-ID gates for the exact artifact.
2. Catalog export and a restoration plan before sacrificial changes.
3. Owner-selected app-only flash at `0x10000`, without erase or assumed port.
4. Actual station and Favorite DELETE requests for empty/sign/space/junk/
   overlength/255/256/live-count boundaries plus valid zero/middle deletion,
   with response and byte-comparable before/after JSON.
5. Physical and serial one/many/empty/stale Next/Previous behavior.
6. Radio and connected-Bluetooth Down to zero and again at zero.
7. Opaque AAC/AAC+ playing-screen Favorite, JSON codec observation, actual
   reboot/reload/decoder/audio; opaque MP3 and verified explicit `.aac` cases.
8. Dated HTTP/HTTPS MP3, AAC+, metadata, Recent, Favorites, web/local/e-paper,
   Wi-Fi, Bluetooth/AVRCP/metadata/transition and diagnostics regression.
9. Full serial/HTTP/flash evidence and catalog restoration.

The previously observed opaque KIIS URL is listed only as a dated preflight
candidate; stream availability must be verified during the test. Missing or
unavailable cases remain PENDING and are never converted to modeled PASS.

## Remaining hardware checks

- Owner download/hash and deliberate app-only flash of the exact binary.
- `/api/diagnostics` confirmation of build ID `8fac1da6ccd7`.
- Every B01/B03/B04-empty-stale/B06 matrix row with observed evidence.
- Representative regression and post-test catalog restoration.
- Actual flashed identity, test date, board/port and complete logs.

No hardware was accessed automatically. Actual flashed firmware remains
UNKNOWN. The common gate remains OPEN / NOT PASSED, O01–O17 remain OPEN, CCM
1.0.0 remains OWNER APPROVED/FROZEN, and TUNER Native API v1 remains
UNAPPROVED/UNFROZEN/NOT IMPLEMENTED.
