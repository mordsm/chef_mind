---
id: RUL-SAUCE-001
type: CULINARY_RULE
name: "פיזור עמילן בנוזל קר למניעת גושים (Starch Slurry Cold Dispersion)"
domain: RULES
rule_scope: "COOKING_DECISION"
trigger_conditions:
  food_class: "STARCH"
  observed_problem: "מסמיכים רוטב בקורנפלור"
  cooking_phase: "FINISHING"
recommended_action:
  action_code: "DISPERSE_IN_COLD_LIQUID_FIRST"
  parameters:
    heat_adjustment: "GENTLE_SIMMER"
    liquid_addition_ml: 30
    cover_vessel: false
  explanation: "ערבב את הקורנפלור עם מעט נוזל קר עד להמסה מלאה (Slurry), והוסף לרוטב המבעבע בעדינות תוך טריפה."
expected_effects:
  moisture_retention: "STABLE_GEL"
  reaction_rate: "UNIFORM_GELATINIZATION"
scientific_rationale: "הפרדת גרנולות העמילן בנוזל קר לפני החשיפה לחום מונעת ג'לטיניזציה מיידית של המעטפת וכליאת גושים יבשים."
observations:
  - "בדוק ודווח אם הרוטב נעשה אחיד, מבריק וסמיך ללא גושים"
safety_notes:
  - "היזהר מהתזה של נוזל חם בזמן הטריפה; סמיכות הרוטב אינה בדיקת בטיחות מזון"
tags:
  - "קורנפלור"
  - "עמילן"
  - "רוטב"
  - "גושים"
  - "הסמכה"
  - "starch"
  - "slurry"
confidence: 90
verified_on: "2026-10-21"
required_ingredients:
  - "קורנפלור"
exceptions: []
relationships:
  - type: SUPPORTED_BY
    target_id: "SCI-CARB-001"
    target_name: "[[Starch-Gelatinization-Retrogradation]]"
  - type: SUPPORTED_BY
    target_id: "SRC-BCCAMPUS-PASTRY-2015"
    target_name: "[[SRC-BCCAMPUS-PASTRY-2015]]"
sources:
  - source_id: "SRC-BCCAMPUS-PASTRY-2015"
    citation: "BCcampus, Modern Pastry and Plated Dessert Techniques, 2015, Gelatinization"
verification_status: VERIFIED
---

# כלל החלטה: פיזור עמילן בנוזל קר למניעת גושים (`RUL-SAUCE-001`)

## הצהרת הכלל (Rule Statement)
**אם** נדרשת הסמכת רוטב חם באמצעות קורנפלור (`[[Starch-Cornstarch-Flour]]`), **אז** חובה לטרוף את הקורנפלור בנוזל קר תחילה ורק אז להוסיפו לרוטב המבעבע, **משום ש**פיזור מוקדם מאפשר ג'לטיניזציה אחידה של כל גרנולה (`[[Starch-Gelatinization-Retrogradation]]`).
