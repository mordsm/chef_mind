---
id: DEC-CORR-001
type: SCIENTIFIC_PRINCIPLE
name: "מטריצת תיקון מרקם, סמיכות ותיבול (Sauce & Texture Correction Matrix)"
domain: DECISION_MAKING
category: "EMULSION"
description: "שינוי מבוקר של משתנה אחד בכל פעם לתיקון רוטב סמיך מדי, דליל מדי או מלוח מדי"
conditions:
  temperature_range_c:
    min: 50
    max: 100
  water_activity_aw:
    min: 0.70
    max: 1.0
  ph_range:
    min: 3.5
    max: 7.5
  catalysts: ["gradual_dilution", "evaporative_reduction", "starch_slurry"]
effects:
  molecular_change: "התאמת ריכוז המוצקים המומסים והצמיגות ההידרודינמית של הרוטב"
  sensory_consequences:
    taste: ["BALANCED_SALINITY_AND_ACIDITY"]
    aroma: []
    color: []
    texture: "סמיכות מותאמת למנה"
exceptions:
  - "הגדלת נפח הרוטב או דילולו מחייבים בדיקת תיבול מחדש לאחר השינוי"
relationships:
  - type: REQUIRES
    target_id: "TEX-VISC-001"
    target_name: "[[Starch-And-Emulsion-Viscosity]]"
  - type: ENABLES
    target_id: "RUL-SAUCE-001"
    target_name: "[[Rule-Starch-Slurry-Dispersion]]"
  - type: SUPPORTED_BY
    target_id: "SRC-BCCAMPUS-PASTRY-2015"
    target_name: "[[SRC-BCCAMPUS-PASTRY-2015]]"
sources:
  - source_id: "SRC-BCCAMPUS-PASTRY-2015"
    citation: "BCcampus, Modern Pastry and Plated Dessert Techniques, 2015, Gelatinization"
verification_status: VERIFIED
---

# מטריצת תיקון מרקם, סמיכות ותיבול (Sauce & Texture Correction Matrix)

## פרוטוקול תיקון הדרגתי (Single-Variable Correction Protocol)
* **רוטב סמיך מדי**: הוספת נוזל מתאים (מים, ציר לא מלוח, או מי בישול פסטה) בהדרגה תוך ערבוב ובדיקת סמיכות אחרי כל תוספת.
* **רוטב דליל מדי**: צמצום בבעבוע עדין בסיר פתוח (`[[Covered-Vs-Uncovered-Evaporation]]`), או הסמכה באמצעות קורנפלור המפוזר בנוזל קר (`[[Rule-Starch-Slurry-Dispersion]]`).
* **מנה מלוחה מדי**: עצירת הוספת מלח ורכיבים מלוחים; הגדלת נפח המנה באמצעות מרכיבים לא מומלחים (נוזל, ירקות, עמילן או שומן/שמנת בהתאם לכשרות ולאלרגנים).
