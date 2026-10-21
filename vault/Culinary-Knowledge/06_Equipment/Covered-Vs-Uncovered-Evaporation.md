---
id: EQP-ENV-001
type: SCIENTIFIC_PRINCIPLE
name: "בקרת אידוי ולחות: סיר מכוסה מול פתוח (Covered vs. Uncovered Evaporation Control)"
domain: EQUIPMENT
category: "THERMODYNAMICS"
description: "שליטה בלחץ האדים החלקי, בריכוז הנוזלים ובקצב העברת החום באמצעות פתיחה או סגירה של מכסה כלי הבישול"
conditions:
  temperature_range_c:
    min: 70
    max: 100
  water_activity_aw:
    min: 0.60
    max: 1.0
  ph_range:
    min: 3.0
    max: 9.0
  catalysts: ["lid_seal", "steam_condensation"]
effects:
  molecular_change: "סיר מכוסה לוכד קיטור ומחזיר חום כמוס במעגל עיבוי; סיר פתוח מאפשר אידוי מים וריכוז מומסים (Reduction)"
  sensory_consequences:
    taste: ["CONCENTRATED_FLAVOR_WHEN_UNCOVERED"]
    aroma: []
    color: []
    texture: "שמירה על לחות בסיר מכוסה מול הסמכת רוטב או שמירת פריכות בסיר פתוח"
exceptions:
  - "כיסוי מזון פריך לאחר צריבה הורס את הקראסט עקב עיבוי אדים"
relationships:
  - type: AFFECTS
    target_id: "TEX-VISC-001"
    target_name: "[[Starch-And-Emulsion-Viscosity]]"
  - type: INHIBITS
    target_id: "TEX-CRUST-001"
    target_name: "[[Surface-Browning]]"
  - type: SUPPORTED_BY
    target_id: "SRC-MODCUIS-2011"
    target_name: "[[SRC-MODCUIS-2011]]"
sources:
  - source_id: "SRC-MODCUIS-2011"
    citation: "Modernist Cuisine, Vol 1: Heat and Water"
verification_status: VERIFIED
---

# בקרת אידוי ולחות: סיר מכוסה מול פתוח (Covered vs. Uncovered Evaporation Control)

## השלכות קולינריות מעשיות (Culinary Implications)
* **מתי לכסות**: כאשר המטרה היא ריכוך ללא השחמה או אובדן נוזלים (כמו בריכוך בצל שהשחים מוקדם מדי `[[Rule-Onion-Browning-Before-Softening]]`, או בבישול ארוך `[[Low-Slow-Braising]]`).
* **מתי לבשל פתוח**: כאשר רוצים לרכז רוטב דליל (`[[Sauce-Texture-Correction-Matrix]]`) או לאפשר לאדים להתנדף בזמן צריבה (`[[High-Heat-Pan-Searing]]`).
