# A-REMOTE-011 Stage 5 volume slider binding

Date: 2026-10-15  
Status: IMPLEMENTED / FOCUSED TEST PASS / PRODUCTION BUILD PASS / NOT INSTALLED

## Result

The private REMOTE implementation reuses the generated LVGL `screen_slider_1` widget and its existing 0–255 range. No widget or screen was added and the generated layout was not changed. The former backlight event callback was removed from the application binding; the slider is non-clickable, non-focusable and display-only for this milestone.

The existing LVGL timer remains the sole widget-update owner. It reads the copied `control_home::Snapshot` and updates the slider only when that snapshot contains a connected, authoritative CCM `volume.level`. The 0–100 supported TUNER volume grid maps monotonically to 101 distinct positions in the existing 0–255 slider range. Unknown, disconnected or stale state disables the indicator visually and cannot create a new displayed value.

Encoder input remains on the existing bounded CCM `volume.set` path. It does not write the slider. The slider changes only after a new TUNER observation reaches the CCM snapshot, which also means a local TUNER volume change is reflected through the same path. No touch-originated command or feedback loop exists.

Private files changed:

- `components/user_app/user_app.cpp`
- `components/user_app/volume_slider.hpp`
- `tests/control/volume_slider_tests.cpp`

Focused host tests passed 2/2 with 211 assertions. They cover every supported grid value, one-to-one slider positions, authoritative updates, repeated observations and unavailable state. Previously passing encoder, pairing and RTCP suites were not repeated because their source did not change.

One production `remote01` build passed. The private application is 2,518,656 bytes with SHA-256 `af11826c7d19051a7584ee1f70eebf43efb427d1e55b116e5928a75877ec05eb`. Each unchanged 3 MiB OTA slot retains 627,072 bytes of headroom. PlatformIO reports 47,180 bytes of static RAM use and 2,518,157 bytes of flash use.

No hardware access, flash operation, live command, TUNER modification, pairing/NVS/GPIO change, private-source/binary publication or PR merge occurred. Installation and the first controlled encoder rotation require separate owner authorization.

