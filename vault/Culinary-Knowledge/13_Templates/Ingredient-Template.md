---
id: ING-TEMPLATE
type: INGREDIENT
name: "שם חומר הגלם (Ingredient Name)"
domain: INGREDIENTS
category: "חלבון מן החי / ירק / דגן / שומן / מוצר חלב"
composition:
  water_pct: 0.0
  protein_pct: 0.0
  fat_pct: 0.0
  carb_pct: 0.0
  ph_level: 7.0
physical_properties:
  density_g_cm3: 1.0
  thermal_conductivity: "MEDIUM"
  cellular_structure: "תאי צמחי / סיבי שריר"
sensory_profile:
  dominant_taste: ["UMAMI", "SWEET"]
  aroma_compounds: []
  raw_texture: "FIRM"
storage_and_safety:
  shelf_life_days_refrigerated: 3
  minimum_internal_temp_c: null
  allergens: []
  kashrut_class: "PAREVE" # MEAT / DAIRY / PAREVE
relationships:
  - type: IS_A
    target_id: "ING-CATEGORY-ID"
    target_name: "שם הקטגוריה"
  - type: PAIRS_WELL_WITH
    target_id: "ING-OTHER-ID"
    target_name: "שם חומר גלם משלים"
sources:
  - source_id: "SRC-USDA-FOODDATA"
    citation: "USDA FoodData Central"
verification_status: DRAFT # DRAFT / PRELIMINARY / VERIFIED
---

# {{name}}

## תיאור כללי (Description)
תיאור תמציתי ומדויק של חומר הגלם, מקורו ומאפייניו הבוטניים או הזואולוגיים.

## התנהגות בבישול (Cooking Behavior)
* **חום יבש**: כיצד המזון מגיב לצריבה, צלייה או אפייה.
* **חום רטוב**: פירוק רקמות, הפרשת עמילן או ג'לטין.
* **רגישות תרמית**: נקודות שבירה, התייבשות או איבוד צבע.

## שידוכי טעמים מובילים (Flavor Pairings)
* [[מרכיב משלים 1]]
* [[מרכיב משלים 2]]

## שגיאות נפוצות ואזהרות (Common Pitfalls)
* מה עלול להשתבש בטיפול שגוי בחומר הגלם.

