# A-REMOTE-011 authenticated TCP record profile (RTCP/1)

Status: Phase 2 implementation specification. It binds transport security for the first CCM 1.1.0 milestone and does not alter CCM semantics.

All integers are unsigned, network byte order. Octet strings are transmitted without text encoding. Implementations use fixed buffers, reject non-canonical lengths and clear session secrets on every close. The only operational secret is a random 32-byte per-pair PSK provisioned privately; it must never enter source control or logs. `pairing_id` is a random 16-byte non-secret lookup identifier.

## Connection and handshake

REMOTE opens one persistent TCP connection to TUNER. TUNER accepts at most one authenticated peer. Handshake messages have this eight-byte header:

| Offset | Size | Field | Value |
| ---: | ---: | --- | --- |
| 0 | 4 | magic | ASCII `RTCP` |
| 4 | 1 | version | `1` |
| 5 | 1 | message type | `1` ClientHello, `2` ServerHello, `3` ClientFinish |
| 6 | 2 | body length | exact length below |

The fixed exchange is:

1. `ClientHello` (40 bytes total): header with body length 32, `pairing_id[16]`, fresh CSPRNG `client_nonce[16]`.
2. `ServerHello` (56 bytes total): header with body length 48, fresh CSPRNG `server_nonce[16]`, `server_proof[32]`.
3. `ClientFinish` (40 bytes total): header with body length 32, `client_proof[32]`.

Define `CH` as the complete ClientHello. Define `SH_prefix` as the ServerHello header followed by `server_nonce`. Then:

```
server_proof = HMAC-SHA-256(PSK,
    ASCII("RTCP1 server proof") || CH || SH_prefix)
SH = SH_prefix || server_proof
CF_prefix = ClientFinish header
client_proof = HMAC-SHA-256(PSK,
    ASCII("RTCP1 client proof") || CH || SH || CF_prefix)
CF = CF_prefix || client_proof
transcript_hash = SHA-256(CH || SH || CF)
```

Compare proofs in constant time. Neither side treats the session as authenticated until its peer proof verifies. Nonces must come from the platform CSPRNG and must not repeat with the same PSK. A repeated local nonce, unknown pairing ID, wrong size/version/type, failed proof, timeout or extra handshake byte closes the connection without application processing. The handshake deadline is three seconds from TCP accept/connect. No authentication error detail is sent to the peer.

## Key derivation

Use RFC 5869 HKDF-SHA-256. Existing mbedTLS HMAC-SHA-256 primitives may implement RFC 5869 where the pinned framework does not expose an HKDF component.

```
salt = SHA-256(ASCII("RTCP1 HKDF salt") || client_nonce || server_nonce)
PRK  = HKDF-Extract(salt, PSK)
```

Each output below is a separate `HKDF-Expand(PRK, info, L)`:

| Output | L | info |
| --- | ---: | --- |
| client-to-server AES key | 16 | `ASCII("RTCP1 c2s key") || transcript_hash` |
| server-to-client AES key | 16 | `ASCII("RTCP1 s2c key") || transcript_hash` |
| client-to-server nonce prefix | 4 | `ASCII("RTCP1 c2s nonce") || transcript_hash` |
| server-to-client nonce prefix | 4 | `ASCII("RTCP1 s2c nonce") || transcript_hash` |
| session ID | 8 | `ASCII("RTCP1 session id") || transcript_hash` |

The 32-byte PSK is input keying material and is not truncated to an AES key. AES keys and nonce prefixes are directional. Session ID, keys, prefixes and counters are volatile and invalidated on disconnect, sleep, authentication failure or reconnect.

## Authenticated records

Every record is one fixed header, ciphertext of the declared length and a 16-byte AES-128-GCM tag. Maximum plaintext/ciphertext is 512 bytes. Header size is 28 bytes and maximum wire size is 556 bytes.

| Offset | Size | Field | Rule |
| ---: | ---: | --- | --- |
| 0 | 4 | magic | ASCII `RTCR` |
| 4 | 1 | version | `1` |
| 5 | 1 | record type | `1` application; other values currently invalid |
| 6 | 2 | flags | zero |
| 8 | 8 | session ID | derived value above |
| 16 | 8 | counter | starts at 1, strictly consecutive per direction |
| 24 | 2 | plaintext length | 0 through 512 |
| 26 | 2 | reserved | zero |

The complete 28-byte header is GCM associated data. The 96-bit GCM nonce is `directional_nonce_prefix[4] || counter_u64_be`. The wire value is `header || ciphertext || tag[16]`. A sender increments its counter only after forming a record and closes before counter exhaustion; it must never reuse a key/nonce pair. A receiver accepts only its exact next counter. Duplicate, lower, skipped or exhausted counters, wrong session/header/length, truncation, trailing bytes or tag failure invalidate the whole session and close the socket before payload parsing. Failed records do not advance application state.

TCP framing reads the fixed header first, validates its public bounds, then reads exactly `length + 16` bytes. There is one 556-byte receive buffer and one 556-byte transmit buffer. The application permits one command awaiting its CCM result. Transport delivery does not imply command success, and neither transport nor application automatically retries a command.

## Reconnect and first milestone

Socket loss, handshake failure or bounded liveness timeout clears all session material and queued session data. Reconnect always uses fresh nonces and a new session. The first encrypted application exchange performs CCM device identity/version negotiation and capability discovery. REMOTE then requests a full read-only snapshot of `volume.level` and `playback.state`. Only `volume.set` is enabled in the first milestone. Old-session observations and results are discarded by CCM session/request identity rules.

Sleep closes TCP through the existing network/power owner path, clears volatile transport state and requires a complete authenticated reconnect plus resynchronization after wake. No ESP-NOW lifecycle is involved.

## Failure and logging rules

- Fail closed on authentication, counter, framing, entropy or internal allocation failure.
- Do not fall back to plaintext or reuse an old session.
- Do not log PSKs, derived material, nonces plus proofs, plaintext payloads, tags or full records. Sanitized reason categories and counters may be logged without peer-specific values.
- Pairing/PSK provisioning and replacement are separate owner-controlled operations. Phase 2 creates no operational key.
- The coherent rollback exception accepted in CCM 1.1.0 remains unchanged; this record layer adds no new persistence semantics.

## Public executable vectors

`tools/qualification/a_remote_011_transport/reference.py` and `test_vectors.json` are normative examples for byte layout. Their sequential-byte PSK is conspicuously non-secret and must never be provisioned. `test_transport.py` covers deterministic transcript derivation, direction separation, authenticated round trip, 512/513-byte boundaries, header/ciphertext/tag tampering, duplicate/gap/exhausted counters, truncation and old-session rejection after reconnect.
