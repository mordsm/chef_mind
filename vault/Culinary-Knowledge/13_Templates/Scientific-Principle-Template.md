---
id: SCI-TEMPLATE
type: SCIENTIFIC_PRINCIPLE
name: "שם העיקרון המדעי (Scientific Principle)"
domain: FOOD_SCIENCE
category: "THERMODYNAMICS / CHEMICAL_REACTION / PROTEIN / CARBOHYDRATE / EMULSION"
description: "תיאור תמציתי של התהליך המדעי"
conditions:
  temperature_range_c:
    min: 0
    max: 100
  water_activity_aw:
    min: 0.0
    max: 1.0
  ph_range:
    min: 0.0
    max: 14.0
  catalysts: []
effects:
  molecular_change: "תיאור השינוי המולקולרי ברמת החלבון/פחמימה/שומן"
  sensory_consequences:
    taste: []
    aroma: []
    color: "שינוי צבע"
    texture: "שינוי מרקם"
exceptions:
  - "תנאי קצה או חריגים שבהם התהליך אינו מתרחש"
relationships:
  - type: AFFECTS
    target_id: "TEX-TARGET-ID"
    target_name: "מרקם מושפע"
  - type: ENABLES
    target_id: "TEC-TARGET-ID"
    target_name: "טכניקה מאופשרת"
sources:
  - source_id: "SRC-MCGEE-2004"
    citation: "McGee, On Food and Cooking, 2004"
    chapter: "Chapter Name"
    pages: "pp. 100-105"
verification_status: PRELIMINARY # DRAFT / PRELIMINARY / VERIFIED
---

# {{name}}

## מנגנון מדעי מפורט (Scientific Mechanism)
הסבר מעמיק של התהליך הכימי או הפיזיקלי: מה מתרחש ברמה המולקולרית והתאית בעת הבישול.

## תנאי סף וטריגרים (Thresholds & Triggers)
* טמפרטורה מדויקת להתחלת התהליך ולשיאו.
* תפקיד המים, הלחות היחסית וריכוז הסוכרים/מלחים.

## השלכות קולינריות מעשיות (Culinary Implications)
* כיצד שף מיישם או מנצל עיקרון זה בפועל במטבח.
* כיצד מונעים תוצאות לוואי בלתי רצויות.

## מושגים קשורים (Related Concepts)
* [[מושג מדעי מקושר]]
* [[טכניקה תואמת]]

