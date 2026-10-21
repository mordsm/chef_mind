---
id: RUL-TEC-001
type: CULINARY_RULE
name: "מניעת צפיפות יתר במחבת בזמן צריבה (Pan Crowding Steam Inhibition Rule)"
domain: RULES
rule_scope: "COOKING_DECISION"
trigger_conditions:
  food_class: "MEAT"
  observed_problem: "המחבת עמוסה והמזון מפריש נוזלים במקום להשחים"
  cooking_phase: "MID_COOKING"
recommended_action:
  action_code: "SEAR_IN_BATCHES_DRY_SURFACE"
  parameters:
    heat_adjustment: "HIGH_PREHEATED"
    liquid_addition_ml: 0
    cover_vessel: false
  explanation: "חלק את המזון לנגלות עם מרווח בין הנתחים וייבש את שטח הפנים לפני ההכנסה למחבת כדי לאפשר לאדים להתנדף."
expected_effects:
  moisture_retention: "CRISP_SURFACE"
  reaction_rate: "MAILLARD_ACCELERATED"
scientific_rationale: "צפיפות יתר במחבת מפילה את טמפרטורת המתכת וכולאת אדי מים, מה שמגביל את טמפרטורת פני השטח ל־100°C ומונע תגובת מייאר (140°C+)."
observations:
  - "בדוק ודווח אם הנוזלים מתאדים ומתחילה השחמה זהובה-חומה בשטח הפנים"
safety_notes:
  - "אל תכניס נייר סופג למחבת חמה או לשמן חם; ייבש את המזון רק מחוץ למחבת"
tags:
  - "צריבה"
  - "מחבת"
  - "צפיפות"
  - "השחמה"
  - "מייאר"
  - "searing"
  - "crowding"
confidence: 88
verified_on: "2026-10-21"
exceptions: []
relationships:
  - type: SUPPORTED_BY
    target_id: "SCI-HEAT-001"
    target_name: "[[Heat-Transfer]]"
  - type: SUPPORTED_BY
    target_id: "SCI-CHEM-001"
    target_name: "[[Maillard-Reaction]]"
  - type: AFFECTS
    target_id: "TEX-CRUST-001"
    target_name: "[[Surface-Browning]]"
sources:
  - source_id: "SRC-MODCUIS-2011"
    citation: "Modernist Cuisine, Vol 2: Traditional Cooking"
  - source_id: "SRC-FOODLAB-2015"
    citation: "The Food Lab, Chapter 3"
verification_status: VERIFIED
---

# כלל החלטה: מניעת צפיפות יתר במחבת בזמן צריבה (`RUL-TEC-001`)

## הצהרת הכלל (Rule Statement)
**אם** המטרה היא השחמה (`[[Surface-Browning]]`) והמחבת עמוסה בחומרי גלם המפרישים נוזלים, **אז** יש לעבוד בנגלות עם מרווח בין הנתחים ולייבש את שטח הפנים מראש, **משום ש**אדים כלואים ונפילת מסה תרמית (`[[Cast-Iron-Vs-Stainless-Thermal-Mass]]`) נועלים את הטמפרטורה על 100°C ומונעים את `[[Maillard-Reaction]]`.
