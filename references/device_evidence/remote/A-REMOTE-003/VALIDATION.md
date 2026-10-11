# Publication validation

- Execution input and freshly fetched origin/main:531aa8cd0435ed9813ab39664888992583df0d28;no concurrent changes at recheck. Existing task/package/rules/current statuses/handoffs read. PM registers/TUNER untouched.
- Full4040-file device hash comparison:4039 entry files unchanged,only append-only CHANGELOG changed;new files limited to docs/A_REMOTE_003_D0_QUALIFICATION.md and isolated tools/qualification/a_remote_003. No .pio/source/tests/config/artifact changes. Details SCOPE_VALIDATION.json.
- Installed pinned NVS storage/page/handle/constants/nvs.h bytes match A-002 snapshots;frozen CCM hash unchanged. New standalone source mirrored byte-exact to device;not selected by CMake/main/components.
- Handoff matches exact template headings/fields;archive matches original input Git blob bytes. Prior archive untouched.
- Host run PASS13 tests/3859 counted checks,0failures/errors;87 scenarios;model counterexample captured. Current maximal-size derivation equals44284-byte fixture. No firmware normal/soak/build/upload/hardware run.
- Administrative .gitattributes exception applies only to new A-003 evidence so native CRLF bytes/hashes survive publication;root SHA256SUMS refreshed from staged canonical bytes.
- Authored local Markdown links and staged checksum manifest validated before commit. git -c core.whitespace=cr-at-eol diff --cached --check checked (native evidence CRLF preserved). Archived links retain their original handoff base;archive bytes are never rewritten. Final commit/PR/readback reported in publication response;no automatic merge.
