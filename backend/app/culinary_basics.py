"""Versioned educational summaries, separate from approved recipe instructions.

Sources read 2026-10-19. Paraphrases only; no copied recipes or images.
Similar-dish examples are editorial analogies, not validated cooking schedules.
"""

import re

CIA = "https://www.ciachef.edu/blog/3-types-cooking-methods-foods-love/"
BC = "https://opentextbc.ca/meatcutting/chapter/meat-fibres-and-tenderness-factors/"


def basics_for(query):
    words = set(re.findall(r"[^\W_]+", query.lower()))
    meat = bool(
        words
        & {
            "בשר",
            "בקר",
            "הודו",
            "עוף",
            "כנפיים",
            "כנפי",
            "נתח",
            "כתף",
            "שוק",
            "קולגן",
            "collagen",
            "meat",
            "beef",
            "chicken",
            "turkey",
            "braise",
        }
    )
    cards = []
    if meat:
        cards.append(
            {
                "title": "למה סוג הנתח משנה?",
                "text": "כתף ושוק הם שרירים עובדים, שבדרך כלל מרקמם גס יותר ויש בהם יותר רקמת חיבור לעומת פילה. לכן אין להעביר שיטת הכנה מנתח אחד לאחר רק לפי המשקל.",
                "source": BC,
            }
        )
        cards.append(
            {
                "title": "בישול לח לעומת צלייה",
                "text": "נתחים קשים מתאימים בדרך כלל לבישול ממושך בשילוב נוזל. נתחים עדינים מתאימים יותר לשיטות חום יבש. ההבדל הוא במבנה הנתח, לא רק בשם המנה.",
                "source": CIA,
            }
        )
        cards.append(
            {
                "title": "מה אפשר ללמוד ממנות דומות?",
                "text": "בברייז מבשלים נתח גדול יחסית; בתבשיל קוביות משתמשים בחתיכות קטנות יותר, וכמות הנוזל משתנה. להשוואה: צלי כתף מול תבשיל קוביות בקר. זו הקבלה לימודית; הזמנים אינם ניתנים להעתקה בין המנות.",
                "source": CIA,
            }
        )
    else:
        cards.append(
            {
                "title": "בחירת שיטת הכנה",
                "text": "צלייה והקפצה משתמשות בחום יבש; אידוי ובישול בנוזל משתמשים בחום לח. שילוב השיטות כולל לרוב השחמה ואחריה בישול בנוזל. בוחרים לפי המרקם שרוצים ולפי חומר הגלם.",
                "source": CIA,
            }
        )
    cards.append(
        {
            "title": "אותו ירק, תוצאה אחרת",
            "text": "מבנה הירק ותכולת המים משפיעים על השיטה המתאימה: קישוא ופלפל מתאימים להקפצה או לצלייה; ירקות עליים יכולים להתרכך בבישול לח. להשוואה: ירקות צלויים מול ירקות בתבשיל.",
            "source": CIA,
        }
    )
    return cards
