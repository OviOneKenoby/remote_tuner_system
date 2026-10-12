# Owner project scope — robust public hobby beta

Owner decision2026-10-12, coordination input `aaed9dbedb50da03d2e33dd757a8b953432b8aac`. TUNER//01 and REMOTE//01 are hobby/open-source firmware projects intended for a robust public beta. This records product scope; it does not authorize automatic task execution or replace shared-contract approval.

STL/CAD files and complete commercial assembly manuals are distributed separately through Cults3D and are not part of the public firmware repositories.

Reserve deep forensic investigation for severe, reproducible functional defects, data-loss/bricking risks, security issues or failures without practical recovery. Document non-critical theoretical uncertainty without automatically blocking feature development. Practical hardware validation, USB recovery and honest known-issue documentation remain required; hardware execution still needs task-specific authorization.

Current roadmap:

1. REMOTE build baseline.
2. 64 KiB layout and USB recovery.
3. Minimum persistence.
4. Common REMOTE–TUNER API.
5. Functional REMOTE control.
6. MQTT and Smart Home/SmartThings.
7. UI.
8. AAC/AAC+ repair later.

TUNER web/network access must remain functional while Bluetooth audio is active. REMOTE displays station artwork/logo based on the station selected by TUNER; current-track artwork is not the requirement.

A008 IN PROGRESS; A009 BLOCKED / NOT STARTED. CCM1.1.0 OWNER APPROVED/FROZEN and historical CCM1.0.0 unchanged. Native API UNAPPROVED/UNFROZEN/NOT IMPLEMENTED; O01–O17 OPEN; common gate OPEN/NOT PASSED. Architectural64KiB approval is not migration, persistent-write, backend or production acceptance. No firmware/device task, hardware operation, source publication or PR merge is authorized by this scope record.
