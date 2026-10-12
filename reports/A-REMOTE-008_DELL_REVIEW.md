# A-REMOTE-008 Dell evidence review and practical closure

Coordination input `b3ee531bec15d690f0e33f35a2d353deec7163b1`; review 2026-10-12T17:57:51.204673+00:00; same PR14 OPEN/unmerged. **PASS â€” PRACTICAL DELL SOURCE-TO-BUILD REPRODUCTION (HOBBY / PUBLIC-BETA SCOPE)**. A008 execution/review **DONE at the owner-approved practical hobby/public-beta level**, delivery **READY FOR OWNER REVIEW**. A009 remains **BLOCKED / NOT STARTED**. This supersedes the current pre-Dell INCONCLUSIVE/build-blocked disposition, not its historical raw evidence. No production source/config/partition changes, hardware operations, PR merge or source/archive publication.

## Archive and evidence verification

Before extraction, results archive size1,597,657,193 bytes and SHA-256 `792432a5581ce92a2ddec35c4b2d6f9deec57ef03593912c34aa3a7aa6c593ec` exactly match owner-supplied identity. New private TEMP extraction path/member safety checked,42,780 files /5,955,153,681 uncompressed bytes hashed privately. No incoming script executed. Original private archive, source, SDK/toolchain, generated artifacts and absolute paths are not published.

Owner reports initial bundle archive/all29,831 manifest entries verified on Dell. Reviewer separately verifies44 outcome names/exit codes, all raw log hashes and contents,40 object hashes, every recorded clean-build artifact hash, image/ELF metadata and raw comparison records against actual extracted files. All three1,613-file source copies byte-match the approved private bundle; no missing/different file. Effective SDK configuration dictionaries identical across all three Dell builds and the historical original profile. Pinned versions, complete package identities and both complete Python distribution sets match; all2,049 copied toolchain file hashes and the original RGB SDK source match the approved bundle.

Dell: Windows11Pro10.0.26200, amd64; Intel Core i5-7440HQ4cores/4threads, RAM17,050,853,376 bytes; recorded free disk118,531,428,352 bytes; PowerShell5.1.26100.9444. Python3.11.7, PlatformIO6.2.0, espressif32@6.13.0, framework3.50503.0 / IDF5.5.3, GCC14.2.0+20251107, binutils2.43.1. Host inventory timestamp2026-10-12T16:35:51Z,19:35:51 Europe/Bucharest. Complete versions retained privately; [sanitized review manifest](../references/device_evidence/remote/A-REMOTE-008/DELL_REVIEW_RESULT.json).

## Dell totals and serial execution

| Check | PASS | FAIL / ICE | Evidence |
| --- | --- | --- | --- |
| CONFIGURE_RGB |1/1, exit0 |0/0 | actual log/record |
| Retained frozen-preprocessed unit |20/20, all exit0 |0/0 |20 actual objects, identical SHA1c9697744e5ba5e57f6fbdb44bcbc15a87213ebb42df7ee8f1dcc17c07482745; same as Ryzen frozen-input smoke object |
| Original SDK RGB source command |20/20, all exit0 |0/0 |20 actual objects, identical SHAf683eb5e1b849346047f4b9e903601df1c8ae0fe9b0e59d1c34a03ba2f760bc5 |
| Fresh full clean builds |3/3, all exit0, -j1 |0/0 |608.444s /584.057s /582.254s; complete BIN/ELF/map/bootloader/partitions |

The runner SUMMARY deliberately retains the pre-review INCONCLUSIVE label; this review supersedes that label using the completed outcome evidence, without editing the private raw record. All44 records match the expected sequence. No failed build, missing required artifact or ICE found. Recorded actions are configuration/compiler/build-only. No reviewer rerun, upload, serial access, flashing or hardware mutation. [Sanitized logs](../references/device_evidence/remote/A-REMOTE-008/DELL_TEST_LOGS_SANITIZED.log) omit private absolute paths, source-code excerpts and complete raw compiler commands; original log hashes bind private evidence. Source command and frozen-input object hashes differ from each other as separate diagnostic populations; no cross-population identity claim.

## Clean-build comparison and material differences

The three builds are **not mutually byte-identical**. Application BIN/ELF/map and bootloader BIN/ELF hashes differ. Partition table, initial OTA data, bootloader map and compiler-ABI probe artifacts are byte-identical. [All artifact hashes](../references/device_evidence/remote/A-REMOTE-008/DELL_ARTIFACT_HASHES.md); every artifact rehashed independently.

Build1/2 application size2,485,824 bytes; build3 size2,485,568 bytes. ELF size17,758,832 bytes in all three. All application image headers/entry/7-segment count/project12_LVGL_Test/version1/IDF5.5.3 agree. Dates/times and embedded ELF hashes remain visibly different: app times19:41:28 /19:51:39 /20:01:25, dateOct12,2026. Absolute paths remain in private ELF metadata and are sanitized only in public prose/logs, not in artifacts. No output normalization manufactured equality.

A bounded existing-data check covers the260-byte flash-text span reduction in build3 (991126 /991126 /990866 ELF section bytes). The actual selected archive-member multiset is identical:895 members in each build. Three function sizes differ (`setup_scr_screen`, `tx_param`, `tx_color`), but each retains the same provider and byte-identical pre-link instructions **and relocation records** across builds. Final positions/sizes vary consistently with Xtensa linker layout/relaxation. Initial map referencing-object lines must not be read as alternate definitions: the UI function provider is the same generated UI object in all builds. No selected-source, effective configuration, partition layout or demonstrated functional-content discrepancy was found. This is sufficient for the approved practical build baseline; it is not a runtime semantic-equivalence proof. No further ordering/timestamp/discovery investigation is opened.

## Historical installed/A006 comparison

Historical application SHA7e8d77c21898014fbd7ea625cf2d25aa7f77941d5ba1d24484090f7361279afb differs from every Dell BIN. Historical image header, entry0x4037c44c,7segments, project/version/IDF agree; build1/2 share historical image length/segment layout. Build3 has the documented smaller text span. Historical app descriptor dateOct6,2026/time23:57:20 versus DellOct12 times; debug paths, linked layout and embedded ELF hashes differ. Historical partition table is **byte-identical** to all three Dell outputs (SHAd7ffd497cfcd33e697304b3cf8112e7a1f1cb0619639fe9879ed431cbbdc8835). Source files/configuration of the current bundle are confirmed reproducibly buildable on Dell, but exact historical binary identity and full installed runtime semantic equivalence are **NOT DEMONSTRATED**. A006 flashed-source commit remains UNKNOWN; no new device inspection or flash.

## Ryzen/Dell reconciliation and final verdict

Ryzen had intermittent original-source compiler process failures/ICE; unchanged frozen .i repeatedly compiled, original source alternated PASS/ICE, same official toolchain/pinned flags retained. Dell passed20/20 original-source compilations and3/3 complete serial clean builds from the approved bundle. Therefore the narrowest supported classification is **intermittent Ryzen host/environment/compiler-process failure, not a reproducible source defect in the reviewed tests**. Exact OS/compiler interaction or hardware cause remains UNKNOWN; no hardware fault is proven. Earlier Ryzen ICE and SCons image-action TypeError records remain historical, but they no longer block practical A008 build closure.

**PASS â€” PRACTICAL DELL SOURCE-TO-BUILD REPRODUCTION (HOBBY / PUBLIC-BETA SCOPE)**; A008 execution/review DONE, owner acceptance pending. Current-source-to-generated-Dell-artifact confidence established; reproducible byte identity and deployed behavior are separate, unclaimed properties. Remaining limits are proportionate: no fresh runtime/hardware/USB-recovery/migration/partition-write/persistence/backend qualification, no historical byte-identity proof, no isolated Ryzen root cause. No industrial/production certification work is reopened.

## PR disposition and next owner decision

Recommend owner accept the practical A008 closure and merge PR14 as **documentation/evidence only** after review, with byte-identity/runtime limits explicitly retained. PR14 is kept OPEN/unmerged by this publisher. Then separately decide/authorize the next A009 scope; none is started or automatically dispatched here. Native remains UNAPPROVED/UNFROZEN/NOT IMPLEMENTED; CCM1.1.0 frozen and historical1.0.0 untouched, O01â€“O17 OPEN, common gate OPEN/NOT PASSED. D00864KiB is architectural approval only; backend/migration/production gaps and historical ADCFAIL/rollback-residency PENDING remain. TUNER source/evidence/handoff unchanged.
