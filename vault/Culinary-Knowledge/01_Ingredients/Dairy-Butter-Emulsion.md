---
id: ING-DAI-001
type: INGREDIENT
name: "חמאה ושמנת — תחליבי שומן ומוצקי חלב (Butter & Dairy Cream)"
domain: INGREDIENTS
category: "מוצר חלב"
composition:
  water_pct: 16.0
  protein_pct: 1.0
  fat_pct: 82.0
  carb_pct: 0.8
  ph_level: 6.4
physical_properties:
  density_g_cm3: 0.91
  thermal_conductivity: "LOW"
  cellular_structure: "תחליב מים-בשמן (חמאה) או שמן-במים (שמנת) עם כדוריות שומן עטופות ממברנה"
sensory_profile:
  dominant_taste: ["RICH", "SWEET", "CREAMY"]
  aroma_compounds: ["diacetyl", "lactones", "butyric_acid"]
  raw_texture: "PLASTIC_SOLID_OR_CREAM"
storage_and_safety:
  shelf_life_days_refrigerated: 30
  minimum_internal_temp_c: null
  allergens: ["milk"]
  kashrut_class: "DAIRY"
relationships:
  - type: ENABLES
    target_id: "SCI-CHEM-001"
    target_name: "[[Maillard-Reaction]]"
  - type: ENABLES
    target_id: "TEX-VISC-001"
    target_name: "[[Starch-And-Emulsion-Viscosity]]"
sources:
  - source_id: "SRC-MCGEE-2004"
    citation: "McGee, On Food and Cooking, 2004, Chapter 1"
verification_status: VERIFIED
---

# חמאה ושמנת — תחליבי שומן ומוצקי חלב (Butter & Dairy Cream)

## תיאור כללי (Description)
חמאה היא תחליב מים-בשמן המכיל כ-82% שומן חלב, 16% מים וכ-2% מוצקי חלב (חלבוני קזאין ומי גבינה + סוכר לקטוז).

## התנהגות בבישול (Cooking Behavior)
* **המסה ואידוי**: ב-32°C–35°C השומן נמס; ב-100°C המים מתאדים בבעבוע.
* **חמאה חומה (Beurre Noisette) מול שריפה**: ב-120°C–140°C מוצקי החלב והלקטוז עוברים `[[Maillard-Reaction]]` ויוצרים ארומה אגוזית, אך מעל 165°C מוצקי החלב נשרפים במהירות.
* **בטיחות וכשרות**: מכיל אלרגן חלב (`milk`) וחלבי (`DAIRY`) — חסום לשילוב עם בשר בפרופיל השומר על הפרדת בשר וחלב.
