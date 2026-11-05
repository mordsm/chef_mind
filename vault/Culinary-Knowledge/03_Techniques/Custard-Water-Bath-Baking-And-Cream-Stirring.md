---
id: TEC-EGG-003
type: COOKING_TECHNIQUE
name: "אפיית קסטרדים באמבט מים ובישול קרמים בחושים (Custard Water-Bath Baking & Stirred Creams)"
title_he: "אפיית קסטרדים באמבט מים ובישול קרמים בחושים (Crème Anglaise, Pâtissière, Cheesecake)"
domain: TECHNIQUES
heat_environment: "MOIST_OR_INDIRECT"
book_title: "On Food and Cooking: The Science and Lore of the Kitchen"
author: "Harold McGee"
edition: "2nd Edition, Completely Revised and Updated"
publication_year: 2004
chapter: "Chapter 2: Eggs (Egg-Liquid Mixtures: Custards and Creams)"
pdf_page: "106-114"
printed_page: "92-100"
knowledge_type: "COOKING_TECHNIQUE"
claim_type: "DIRECT_SOURCE_CLAIM"
description: "הבחנה מבנית ופרוצדורלית בין קסטרדים אפויים ללא בחישה (היוצרים ג'ל מוצק בכלי ההגשה: פלאן, קרם ברולה, קיש, עוגת גבינה) לבין קרמים בחושים על הכיריים (היוצרים רוטב או מילוי: קרם אנגלז, קרם פטיסייר, Bouillie, וקורד פירות)"
heat_transfer_methods:
  - "CONDUCTION"
  - "CONVECTION"
recommended_equipment:
  - "אמבט מים פתוח (Bain-Marie) ממתכת דקה עם רשת תחתית לקסטרדים"
  - "סיר כבד או סיר כפול (Double Boiler) לקרמים בחושים"
target_foods:
  - "קרם קרמל, קרם ברולה, קיש, עוגת גבינה (Cheesecake), קרם אנגלז, קרם פטיסייר, Lemon Curd"
conditions:
  surface_temperature_min_c: 79
  surface_temperature_max_c: 100
  cooking_medium: "WATER_BATH_OR_STOVETOP"
  duration_range: "10-25 min (stovetop creams) to 45-60 min (baked custards)"
effects:
  primary_outcome: "יצירת רשת חלבונים עדינה (ג'ל רציף ללא בחישה בקסטרד; תחליב חלבוני מפורק וניגר בבחישה מתמדת בקרם אנגלז)"
  texture_change: "ג'ל חלק ועדין בקסטרד; רוטב בעל סמיכות של שמנת מתוקה בקרם אנגלז (80°C); קרם יציב לחיתוך או זילוף בקרם פטיסייר מורתח"
  moisture_loss_pct_estimate: 3.0
exceptions:
  - "קיש (Quiche) מכיל 2 ביצים שלמות לכוס נוזל (250 מ\"ל) ונאפה ללא הגנת אמבט מים כדי שיהיה מוצק מספיק לחיתוך למשולשים (McGee p. 96)"
relationships:
  - type: REQUIRES
    target_id: "SCI-PROT-003"
    target_name: "[[Custard-Dilution-Ion-Shielding-And-Starch-Protection]]"
    condition: "בקרת דילול, יונים ועמילן"
    evidence: "McGee 2004, Ch. 2, pp. 93-95, 98-100 (PDF pp. 107-109, 112-114)"
    confidence: 99
  - type: REQUIRES
    target_id: "EQP-EGG-001"
    target_name: "[[Water-Bath-Materials-And-Copper-Whisking-Bowls]]"
    condition: "בחירת חומר תבנית אמבט המים והימנעות מכיסוי בנייר אלומיניום או מגבת בד"
    evidence: "McGee 2004, Ch. 2, pp. 95-96 (PDF pp. 109-110)"
    confidence: 99
  - type: ENABLES
    target_id: "RUL-EGG-003"
    target_name: "[[Rule-Starch-Stabilized-Pastry-Cream-Boiling]]"
    condition: "הרתחת קרם פטיסייר מול אי-הרתחת קרם אנגלז"
    evidence: "McGee 2004, Ch. 2, pp. 98-100 (PDF pp. 112-114)"
    confidence: 99
  - type: ENABLES
    target_id: "RUL-EGG-005"
    target_name: "[[Rule-Custard-Water-Bath-And-Tempering-Control]]"
    condition: "פרוטוקול השוואת טמפרטורות (Tempering) ואמבט מים"
    evidence: "McGee 2004, Ch. 2, pp. 93-96 (PDF pp. 107-110)"
    confidence: 99
  - type: SUPPORTED_BY
    target_id: "SRC-MCGEE-2004"
    target_name: "[[SRC-MCGEE-2004]]"
    note: "Chapter 2, Printed pp. 92-100 (PDF pp. 106-114)"
sources:
  - source_id: "SRC-MCGEE-2004"
    citation: "Harold McGee, On Food and Cooking (2nd Ed., 2004), Chapter 2: Eggs, Printed pp. 92-100 (PDF pp. 106-114)"
verification_status: VERIFIED
created_at: 2026-10-21
updated_at: 2026-10-21
---

# אפיית קסטרדים באמבט מים ובישול קרמים בחושים (`TEC-EGG-003`)

## 1. הבחנה יסודית: קסטרד (Custard) מול קרם (Cream)
למרות שהתערובת הבסיסית כמעט זהה (סביב **4 חלקים נוזל לחלק אחד ביצה**, או כוס של 250 מ"ל חלב/שמנת ל-1–2 ביצים ו-30 גרם סוכר), אופן הבישול יוצר שני מבנים שונים לחלוטין (עמ' מודפס 92–93 | PDF עמ' 106–107):
1. **קסטרד (Custard — אפוי וללא בחישה)**: מתבשל ומוגש באותו כלי ללא בחישה, כך שחלבוני הביצה יוצרים **רשת ג'ל תלת-ממדית רציפה ומוצקה** (כולל פלאן, קרם קרמל, קרם ברולה, קיש, טרין ועוגת גבינה).
   - **יחסי ביצים לחילוץ מהתבנית (Unmolding)**: קסטרד המוגש בתוך הכלי יכול להיות רך כרצון השף; אך קסטרד שיש לחלץ מתבנית (*Crème Caramel*) חייב להכיל **חלבון ביצה שלם או לפחות 3 חלמונים לכל כוס (250 מ"ל) נוזל**, משום שחלבוני החלמון הקשורים ל-LDL יוצרים רשת חלשה יותר מחלבוני האלבומין החופשיים (עמ' מודפס 95 | PDF עמ' 109).
2. **קרם (Cream — מבושל על הכיריים בבחישה מתמדת)**: הבחישה המתמדת מונעת מהחלבונים ליצור ג'ל מוצק אחיד, ויוצרת מסה סמיכה וניגרת:
   - **קרמים ניגרים (`Crème Anglaise`)**: מבושלים בבחישה מתמדת עד הסמכה קלה המצפה את גב הכף ב-**80°C (180°F)** — הרחק מתחת לנקודת הרתיחה — ומסוננים מיד.
   - **קרמים יציבים מועשרים בעמילן (`Crème Pâtissière`)**: מכילים `1–2 כפות קמח (10–20 גרם)` או מחצית הכמות קורנפלור לכל כוס (250 מ"ל) נוזל, **וחייבים לרתוח כדקה** להשבתת עמילאז החלמון, ולאחר מכן להתקרר **ללא בחישה מיותרת** (בחישה בזמן הקירור שוברת את רשת העמילן המתגבשת ומדללת את הקרם! עמ' מודפס 99–100 | PDF עמ' 113–114).

---

## 2. פרוטוקול 4 השלבים למניעת סדקים ושקיעה בעוגת גבינה (Cheesecake)
עוגת גבינה היא קסטרד עשיר (כביצה אחת ו-60 גרם סוכר לכל 250 מ"ל תערובת גבינה/שמנת). סדקים ושקע במרכז נוצרים כאשר התערובת מתנפחת ותופחת באפייה (כמו סופלה) ואז מתכווצת בקירור. ארבע אסטרטגיות של מקג'י למניעתם (עמ' מודפס 97–98 | PDF עמ' 111–112):
1. **ערבוב איטי, עדין וקצר**: הימנע מהקצפה ממושכת המחדירה בועות אוויר שיתמלאו בקיטור ויתפשטו בתנור.
2. **אפייה איטית בתנור נמוך (`163°C / 325°F`, לרוב באמבט מים)**: מאפשרת לאוויר ולקיטור להתפזר בהדרגה ובאופן שווה.
3. **הימנעות מאפיית-יתר**: אפיית-יתר מייבשת את המלית וגורמת לה להתכווץ ולהיסדק מאובדן לחות.
4. **קירור הדרגתי בתנור כבוי עם דלת פתוחה למחצה**: ממתן את התכווצות האוויר והקיטור ומונע משיכה פתאומית של פני העוגה פנימה.

