---
id: ING-MEAT-001
type: INGREDIENT
name: "נתחי שריר עתירי קולגן (כתף, שוק, קורקבנים)"
domain: INGREDIENTS
category: "חלבון מן החי"
composition:
  water_pct: 71.0
  protein_pct: 21.0
  fat_pct: 7.0
  carb_pct: 0.0
  ph_level: 5.6
physical_properties:
  density_g_cm3: 1.05
  thermal_conductivity: "MEDIUM"
  cellular_structure: "סיבי שריר עבים העטופים ברשת צפופה של רקמת חיבור (קולגן ואלסטין)"
sensory_profile:
  dominant_taste: ["UMAMI", "SAVORY"]
  aroma_compounds: ["thiazoles", "thiophenes"]
  raw_texture: "TOUGH_FIBROUS"
storage_and_safety:
  shelf_life_days_refrigerated: 3
  minimum_internal_temp_c: 63.0
  allergens: []
  kashrut_class: "MEAT"
relationships:
  - type: REQUIRES
    target_id: "SCI-PROT-001"
    target_name: "[[Collagen-Hydrolysis-Gelatin]]"
  - type: ENABLES
    target_id: "TEX-TEND-001"
    target_name: "[[Collagen-Driven-Tenderness]]"
  - type: SUPPORTED_BY
    target_id: "SRC-BCCAMPUS-MEAT-2015"
    target_name: "[[SRC-BCCAMPUS-MEAT-2015]]"
sources:
  - source_id: "SRC-BCCAMPUS-MEAT-2015"
    citation: "BCcampus, Meat Cutting and Processing for Food Service, 2015"
  - source_id: "SRC-MCGEE-2004"
    citation: "McGee, On Food and Cooking, 2004, Chapter 3"
verification_status: VERIFIED
---

# נתחי שריר עתירי קולגן (Collagen-Rich Working Muscles)

## תיאור כללי (Description)
נתחים שמקורם בשרירים עובדים הנושאים משקל או מבצעים פעולה מתמדת (כגון כתף בקר, שוק/אוסובוקו, אסאדו, צוואר וקורקבני עוף). שרירים אלו מתאפיינים במעטפת עבה של רקמת חיבור חלבונית מסוג קולגן.

## התנהגות בבישול (Cooking Behavior)
* **חום יבש ומהיר**: גורם להתכווצות סיבי השריר ולאיבוד נוזלים עוד לפני שהקולגן מספיק להתפרק, מה שמניב מרקם קשה וסיבי.
* **חום רטוב וממושך (`[[Low-Slow-Braising]]`)**: בנוכחות מים ובטמפרטורה מעל 68°C לאורך זמן, סלילי הקולגן עוברים הידרוליזה לג'לטין (`[[Collagen-Hydrolysis-Gelatin]]`), המעניק עסיסיות ומרקם נימוח (`[[Collagen-Driven-Tenderness]]`).
* **הבחנה בין בטיחות למרקם**: סף הבטיחות המיקרוביאלי (63°C בבקר שלם עם מנוחה, 74°C בעוף/קורקבנים) מושג זמן רב לפני שהנתח מתרכך קולינרית.
