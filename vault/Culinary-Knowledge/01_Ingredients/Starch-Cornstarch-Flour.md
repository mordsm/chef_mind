---
id: ING-STR-001
type: INGREDIENT
name: "עמילן תירס וחיטה — עמילוז ועמילופקטין (Food Starches)"
domain: INGREDIENTS
category: "דגן"
composition:
  water_pct: 10.0
  protein_pct: 0.5
  fat_pct: 0.1
  carb_pct: 89.0
  ph_level: 6.5
physical_properties:
  density_g_cm3: 1.5
  thermal_conductivity: "LOW"
  cellular_structure: "גרנולות חצי-גבישיות הבנויות משרשראות עמילוז קוויות ועמילופקטין מסועף"
sensory_profile:
  dominant_taste: ["NEUTRAL"]
  aroma_compounds: []
  raw_texture: "POWDERY_CHALKY"
storage_and_safety:
  shelf_life_days_refrigerated: 365
  minimum_internal_temp_c: null
  allergens: []
  kashrut_class: "PAREVE"
relationships:
  - type: ENABLES
    target_id: "SCI-CARB-001"
    target_name: "[[Starch-Gelatinization-Retrogradation]]"
  - type: ENABLES
    target_id: "TEX-VISC-001"
    target_name: "[[Starch-And-Emulsion-Viscosity]]"
  - type: SUPPORTED_BY
    target_id: "SRC-BCCAMPUS-PASTRY-2015"
    target_name: "[[SRC-BCCAMPUS-PASTRY-2015]]"
sources:
  - source_id: "SRC-BCCAMPUS-PASTRY-2015"
    citation: "BCcampus, Modern Pastry and Plated Dessert Techniques, 2015, Gelatinization"
verification_status: VERIFIED
---

# עמילן תירס וחיטה — עמילוז ועמילופקטין (Food Starches)

## תיאור כללי (Description)
גרנולות רב-סוכר המשמשות להסמכת רטבים, מרקים וקרמים (`[[Starch-And-Emulsion-Viscosity]]`). קורנפלור הוא עמילן שורש/זרע טהור ללא גלוטן, בעוד קמח חיטה מכיל גם חלבוני גלוטן (אלרגן חיטה).

## התנהגות בבישול (Cooking Behavior)
* **חובת פיזור מוקדם (`[[Rule-Starch-Slurry-Dispersion]]`)**: הוספת עמילן יבש ישירות לנוזל חם גורמת לג'לטיניזציה מיידית של המעטפת החיצונית וכליאת אבקה יבשה במרכז (גושים). יש לפזר בנוזל קר (Slurry) או בשומן (Roux) לפני ההוספה.
