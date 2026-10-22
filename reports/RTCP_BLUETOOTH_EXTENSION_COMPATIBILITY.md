# RTCP/1 Bluetooth Extension v1 compatibility matrix

Status: **PROPOSED / NOT IMPLEMENTED / NOT HARDWARE TESTED**

Contract: [BTX/1.0 proposal](../references/RTCP_1_BLUETOOTH_EXTENSION_V1_PROPOSED.md)

## Version combinations

| REMOTE | TUNER | Capability sequence | Bluetooth result | Existing behavior |
| --- | --- | --- | --- | --- |
| Old | Old | one ID 3 → ID 4 | unavailable | unchanged D-009 and volume |
| Old | New | one ID 3 → exact legacy ID 4 | unavailable | unchanged D-009 and volume; no IDs 12–15 |
| New | Old | first ID 3 → ID 4; second ID 3 → ID 4 | clean fallback | unchanged D-009 and volume; buttons unavailable |
| New | New | first ID 3 → ID 4; second ID 3 → ID 12 | BTX negotiated | radio remains D-009; Bluetooth uses IDs 13–15 |

## Lifecycle combinations

| Event | Required behavior |
| --- | --- |
| RTCP reconnect | clear negotiation, pending command, source state and metadata; repeat both capability queries |
| REMOTE sleep | close session and clear all BTX authority; no stale action after wake |
| TUNER restart | fresh RTCP session and fresh callback state; no stored negotiation |
| Phone disconnect | increment source/connection generation, clear metadata, withdraw commands |
| Different phone reconnect | new generation; old command and metadata cannot apply |
| Bluetooth → radio | ID 14 clears Bluetooth state; fresh D-009 restores station and StreamTitle |
| Radio → Bluetooth | radio metadata is invalidated before Bluetooth metadata is displayed |
| TUNER rollback | second query returns legacy ID 4; REMOTE fails closed to D-009 |
| REMOTE rollback | no second query; TUNER remains legacy for the session |

## Decoder and malformed-data behavior

| Input | Required disposition |
| --- | --- |
| ID 12 without probe window | invalid; close session |
| ID 13/15 before negotiation | invalid; close session |
| ID 4 to the second query | supported legacy fallback; keep session |
| malformed ID 12/14/15 | invalid; close session |
| invalid locally sourced phone UTF-8 | omit affected field; keep session |
| valid command refusal | correlated ID 8; keep session |
| timeout/disconnect after command | ambiguous delivery; clear pending; never retry |

## Required compatibility verification

1. Byte-compare old-REMOTE/new-TUNER first capability response with the frozen legacy vector.
2. Run old REMOTE through radio metadata, playback controls and volume against new TUNER.
3. Run new REMOTE against the installed old TUNER and verify the second ID 4 fallback without reconnect.
4. Run new/new through source changes, phone reconnect and session replacement.
5. Roll back each application independently and repeat identity, D-009 and volume checks.

All cells remain software/hardware pending until firmware implementation is separately authorized.
