# Kitchen interface

Setup now asks for the dish first, offers only recommended preparation methods,
and ends with the primary start action. Ingredients, mentor style, example
journeys and account connection are secondary disclosures. During cooking the
setup closes; the user can reopen it to update the dish or choose “מנה חדשה”.

The user workflow has one reading column: named timer, current action with
guidance and one decision question, then one composer for either a report or a
question. “יש בעיה” opens the existing rule-based problem choices directly.
Selecting an option closes the problem chooser. The editable plan, other steps,
history, measurements and reference knowledge remain available on demand.
An available graph plan can be explicitly adopted to populate ordered steps.
The user workflow no longer interrupts with automatic inactivity questions;
explicitly scheduled timer reminders still run.

The shared composer keeps text on failed requests. Switching report/question
mode preserves its draft; microphone input uses the same field. An explicit
listening indicator and stop button accompany browser dictation. Text is sent
only when the user presses send. This is user-initiated dictation, not continuous
environmental monitoring. Photo attachments are still local previews only.

The timer is labelled with the current action and has start, pause/resume and
cancel controls. Pause affects accompaniment as labelled; cancel clears the
timer without finishing the action. Neither performs a physical kitchen action.
The timer is a browser reminder, not a guaranteed background alarm.

Large touch controls, readable instruction text, RTL start alignment and a
single-column responsive layout support countertop use. Guidance paragraphs
are displayed as numbered reading items without changing their content.
Safety warnings and hazard resolution controls remain visible in context.

Focused verification: `tests/test_kitchen_timer.py` and
`scripts/check_kitchen_focus_browser.py`. Browser microphone verification uses
a mock recognizer; physical microphones and noisy-kitchen usability require
testing on the actual device.
