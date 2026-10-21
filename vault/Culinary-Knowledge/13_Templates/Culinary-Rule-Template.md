---
id: RUL-TEMPLATE
type: CULINARY_RULE
name: "שם הכלל הקולינרי (Rule Name)"
domain: RULES
rule_scope: "COOKING_DECISION / DIAGNOSIS / FOOD_SAFETY / TECHNIQUE_CHOICE"
trigger_conditions:
  food_class: "MEAT / VEGETABLE / STARCH / DAIRY"
  observed_problem: "בצל משחים לפני ריכוך / בשר מתייבש"
  cooking_phase: "MID_COOKING / PREPARATION / FINISHING"
recommended_action:
  action_code: "LOWER_HEAT_AND_COVER"
  parameters:
    heat_adjustment: "REDUCE_TO_LOW"
    liquid_addition_ml: 30
    cover_vessel: true
  explanation: "הסבר ההמלצה התפעולית"
expected_effects:
  moisture_retention: "INCREASED"
  reaction_rate: "SLOWED"
scientific_rationale: "קישור לעיקרון מדעי המסביר מדוע הפעולה עובדת"
exceptions:
  - "כאשר המטרה היא קצוות פריכים מובהקים"
relationships:
  - type: SUPPORTED_BY
    target_id: "SCI-HEAT-001"
    target_name: "מעבר חום"
  - type: AFFECTS
    target_id: "TEX-CRUST-001"
    target_name: "קראסט"
sources:
  - source_id: "SRC-CHEF-CURATED"
    citation: "Chef Core Experimental Protocol"
verification_status: VERIFIED # DRAFT / PRELIMINARY / VERIFIED
---

# {{name}}

## הצהרת הכלל (Rule Statement)
**אם** [מתקיימים תנאי X], **אז** [יש לבצע פעולה Y], **משום ש** [הסבר תרמודינמי/כימי Z].

## מצבי יישום תפעוליים (Operating Context)
פירוט התרחיש המעשי במטבח שבו מנוע השף יפעיל כלל זה.

## חריגים ומגבלות (Exceptions)
מצבים שבהם אסור להפעיל את הכלל למרות קיום הטריגר.

