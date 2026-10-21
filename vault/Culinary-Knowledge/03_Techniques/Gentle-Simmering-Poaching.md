---
id: TEC-MOIST-001
type: COOKING_TECHNIQUE
name: "בישול עדין ובעבוע מבוקר (Gentle Simmering & Poaching)"
domain: TECHNIQUES
heat_environment: "MOIST"
heat_transfer_methods:
  - "CONVECTION"
recommended_equipment:
  - "סיר בעל תחתית עבה ומדחום נוזלים"
target_foods:
  - "ביצים וקרמים"
  - "דגים עדינים"
  - "קורקבנים, מרקים, קטניות ודגנים"
conditions:
  surface_temperature_min_c: 80
  cooking_medium: "WATER"
  duration_range: "Variable by ingredient"
effects:
  primary_outcome: "העברת חום אחידה ומתונה ללא פירוק מכני מאגרסיביות בועות הרתיחה"
  texture_change: "UNIFORM_TENDER_SET"
  moisture_loss_pct_estimate: 8.0
exceptions:
  - "אינו מייצר השחמת מייאר או קראסט פריך עקב מחסום ה-100°C של המים"
relationships:
  - type: REQUIRES
    target_id: "SCI-HEAT-001"
    target_name: "[[Heat-Transfer]]"
  - type: AFFECTS
    target_id: "SCI-PROT-002"
    target_name: "[[Protein-Denaturation-Coagulation]]"
  - type: INHIBITS
    target_id: "TEX-CRUST-001"
    target_name: "[[Surface-Browning]]"
sources:
  - source_id: "SRC-MCGEE-2004"
    citation: "McGee, On Food and Cooking, 2004, Chapter 14"
verification_status: VERIFIED
---

# בישול עדין ובעבוע מבוקר (Gentle Simmering & Poaching)

## תיאור הטכניקה (Overview)
בישול בנוזל בטמפרטורה מתחת לנקודת הרתיחה הסוערת (Poaching: 70°C–82°C; Simmering: 85°C–94°C). מונע התפרקות מכנית של חלבונים עדינים (כגון דגים וביצים) ומאפשר מיצוי טעמים צלול בצירים.
