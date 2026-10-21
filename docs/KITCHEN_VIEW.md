# Kitchen view

Seven implementation steps before checks: focused dialog, explicit outcome reporting, manual reminder, local-only read-aloud, screen-awake controls, browser regression coverage, and operating documentation.

After receiving guidance in the local console, press **Kitchen view / מצב מטבח**. The dark dialog shows the latest source-grounded instruction and success signal in large text. Reason and sources are collapsed under a disclosure. Safety notes remain visible. It does not invent subsequent recipe steps, infer completion or operate equipment. Clarification and blocked decisions can also be read here; reminders are available only for action decisions.

## Report what happened

Write an actual observation and choose **Add report to form**. This appends text to the visible reports field without making any API request. It is submitted only with the next explicit question. Blank reports and more than thirty report lines are rejected. Reporting completion is not a temperature measurement, food-safety assessment or approval to advance. Closing the dialog retains the form; a new cooking session or disconnect clears the kitchen state.

## Manual reminder

Choose an integer from 1 to 14400 seconds. The field is empty by default; no time is invented from source content. The countdown uses a monotonic browser deadline and a visual/status reminder. It is not a doneness indicator, alarm clock or guaranteed background notification. Browsers may throttle/suspend the page; do not rely on it when switching apps, locking the device or leaving the kitchen. Closing the dialog cancels a running reminder after confirmation. New guidance or session reset cancels it. Reload loses the reminder.

## Read aloud

Read-aloud is explicit and speaks only the current instruction. The browser selects a matching Hebrew/English voice only when `localService=true`; no remote voice fallback is attempted. Markdown marker characters and URLs are omitted from spoken instructions. If no suitable local voice is listed, text remains available and an explanatory message appears. This relies on the browser/OS's voice classification; it is not an independent network audit. No microphone, voice commands or OpenAI speech call is added. Speech stops when closing/resetting the kitchen or hiding the tab. See [MDN localService](https://developer.mozilla.org/en-US/docs/Web/API/SpeechSynthesisVoice/localService).

## Keep screen awake

Press **Keep screen awake** to request a screen wake lock. The browser may refuse or release it for battery/visibility/platform reasons. The UI reports the actual request outcome and releases its lock on closing or hiding the tab. It does not automatically reacquire a released lock. Localhost is normally a secure context, but support varies by device. See [MDN Screen Wake Lock API](https://developer.mozilla.org/en-US/docs/Web/API/Screen_Wake_Lock_API).

## Verification scope

The headless browser smoke uses synthetic source/decision data. It tests dialog navigation, focus/keyboard cancellation, invalid and completed reminders, report staging without submission, decimal inventory, token clearing and responsive widths. Speech voices and wake-lock responses are mocked to verify local-only selection and release behavior without playing audio or asserting physical device behavior. Hardware/browser voice availability, audible output, sleep prevention and background timing require a real-device check; automated mocks do not establish those capabilities.
