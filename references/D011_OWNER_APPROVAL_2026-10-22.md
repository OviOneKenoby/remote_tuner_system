# D-011 BTX/1.0 owner approval - 2026-10-22

Status: **OWNER APPROVED / FROZEN**

Reviewed proposal head: `e5bec2d639ec6c99cd52aabaafa3e52582754105`

Approved contract: [RTCP/1 Bluetooth Extension v1](RTCP_1_BLUETOOTH_EXTENSION_V1_PROPOSED.md)

The owner explicitly approved:

- BTX/1.0 and D-011;
- the authenticated consecutive second-ID-3 negotiation;
- message IDs 12–15 and reuse of correlated result ID 8;
- artist maximum 96 UTF-8 bytes and title maximum 127 UTF-8 bytes;
- authoritative Bluetooth playback state from A2DP callbacks;
- source and phone-generation fencing;
- the specified resource budgets and TUNER-first rollout;
- exact backward compatibility with frozen D-009.

This approval authorizes coordination status recording plus TUNER source implementation, focused tests, one production build and publication to review branches. It does not authorize REMOTE source changes, hardware flashing, NVS/pairing/partition changes, PR merges or releases.

The reviewed wire fields and semantic rules are frozen for implementation. Frozen D-009, RTCP/1 transport security and CCM 1.1.0 remain unchanged.
