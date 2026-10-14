# A-REMOTE-011 Stage 5: first controlled volume command

## Result

**STOPPED BEFORE TRANSMISSION — THE PRODUCTION REMOTE HAS NO WIRED `volume.set` INPUT PATH.**

The owner authorized exactly one RTCP/1 `volume.set`. The precondition review confirmed a live authenticated session: REMOTE reported session 1, a current nonzero capability revision, connected networking, the Core owner invariant intact, zero failed allocations and zero command dispatches.

Source inspection then found a functional integration gap before any command was formed:

- the RTCP adapter and client implement validated, correlated `volume.set` transport;
- the production facade exposes only `PREVIOUS`, `TOGGLE` and `NEXT` intents;
- `Facade::handle` has no volume action or request-construction branch;
- the fixed serial development hook rejects its command set whenever the session uses the real RTCP device;
- the read-only diagnostics expose session/capability/counter state but do not expose the selected current volume or a production command endpoint.

Consequently, the current production REMOTE cannot originate the authorized operation through an implemented user or commissioning path. Fabricating a raw RTCP record externally would bypass REMOTE and would not satisfy the requirement to send through REMOTE. Changing firmware would exceed the Stage 5 authorization.

No `volume.set` or other control command was transmitted. Dispatches remained zero. No firmware, pairing, NVS, settings or hardware state was modified, and owner confirmation of an audible change was therefore not requested.

## Minimum next action

Separately authorize a narrow source change that adds one bounded REMOTE volume intent path using the already implemented CCM admission and RTCP adapter. It should expose the fresh current value and exact 1/100 grid, select one adjacent safe step, permit one explicit owner-triggered command, and retain the existing no-retry/correlated-result rules. Build and review that change before any new hardware operation.
