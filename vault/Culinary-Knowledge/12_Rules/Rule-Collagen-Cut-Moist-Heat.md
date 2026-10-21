---
id: RUL-MEAT-001
type: CULINARY_RULE
name: "התאמת חום לח לנתחים עתירי קולגן (Collagen-Rich Cut Moist Heat Rule)"
domain: RULES
rule_scope: "TECHNIQUE_CHOICE"
trigger_conditions:
  food_class: "MEAT"
  observed_problem: "הנתח זוהה כעשיר ברקמת חיבור ומתאים לבישול לח"
  cooking_phase: "PREPARATION"
recommended_action:
  action_code: "SELECT_MOIST_SLOW_COOKING"
  parameters:
    heat_adjustment: "SIMMER_85_92C"
    liquid_addition_ml: 250
    cover_vessel: true
  explanation: "אמת את שם הנתח ובחר בישול ממושך בנוזל (צלי קדרה, בישול בסיר מכוסה או סיר לחץ) לפירוק הקולגן לג'לטין."
expected_effects:
  moisture_retention: "INCREASED"
  reaction_rate: "COLLAGEN_HYDROLYSIS_ENABLED"
scientific_rationale: "שרירים עובדים כמו כתף, שוק וקורקבנים עשירים בקולגן הדורש חום לח וזמן להידרוליזה לג'לטין רך."
observations:
  - "בדוק ודווח על שינוי ברכות הנתח; רכות לבדה אינה בדיקת בטיחות"
safety_notes:
  - "יש לאמת טמפרטורת ליבה בטוחה במדחום לפי סוג הבשר (74°C בעוף/קורקבנים, 63°C עם מנוחה בנתח בקר שלם)"
tags:
  - "קולגן"
  - "רקמת חיבור"
  - "ריכוך"
  - "קורקבנים"
  - "כתף"
  - "collagen"
  - "braise"
confidence: 90
verified_on: "2026-10-21"
exceptions: []
relationships:
  - type: SUPPORTED_BY
    target_id: "SCI-PROT-001"
    target_name: "[[Collagen-Hydrolysis-Gelatin]]"
  - type: SUPPORTED_BY
    target_id: "SRC-BCCAMPUS-MEAT-2015"
    target_name: "[[SRC-BCCAMPUS-MEAT-2015]]"
sources:
  - source_id: "SRC-BCCAMPUS-MEAT-2015"
    citation: "BCcampus, Meat Cutting and Processing for Food Service, 2015"
verification_status: VERIFIED
---

# כלל החלטה: התאמת חום לח לנתחים עתירי קולגן (`RUL-MEAT-001`)

## הצהרת הכלל (Rule Statement)
**אם** חומר הגלם הוא שריר עובד עשיר בקולגן (`[[Beef-Chuck-Collagen-Rich]]`, קורקבנים, כתף, שוק), **אז** יש לבחור בישול ממושך בנוזל (`[[Low-Slow-Braising]]`) ולהימנע מצלייה יבשה קצרה, **משום ש**פירוק הקולגן לג'לטין (`[[Collagen-Hydrolysis-Gelatin]]`) דורש מים וזמן.
