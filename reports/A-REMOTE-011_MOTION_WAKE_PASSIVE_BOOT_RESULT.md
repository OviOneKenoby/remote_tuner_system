# REMOTE//01 motion-wake passive boot result

Date: 2026-10-15

Verdict: **INCONCLUSIVE FOR THE EXACT QMI STAGE; NORMAL REBOOT RESTORED IMU READINESS.**

The previously verified REMOTE serial interface was present and healthy. A passive 115200-baud monitor opened with DTR and RTS inactive, reported capture-ready, and sent no data. The owner then performed exactly one normal hardware reboot.

The native USB serial interface disconnected during that reboot. The Windows monitor terminated on `ClearCommError` before receiving data and did not reconnect automatically. The complete private UART capture is therefore zero bytes, with SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. It contains no `POWER_WOM`, QMI8658 or other boot message. No failed QMI stage or ESP-IDF/I²C error can be inferred from an empty capture.

After the device re-enumerated on the same verified interface, one read-only diagnostics status capture reported:

- power state: display idle (`1`);
- IMU readiness: true (`1`);
- motion events: `0`;
- wake count: `0`;
- I²C/bus errors: `0`;
- last sleep cause: `0`;
- private status SHA-256: `d5539160792fe278f81b5a183d70955a31130be05fb47e730bd55659b1488b82`.

Before reboot, the same installed firmware reported `IMU=0` with zero runtime bus errors. After the single normal reboot it reports `IMU=1`. This demonstrates an intermittent boot-state difference and confirms that reboot restored QMI wake-on-motion readiness. It does not identify the precise failed transaction from the preceding boot, and motion-triggered display wake was not exercised in this stage.

The minimum next diagnostic action, if the exact stage is still required, is one separately authorized normal reboot with a bounded passive monitor that catches USB serial disconnects and automatically reopens the same verified interface after re-enumeration. No firmware instrumentation is required. A stable external UART0 adapter would be an alternative only if separately authorized and already wired safely.

No automated reset, repeated reboot, command transmission, firmware/source/build change, flash access, NVS/configuration write, encoder/TUNER operation or PR merge occurred.
