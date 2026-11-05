"""Bounded guidance from the local simmering rules; no invented cooking time."""

import re
import json
from pathlib import Path


PROTOCOL = json.loads((Path(__file__).parent / "data" / "gizzard_user_protocol.json").read_text(encoding="utf-8"))


def timing_guidance():
    low, high = PROTOCOL["simmer_minutes"]
    return (
        "עבור 1 ק״ג קורקבנים מופשרים ונקיים, "
        "חתוכים לחצאים, בסיר רגיל כבד עם מכסה כבד ונוזל כמעט עד גובה הקורקבנים, "
        f"טווח הריכוך המשוער הוא {low}–{high} דקות. בליווי הזה נספור מתחילת הבעבוע העדין לאחר הרתיחה. "
        "זהו טווח לבדיקת רכות, ולא אישור מוכנות לפי שעון. בתנאים אחרים הטווח אינו בהכרח מתאים. "
        "בתחילת הטווח בדוק חתיכה באמצעות מזלג וכלי נקי; אם היא עדיין גמישה וקשה, המשך בבעבוע עדין ובדוק שוב. "
        "אל תיגע במזון חם בידיים ואל תטעם עוף לפני בדיקת מוכנות. "
        "אפשר להפעיל תזכורת לבדיקה; היא תפעל רק לאחר לחיצה על הפעלת הטיימר."
    )


def preparation_guidance():
    return (
        "הכן קורקבנים נקיים ומופשרים לחלוטין וכלים נקיים. אם עובדים לפי הפרוטוקול שסיפקת, "
        "חתוך לחצאים והשתמש בסיר רגיל כבד עם נוזל כמעט עד גובהם. "
        "הבא לרתיחה ראשונית, ואז הנמך מיד לבעבוע עדין וכסה בהתאם לסיר. "
        "המלח בעדינות בתחילה ובדוק תיבול בסיום לאחר בדיקת מוכנות. דווח כשהנוזל רותח.\n\n"
        + timing_guidance()
        + "\n\nמה הכמות בפועל, האם הקורקבנים שלמים או חתוכים, ובאיזה סיר ומכסה אתה משתמש?"
    )


def is_gizzard_simmer(state):
    graph = state["context"]["graph"]
    title = " ".join([state["dish_title"], *state["ingredients"]]).casefold()
    return (
        any(word in title for word in ("קורקבנ", "קורקבן", "קוקבנ", "קוקבן", "gizzard"))
        and (graph.get("method") or {}).get("id") == "boil_simmer"
    )


def report_guidance(state, text):
    if not is_gizzard_simmer(state):
        return None
    text = re.sub(r"[^\w\s]", " ", text.casefold())
    negative = any(word in text for word in ("לא רתח", "לא רותח", "טרם רתח", "עדיין לא", "has not", "not boiling"))
    boiling = not negative and any(word in text for word in ("רתח", "רותח", "רוטח", "בעבוע", "מבעבע", "boiling", "boiled"))
    if boiling:
        return (
            "השלב הבא: הנמך עכשיו את האש עד לבעבוע עדין, במקום רתיחה סוערת. "
            "בדוק שהבעבוע נשאר עדין ושיש נוזל בסיר; אם הנוזל מצטמצם, דווח לי לפני שהסיר מתייבש.\n\n"
            "המשך בבישול הלח ובדוק רכות בנפרד מבטיחות. אם הקורקבנים עדיין קשים ויש נוזל, המשך בבעבוע עדין.\n\n"
            + timing_guidance()
            + "\n\nדווח: כמה זמן עבר מתחילת הבעבוע, מה הכמות, האם הם חתוכים, ומה מצב הנוזל והרכות כעת?"
        )
    if any(word in text for word in ("כמה זמן", "מתי להוריד", "how long")):
        return (
            "מנמיכים את האש כשהנוזל מגיע לרתיחה ושומרים על בעבוע עדין. "
            + timing_guidance()
            + "\n\nמה הכמות, האם הם שלמים או חתוכים, וכמה זמן הם כבר בבעבוע?"
        )
    if any(word in text for word in ("עדיין קשה", "עדיין קשים", "לא התרכך", "לא התרככו", "גומי")):
        return (
            "אם עדיין קשה ויש נוזל, המשך בבעבוע עדין ובדוק שוב באמצעות מזלג וכלי נקי. "
            "בדוק שהנוזל לא התאדה ושהתחתית אינה נחרכת. אל תגביר לרתיחה סוערת כדי לקצר את הזמן.\n\n"
            + timing_guidance()
            + "\n\nכמה זמן עבר מתחילת הבעבוע ומה מצב הנוזל?"
        )
    return None
