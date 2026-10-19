# A-REMOTE-013 D-009 REMOTE UI integration notes

## Verified structure

The generated 172×640 carousel has elements 0 and 1 in `components/ui_bsp/generated/setup_scr_screen.c`. Element 1 contains the existing generated brightness page and `screen_slider_1`; it is not a volume control and remains unchanged. `components/user_app/user_app.cpp::remote01_mockup_create()` adds the accepted HOME page as carousel index 2.

HOME index 2 currently contains:

- status label at y=68;
- unchanged 148×148 `TUNER//01 / ARTWORK` placeholder at y=96;
- `home.title`, 148 pixels wide at y=262, 20-point font, dot overflow;
- `home.subtitle`, 148 pixels wide at y=290, 14-point font, clipped overflow;
- playback status at y=316;
- existing previous/toggle/next buttons at y=350;
- authoritative/provisional volume text and indicator at y=418/450;
- existing FAVORITES/DEVICES/REMOTES rows and network footer.

The 20 ms `home_refresh` LVGL timer is the only widget-update path. It consumes a copied `control_home::Snapshot`; network or Core code does not call LVGL.

## Proposed text binding

- `home.title`: selected station name from authoritative `media.subtitle`.
- `home.subtitle`: exact combined StreamTitle from `media.title`; if trustworthy split fields exist, compose `media.artist` and `media.title` in the UI-owned fixed buffer.
- absent/stale station or metadata: neutral `--`; never retain text from an older generation/session.
- long text: Core retains the bounded wire value; the UI fixed buffer truncates on a UTF-8 boundary and the existing label overflow policy applies.

No generated UI source, geometry, screen, graphical widget, artwork, logo, brightness behavior or carousel navigation changes are proposed. The three existing HOME playback buttons become enabled only from fresh contextual capabilities. Physical-button action assignment remains outside this slice.

## Layout limitation

There are only two existing metadata text lines. They can show station plus one now-playing line. Separate artist and title cannot both receive dedicated rows without redesign; when split data exists, they are composed into the existing second line. The narrow 148-pixel labels may visually clip or ellipsize long text even though the authoritative bounded value remains available in Core.
