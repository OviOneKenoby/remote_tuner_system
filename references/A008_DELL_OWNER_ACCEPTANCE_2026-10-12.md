OWNER DECISION — END FORENSIC EXCLUSION ANALYSIS AND PREPARE THE DELL BUNDLE

The project target is a robust public hobby/open-source beta, not industrial or production certification.

The current linker-order difference is accepted as host/build-system nondeterminism because:

- the library multiset is identical;
- the ordering varies between A captures as well;
- causation by removing components/esp_wifi_bsp is not demonstrated;
- selected commands, components and tested preprocessing/dependencies otherwise match;
- the RGB preprocessing comparison is byte-identical;
- fixed-epoch temporal comparisons passed where evaluated.

Do not continue investigating library ordering, timestamps, discovery metadata, or other non-functional nondeterminism during bundle preparation.

OWNER ACCEPTANCE

I accept exclusion of:

components/esp_wifi_bsp/

from the private cross-host bundle.

Document that:

- the transferred source tree is intentionally not byte-identical to the complete private workspace;
- the excluded component contains credentials;
- available evidence shows it is outside the selected build;
- residual uncertainty is acceptable for a public hobby beta;
- final confidence will come from successful builds on the Dell host.

Do not modify or delete the original directory.

WORKING POLICY

From this point onward:

- stop only for a secret contained in an effective build input;
- stop for missing/corrupt files required to build;
- stop for a real compiler/linker input difference that prevents reproduction;
- stop for a destructive action or required hardware access;
- do not stop for timestamps, absolute paths, generated inventory records, ordering variation already observed within the same configuration, or metadata without demonstrated functional effect;
- document such differences and continue.

BUNDLE PREPARATION

1. Complete the secret scan of the proposed bundle.

2. For findings outside the effective build graph:
   - exclude the complete unrelated file or directory;
   - record the exclusion and non-sensitive reason;
   - continue without requesting separate owner approval.

3. For a secret inside an effective build input:
   - stop;
   - report only the path and secret category;
   - do not reveal its value.

4. Include everything required to reproduce the configured REMOTE build:
   - effective source and configuration inputs;
   - PlatformIO configuration and scripts;
   - partition input;
   - sdkconfig inputs;
   - exact dependency information;
   - exact framework/platform/toolchain identities;
   - original RGB compile command;
   - retained `.i` diagnostic input;
   - scripts needed for the Dell test.

5. Do not include:
   - components/esp_wifi_bsp/;
   - credentials;
   - GitHub authentication material;
   - device/NVS dumps;
   - previous build directories;
   - unrelated evidence archives;
   - temporary files.

6. Prefer an offline self-contained bundle where practical. If exact official packages are too large to include, provide a verified installer/bootstrap process pinned to exact versions and hashes. Do not silently select newer packages.

7. Create:
   - `BUNDLE_MANIFEST_SHA256.txt`;
   - `BUNDLE_EXCLUSIONS.md`;
   - `ENVIRONMENT_MANIFEST.md`;
   - `SECOND_HOST_PROTOCOL.md`;
   - `RUN_SECOND_HOST_TEST.ps1`;
   - archive SHA-256;
   - a private archive suitable for copying to the Dell laptop.

DELL TEST RUNNER

The PowerShell runner must:

1. Verify the archive/bundle manifest before doing anything else.
2. Use an isolated directory.
3. Avoid global upgrades or modification of unrelated installations.
4. Record Windows version, architecture, CPU, RAM and free disk space.
5. Record exact PlatformIO, platform, framework, GCC and binutils versions.
6. Perform:
   - 20 serial compilations of the retained `.i`;
   - 20 serial compilations from the original `esp_lcd_panel_rgb.c` command;
   - SHA-256 comparison of successful object files;
   - three complete serial clean builds using `-j1`.
7. Preserve every PASS, failure and ICE.
8. Hash firmware, ELF, map, bootloader and partitions artifacts from every successful clean build.
9. Compare successful builds with one another.
10. Compare the resulting application firmware structurally with the historical/installed A-006 artifact whose SHA-256 is:

7e8d77c21898014fbd7ea625cf2d25aa7f77941d5ba1d24484090f7361279afb

11. Keep timestamp, Git-version and path metadata visible in final artifact analysis. Do not manufacture a binary match through normalization.
12. Never access, flash or modify REMOTE hardware.

LOCAL VERIFICATION

Before reporting completion:

- extract the archive into a fresh temporary directory;
- verify every manifest entry;
- verify the PowerShell runner parses correctly;
- verify no excluded credential-bearing path is present;
- verify the archive itself was not added to Git;
- verify no REMOTE private source was published.

PROJECT POLICY RECORD

Add a concise English project-scope record to the coordination repository:

- TUNER//01 and REMOTE//01 are hobby/open-source firmware projects intended for a robust public beta.
- STL/CAD files and complete commercial assembly manuals are distributed separately through Cults3D and are not part of the public firmware repositories.
- Deep forensic investigation is reserved for severe, reproducible functional defects, data-loss/bricking risks, security issues, or failures without practical recovery.
- Non-critical theoretical uncertainty is documented but does not automatically block feature development.
- Practical hardware validation, USB recovery and honest known-issue documentation are required.
- Current roadmap:
  1. REMOTE build baseline;
  2. 64 KiB layout and USB recovery;
  3. minimum persistence;
  4. common REMOTE–TUNER API;
  5. functional REMOTE control;
  6. MQTT and Smart Home/SmartThings;
  7. UI;
  8. AAC/AAC+ repair later.
- TUNER web/network access must remain functional while Bluetooth audio is active.
- REMOTE displays station artwork/logo based on the station selected by TUNER; current-track artwork is not the requirement.

PUBLICATION AND STOP POINT

Update the existing PR #14 with:

- the owner acceptance;
- the revised hobby-beta scope;
- the sanitized bundle methodology;
- the private archive hash and size;
- no private source and no archive contents.

Keep PR #14 OPEN and unmerged.

Do not start A-REMOTE-009.

Stop only when either:

A. the bundle is ready and locally verified; report:
   - archive path;
   - archive filename;
   - size;
   - SHA-256;
   - included-file count;
   - excluded paths;
   - secret-scan result;
   - exact item the owner must copy;
   - one initial PowerShell command to run on Dell;

or:

B. an actual effective-build secret or missing required input prevents creation; report that single concrete blocker.

Do not return another timestamp, inventory, or linker-order investigation as a blocker.