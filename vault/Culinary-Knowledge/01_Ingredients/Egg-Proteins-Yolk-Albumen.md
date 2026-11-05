---
id: ING-EGG-001
type: INGREDIENT
name: "ביצת תרנגולת — חלבון וחלמון (Chicken Egg)"
title_he: "ביצת תרנגולת — חלבון וחלמון (Chicken Egg)"
domain: INGREDIENTS
category: "חלבון מן החי"
book_title: "On Food and Cooking: The Science and Lore of the Kitchen"
author: "Harold McGee"
edition: "2nd Edition, Completely Revised and Updated"
publication_year: 2004
chapter: "Chapter 2: Eggs"
pdf_page: "82-131"
printed_page: "68-117"
knowledge_type: "INGREDIENT_PROPERTY"
claim_type: "DIRECT_SOURCE_CLAIM"
composition:
  shelled_weight_g: 55.0
  white_weight_g: 38.0
  yolk_weight_g: 17.0
  water_pct: 76.0
  protein_pct: 12.0
  fat_pct: 10.9
  carb_pct: 1.1
  cholesterol_mg: 213
  sodium_mg: 71
  calories_kcal: 84
  ph_level_fresh_white: 7.7
  ph_level_aged_white: 9.2
  ph_level_fresh_yolk: 6.0
  ph_level_aged_yolk: 6.6
physical_properties:
  density_g_cm3: 1.03
  shell_pores_count: 10000
  thermal_conductivity: "LOW_TO_MEDIUM"
  cellular_structure: "תמיסת חלבונים גלובולריים (אלבומין: 88% מים, 10.3% חלבון) ותחליב כדורי מקונן של ליפו-פרוטאינים בצפיפות נמוכה (LDL) ולציטין בחלמון (48% מים, 35% שומן, 16% חלבון)"
sensory_profile:
  dominant_taste: ["SAVORY", "RICH", "MILD_SWEET_BUTTERY_YOLK"]
  aroma_compounds: ["hydrogen_sulfide_above_60c", "ammonia_trace", "triethylamine_if_choline_defect"]
  raw_texture: "VISCOUS_LAMINATED_LIQUID"
storage_and_safety:
  shelf_life_days_refrigerated: 28
  minimum_internal_temp_c: 71.0
  salmonella_pasteurization_schedules:
    - "60°C (140°F) for 5 minutes (runny yolk preserved)"
    - "70°C (160°F) for 1 minute (firm yolk)"
    - "65°C (150°F) water bath for 15 minutes for poached eggs"
  allergens: ["eggs"]
  kashrut_class: "PAREVE"
relationships:
  - type: ENABLES
    target_id: "SCI-PROT-002"
    target_name: "[[Protein-Denaturation-Coagulation]]"
    condition: "חימום בטווח 60°C–80°C, הקצפה מכנית או חשיפה לחומצה/מלח"
    evidence: "McGee 2004, Ch. 2, pp. 84-86 (PDF pp. 98-100)"
    confidence: 98
  - type: ENABLES
    target_id: "SCI-CHEM-002"
    target_name: "[[Caramelization-And-Emulsification]]"
    condition: "שימוש בחלקיקי LDL ולציטין מהחלמון לתחליבים (מיונז, הולנדז)"
    evidence: "McGee 2004, Ch. 2, pp. 75-77 (PDF pp. 89-91)"
    confidence: 97
  - type: ENABLES
    target_id: "SCI-FOAM-001"
    target_name: "[[Egg-Foam-Stability-Disulfide-And-Acid-Copper-Chemistry]]"
    condition: "הקצפת אלבומין ללא זיהום שומן או חלמון"
    evidence: "McGee 2004, Ch. 2, pp. 100-104 (PDF pp. 114-118)"
    confidence: 98
  - type: AFFECTS
    target_id: "ING-EGG-002"
    target_name: "[[Egg-Albumen-Key-Proteins]]"
    condition: "הרכב שבעת חלבוני האלבומין קובע את טמפרטורות ההתמצקות וכושר ההקצפה"
    evidence: "McGee 2004, Ch. 2, pp. 77-78 (PDF pp. 91-92)"
    confidence: 98
  - type: AFFECTS
    target_id: "ING-EGG-003"
    target_name: "[[Egg-Yolk-Lipoproteins-And-Amylase]]"
    condition: "מבנה כדורי החלמון, גרנולות ה-LDL ואנזים העמילאז העמיד לחום"
    evidence: "McGee 2004, Ch. 2, pp. 75-76, 98 (PDF pp. 89-90, 112)"
    confidence: 98
  - type: AFFECTS
    target_id: "ING-EGG-004"
    target_name: "[[Egg-Aging-Alkalinization-And-Grades]]"
    condition: "איבוד פחמן דו-חמצני דרך נקבוביות הקליפה מעלה pH ומדלל את החלבון הסמיך"
    evidence: "McGee 2004, Ch. 2, pp. 80-82 (PDF pp. 94-96)"
    confidence: 98
  - type: SUPPORTED_BY
    target_id: "SRC-BCCAMPUS-PASTRY-2015"
    target_name: "[[SRC-BCCAMPUS-PASTRY-2015]]"
    note: "תיקוף מקביל של תפקודי קרישה ואמולסיה באפייה"
  - type: SUPPORTED_BY
    target_id: "SRC-MCGEE-2004"
    target_name: "[[SRC-MCGEE-2004]]"
    note: "Chapter 2: Eggs, Printed pp. 68-117 (PDF pp. 82-131)"
sources:
  - source_id: "SRC-BCCAMPUS-PASTRY-2015"
    citation: "BCcampus, Modern Pastry and Plated Dessert Techniques, 2015, Coagulation"
  - source_id: "SRC-MCGEE-2004"
    citation: "Harold McGee, On Food and Cooking (2nd Ed., 2004), Chapter 2: Eggs, Printed pp. 68-117 (PDF pp. 82-131)"
verification_status: VERIFIED
updated_at: 2026-10-21
---

# ביצת תרנגולת — חלבון וחלמון (Chicken Egg)

## 1. תיאור כללי ומבנה אנטומי-ביוכימי (Overview & Anatomy)
ביצת התרנגולת (*Gallus gallus*) היא מערכת ביוכימית דו-מדורית מתוחכמת שנועדה להזין ולהגן על העובר המתפתח במשך 21 יום, ולכן משמשת במטבח כבונה המבנים הרב-תכליתי ביותר (ממרנג אוורירי ועד קסטרד עשיר ואמולסיות חלקות).
* **הקליפה והממברנות (Shell & Membranes)**: הקליפה בנויה מגבישי סידן פחמתי ($\text{CaCO}_3$) וחלבון, מנוקבת בכ-**10,000 נקבוביות** זעירות (בעיקר בצד הקהה) ומצופה בשכבת חלבון דקה (*Cuticle*). מתחתיה שתי ממברנות חלבוניות אנטי-מיקרוביאליות הנפרדות בצד הקהה עם התקררות הביצה מהטלתה (41°C) ליצירת **תא האוויר (Air Cell)** (עמ' מודפס 74–75 | PDF עמ' 88–89).
* **החלבון (Albumen / Egg White)**: מהווה כמעט שני שלישים ממשקל תוכן הביצה (38 גרם בביצת Large), מתוכם כ-**88%–90% מים** וכ-**10% חלבונים** גלובולריים וסיביים (`[[Egg-Albumen-Key-Proteins]]`), בנוסף לכ-**0.25 גרם גלוקוז** חופשי (האחראי להשחמת מייאר בביצים בבישול ארוך כמו חמינדוס) וויטמין ריבופלבין המעניק גוון צהבהב-ירקרק עדין (עמ' מודפס 77, 89 | PDF עמ' 91, 103).
* **החלמון (Egg Yolk)**: מהווה כשליש ממשקל תוכן הביצה (17 גרם), תלוי במרכז באמצעות שני מיתרי חלבון אלסטיים מפותלים (**כלזה / Chalazae**). מכיל כ-75% מהקלוריות של הביצה, את כל השומן והכולסטרול, ורוב הברזל, התיאמין וויטמין A. צבעו הצהוב מקורו בפיגמנטים צמחיים ממשפחת ה**קסנתופילים (Xanthophylls)** (לוטאין וזאקסנטין מתירס ואספסת) ולא בבטא-קרוטן (עמ' מודפס 74–75, 78 | PDF עמ' 88–89, 92).

---

## 2. הרכב תזונתי וכימי של ביצת U.S. Large (55 גרם ללא קליפה)
> מקור: *On Food and Cooking* (2004), פרק 2, עמ' מודפס 79 (PDF עמ' 93) — `DIRECT_SOURCE_CLAIM`:

| רכיב | ביצה שלמה (Whole Egg) | חלבון (Egg White) | חלמון (Egg Yolk) | משמעות קולינרית |
| :--- | :--- | :--- | :--- | :--- |
| **משקל** | 55 גרם | 38 גרם (69%) | 17 גרם (31%) | יחס נפחי של כ-2 כפות חלבון ל-1 כף חלמון |
| **מים** | ~41.8 גרם (~76%) | ~33.8 גרם (~89%) | ~8.0 גרם (~47%) | בחלמון כמעט כל המים קשורים; רק כ-2 מ"ל מים חופשיים (`[[Egg-Yolk-Lipoproteins-And-Amylase]]`) |
| **חלבון (Protein)** | 6.6 גרם | 3.9 גרם (10.3%) | 2.7 גרם (15.9%) | החלמון עשיר יותר בחלבון באחוזים, אך חלבוניו כלואים בחלקיקי LDL |
| **שומן סך הכל** | 6.0 גרם | 0 גרם | 6.0 גרם (35.3%) | כולל 2.5g חד-בלתי-רווי, 0.7g רב-בלתי-רווי, 2.0g רווי + פוספוליפידים (לציטין) |
| **פחמימות (גלוקוז)** | 0.6 גרם | 0.3 גרם (~0.25g גלוקוז) | 0.3 גרם | מספיק ליצירת תגובת מייאר בחלבון בבישול ממושך (`[[Maillard-Reaction]]`) |
| **כולסטרול** | 213 מ"ג | 0 מ"ג | 213 מ"ג | מרוכז כולו בחלמון (`[[Conflict-Dietary-Egg-Cholesterol-Vs-Saturated-Fat]]`) |
| **נתרן (Sodium)** | 71 מ"ג | 62 מ"ג | 9 מ"ג | יונים טבעיים המסייעים ביצירת רשת קרישה |
| **אנרגיה** | 84 קק"ל | 20 קק"ל | 64 קק"ל | כ-60% מהקלוריות מקורן בשומן החלמון |

---

## 3. התנהגות בבישול וסיפי טמפרטורה (Cooking Thresholds)
* **מדרגות קרישה של ביצה לא מדוללת (`[[Protein-Denaturation-Coagulation]]`)**:
  - **חלבון הביצה (Albumen)**: מתחיל להסמיך ב-**63°C (145°F)** (בשל קרישת `Ovotransferrin`), הופך למוצק רך ועדין ב-**65°C (150°F)**, אך מתמצק בחוזקה רק סביב **80°C (180°F)** כאשר החלבון המרכזי `Ovalbumin` (54%) נקרש (עמ' מודפס 85 | PDF עמ' 99).
  - **חלמון הביצה (Yolk)**: מתחיל להסמיך ב-**65.5°C (150°F)** ומתייצב למוצק ב-**70°C (158°F)**.
  - **ביצה שלמה מעורבבת (מקושקשת/חביתה)**: מתייצבת סביב **73°C (165°F)**, מאחר שהברזל השופע בחלמון נקשר ל-`Ovotransferrin` שבחלבון ומעלה את עמידותו לחום מ-60°C לכיוון 70°C+ (עמ' מודפס 78, 85 | PDF עמ' 92, 99).
* **בקרמים ורטבים (`[[Rule-Custard-Curdling-Rescue]]`, `[[Custard-Dilution-Ion-Shielding-And-Starch-Protection]]`)**: דילול בחלב או שמנת ותוספת סוכר מעלים את טמפרטורת הקרישה ל-**79°C–83°C (175°F–185°F)**, אך חריגה של 3°C–5°C בלבד (5°F–10°F) מעבר לטווח זה גורמת להתגבנות (Curdling) ולהפרדת מים (Syneresis).
