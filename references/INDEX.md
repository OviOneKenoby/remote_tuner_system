# Coordination evidence index
Date (UTC): 2026-10-08T13:55:34Z
Coordination planning input: dd63c07e485218dfc34ceb6a8855c8a929b4ae89

## Provenance and availability
The owner supplied REMOTE_TUNER_PROJECT_MANAGER_STARTER.zip earlier in this PM conversation. The complete package was read; its 12 manifest checksums matched. All 13 entries are copied byte-for-byte into starter_2026-10-08/; original filenames, CRLF/LF and status text are retained. These are immutable historical/source-audit reference copies, not synchronized current firmware. Do not edit them. Original relative links to files absent/renamed in that package may be unresolved; use this index and source provenance instead of fabricating targets.

The final approved CCM 1.0.0 file and original approval record are not included. Freeze status is established in later supplied records; candidate.4 is only a semantic historical reference. A-REMOTE-001 must recover the actual frozen artifact and approval provenance.

## Original package SHA-256
| Path under starter_2026-10-08/ | SHA-256 | Bytes |
| --- | --- | --- |
| 00_READ_ME_FIRST.md | cb6ed83897f226c2b5dab02a9d07cff02d432ee96f1f6c52145d6bf7dabcd619 | 2939 |
| PROJECT_MANAGER_BOOTSTRAP_PROMPT.md | 2f34e89cf00ca7858ade8017be1c2ddbec0e6bd31a7298865d278a720cb25645 | 9034 |
| REMOTE/COMMON_CONTROL_MODEL_V1_PRE_FREEZE_REFERENCE.md | 0aae4c13c1f41c2e434970ef6d69a664f5e92addd57e5c37e4abd66512359ad0 | 112311 |
| REMOTE/CONTROL_ARCHITECTURE.md | f3e9ac95b92935bf4d26978f6192f077ff52b458fcb81ab054c91a0117a697fc | 56883 |
| REMOTE/REMOTE01_PRODUCT_DECISIONS.md | 22c36123ff0db505e2e18db02263f54f998bbec19223f4a376800d77fafd9b0f | 9774 |
| REMOTE/REMOTE_CHANGELOG_AVAILABLE_2026-10-06.md | 827813bf0b8d7a5f1deaf225598a519b391a23a918519ffde9e83730b047b35b | 131119 |
| REMOTE/TUNER_NATIVE_API_V1_PRE_AUDIT_CANDIDATE.md | 830648708076820d90187c4a081bbe7c483e82983c43289c05f13667b6981a1b | 64049 |
| SHA256SUMS.txt | 826ab53439d3774335793095eee01fb754c5ffdb6e4564ed73b6f1461ef8645c | 1270 |
| SHARED/TUNER_REQUIREMENTS_FROM_REMOTE.md | fc6303f73c231e3abad91171ce0ea29ad05afe2b4c27833c5bd8743f79246c12 | 36321 |
| TUNER/TUNER_IMPLEMENTATION_AUDIT.md | 3fde627d398b66c5494e91bad1ea06ae32210138bb98f9107b183fdbef4c4024 | 29480 |
| TUNER/TUNER_REMOTE_CAPABILITY_MATRIX.md | 6f29c97863baaf16079b1d948d6d0d6da0159e9566e45dfebb568566008922e4 | 5353 |
| TUNER/TUNER_REMOTE_IMPLEMENTATION_PLAN.md | c28ba9c9a8f637b29a2a9b59ddf8b96905e5d83588c2ffad9701bc46760691b5 | 5909 |
| TUNER/TUNER_REMOTE_SYSTEM_ARCHITECTURE.md | 46ac32be362fed8df3a8c3fc0ed7db5f1678a840a3c405188fbf90c1bd794d4c | 5310 |

## Authority / limits
| Reference | Available evidence | Limit / required next input |
| --- | --- | --- |
| Frozen CCM 1.0.0 | Later freeze entry in REMOTE changelog, current architecture and handoff | Actual approved artifact and original approval provenance still missing |
| Historical CCM candidate.4 | REMOTE/COMMON_CONTROL_MODEL_V1_PRE_FREEZE_REFERENCE.md | Stale header; do not promote/rename or silently change semantics |
| Native API candidate | REMOTE/TUNER_NATIVE_API_V1_PRE_AUDIT_CANDIDATE.md | Unapproved design; later handoff supersedes evidence/status/ownership assumptions |
| Canonical cross-device handoff | SHARED/TUNER_REQUIREMENTS_FROM_REMOTE.md,2026-10-07 | Sections22 acceptance/24 O01-O17; requirements are not implementation |
| TUNER audit/plan/matrix/architecture | TUNER/ four documents, expected main / 371cdeb/v1.1.0 | Supplied source-backed audit; no fresh build/runtime/hardware proof |
| REMOTE decisions/architecture/changelog | REMOTE/ snapshots through 2026-10-06 | Later entries supersede earlier statements; current checkout/flashed image unknown |
| Provenance warning | 00_READ_ME_FIRST.md | Read before using candidate headers |
| Live TUNER source | https://github.com/OviOneKenoby/ESP32-WROVER-Internet-radio/tree/371cdebce7ba2648ea71636d5bdb5d738b42e680 | PM verified remote main/version; local tree/build/hardware NOT VERIFIED |
| Live REMOTE source | UNKNOWN; supplied historical local path C:/Users/RYZEN/Documents/REMOTE01/Code | Device actor must locate current checkout and record Git identity or reproducible manifest |

## Current verification
PM used GitHub get-ref and fetch-file at TUNER commit 371cdebce7ba2648ea71636d5bdb5d738b42e680; src/config.h contains FIRMWARE_VERSION1.1.0. Source confirmation is separate from running firmware.
No passwords/tokens/private telemetry added. Both latest device handoffs remain the owners' initial placeholders until device inspections publish results.
