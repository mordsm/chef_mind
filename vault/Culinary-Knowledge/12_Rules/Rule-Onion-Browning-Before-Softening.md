---
id: RUL-VEG-001
type: CULINARY_RULE
name: "בצל משחים לפני שהתרכך (Onion Browning Before Softening)"
domain: RULES
rule_scope: "DIAGNOSIS"
trigger_conditions:
  food_class: "VEGETABLE"
  observed_problem: "הבצל משחים לפני שהתרכך"
  cooking_phase: "MID_COOKING"
recommended_action:
  action_code: "LOWER_HEAT_ADD_WATER_COVER"
  parameters:
    heat_adjustment: "REDUCE_TO_LOW"
    liquid_addition_ml: 30
    cover_vessel: true
  explanation: "הנמך לחום נמוך, הוסף כף או שתיים של מים וכסה את המחבת ל־2 עד 3 דקות תוך ערבוב עדין."
expected_effects:
  moisture_retention: "INCREASED"
  reaction_rate: "SLOWED"
scientific_rationale: "חום פני שטח גבוה מאדה את הלחות החיצונית של הבצל ומאיץ תגובת מייאר וקרמליזציה בקצוות לפני שהחום מרכך את פנים הגלד."
observations:
  - "הבצל נעשה שקוף ורך יותר והשחמת הקצוות מתמתנת"
safety_notes:
  - "הוסף מים בזהירות למחבת חמה כדי להימנע מהתזה של שמן חם"
tags:
  - "בצל"
  - "השחמה"
  - "ריכוך"
  - "onion"
  - "sweating"
confidence: 85
verified_on: "2026-10-21"
exceptions: []
relationships:
  - type: SUPPORTED_BY
    target_id: "SCI-HEAT-001"
    target_name: "[[Heat-Transfer]]"
  - type: AFFECTS
    target_id: "ING-VEG-001"
    target_name: "[[Allium-Onion-Sulfur-Sugars]]"
sources:
  - source_id: "SRC-MCGEE-2004"
    citation: "McGee, On Food and Cooking, 2004, Chapter 6"
verification_status: VERIFIED
---

# כלל החלטה: בצל משחים לפני שהתרכך (`RUL-VEG-001`)

## הצהרת הכלל (Rule Statement)
**אם** הבצל משחים בקצוות לפני שפנים הגלד התרכך, **אז** יש להנמיך לחום נמוך, להוסיף 1–2 כפות מים ולכסות ל-2–3 דקות, **משום ש**אדי המים מורידים את טמפרטורת פני השטח ל-100°C (עוצרים את `[[Maillard-Reaction]]`) ומעבירים חום כמוס המרכך את פקטין דפנות התא (`[[Allium-Onion-Sulfur-Sugars]]`).
