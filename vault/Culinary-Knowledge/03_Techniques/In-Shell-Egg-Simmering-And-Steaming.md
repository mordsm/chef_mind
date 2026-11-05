---
id: TEC-EGG-001
type: COOKING_TECHNIQUE
name: "בישול ביצים בקליפתן — בעבוע עדין, אידוי ובישול ארוך חמינדוס (In-Shell Egg Simmering, Steaming & Hamindas)"
title_he: "בישול ביצים בקליפתן — בעבוע עדין, אידוי ובישול ארוך (חמינדוס)"
domain: TECHNIQUES
heat_environment: "MOIST"
book_title: "On Food and Cooking: The Science and Lore of the Kitchen"
author: "Harold McGee"
edition: "2nd Edition, Completely Revised and Updated"
publication_year: 2004
chapter: "Chapter 2: Eggs (Basic Egg Dishes: Eggs Cooked In the Shell)"
pdf_page: "101-103"
printed_page: "87-89"
knowledge_type: "COOKING_TECHNIQUE"
claim_type: "DIRECT_SOURCE_CLAIM"
description: "פרוטוקול בישול ביצים בקליפתן ללא רתיחה סוערת: מביצה רכה (Oeuf à la coque / Mollet) דרך ביצה קשה בבעבוע עדין (80°C–85°C) או באידוי חסכוני באנרגיה, ועד בישול איטי ארוך של 6–18 שעות ב-71°C–74°C (חמינדוס)"
heat_transfer_methods:
  - "CONVECTION"
  - "CONDUCTION"
recommended_equipment:
  - "סיר מים בבעבוע שקט (80°C–85°C) או סלסילת אידוי עם מכסה פתוח מעט (Lid slightly ajar)"
target_foods:
  - "ביצים שלמות בקליפתן (רכות, Mollet, קשות, ביצי תה סיניות, חמינדוס)"
conditions:
  surface_temperature_min_c: 71
  surface_temperature_max_c: 85
  cooking_medium: "WATER_OR_STEAM"
  duration_range: "2-3 min (à la coque), 3-5 min (coddled), 5-6 min (mollet), 10-15 min (hard-cooked), 6-18 hours (hamindas at 71-74°C)"
effects:
  primary_outcome: "התמצקות מבוקרת של החלבון והחלמון ללא סדיקת הקליפה, ללא מרקם גומיי וללא טבעת ירוקה-אפורה (FeS)"
  texture_change: "רצף מרקמים מנוזלי למחצה ועד מוצק נימוח; בחמינדוס ב-71°C–74°C מתקבל חלבון שחום ורך מאוד וחלמון קרמי"
  moisture_loss_pct_estimate: 0.0
exceptions:
  - "בביצים רכות מאוד (3–5 דקות) זמן הבישול הקצר מונע התפתחות מרקם גומיי בשכבה החיצונית גם במים המבעבעים קלות סמוך לרתיחה (McGee p. 87)"
relationships:
  - type: REQUIRES
    target_id: "SCI-PROT-002"
    target_name: "[[Protein-Denaturation-Coagulation]]"
    condition: "שליטה במפל הטמפרטורה בין הקליפה למרכז החלמון"
    evidence: "McGee 2004, Ch. 2, pp. 87-88 (PDF pp. 101-102)"
    confidence: 99
  - type: INHIBITS
    target_id: "FLV-EGG-001"
    target_name: "[[Egg-Sulfur-Volatiles-And-Ferrous-Sulfide-Greening]]"
    condition: "בישול ב-80°C–85°C וקירור מיידי במי קרח מונעים היווצרות ברזל גופרי ירוק (FeS) וריח גופרית"
    evidence: "McGee 2004, Ch. 2, pp. 88-89 (PDF pp. 102-103)"
    confidence: 99
  - type: ENABLES
    target_id: "SCI-CHEM-001"
    target_name: "[[Maillard-Reaction]]"
    condition: "בישול ארוך של 6–18 שעות ב-71°C–74°C בחמינדוס מפעיל תגובת מייאר בין 0.25g גלוקוז לאלבומין בסביבה בסיסית"
    evidence: "McGee 2004, Ch. 2, p. 89 (PDF p. 103)"
    confidence: 99
  - type: ALTERNATIVE_TO
    target_id: "TEC-MOIST-001"
    target_name: "[[Gentle-Simmering-Poaching]]"
    condition: "אידוי עם מכסה מוסט קלות כחלופה לבישול בסיר מים"
    evidence: "McGee 2004, Ch. 2, p. 88 (PDF p. 102)"
    confidence: 98
  - type: SUPPORTED_BY
    target_id: "SRC-MCGEE-2004"
    target_name: "[[SRC-MCGEE-2004]]"
    note: "Chapter 2, Printed pp. 87-89 (PDF pp. 101-103)"
sources:
  - source_id: "SRC-MCGEE-2004"
    citation: "Harold McGee, On Food and Cooking (2nd Ed., 2004), Chapter 2: Eggs, Printed pp. 87-89 (PDF pp. 101-103)"
verification_status: VERIFIED
created_at: 2026-10-21
updated_at: 2026-10-21
---

# בישול ביצים בקליפתן — בעבוע עדין, אידוי ובישול ארוך (חמינדוס) (`TEC-EGG-001`)

## 1. מדוע "הרתחת ביצה" (Boiling) היא טעות מדעית?
למרות השם השגור "ביצה קשה/רכה מורתחת" (*Hard/Soft-Boiled*), מקג'י מדגיש כי רתיחה סוערת (100°C) היא דרך גרועה לבשל ביצים משתי סיבות (עמ' מודפס 87–88 | PDF עמ' 101–102):
1. **סדיקה מכנית**: מערבולות המים הרותחים מטיחות את הביצים זו בזו ובדפנות הסיר וסודקות את הקליפה.
2. **קרישת-יתר של השכבה החיצונית**: טמפרטורה של 100°C גבוהה בהרבה מסף הקרישה של החלבונים (63°C–80°C), ולכן עד שהחום חודר למרכז החלמון, השכבות החיצוניות של החלבון מתכווצות והופכות גומיות ועתירות מימן גופרי ($\text{H}_2\text{S}$).
* **הפתרון — בעבוע חסר בועות (`80°C–85°C / 180°F–190°F`) או אידוי (`Steaming`)**: אידוי דורש מעט מאוד מים ואנרגיה, והשארת מכסה הסיר פתוח מעט (*Lid slightly ajar*) מורידה את טמפרטורת האפקטיבית מתחת ל-100°C ומניבה חלבון רך ועדין.

---

## 2. ספקטרום הזמנים והמרקמים בבישול בקליפה (עמ' מודפס 88–89 | PDF עמ' 102–103)
| סגנון | זמן בישול (ממוצע) | מצב החלבון (Albumen) | מצב החלמון (Yolk) | אופן הגשה והערות |
| :--- | :--- | :--- | :--- | :--- |
| **Oeuf à la coque** | **2–3 דקות** | חצי-נוזלי לכל אורכו | חם ונוזלי | נאכל בכפית מתוך הקליפה |
| **Coddled / Soft-Boiled** | **3–5 דקות** | מעטפת חיצונית מוצקה בקושי, פנים חלבי | חם ונוזלי | נאכל מתוך הקליפה |
| **Oeuf Mollet** | **5–6 דקות** | חלבון חיצוני יציב מספיק לקילוף | חצי-נוזלי וקרמי | מקולף ומוגש שלם |
| **Hard-Cooked (10 דק')** | **10 דקות** | מוצק אך נימוח | צהוב כהה, לח ומשחתי מעט | קירור מיידי במי קרח לעצירת הבישול |
| **Hard-Cooked (15 דק')** | **15 דקות** | מוצק לגמרי | צהוב בהיר, יבש ומתפורר (Granular) | חשיפת יתר מגבירה סיכון לטבעת ירוקה (`[[Egg-Sulfur-Volatiles-And-Ferrous-Sulfide-Greening]]`) |
| **חמינדוס / Beid Hamine** | **6–18 שעות ב-`71°C–74°C` (`160°F–165°F`)** | צבע חום-שזוף, מרקם רך ועדין במיוחד! | קרמי ונימוח | תגובת מייאר איטית בסביבה בסיסית בין 0.25g גלוקוז לאלבומין; מתחת לסף הקרישה הקשיח של `Ovalbumin` (80°C)! |

---

## 3. מבחן הסחרור להבחנה בין ביצה נאה לביצה מבושלת (עמ' מודפס 87 | PDF עמ' 101)
* **בדיקה פיזיקלית מהירה**: סובב את הביצה השלמה על צידה על משטח ישר. אם היא מסתובבת **מהר ובחלקות** — היא מבושלת (מוצק קשיח). אם סיבובה **מקרטע ומתנדנד** — היא נאה (הנוזל הפנימי מחליק ומתנגד לתנועת הקליפה המוצקה).

