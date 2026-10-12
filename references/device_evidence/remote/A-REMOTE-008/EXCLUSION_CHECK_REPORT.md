# A-REMOTE-008 conditional component exclusion verification
Coordination input: `f1fa75ba2f0cabeb54d988492b93f40afd01da60`. Owner decision: 2026-10-12 Europe/Bucharest. Procedure recorded at 2026-10-12T04:05:06Z. Same PR14 **OPEN / unmerged**. New project material is English; previously published reports, evidence and archives are preserved without translation.

Current verdict: **INCONCLUSIVE — BUILD REPRODUCTION BLOCKED BY INTERMITTENT COMPILER PROCESS FAILURE**. A008 **IN PROGRESS**; source-to-build UNKNOWN; A009 **BLOCKED / NOT STARTED**. No complete new firmware builds or second-host tests.

## Conditional authorization and actual gate
Owner allows excluding the complete `components/esp_wifi_bsp/` from private offline transfer **only after every effective-input/indirect-influence and A/B invariance check is satisfied**. No placeholder or redacted source, original edits, credential transfer, source/bundle publication, SDK/hardware/security changes, PR merge or A009. Owner also requires stopping on further secrets. No exclusion from transfer has been applied.

The requested conditions are not all certified. Generated `project_description.json` records this component in `all_component_info`, including its directory/include directory/library/target and declared private dependencies `esp_wifi`, `esp_event`, `nvs_flash`. Removing the directory changes this generated discovery/dependency record. **This is distinguished from a positive selected-code dependency: none was found in the performed checks.** Interpreting the owner's no-generated-file/configuration/dependency-graph-use/change conditions literally, the metadata reference/change prevents an unconditional exclusion certificate. No relaxation of those conditions is assumed.

## Disposable A/B procedure
Create a separate disposable copy from the prior private first-host source tree with its local baseline/dirty version context, no reused .pio/build. Preserve original source bytes and restored LVGL files; no original directory edited or removed. Run `python -m platformio run -e remote01 -v -j1 -t compiledb` with installed-only/offline package guard and selected PIO6.2.0/platform6.13.0/framework3.50503.0/GCC14.2.0+20251107. PRESENT configure succeeds exit0, guard events NONE. Retain its generated inputs locally. Move only the entire disposable esp_wifi_bsp directory to a restricted local backup, verify resolved paths remain inside disposable/audit roots, remove only the disposable generated build directory, rerun the same command at the same source path. ABSENT configure succeeds exit0, guard events NONE. These are configuration/compile-database checks, not full builds. Raw commands/logs/generated files and backup remain private.

## Results and remaining checks
| Owner condition | Observed result |
| --- | --- |
| 1. Absent from effective component list | PASS: absent in historical original and fresh PRESENT/ABSENT effective lists; PRESENT and ABSENT lists equal |
| 2. No selected source includes component headers | No direct literal include matches for esp_wifi_bsp.h/name in selected source scan; full transitive/macro include closure NOT CERTIFIED |
| 3. No selected configuration/generated/dependency graph use | NOT SATISFIED under strict reading: root CMake retains negative EXCLUDE_COMPONENTS declaration; generated project_description discovery graph stores directory/include/target/private dependency information |
| 4. Removal invariance | 1449 translation units and full compile-command database byte-identical; sdkconfig.h/sdkconfig.cmake/sdkconfig.json, CMakeCache.txt and build.ninja byte-identical. Only project_description field all_component_info changes, losing esp_wifi_bsp entry; required zero generated-record/configuration/graph change not met |
| 4. Remaining pair checks | Failing-TU preprocessing pair, full linker-command/intended-artifact and dependency-resolution certificate NOT COMPLETED after metadata/configuration gate stopped dependent preparation; no implied PASS |
| 5. Historical exclusion | PASS: retained historical configured effective list omits component; unchanged root EXCLUDE_COMPONENTS contains esp_wifi_bsp |

Identical build.ninja includes identical generated link rules, but this is not represented as a full SCons final linker-command certificate. Compiler/SDK/application defects and hardware faults are not inferred from this metadata difference. Both restored zero-byte LVGL files remain in the disposable source tree; no transfer omission performed.

## Restricted evidence and preservation
The component directory-level content hash was computed locally from sorted relative names and file SHA-256 values. The directory hash, per-file hashes/content, SSID/password values and the restricted hash-record hash are **not published**, to avoid assisting credential guessing. The original component remains intact. No Git commit contains its source or credentials. New public evidence contains only sanitized procedure/results, not source/.i/raw logs/generated secret-bearing data/archive/toolchain binaries.

## Delivery disposition
| Requested field | Result |
| --- | --- |
| Private transfer archive path | NOT CREATED |
| Archive size / SHA-256 / included file count | NOT APPLICABLE; no archive |
| Excluded transfer paths | NONE applied; components/esp_wifi_bsp/ candidate not yet certified under every condition |
| Full remaining-input secret scan | NOT RUN; gated on conclusive authorized exclusion |
| Local bundle verification | NOT RUN; no bundle; disposable exclusion verification results above |
| Copy instructions / single initial second-host command | NONE; no validated transferable bundle/protocol |
| Transfer / second-host20x.i /20xsource /two complete clean builds/comparison | NOT RUN |

## Owner clarification required
Can the difference limited to **non-selected component-discovery metadata** be permitted while requiring effective compile/link/configuration/dependency inputs and all remaining checks to remain unchanged, or must the strict zero-generated-file/graph-change condition remain? This is an unresolved scope interpretation, not evidence of a compiled dependency or source mismatch. No exception applied. If strict conditions remain, preparation stays blocked. If explicitly permitted, complete all outstanding effective-input/preprocessing/secret-scan checks before bundling; no automatic transfer/device task/merge.

This English record supersedes the prior pending-owner-decision disposition only for receipt and verification of the conditional exclusion authorization. Historical [preparation stop](CROSS_HOST_PREPARATION.md) remains unchanged. [Machine-readable results](EXCLUSION_CHECK_RESULT.json); [first-host compiler diagnosis](ICE_DIAGNOSTIC.md). CCM1.1.0 frozen, Native unapproved, O01–O17/common gate OPEN/NOT PASSED; TUNER/production/backend/migration/hardware gaps unchanged.
