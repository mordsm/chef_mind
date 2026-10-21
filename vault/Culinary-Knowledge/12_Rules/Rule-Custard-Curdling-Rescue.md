---
id: RUL-EGG-001
type: CULINARY_RULE
name: "עצירת התגבנות בקרם ביצים (Custard Curdling Rescue)"
domain: RULES
rule_scope: "DIAGNOSIS"
trigger_conditions:
  food_class: "DAIRY"
  observed_problem: "קרם הביצים מתחיל להתגבן"
  cooking_phase: "MID_COOKING"
recommended_action:
  action_code: "STOP_HEAT_IMMEDIATELY"
  parameters:
    heat_adjustment: "REMOVE_FROM_HEAT"
    liquid_addition_ml: 0
    cover_vessel: false
  explanation: "עצור מיד את חימום הקרם, הסר ממקור החום ובדוק את מידת ההתגבנות לפני שממשיכים."
expected_effects:
  moisture_retention: "PRESERVED"
  reaction_rate: "HALTED"
scientific_rationale: "חימום יתר של תערובת ביצים וחלב מעבר ל־83°C גורם לקרישת יתר של חלבוני הביצה ולהפרדת נוזלים (Syneresis)."
observations:
  - "דווח אם מופיעים גרגירים או הפרדת נוזל בקרם"
safety_notes:
  - "הפסקת החימום מונעת המשך התגבנות; מרקם לבדו אינו מוכיח שהביצים עברו פסטור מלא"
tags:
  - "קרם"
  - "ביצים"
  - "התגבנות"
  - "custard"
  - "curdling"
confidence: 85
verified_on: "2026-10-21"
exceptions: []
relationships:
  - type: SUPPORTED_BY
    target_id: "SCI-PROT-002"
    target_name: "[[Protein-Denaturation-Coagulation]]"
  - type: SUPPORTED_BY
    target_id: "SRC-BCCAMPUS-PASTRY-2015"
    target_name: "[[SRC-BCCAMPUS-PASTRY-2015]]"
sources:
  - source_id: "SRC-BCCAMPUS-PASTRY-2015"
    citation: "BCcampus, Modern Pastry and Plated Dessert Techniques, 2015, Coagulation"
verification_status: VERIFIED
---

# כלל החלטה: עצירת התגבנות בקרם ביצים (`RUL-EGG-001`)

## הצהרת הכלל (Rule Statement)
**אם** קרם הביצים מראה סימני התגבנות ראשונים, **אז** יש להסיר מיד ממקור החום ולעצור את עליית הטמפרטורה, **משום ש**דנטורציית יתר של חלבוני הביצה (`[[Protein-Denaturation-Coagulation]]`) מכווצת את הרשת החלבונית ופולטת מים באופן בלתי הפיך.
