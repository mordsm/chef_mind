---
id: SCI-CARB-001
type: SCIENTIFIC_PRINCIPLE
name: "ג'לטיניזציה ורטרוגרדציה של עמילן (Starch Gelatinization & Retrogradation)"
domain: FOOD_SCIENCE
category: "CARBOHYDRATE"
description: "ספיחת מים והתנפחות גרנולות עמילן בחום ליצירת צמיגות ורשת ג'ל, והתגבשותן מחדש בקירור"
conditions:
  temperature_range_c:
    min: 55
    max: 95
  water_activity_aw:
    min: 0.80
    max: 1.0
  ph_range:
    min: 4.0
    max: 8.0
  catalysts: ["water", "heat", "gentle_agitation"]
effects:
  molecular_change: "שבירת הקשרים הגבישיים בגרנולת העמילן, חדירת מים ושחרור שרשראות עמילוז המאטות את תנועת המים החופשיים"
  sensory_consequences:
    taste: ["LOSS_OF_RAW_CHALKINESS"]
    aroma: []
    color: "מעבר מעכור/לבן לחצי-שקוף ומבריק"
    texture: "הסמכת נוזלים לצמיגות קטיפתית או התייצבות לג'ל"
exceptions:
  - "הוספת עמילן יבש לנוזל חם ללא פיזור מוקדם יוצרת גושים אטומים"
  - "ערבוב אגרסיבי מדי או חומציות גבוהה בבישול ממושך שוברים את רשת העמילן ומדללים את הרוטב"
relationships:
  - type: AFFECTS
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
    citation: "BCcampus, Modern Pastry and Plated Dessert Techniques, 2015"
    chapter: "Gelatinization"
    pages: "Chapter 2"
verification_status: VERIFIED
---

# ג'לטיניזציה ורטרוגרדציה של עמילן (Starch Gelatinization & Retrogradation)

## מנגנון מדעי מפורט (Scientific Mechanism)
גרנולות עמילן (`[[Starch-Cornstarch-Flour]]`) אינן מתמוססות במים קרים, אלא יוצרות תרחיף (Slurry). בחימום ל-60°C–85°C (בהתאם לסוג העמילן), הגרנולות סופחות מים, מתנפחות ופולטות מולקולות עמילוז היוצרות רשת תלת-ממדית המעלה דרמטית את צמיגות הנוזל (`[[Starch-And-Emulsion-Viscosity]]`). בקירור מתרחשת **רטרוגרדציה** — התארגנות מחדש של שרשראות העמילוז למבנה גבישי קשיח יותר.
