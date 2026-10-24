# RTCP/1 Bluetooth Extension v1 reference codec

These host-only files implement the proposed BTX/1.0 application plaintext layouts. They contain no operational secret, identity or private metadata and do not implement a cryptographic stack.

Run from the repository root:

```text
python -m unittest discover -s tools/qualification/rtcp_bluetooth_v1 -p "test_*.py" -v
```

Regenerate the deterministic vectors only when the proposed wire contract intentionally changes:

```text
python tools/qualification/rtcp_bluetooth_v1/reference.py --vectors
```

The committed vectors cover the exact legacy capability fallback, BTX capability response, state request/response, maximum metadata response, command and accepted/stale results. RTCP/1 encryption and record-counter behavior remain covered by `tools/qualification/a_remote_011_transport`.
