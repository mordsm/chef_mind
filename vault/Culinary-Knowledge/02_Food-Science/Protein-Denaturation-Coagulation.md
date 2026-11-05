---
id: SCI-PROT-002
type: SCIENTIFIC_PRINCIPLE
name: "דנטורציה וקרישת חלבונים (Protein Denaturation & Coagulation)"
title_he: "דנטורציה וקרישת חלבונים (Protein Denaturation & Coagulation)"
domain: FOOD_SCIENCE
category: "PROTEIN"
book_title: "On Food and Cooking: The Science and Lore of the Kitchen"
author: "Harold McGee"
edition: "2nd Edition, Completely Revised and Updated"
publication_year: 2004
chapter: "Chapter 2: Eggs (The Chemistry of Egg Cooking)"
pdf_page: "98-100"
printed_page: "84-86"
knowledge_type: "CULINARY_PRINCIPLE"
claim_type: "DIRECT_SOURCE_CLAIM"
description: "פתיחת המבנה המרחבי של חלבונים בחום, בחומצה, במלח או בהקצפה מכנית ויצירת רשת תלת-ממדית הלוכדת מים בג'ל או פולטת אותם בקרישת-יתר"
conditions:
  temperature_range_c:
    min: 50
    max: 85
  water_activity_aw:
    min: 0.70
    max: 1.0
  ph_range:
    min: 3.5
    max: 12.0
  catalysts: ["heat", "acid", "salt_ions", "mechanical_shear_whipping", "alkali"]
effects:
  molecular_change: "שבירת קשרים חלשים השומרים על הקיפול הכדורי של החלבון (Denaturation), חשיפת אזורים הידרופוביים וקבוצות גופרית, והיקשרות שרשראות סמוכות לרשת מרחבית רציפה (Coagulation)"
  sensory_consequences:
    taste: ["ריכוך חמיצות בעת קשירת יונים"]
    aroma: ["שחרור מימן גופרי H2S בחלבון ביצה מעל 60°C"]
    color: "מעבר משקוף לאטום (Opaque) עקב פיזור אור על ידי צברי החלבונים"
    texture: "התמצקות מנוזל (1,000 מולקולות מים לכל מולקולת חלבון בביצה) לג'ל רך ולח; בחימום יתר — התכווצות הרשת, מרקם גומי או התגבנות והפרדת מים (Syneresis)"
exceptions:
  - "חימום מעבר ל-83°C–85°C בקרם ביצים גורם לקרישת יתר (Curdling) ולפליטת המים הכלואים (Syneresis)"
  - "בדילול קיצוני בנוזל נטול מינרלים/מלח (כגון ביצה במים מזוקקים), המטען השלילי של החלבונים מונע יצירת ג'ל אחיד ונוצרים פתיתים נפרדים"
relationships:
  - type: AFFECTS
    target_id: "ING-EGG-001"
    target_name: "[[Egg-Proteins-Yolk-Albumen]]"
    condition: "קרישה מדורגת של חלבוני אלבומין (60°C–80°C) וחלמון (65°C–70°C)"
    evidence: "McGee 2004, Ch. 2, pp. 84-86 (PDF pp. 98-100)"
    confidence: 99
  - type: AFFECTS
    target_id: "ING-EGG-002"
    target_name: "[[Egg-Albumen-Key-Proteins]]"
    condition: "Ovotransferrin נקרש ראשון ב-60°C–65°C ואילו Ovalbumin נקרש רק ב-80°C"
    evidence: "McGee 2004, Ch. 2, pp. 77-78, 85 (PDF pp. 91-92, 99)"
    confidence: 99
  - type: AFFECTS
    target_id: "ING-POUL-001"
    target_name: "[[Poultry-Breast-Lean]]"
    condition: "קרישת מיוצין ואקטין בסיבי השריר"
    evidence: "McGee 2004, Ch. 3, pp. 148-152"
    confidence: 98
  - type: ENABLES
    target_id: "SCI-PROT-003"
    target_name: "[[Custard-Dilution-Ion-Shielding-And-Starch-Protection]]"
    condition: "יצירת רשת ג'ל עדינה בקסטרד בנוכחות יונים ודילול סוכר/חלב"
    evidence: "McGee 2004, Ch. 2, pp. 85-86, 93-94 (PDF pp. 99-100, 107-108)"
    confidence: 98
  - type: SUPPORTED_BY
    target_id: "SRC-BCCAMPUS-PASTRY-2015"
    target_name: "[[SRC-BCCAMPUS-PASTRY-2015]]"
    note: "Coagulation chapter"
  - type: SUPPORTED_BY
    target_id: "SRC-MCGEE-2004"
    target_name: "[[SRC-MCGEE-2004]]"
    note: "Chapter 2, Printed pp. 84-86 (PDF pp. 98-100)"
sources:
  - source_id: "SRC-BCCAMPUS-PASTRY-2015"
    citation: "BCcampus, Modern Pastry and Plated Dessert Techniques, 2015"
    chapter: "Coagulation"
    pages: "Chapter 3"
  - source_id: "SRC-MCGEE-2004"
    citation: "Harold McGee, On Food and Cooking (2nd Ed., 2004), Chapter 2: Eggs"
    chapter: "The Chemistry of Egg Cooking: How Eggs Get Hard and Custards Thicken"
    pages: "Printed pp. 84-86 (PDF pp. 98-100)"
verification_status: VERIFIED
updated_at: 2026-10-21
---

# דנטורציה וקרישת חלבונים (Protein Denaturation & Coagulation)

## 1. מנגנון מדעי מפורט (Scientific Mechanism)
בביצה נאה, החלבון והחלמון הם תמיסות מימיות שבהן מולקולות המים עולות במספרן על מולקולות החלבון ביחס של כ-**1,000 ל-1** (עמ' מודפס 84 | PDF עמ' 98). כל מולקולת חלבון היא שרשרת בת אלפי אטומים המקופלת לפקעת קומפקטית, ובסביבה הכימית של ביצה טרייה רוב החלבונים נושאים **מטען חשמלי שלילי** הגורם להם לדחות זה את זה ולהישאר מפוזרים בנוזל.

תהליך ההתמצקות מתרחש בשני שלבים עוקבים:
1. **דנטורציה (Denaturation — פתיחת הקיפול)**: חימום מגביר את התנועה התרמית וההתנגשויות בין המולקולות עד לשבירת הקשרים החלשים המחזיקים את השרשרת מקופלת. אותו אפקט מושג גם על ידי **חומצה, מלח או כוח גזירה בהקצפה** (עמ' מודפס 84–85 | PDF עמ' 98–99).
2. **קרישה (Coagulation — היקשרות לרשת תלת-ממדית)**: השרשראות שנפתחו מסתבכות זו בזו ויוצרות קשרים כימיים ליצירת רשת מרחבית רציפה הלוכדת את המים באינספור כיסים מיקרוסקופיים. מכיוון שצברי החלבונים גדולים מספיק כדי להסיט קרני אור, האלבומין השקוף הופך לאטום ולבן.

---

## 2. סיפי טמפרטורה מדויקים בביצים ובבשר (Thermal Thresholds)
> מקור: *On Food and Cooking* (2004), עמ' מודפס 85–86 (PDF עמ' 99–100) — `DIRECT_SOURCE_CLAIM`:

| מערכת מזון | תחילת הסמכה | התייצבות למוצק רך | התמצקות מלאה / סף שבירה | החלבון הקובע והערות מנגנוניות |
| :--- | :--- | :--- | :--- | :--- |
| **חלבון ביצה נקי (Albumen)** | **63°C** (145°F) | **65°C** (150°F) | **80°C** (180°F) | `Ovotransferrin` (12%) נקרש ראשון ב-60–65°C; `Ovalbumin` (54%) נקרש רק ב-80°C; `Ovomucin` עמיד ביותר לחום |
| **חלמון ביצה נקי (Egg Yolk)** | **65.5°C** (150°F) | **70°C** (158°F) | מעל 75°C מתייבש ומתפורר | חלבוני ליפו-פרוטאין (LDL) בתוך כדורי החלמון (`[[Egg-Yolk-Lipoproteins-And-Amylase]]`) |
| **ביצה שלמה מעורבבת** | ~66°C | **73°C** (165°F) | מעל 80°C הופכת גומיית | ברזל מהחלמון נקשר ל-`Ovotransferrin` ומעלה את עמידותו לחום |
| **תערובת קסטרד (חלב + סוכר + ביצה)** | **78°C–80°C** (175°F–180°F) | **79°C–83°C** (175°F–185°F) | **>85°C–88°C** (התגבנות / Curdling) | דילול המים ומיסוך הסוכר מעלים את סף הקרישה ב-8°C–11°C (`[[Custard-Dilution-Ion-Shielding-And-Starch-Protection]]`) |
| **בשר ודגים** | **50°C–55°C** (מיוצין) | **60°C–65°C** (קולגן מתכווץ) | **66°C–80°C** (אקטין נקרש) | דנטורציה של חלבוני השריר ודחיקת מיצים |

---

## 3. השפעת תוספים על קרישת חלבוני הביצה (Effects of Added Ingredients)
* **דילול בנוזלים וסוכר (מעלים טמפרטורת קרישה ומעדנים מרקם)**: הוספת חלב, שמנת או סוכר מרחיקה את מולקולות החלבון זו מזו (כף סוכר אחת מקיפה כל חלבון באלפי מולקולות סוכרוז), ולכן נדרשת טמפרטורה גבוהה יותר (**79°C–83°C**) ליצירת מפגשים וקשרים, והג'ל הנוצר דק ועדין הרבה יותר (`[[Custard-Dilution-Ion-Shielding-And-Starch-Protection]]`).
* **חומצה ומלח (מורידים טמפרטורת קרישה אך מרככים מרקם!)**: בניגוד למיתוס הנפוץ, מלח וחומצה מנטרלים את המטען החשמלי השלילי של חלבוני הביצה ולכן גורמים להם להיקשר מוקדם יותר בטמפרטורה נמוכה יותר — בעודם מקופלים חלקית ולפני שהם מספיקים להסתבך בצפיפות וליצור קשרי גופרית קשיחים (`[[Conflict-Acid-And-Salt-Tenderize-Vs-Toughen-Eggs]]`, עמ' מודפס 86 | PDF עמ' 100).
* **סכנת קרישת-יתר (Overcoagulation & Syneresis)**: כאשר מחממים מעבר לסף הקרישה, החלבונים נקשרים זה לזה בצפיפות יתרה ודוחקים החוצה את המים: בביצה קשה או מטוגנת המים בורחים כקיטור והמרקם הופך גומיי, ואילו בקסטרד ובמקושקשת מדוללת התערובת נפרדת לגושים קשים השוחים בנוזל מימי (`[[Rule-Custard-Curdling-Rescue]]`).
