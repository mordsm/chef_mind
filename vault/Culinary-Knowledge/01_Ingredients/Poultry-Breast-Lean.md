---
id: ING-POUL-001
type: INGREDIENT
name: "חזה עוף והודו רזה (Lean Poultry Breast)"
domain: INGREDIENTS
category: "חלבון מן החי"
composition:
  water_pct: 74.0
  protein_pct: 23.0
  fat_pct: 1.5
  carb_pct: 0.0
  ph_level: 5.9
physical_properties:
  density_g_cm3: 1.04
  thermal_conductivity: "MEDIUM"
  cellular_structure: "סיבי שריר לבנים עדינים ודלי קולגן ושומן תוך-שרירי"
sensory_profile:
  dominant_taste: ["MILD_UMAMI"]
  aroma_compounds: ["aldehydes", "lactones"]
  raw_texture: "TENDER_SOFT"
storage_and_safety:
  shelf_life_days_refrigerated: 2
  minimum_internal_temp_c: 74.0
  allergens: []
  kashrut_class: "MEAT"
relationships:
  - type: AFFECTS
    target_id: "SCI-PROT-002"
    target_name: "[[Protein-Denaturation-Coagulation]]"
  - type: REQUIRES
    target_id: "SAF-TEMP-001"
    target_name: "[[Minimum-Internal-Temperatures]]"
  - type: SUPPORTED_BY
    target_id: "SRC-USDA-FSIS-2024"
    target_name: "[[SRC-USDA-FSIS-2024]]"
sources:
  - source_id: "SRC-USDA-FSIS-2024"
    citation: "USDA FSIS Safe Minimum Internal Temperature Chart"
  - source_id: "SRC-MCGEE-2004"
    citation: "McGee, On Food and Cooking, 2004, Chapter 3"
verification_status: VERIFIED
---

# חזה עוף והודו רזה (Lean Poultry Breast)

## תיאור כללי (Description)
נתח חלבון רזה במיוחד המתאפיין באחוז שומן נמוך מאוד (1%–2%) ומיעוט רקמת חיבור.

## התנהגות בבישול (Cooking Behavior)
* **רגישות לייבוש**: מאחר שאין שומן תוך-שרירי או ג'לטין שיפצו על דחיסת סיבי האקטין (מעל 66°C), בישול יתר מעבר לסף הבטיחות גורם להתייבשות מהירה.
* **דרישת בטיחות מחייבת**: עקב סיכון לסלמונלה וקמפילובקטר, נדרשת מדידת ליבה של לפחות **74°C** בחלק העבה ביותר (`[[Rule-Poultry-Safe-Core-Temperature]]`).
