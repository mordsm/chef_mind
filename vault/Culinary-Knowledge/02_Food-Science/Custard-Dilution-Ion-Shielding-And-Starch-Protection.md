---
id: SCI-PROT-003
type: SCIENTIFIC_PRINCIPLE
name: "כימיה של קסטרד וקרמים — דילול, מיסוך יוני והגנת עמילן (Custard Dilution, Ion Shielding & Starch Protection)"
title_he: "כימיה של קסטרד וקרמים — דילול, מיסוך יוני והגנת עמילן"
domain: FOOD_SCIENCE
category: "PROTEIN_CARBOHYDRATE_INTERACTION"
book_title: "On Food and Cooking: The Science and Lore of the Kitchen"
author: "Harold McGee"
edition: "2nd Edition, Completely Revised and Updated"
publication_year: 2004
chapter: "Chapter 2: Eggs (The Effects of Added Ingredients; Egg-Liquid Mixtures: Custards and Creams)"
pdf_page: "99-100, 106-109, 112-114"
printed_page: "85-86, 92-95, 98-100"
knowledge_type: "CULINARY_PRINCIPLE"
claim_type: "DIRECT_SOURCE_CLAIM"
description: "העקרונות הכימיים השולטים בהתמצקות תערובות ביצים ונוזלים: העלאת סף הקרישה על ידי דילול במים ומיסוך בסוכרוז, חובת נוכחות מינרלים/יונים ליצירת ג'ל רציף, ומנגנון ההגנה הכפול של עמילן מפני התגבנות ברתיחה"
conditions:
  temperature_range_c:
    min: 77
    max: 100
  water_activity_aw:
    min: 0.90
    max: 0.99
  ph_range:
    min: 6.0
    max: 7.5
  catalysts: ["water_dilution_6x", "sucrose_molecular_screen", "dissolved_mineral_ions", "starch_gelatinization_at_77c"]
effects:
  molecular_change: "דילול במים וסוכר מעלה את סף הקרישה מ-70°C ל-79°C–83°C; יונים חיוביים מנטרלים דחייה אלקטרוסטטית בין חלבונים ליצירת ג'ל אחיד; גרגירי עמילן עוברים ג'לטיניזציה ב-77°C, בולעים חום ומונעים פיזית קשירה צפופה של חלבוני הביצה"
  sensory_consequences:
    taste: ["מתיקות ועידון טעם הביצה"]
    aroma: ["ניחוח שמנת/וניל עם הפחתת ריח גופריתי"]
    color: "צהוב-שנהב אטום ומבריק"
    texture: "ג'ל רך ועדין בקסטרד אפוי; נוזל קטיפתי בקרם אנגלז; קרם יציב וסמיך בקרם פטיסייר"
exceptions:
  - "בתערובת ביצה ומים מזוקקים/טהורים ללא מלח או מינרלים לא נוצר ג'ל קסטרד אחיד אלא פתיתי ביצה קרושים הצפים במים (McGee p. 94)"
  - "בדילול קיצוני (כגון ליקר Advocaat או Eggnog), חלבוני הביצה מדוללים מכדי ליצור רשת ג'ל ומספקים רק סמיכות קלה (Body) לנוזל (McGee p. 86)"
relationships:
  - type: REQUIRES
    target_id: "SCI-PROT-002"
    target_name: "[[Protein-Denaturation-Coagulation]]"
    condition: "פתיחת קיפול חלבוני הביצה בחום"
    evidence: "McGee 2004, Ch. 2, pp. 84-86 (PDF pp. 98-100)"
    confidence: 99
  - type: AFFECTS
    target_id: "ING-EGG-001"
    target_name: "[[Egg-Proteins-Yolk-Albumen]]"
    condition: "חלבוני ביצה אחת נמתחים על פני 18–20 כפות נוזל במקום 3 כפות בביצה נקייה"
    evidence: "McGee 2004, Ch. 2, p. 86 (PDF p. 100)"
    confidence: 99
  - type: REQUIRES
    target_id: "SCI-CARB-001"
    target_name: "[[Starch-Gelatinization-Retrogradation]]"
    condition: "ג'לטיניזציה של עמילן ב-77°C (175°F) בקרמים מבושלים"
    evidence: "McGee 2004, Ch. 2, p. 94 (PDF p. 108)"
    confidence: 99
  - type: ENABLES
    target_id: "RUL-EGG-001"
    target_name: "[[Rule-Custard-Curdling-Rescue]]"
    condition: "הגדרת חלון הקרישה הצר 79°C–83°C"
    evidence: "McGee 2004, Ch. 2, p. 93 (PDF p. 107)"
    confidence: 99
  - type: ENABLES
    target_id: "RUL-EGG-003"
    target_name: "[[Rule-Starch-Stabilized-Pastry-Cream-Boiling]]"
    condition: "הגנת עמילן מאפשרת הרתחה מלאה להשבתת עמילאז החלמון"
    evidence: "McGee 2004, Ch. 2, pp. 94, 98-100 (PDF pp. 108, 112-114)"
    confidence: 99
  - type: SUPPORTED_BY
    target_id: "SRC-MCGEE-2004"
    target_name: "[[SRC-MCGEE-2004]]"
    note: "Chapter 2, Printed pp. 85-86, 92-95, 98-100 (PDF pp. 99-100, 106-109, 112-114)"
sources:
  - source_id: "SRC-MCGEE-2004"
    citation: "Harold McGee, On Food and Cooking (2nd Ed., 2004), Chapter 2: Eggs, Printed pp. 85-86, 92-95, 98-100 (PDF pp. 99-100, 106-109, 112-114)"
verification_status: VERIFIED
created_at: 2026-10-21
updated_at: 2026-10-21
---

# כימיה של קסטרד וקרמים — דילול, מיסוך יוני והגנת עמילן (`SCI-PROT-003`)

## 1. אפקט הדילול והמיסוך המולקולרי של סוכר וחלב
בביצה לא מדוללת, החלבונים של ביצה אחת חובקים כ-3 כפות נוזל בלבד ומתמצקים כבר ב-**70°C–73°C**. לעומת זאת, במתכון קסטרד או קרם אנגלז קלאסי (`1 ביצה שלמה + 1 כוס / 250 מ"ל חלב + 2 כפות / 30 גרם סוכר`):
1. **דילול נפחי פי 6 (`Volume Dilution`)**: החלב לבדו מגדיל פי 6 את הנפח שעל חלבוני הביצה לגשר עליו (18–20 כפות נוזל לביצה אחת!). המרחק הגדול בין מולקולות החלבון מחייב טמפרטורה גבוהה יותר ותנועה תרמית מהירה יותר כדי שהחלבונים ייפגשו וייקשרו (עמ' מודפס 86, 93 | PDF עמ' 100, 107).
2. **מסך מולקולות הסוכרוז (`Sucrose Screening`)**: כף סוכר אחת מקיפה כל מולקולת חלבון בביצה במסך צפוף של **אלפי מולקולות סוכרוז** המפריעות פיזית למפגש בין שרשראות החלבון.
3. **התוצאה התרמית**: שילוב המים, הסוכר ושומן החלב מעלה את תחילת הקרישה מ-70°C ל-**79°C–83°C (175°F–185°F)**. הרשת שנוצרת דקה, פתוחה ועדינה מאוד, אך חציית טווח זה ב-**3°C–5°C בלבד (5°F–10°F)** גורמת לקריסת הרשת ולהתגבנות (עמ' מודפס 93 | PDF עמ' 107).

---

## 2. חובת נוכחות מינרלים ויונים ליצירת ג'ל קסטרד (Mineral Ion Shielding)
* **ניסוי המים הטהורים של מקג'י (עמ' מודפס 94 | PDF עמ' 108)**: אם מערבבים ביצה עם כוס מים רגילים/טהורים ומחממים, **לא מתקבל קסטרד** אלא פתיתי ביצה קרושים הצפים במים נפרדים. אך אם מוסיפים **קורט מלח** (או משתמשים בחלב, שמנת, ציר עוף/בוניטו ב-*Chawan-mushi* או ציר ירקות), מתקבל ג'ל קסטרד אחיד ויציב.
* **המנגנון האלקטרוסטטי**: ללא מינרלים מומסים, חלבוני הביצה הנושאים מטען חשמלי שלילי דוחים זה את זה גם כשהם נפתחים בחום, ולכן כל חלבון יוצר קשרים מקומיים מועטים בלבד. נוכחות יונים חיוביים ($\text{Na}^+$, $\text{Ca}^{2+}$) יוצרת "מגן מנטרל" סביב האזורים הטעונים שלילית ומאפשרת לחלבונים להתקרב וליצור רשת תלת-ממדית רציפה הלוכדת את כל המים.

---

## 3. מנגנון "ביטוח ההתגבנות" של עמילן (Starch Curdling Insurance)
הוספת **כף שטוחה קמח (8 גרם)** או **2 כפיות עמילן טהור (5 גרם קורנפלור או ארו-רוט)** לכל **כוס נוזל (250 מ"ל)** מגינה על קרמים וקסטרדים מפני התגבנות אפילו בחימום מהיר וברתיחה מלאה (עמ' מודפס 94 | PDF עמ' 108):
1. **ספיגת אנרגיה תרמית ב-77°C**: כאשר התערובת מגיעה ל-**77°C (175°F)** — בדיוק סף הקרישה של חלבוני הביצה המדוללים — גרגירי העמילן סופגים מים, מתנפחים ובולעים אנרגיית חום, ובכך מאטים את קצב היקשרות החלבונים.
2. **חציצה מרחבית של שרשראות העמילן**: מולקולות העמילן הארוכות הדולפות מהגרגירים המתנפחים חוצצות פיזית בין מולקולות החלבון ומונעות מהן להיקשר זו לזו בצפיפות יתרה. *(גם שוקולד וקקאו מייצבים קרמים באופן דומה הודות לעמילן שבהם).*

