---
id: TEC-EGG-004
type: COOKING_TECHNIQUE
name: "הקצפת מרנג (צרפתי, איטלקי, שווייצרי), קיפול סופלה וזביונה (Meringue, Soufflé & Sabayon Techniques)"
title_he: "הקצפת מרנג (צרפתי, איטלקי, שווייצרי), קיפול סופלה וזביונה"
domain: TECHNIQUES
heat_environment: "MECHANICAL_AND_THERMAL"
book_title: "On Food and Cooking: The Science and Lore of the Kitchen"
author: "Harold McGee"
edition: "2nd Edition, Completely Revised and Updated"
publication_year: 2004
chapter: "Chapter 2: Eggs (Egg Foams: Cooking with the Wrist)"
pdf_page: "119-129"
printed_page: "105-115"
knowledge_type: "COOKING_TECHNIQUE"
claim_type: "DIRECT_SOURCE_CLAIM"
description: "פרוטוקולי שליטה בהקצפת חלבונים וחלמונים: זיהוי 4 שלבי הקצף, 3 שיטות מרנג (לא מבושל, מבושל בסירופ 115–120°C, ומבושל באמבט מים 75–78°C), קיפול איטי של סופלה והקצפת חלמונים חמה בזביונה/סביון (50°C)"
heat_transfer_methods:
  - "CONDUCTION"
  - "CONVECTION"
recommended_equipment:
  - "מטרפה כדורית (Balloon Whisk) או מיקסר פלנטרי (Hypocycloidal motion)"
  - "קערת נחושת או קערה נקייה משומן"
target_foods:
  - "מרנג (צרפתי, איטלקי, שווייצרי), מוס, סופלה, זביונה (Zabaglione), סביון (Sabayon)"
conditions:
  surface_temperature_min_c: 50
  surface_temperature_max_c: 120
  cooking_medium: "AIR_FOAM_AND_WATER_BATH"
  duration_range: "2-15 minutes whipping; slow baking at 93°C (200°F) for dry meringues"
effects:
  primary_outcome: "לכידת אוויר וייצובו בדפנות חלבון/סוכר או חלמון/נוזל"
  texture_change: "מפסגות רכות למבריקות ויציבות (90% אוויר); בזביונה התרחבות פי 4 ב-50°C לקצף קטיפתי"
  moisture_loss_pct_estimate: 10.0
exceptions:
  - "בניגוד לכלל הקיפול האיטי בסופלה, כאשר בסיס הסופלה הוא מחית פרי המבושלת עם סוכר לסירופ סמיך, ניתן לצקת אותו ישירות לתוך החלבונים תוך כדי הקצפה (כמו מרנג איטלקי) וזה אף מגדיל את נפח התערובת (McGee p. 113)"
relationships:
  - type: REQUIRES
    target_id: "SCI-FOAM-001"
    target_name: "[[Egg-Foam-Stability-Disulfide-And-Acid-Copper-Chemistry]]"
    condition: "ייצוב דפנות הבועות בחומצה, נחושת וסוכר"
    evidence: "McGee 2004, Ch. 2, pp. 101-108 (PDF pp. 115-122)"
    confidence: 99
  - type: REQUIRES
    target_id: "SCI-THERM-001"
    target_name: "[[Souffle-Thermodynamics-Gas-Expansion-And-Vaporization]]"
    condition: "התפשטות גז ואידוי מים באפיית סופלה"
    evidence: "McGee 2004, Ch. 2, pp. 111-113 (PDF pp. 125-127)"
    confidence: 99
  - type: AFFECTS
    target_id: "SAF-EGG-001"
    target_name: "[[Egg-Salmonella-Pasteurization-And-Lead-Pidan-Hazards]]"
    condition: "מרנג שווייצרי (75–78°C) מפסטר את החלבונים מסלמונלה, בעוד מרנג איטלקי (55–58°C) אינו מפסטר!"
    evidence: "McGee 2004, Ch. 2, p. 108 (PDF p. 122)"
    confidence: 99
  - type: ENABLES
    target_id: "RUL-EGG-004"
    target_name: "[[Rule-Meringue-And-Egg-Foam-Stabilization-Methods]]"
    condition: "בחירת סוג המרנג ושיטת הייצוב לפי היישום הקולינרי"
    evidence: "McGee 2004, Ch. 2, pp. 105-109 (PDF pp. 119-123)"
    confidence: 99
  - type: SUPPORTED_BY
    target_id: "SRC-MCGEE-2004"
    target_name: "[[SRC-MCGEE-2004]]"
    note: "Chapter 2, Printed pp. 105-115 (PDF pp. 119-129)"
sources:
  - source_id: "SRC-MCGEE-2004"
    citation: "Harold McGee, On Food and Cooking (2nd Ed., 2004), Chapter 2: Eggs, Printed pp. 105-115 (PDF pp. 119-129)"
verification_status: VERIFIED
created_at: 2026-10-21
updated_at: 2026-10-21
---

# הקצפת מרנג (צרפתי, איטלקי, שווייצרי), קיפול סופלה וזביונה (`TEC-EGG-004`)

## 1. ארבעת שלבי הקצפת חלבון הביצה (Foam Stages — עמ' מודפס 105–106 | PDF עמ' 119–120)
1. **פסגות רכות ומבריקות (`Glossy Soft Peaks`)**: קצוות הקצף שומרים על צורה אך צונחים, והקצף עדיין אינו נצמד לקערה; הבועות גסות יחסית וביניהן נוזל רב שיתנקז מהר לתחתית.
2. **פסגות יציבות ומבריקות (`Glossy Stiff Peaks` — ~90% אוויר)**: הקצף מבריק, שומר על קצוות חדים ונצמד לקערה. נותרה בדיוק כמות הנוזל הדרושה לסיכוך (Lubrication) כדי לקפל את הקצף בקלות לבלילות. **זהו השלב האופטימלי למוסים, סופלה ועוגות ספוג**.
3. **שלב "החלקה ופסים" (`Dry Peaks / Slip-and-Streak`)**: מעבר לפסגות יציבות, הקצף הופך מאט ויבש ומתחיל להחליק מדופן הקערה עקב תחילת הפרשת נוזל. קונדיטורים עוצרים בשלב זה **למרנג או עוגיות בלבד** על ידי הוספה מיידית של סוכר שמפריד בין החלבונים וסופג את המים (ומשתמשים במחצית מכמות קרם הטרטר כדי לאפשר הגעה לשלב זה).
4. **הקצפת-יתר גרגירית (`Overbeaten Grainy Stage`)**: הקצף מאבד נפח ונפרד לפתיתים יבשים ולשלולית נוזל מימי.

---

## 2. פיזיקת הקיפול בסופלה: מדוע חובה לקפל **לאט** ולא מהר?
בניגוד להנחיה השגורה בספרי בישול "לקפל מהר", מקג'י מוכיח פיזיקלית כי **חובה לקפל לאט** (עמ' מודפס 112–113 | PDF עמ' 126–127):
* **פרוטוקול דו-שלבי**: תחילה מערבבים נמרצות **רבע מנפח הקצף** לתוך בסיס הסופלה כדי לדלל ולהקליל אותו, ורק אז מקפלים פנימה את יתרת הקצף בעזרת מרית.
* **חוק כוח הגזירה**: כוח הגזירה ההרסני (Disruptive Shear Force) שמרגישה כל בועת אוויר כשהיא נדחפת מול מסת העמילן והשומן של הבסיס **עומד ביחס ישר למהירות תנועת המרית**. ככל שהמרית נעה לאט יותר — כך נהרסות פחות בועות אוויר! (גם בקיפול תקין מאבדים בין 25% ל-50% מנפח הקצף).

---

## 3. זביונה וסביון (*Zabaglione / Sabayon*): הקצפת חלמונים ב-50°C
* **המתכון והמנגנון (עמ' מודפס 113–115 | PDF עמ' 127–129)**: מערבבים נפחים שווים של חלמונים וסוכר, מוסיפים יין (לרוב מרסלה, מנפח זהה ועד פי 4 מנפח החלמונים), ומקציפים מעל אמבט מים מבעבעים.
* **נקודת הקרישה התרמית (`50°C / 120°F`)**: הנוזל, החומצה והאלכוהול מפרקים את גרנולות החלמון ו-LDL, וכשטמפרטורת התערובת מגיעה ל-**50°C (120°F)** חלבוני החלמון מתחילים להיפתח ולהיקשר בדפנות הבועות, והתערובת תופחת **פי 4 ויותר מנפחה**. יש לעצור מיד על סף המעבר מנוזל למוצק; סביון מלוח שהתفرד באחסון ניתן להקצפה חוזרת!

