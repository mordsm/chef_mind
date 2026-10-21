---
id: ING-EGG-001
type: INGREDIENT
name: "ביצת תרנגולת — חלבון וחלמון (Chicken Egg)"
domain: INGREDIENTS
category: "חלבון מן החי"
composition:
  water_pct: 76.0
  protein_pct: 12.5
  fat_pct: 10.0
  carb_pct: 0.7
  ph_level: 7.6
physical_properties:
  density_g_cm3: 1.03
  thermal_conductivity: "LOW_TO_MEDIUM"
  cellular_structure: "תמיסת חלבונים גלובולריים (אלבומין) ותחליב ליפו-פרוטאינים ולציטין (חלמון)"
sensory_profile:
  dominant_taste: ["SAVORY", "RICH"]
  aroma_compounds: ["hydrogen_sulfide_if_overcooked"]
  raw_texture: "VISCOUS_LIQUID"
storage_and_safety:
  shelf_life_days_refrigerated: 28
  minimum_internal_temp_c: 71.0
  allergens: ["eggs"]
  kashrut_class: "PAREVE"
relationships:
  - type: ENABLES
    target_id: "SCI-PROT-002"
    target_name: "[[Protein-Denaturation-Coagulation]]"
  - type: ENABLES
    target_id: "SCI-CHEM-002"
    target_name: "[[Caramelization-And-Emulsification]]"
  - type: SUPPORTED_BY
    target_id: "SRC-BCCAMPUS-PASTRY-2015"
    target_name: "[[SRC-BCCAMPUS-PASTRY-2015]]"
sources:
  - source_id: "SRC-BCCAMPUS-PASTRY-2015"
    citation: "BCcampus, Modern Pastry and Plated Dessert Techniques, 2015, Coagulation"
  - source_id: "SRC-MCGEE-2004"
    citation: "McGee, On Food and Cooking, 2004, Chapter 2"
verification_status: VERIFIED
---

# ביצת תרנגולת — חלבון וחלמון (Chicken Egg)

## תיאור כללי (Description)
מערכת ביוכימית דו-שכבתית: החלבון (Albumen) מכיל כ-88% מים וכ-11% חלבונים (אובטרנספרין, אובלבומין), ואילו החלמון (Yolk) מכיל כ-50% מים, 30% שומן ולציטין, ו-16% חלבון.

## התנהגות בבישול (Cooking Behavior)
* **מדרגות קרישה**: החלבון מתחיל להיאטם ב-60°C–62°C ומתייצב ב-65°C, בעוד החלמון מסמיך ב-65°C–70°C.
* **בקרמים ורטבים (`[[Rule-Custard-Curdling-Rescue]]`)**: דילול בחלב או שמנת מעלה את טמפרטורת הקרישה ל-79°C–83°C, אך חציית סף של 85°C גורמת להתגבנות (Curdling) ולהפרדת מים (Syneresis).
