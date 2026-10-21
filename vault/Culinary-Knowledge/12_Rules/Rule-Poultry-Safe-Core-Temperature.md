---
id: RUL-SAF-001
type: CULINARY_RULE
name: "אימות טמפרטורת ליבה בעוף ובשר במדחום (Safe Core Temperature Verification)"
domain: RULES
rule_scope: "FOOD_SAFETY"
trigger_conditions:
  food_class: "MEAT"
  observed_problem: "יש מדחום מזון מתאים ויודעים מהו סוג הבשר"
  cooking_phase: "FINISHING"
recommended_action:
  action_code: "MEASURE_THICKEST_PART_CORE"
  parameters:
    heat_adjustment: "MAINTAIN_UNTIL_SAFE_THRESHOLD"
    liquid_addition_ml: 0
    cover_vessel: false
  explanation: "מדוד בחלק העבה ביותר של הבשר או העוף, הרחק מעצם, שומן וסחוס, והשווה לסף הבטוח (74°C לעוף/קורקבנים, 71°C לבשר טחון, 63°C עם 3 דקות מנוחה לנתח בקר שלם)."
expected_effects:
  moisture_retention: "OPTIMAL_WITHOUT_OVERCOOKING"
  reaction_rate: "PATHOGEN_LOG_REDUCTION"
scientific_rationale: "צבע הבשר וצבע המיצים אינם מדדים אמינים להשמדת פתוגנים; רק מדידה במרכז התרמי של החלק העבה מאמתת הגעה לסף הבטיחות."
observations:
  - "דווח את סוג הבשר ואת הטמפרטורה הנמוכה ביותר שנמדדה בחלקים העבים"
safety_notes:
  - "אין לאשר שהבשר או העוף בטוחים להגשה ללא מדידת טמפרטורה שעומדת בסף של סוג החלבון"
tags:
  - "מדחום"
  - "טמפרטורה"
  - "בטיחות"
  - "עוף"
  - "בשר"
  - "thermometer"
  - "safety"
confidence: 95
verified_on: "2026-10-21"
exceptions: []
relationships:
  - type: SUPPORTED_BY
    target_id: "SAF-TEMP-001"
    target_name: "[[Minimum-Internal-Temperatures]]"
  - type: SUPPORTED_BY
    target_id: "EQP-SENS-001"
    target_name: "[[Core-Probe-Thermometry]]"
  - type: SUPPORTED_BY
    target_id: "SRC-USDA-FSIS-2024"
    target_name: "[[SRC-USDA-FSIS-2024]]"
sources:
  - source_id: "SRC-USDA-FSIS-2024"
    citation: "USDA FSIS Food Thermometers & Safe Minimum Internal Temperature Chart"
verification_status: VERIFIED
---

# כלל החלטה: אימות טמפרטורת ליבה בעוף ובשר במדחום (`RUL-SAF-001`)

## הצהרת הכלל (Rule Statement)
**אם** בודקים מוכנות של עוף, הודו, קורקבנים, בשר או דג, **אז** יש למדוד במדחום מזון בחלק העבה ביותר הרחק מעצם ושומן (`[[Core-Probe-Thermometry]]`), **משום ש**צבע וזמן אינם מאמתים השמדת פתוגנים לפי תקן `[[SRC-USDA-FSIS-2024]]`.
