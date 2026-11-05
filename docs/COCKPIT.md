# Cooking cockpit

Desktop cooking mode has three stable stations: current step on the right,
countdowns and four action shortcuts in the center, and microphone/transcript on
the left. Preparation remains a separate mode. Compact screens stack the same
stations without reducing the touch targets or instruction font below 24px.

Action parameters are a native modal dialog. In the embedded reporter, a verified
same-origin message expands the existing iframe over the viewport without
reloading it or moving its browsing context. The background stations become inert
until the dialog closes. Cancel/Escape closes without recording an action.

Temperature and duration dials support pointer capture, keyboard arrows,
Home/End, large plus/minus buttons and exact numeric entry. Unknown temperature
remains unknown until entered; adjusting a device setting is not a food reading.
Closing or opening a modal does not start a timer. Confirming a timed action does.

The current step's short explanation is shown only on request. Exact Hebrew
phrases such as "השף, למה?" route directly from speech recognition to narration,
without a model call, question submission or step completion. Other speech stays
in the editable question until the cook explicitly sends it. Hebrew speech output
requires a Hebrew voice installed/available in the browser; unavailable narration
gets a visible explanation/status in the voice station.

`scripts/check_cockpit.py` checks the actual public/local layout, pointer and
keyboard dials, modal focus recovery, short explanation, and Next advancing then
remaining enabled. Speech recognition/synthesis are mocked for repeatability;
this test does not certify a physical microphone or an installed device voice.
