# A-REMOTE-009 preparation owner authorization

Recorded UTC: 2026-10-12T18:22:12.346791+00:00. Coordination input: `e6fa6f4911eb6bcd342d1db9600ad66f134636ab`.

The owner explicitly assigns and authorizes execution of A-REMOTE-009 **preparation only**, at the practical hobby/public-beta assurance level: inspect current private source and effective configuration, prepare only the approved 64KiB partition addition, verify existing partition entries unchanged, build locally in a disposable private copy, and publish sanitized documentation, hashes, safe generated partition evidence and an unexecuted USB/ROM backup/recovery/rollback protocol in a new OPEN/unmerged PR.

No hardware access or persistent hardware operation is authorized: no flash/partition writes, erase, firmware upload, NVS mutation or hardware recovery tests. Stop before the first persistent hardware operation and request explicit owner approval against the concrete reviewed artifacts and protocol. The protocol itself is not execution authorization; execute none of its commands during preparation.

Use accepted A006/A007 facts: physical16MiB flash; installed table matched baseline; factory0x10000; target64KiB at0xE20000 observed65536 erased bytes; retain every existing partition and both3MiB OTA slots. Add no backend, API, MQTT, SmartThings or UI. Do not modify TUNER, reopen CCM/A008, start A010, publish private source/credentials/bundles or conduct unrelated industrial forensics. Further investigation only for concrete functional/data-loss/security/bricking risk. If the known intermittent Ryzen compiler failure occurs, use bounded retry and accepted A008 conclusion.

A008 remains DONE / OWNER ACCEPTED with its evidence and limitations preserved. CCM1.1.0 frozen; historical1.0.0 unchanged; Native UNAPPROVED/UNFROZEN/NOT IMPLEMENTED; O01–O17/common gate OPEN/NOT PASSED. This supersedes only the prior A009 BLOCKED/NOT STARTED preparation status; hardware deployment remains separately gated.
