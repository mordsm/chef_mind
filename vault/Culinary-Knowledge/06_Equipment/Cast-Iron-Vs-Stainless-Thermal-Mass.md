---
id: EQP-PAN-001
type: SCIENTIFIC_PRINCIPLE
name: "מסה תרמית והולכת חום בכלי בישול (Cookware Thermal Mass & Conductivity)"
domain: EQUIPMENT
category: "THERMODYNAMICS"
description: "השפעת עובי הכלי והרכב המתכת (ברזל יצוק, נירוסטה רב-שכבתית, אלומיניום, נחושת) על אגירת חום ואחידות פיזורו"
conditions:
  temperature_range_c:
    min: 20
    max: 260
  water_activity_aw:
    min: 0.0
    max: 1.0
  ph_range:
    min: 2.0
    max: 10.0
  catalysts: ["metal_density", "specific_heat_capacity", "thermal_conductivity_k"]
effects:
  molecular_change: "מסה תרמית גבוהה מונעת נפילת טמפרטורה חדה בעת הנחת מזון קר במחבת"
  sensory_consequences:
    taste: []
    aroma: []
    color: "השחמה אחידה או מקומית בהתאם למוליכות המתכת"
    texture: "קראסט אחיד ללא אזורים מבושלים באדים"
exceptions:
  - "ברזל יצוק לא מצופה עלול להגיב עם רטבים חומציים בבישול ממושך"
relationships:
  - type: ENABLES
    target_id: "TEC-DRY-001"
    target_name: "[[High-Heat-Pan-Searing]]"
  - type: AFFECTS
    target_id: "SCI-HEAT-001"
    target_name: "[[Heat-Transfer]]"
  - type: SUPPORTED_BY
    target_id: "SRC-MODCUIS-2011"
    target_name: "[[SRC-MODCUIS-2011]]"
sources:
  - source_id: "SRC-MODCUIS-2011"
    citation: "Modernist Cuisine, Vol 2: Cookware Materials"
  - source_id: "SRC-FOODLAB-2015"
    citation: "The Food Lab, Chapter 1: Equipment"
verification_status: VERIFIED
---

# מסה תרמית והולכת חום בכלי בישול (Cookware Thermal Mass & Conductivity)

## מנגנון מדעי מפורט (Scientific Mechanism)
* **ברזל יצוק (Cast Iron)**: בעל קיבול חום נפחי (Thermal Mass) גבוה מאוד אך מוליכות תרמית בינונית. דורש חימום מוקדם ממושך, אך שומר על חום גבוה גם כשמניחים עליו נתח בשר קר (`[[High-Heat-Pan-Searing]]`).
* **נירוסטה רב-שכבתית (Clad Stainless Steel)**: משלבת ליבת אלומיניום/נחושת להולכת חום אופקית אחידה עם משטח נירוסטה עמיד לחומצות.
