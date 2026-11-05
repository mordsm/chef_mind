---
id: SCI-THERM-001
type: SCIENTIFIC_PRINCIPLE
name: "תרמודינמיקה של סופלה — חוק שארל מול אידוי מים (Soufflé Thermodynamics: Gas Expansion vs. Water Vaporization)"
title_he: "תרמודינמיקה של סופלה — חוק שארל מול אידוי מים"
domain: FOOD_SCIENCE
category: "THERMODYNAMICS"
book_title: "On Food and Cooking: The Science and Lore of the Kitchen"
author: "Harold McGee"
edition: "2nd Edition, Completely Revised and Updated"
publication_year: 2004
chapter: "Chapter 2: Eggs (Soufflés: A Breath of Hot Air)"
pdf_page: "123-127"
printed_page: "109-113"
knowledge_type: "CULINARY_PRINCIPLE"
claim_type: "DIRECT_SOURCE_CLAIM"
description: "העיקרון הפיזיקלי הכפול המניע את תפיחת הסופלה וצניחתו: התפשטות גז תרמית (חוק שארל) אחראית רק לכ-25% מהתפיחה, בעוד שכ-75% מהתפיחה נובעים מאידוי מתמשך של מים מדפנות הבועות לקיטור בתוך בועות האוויר"
conditions:
  temperature_range_c:
    min: 160
    max: 200
  catalysts: ["trapped_air_bubbles", "water_vaporization_near_boiling", "thermal_gas_expansion"]
effects:
  molecular_change: "התפשטות נפח האוויר הכלוא לפי חוק שארל (25% מהתפיחה) + מעבר פאזה של מים נוזליים מדפנות הבועות לאדי מים המגדילים את מספר מולקולות הגז והלחץ בתוך הבועות (75% מהתפיחה); בקירור — התכווצות האוויר והתעבות הקיטור חזרה לנוזל"
  sensory_consequences:
    taste: ["דורש תיבול-יתר של הבסיס כדי לפצות על דילול הטעם בחלבון התפל ובאוויר (McGee p. 112)"]
    aroma: ["שחרור ארומות נדיפות עם אדי המים"]
    color: "קרום חיצוני שחום ופריך מעל פנים אוורירי"
    texture: "מאפה תפוח ואוורירי הצונח בהדרגה עם התקררותו אך ניתן להתפחה חוזרת בחימום"
exceptions:
  - "ב'סופלה פודינג' (Pudding Soufflé) שבו משלשים את כמות הקמח בבסיס (פי 3 מהרגיל), המבנה הלחמי כל כך יציב שהוא אינו צונח כלל לאחר הוצאתו מהתנור (McGee p. 112)"
relationships:
  - type: REQUIRES
    target_id: "SCI-FOAM-001"
    target_name: "[[Egg-Foam-Stability-Disulfide-And-Acid-Copper-Chemistry]]"
    condition: "קצף חלבונים בשלב פסגות יציבות אך לחות ומבריקות (Stiff Glossy Peaks)"
    evidence: "McGee 2004, Ch. 2, pp. 106, 112 (PDF pp. 120, 126)"
    confidence: 99
  - type: REQUIRES
    target_id: "SCI-HEAT-001"
    target_name: "[[Heat-Transfer]]"
    condition: "מעבר חום מהיר בתנור (160°C–200°C)"
    evidence: "McGee 2004, Ch. 2, pp. 111-113 (PDF pp. 125-127)"
    confidence: 99
  - type: AFFECTS
    target_id: "TEC-EGG-004"
    target_name: "[[Meringue-Souffle-And-Sabayon-Whipping]]"
    condition: "קובע את יחסי הבסיס-קצף, טכניקת הקיפול האיטית וטמפרטורת האפייה"
    evidence: "McGee 2004, Ch. 2, pp. 111-113 (PDF pp. 125-127)"
    confidence: 99
  - type: AFFECTS
    target_id: "CNF-EGG-003"
    target_name: "[[Conflict-Souffle-Dish-Buttering-And-Oven-Door-Myths]]"
    condition: "מסביר מדוע פתיחת דלת התנור לכמה שניות אינה מפילה סופלה ומדוע סופלה שצנח יתפח מחדש בחימום"
    evidence: "McGee 2004, Ch. 2, pp. 110-113 (PDF pp. 124-127)"
    confidence: 99
  - type: SUPPORTED_BY
    target_id: "SRC-MCGEE-2004"
    target_name: "[[SRC-MCGEE-2004]]"
    note: "Chapter 2, Printed pp. 109-113 (PDF pp. 123-127)"
sources:
  - source_id: "SRC-MCGEE-2004"
    citation: "Harold McGee, On Food and Cooking (2nd Ed., 2004), Chapter 2: Eggs, Printed pp. 109-113 (PDF pp. 123-127)"
verification_status: VERIFIED
created_at: 2026-10-21
updated_at: 2026-10-21
---

# תרמודינמיקה של סופלה — חוק שארל מול אידוי מים (`SCI-THERM-001`)

## 1. עקרון הסופלה: מדוע הוא תופח ומדוע הוא חייב לצנוח
הפיזיקאי הצרפתי ז'אק שארל ניסח את **חוק שארל (Charles's Law)**: נפחו של גז נתון עומדביחס ישר לטמפרטורה המוחלטת שלו. אולם מקג'י מראה כי חוק שארל לבדו מסביר רק חלק קטן מתפיחת הסופלה (עמ' מודפס 111 | PDF עמ' 125):
1. **התפשטות תרמית של אוויר (~25% מהתפיחה)**: התחממות בועות האוויר שנלכדו בהקצפה אחראית רק לכרבע מתפיחת הסופלה האופיינית.
2. **אידוי מים מדפנות הבועות לקיטור (~75% מהתפיחה)**: שלושת הרבעים הנותרים של התפיחה נובעים מאידוי מתמשך של מים נוזליים מתוך דפנות הבועות אל חלל הבועות ככל שהתערובת מתקרבת לנקודת הרתיחה. מולקולות אדי המים מתווספות למולקולות האוויר, מגדילות את הלחץ הפנימי ומותחות את דפנות הבועות כלפי מעלה.
3. **הצניחה הבלתי נמנעת בשולחן — והתפחה חוזרת**: ברגע שהסופלה יוצא מהתנור ומתקרר, האוויר בבועות מתכווץ ואדי המים מתעבים חזרה לנוזל, ולכן הסופלה מתכווץ. עם זאת, מכיוון שהבועות ורוב הלחות עדיין נמצאים בפנים, **סופלה שצנח יתפח שוב אם יוחזר לתנור** (לגובה מעט נמוך יותר כי המבנה התקשה וחלק מהמים התאדו — טכניקה המשמשת ב-*Soufflé à la suissesse*, עמ' מודפס 112 | PDF עמ' 126).

---

## 2. משוואת הטמפרטורה והצמיגות בסופלה (Temperature & Consistency Tradeoffs)
| פרמטר שליטה | מצב א': תנור לוהט (`200°C+ / 400°F+`) או בלילה דלילה | מצב ב': תנור מתון (`160°C–180°C / 325°F–350°F`) או בלילה סמיכה |
| :--- | :--- | :--- |
| **גובה ומהירות תפיחה** | תפיחה מהירה ודרמטית מאוד (אידוי מים מואץ); השחמה חיצונית בעוד הפנים נשאר קרמי ונוזלי | תפיחה מתונה ומבוקרת יותר; השחמת החוץ מתزامנת עם התייצבות הפנים |
| **קצב הצניחה בהגשה** | לחץ-יתר גדול בבועות מוביל **לקריסה מהירה ודרמטית** על השולחן | עמידות גבוהה יותר ללחץ-יתר וצניחה איטית ומתונה בהרבה |
| **סכנת כשל בקיצון** | בכלי אישי קטן: קיטור מתחתית הכלי הלוהטת עלול להעיף מחצית מהסופלה החוצה (פתרון: הנחה בתבנית עם מים, עמ' 113) | בתנור איטי מדי או בלילה נוזלית מדי: הסופלה יגלוש לצדדים לפני שחלבוני הביצה יספיקו להיקרש |
