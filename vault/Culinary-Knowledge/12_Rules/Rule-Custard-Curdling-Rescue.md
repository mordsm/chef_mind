---
id: RUL-EGG-001
type: CULINARY_RULE
name: "עצירת התגבנות בקרם ביצים (Custard Curdling Rescue)"
title_he: "כלל החלטה: מניעה ועצירת התגבנות בקרם ביצים וקסטרד (RUL-EGG-001)"
domain: RULES
rule_scope: "DIAGNOSIS"
book_title: "On Food and Cooking: The Science and Lore of the Kitchen"
author: "Harold McGee"
edition: "2nd Edition, Completely Revised and Updated"
publication_year: 2004
chapter: "Chapter 2: Eggs (Egg-Liquid Mixtures: Custards and Creams)"
pdf_page: "99-100, 107-109, 112-113"
printed_page: "85-86, 93-95, 98-99"
knowledge_type: "CONDITIONAL_DECISION_RULE"
claim_type: "DIRECT_SOURCE_CLAIM"
trigger_conditions:
  food_class: "DAIRY"
  observed_problem: "קרם הביצים מתחיל להתגבן"
  cooking_phase: "MID_COOKING"
if_condition: "תערובת ביצים ונוזל (קסטרד אפוי או קרם אנגלז מבושל על הכיריים) מתקרבת או חוצה את טווח 79°C–83°C (175°F–185°F), או מראה סימני הסמכה מהירה וגרגירים ראשונים"
then_action: "הסר מיד ממקור החום (ובקרם בחוש העבר לקערה קרה/אמבט קרח תוך בחישה וסינון במסננת צפופה); לחלופין, אם נדרשת עמידות לרתיחה מראש, שלב עמילן (8 גרם קמח או 5 גרם קורנפלור ל-250 מ\"ל נוזל)"
because_rationale: "בתערובת מדוללת פי 6 בחלב וממוסכת בסוכר, חלבוני הביצה נקרשים בטווח צר מאוד של 79°C–83°C, אך לתגובת הקרישה יש מומנטום תרמי וחריגה של 3°C–5°C בלבד (5°F–10°F) מכווצת את הרשת החלבונית ופולטת מים (Syneresis)"
recommended_action:
  action_code: "STOP_HEAT_IMMEDIATELY"
  parameters:
    heat_adjustment: "REMOVE_FROM_HEAT"
    liquid_addition_ml: 0
    cover_vessel: false
  explanation: "עצור מיד את חימום הקרם, הסר ממקור החום ובדוק את מידת ההתגבנות לפני שממשיכים."
legitimate_methods_and_tradeoffs:
  - method: "בקרת חום עדינה בלבד ללא עמילן (אמבט מים פתוח 80°C–83°C לקסטרד או בן-מארי לקרם אנגלז)"
    pros: "מרקם חלק, משיי וטהור וטעם עשיר ללא מיסוך עמילני"
    cons: "מרווח ביטחון תרמי צר מאוד (3°C–5°C בלבד לפני התגבנות); דורש השגחה צמודה וזמן בישול ארוך"
  - method: "הגנת עמילן מראש (8g קמח או 5g קורנפלור ל-250ml נוזל, כמו בקרם פטיסייר)"
    pros: "מונע התגבנות אפילו ברתיחה מלאה על אש ישירה (גרגירי העמילן עוברים ג'לטיניזציה ב-77°C, בולעים חום וחוצצים פיזית בין חלבוני הביצה)"
    cons: "הופך את המרקם החלק והמשיי לסמיך וגס יותר ומעמעם מעט את עדינות הטעם (McGee p. 94)"
  - method: "הצלה מכנית בסינון (בקרם בחוש בלבד — Crème Anglaise)"
    pros: "מאפשר להציל קרם בחוש שהחל להתגבן קלות על ידי העברה מיידית לכלי קר וסינון הגושים"
    cons: "אינו ישים כלל בקסטרד אפוי המוגש בכלי האפייה שלו — קסטרד אפוי שהתגבן ויצר תעלות מים הוא אובדן בלתי הפיך (McGee p. 93)"
expected_effects:
  moisture_retention: "PRESERVED"
  reaction_rate: "HALTED"
scientific_rationale: "חימום יתר של תערובת ביצים וחלב מעבר ל־83°C גורם לקרישת יתר של חלבוני הביצה ולהפרדת נוזלים (Syneresis)."
observations:
  - "דווח אם מופיעים גרגירים או הפרדת נוזל בקרם"
  - "בקסטרד אפוי: בדוק אם המרכז עדיין רוטט קלות (Jiggly) כדי להוציא לפני קרישת-יתר מהחום השיורי"
safety_notes:
  - "הפסקת החימום מונעת המשך התגבנות; מרקם לבדו אינו מוכיח שהביצים עברו פסטור מלא"
tags:
  - "קרם"
  - "ביצים"
  - "התגבנות"
  - "custard"
  - "curdling"
confidence: 95
verified_on: "2026-10-21"
exceptions:
  - "בקרם פטיסייר או מילוי פאי המכיל עמילן וחלמונים חובה דווקא להגיע לרתיחה מלאה (100°C) למשך דקה כדי להשבית את אנזים העמילאז שבחלמון ([[Rule-Starch-Stabilized-Pastry-Cream-Boiling]])"
  - "במרק ביצים יפני מלוח עם ירקות/פירות (Chawan-mushi) הפרשת נוזלים קלה נחשבת לאפקט מכוון של שילוב מרק וקסטרד (McGee p. 95)"
relationships:
  - type: SUPPORTED_BY
    target_id: "SCI-PROT-002"
    target_name: "[[Protein-Denaturation-Coagulation]]"
    condition: "מנגנון קרישת יתר ודחיקת מים מעל 83°C"
    evidence: "McGee 2004, Ch. 2, pp. 85-86 (PDF pp. 99-100)"
    confidence: 98
  - type: SUPPORTED_BY
    target_id: "SCI-PROT-003"
    target_name: "[[Custard-Dilution-Ion-Shielding-And-Starch-Protection]]"
    condition: "דילול פי 6 בחלב ומיסוך סוכרוז מול הגנת עמילן ב-77°C"
    evidence: "McGee 2004, Ch. 2, pp. 93-94 (PDF pp. 107-108)"
    confidence: 98
  - type: ALTERNATIVE_TO
    target_id: "RUL-EGG-003"
    target_name: "[[Rule-Starch-Stabilized-Pastry-Cream-Boiling]]"
    condition: "שימוש בעמילן מגן לעומת בישול עדין ללא עמילן"
    evidence: "McGee 2004, Ch. 2, pp. 94, 98-99 (PDF pp. 108, 112-113)"
    confidence: 96
  - type: SUPPORTED_BY
    target_id: "SRC-BCCAMPUS-PASTRY-2015"
    target_name: "[[SRC-BCCAMPUS-PASTRY-2015]]"
  - type: SUPPORTED_BY
    target_id: "SRC-MCGEE-2004"
    target_name: "[[SRC-MCGEE-2004]]"
    note: "Chapter 2, Printed pp. 85-86, 93-95, 98-99 (PDF pp. 99-100, 107-109, 112-113)"
sources:
  - source_id: "SRC-BCCAMPUS-PASTRY-2015"
    citation: "BCcampus, Modern Pastry and Plated Dessert Techniques, 2015, Coagulation"
  - source_id: "SRC-MCGEE-2004"
    citation: "Harold McGee, On Food and Cooking (2nd Ed., 2004), Chapter 2: Eggs, Printed pp. 85-86, 93-95, 98-99 (PDF pp. 99-100, 107-109, 112-113)"
verification_status: VERIFIED
updated_at: 2026-10-21
---

# כלל החלטה: מניעה ועצירת התגבנות בקרם ביצים וקסטרד (`RUL-EGG-001`)

## 1. הצהרת הכלל המותנה (`IF / THEN / BECAUSE / EXCEPTIONS`)
* **IF (תנאי הפעלה)**: תערובת של ביצים, חלב/שמנת וסוכר (ביחס קלאסי של ביצה אחת, כוס נוזל של 250 מ"ל ו-2 כפות/30 גרם סוכר) מחוממת להסמכה או התייצבות, ומתקרבת לטווח **79°C–83°C (175°F–185°F)** או מראה סימני התגבנות ראשונים.
* **THEN (פעולה נדרשת)**:
  1. **בזמן אמת**: עצור מיד את החימום והסר ממקור החום. אם מדובר בקרם בחוש (`Crème Anglaise`), העבר מיד לקערה קרה/אמבט קרח תוך בחישה וסנן דרך מסננת צפופה להוצאת גושים. אם מדובר בקסטרד אפוי, הוצא מהתנור כאשר המרכז עדיין רוטט קלות (*Jiggly*).
  2. **בתכנון מראש (בחירת שיטה)**: בחר בין חימום איטי ומבוקר (אמבט מים פתוח 80°C–83°C) לבין הוספת עמילן מגן (`8 גרם קמח` או `5 גרם קורנפלור` לכל `250 מ"ל` נוזל).
* **BECAUSE (נימוק מדעי)**: החלב לבדו מגדיל פי 6 את הנפח שעל חלבוני הביצה לגשר עליו, וכל כף סוכר מקיפה כל מולקולת חלבון באלפי מולקולות סוכרוז. כתוצאה מכך, טמפרטורת הקרישה עולה מ-70°C בביצה נקייה ל-**79°C–83°C**, והרשת החלבונית שנוצרת דקה ושברירית במיוחד. לתגובת הקרישה יש "מומנטום" כימי-תרמי שאינו נעצר ברגע כיבוי האש: חריגה של **3°C–5°C בלבד (5°F–10°F)** גורמת לקרישת-יתר, להתכווצות הרשת, ליצירת תעלות מים (*Tunneling*) בקסטרד אפוי או גושים גרגיריים (*Curds*) בקרם בחוש (`[[Custard-Dilution-Ion-Shielding-And-Starch-Protection]]`, עמ' מודפס 93 | PDF עמ' 107).
* **EXCEPTIONS (חריגים מותנים)**:
  - **קרמים מועשרים בעמילן וחלמון (`[[Rule-Starch-Stabilized-Pastry-Cream-Boiling]]`)**: כאשר הקרם מכיל קמח או קורנפלור (`Crème Pâtissière` או מילוי פאי קרם), העמילן עובר ג'לטיניזציה ב-**77°C (175°F)**, בולע אנרגיית חום ומונע פיזית מחלבוני הביצה להיקשר בצפיפות. במקרה זה **חובה להביא לרתיחה מלאה (100°C)** כדי להשבית את אנזים ה-**Amylase** שבחלמון (עמ' מודפס 94, 98 | PDF עמ' 108, 112).

---

## 2. השוואת שיטות לגיטימיות ופשרות (Tradeoffs Matrix)
| שיטה קולינרית | יתרונות מדעיים וקולינריים | חסרונות ופשרות (Tradeoffs) | מתי לבחור? |
| :--- | :--- | :--- | :--- |
| **1. חימום עדין ללא עמילן (אמבט מים / סיר כפול)** | שומר על מרקם חלק, משיי וטהור ועל מלוא עוצמת הטעם של השמנת, הווניל והחלמון | מרווח טעות צר של 3°C–5°C בלבד; קסטרד אפוי שהתגבן אינו ניתן להצלה | קרם ברולה, פלאן, קרם קרמל, וקרם אנגלז קלאסי |
| **2. ייצוב בעמילן (`8g` קמח או `5g` קורנפלור ל-`250ml`)** | חסין להתגבנות אפילו ברתיחה על להבה ישירה; מאפשר בישול מהיר | הופך את המרקם לסמיך וכבד יותר ומעמעם חלק מעדינות הטעם | קרם פטיסייר, מילויי פאי ופחזניות, ובסיס לסופלה |
| **3. סינון מכני לאחר מעשה (Straining Rescue)** | מציל קרם בחוש (`Crème Anglaise`) שהחל ליצור גרגירים ראשונים | מאבד חלק מהחלבון שנקרש; בלתי אפשרי בקסטרד אפוי המוגש בכליו | רק ברוטבי קרם נוזליים/בחושים שجلשו מעט מעבר ל-83°C |
