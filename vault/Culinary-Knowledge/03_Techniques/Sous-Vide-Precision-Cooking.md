---
id: TEC-PREC-001
type: COOKING_TECHNIQUE
name: "בישול סו-וויד מבוקר טמפרטורה (Sous-Vide Precision Cooking)"
domain: TECHNIQUES
heat_environment: "PRECISION"
heat_transfer_methods:
  - "CONVECTION"
  - "CONDUCTION"
recommended_equipment:
  - "סירקולטור תרמי מדויק ושקית אטומה בוואקום"
target_foods:
  - "נתחי בקר, עוף, דגים וביצים"
conditions:
  surface_temperature_min_c: 54
  cooking_medium: "WATER"
  duration_range: "60 minutes to 48 hours (requires validated time-temperature schedule)"
effects:
  primary_outcome: "שיווי משקל תרמי מדויק בכל עובי הנתח ללא גרדיאנט בישול-יתר חיצוני"
  texture_change: "EDGE_TO_EDGE_UNIFORM_TENDERNESS"
  moisture_loss_pct_estimate: 5.0
exceptions:
  - "מדידת טמפרטורה בודדת אינה מאמתת פסטור בסו-וויד; נדרשת טבלת זמן-טמפרטורה ועובי מאומתת"
relationships:
  - type: REQUIRES
    target_id: "SAF-TEMP-001"
    target_name: "[[Minimum-Internal-Temperatures]]"
  - type: ALTERNATIVE_TO
    target_id: "TEC-COMB-001"
    target_name: "[[Low-Slow-Braising]]"
  - type: SUPPORTED_BY
    target_id: "SRC-MODCUIS-2011"
    target_name: "[[SRC-MODCUIS-2011]]"
sources:
  - source_id: "SRC-MODCUIS-2011"
    citation: "Modernist Cuisine, Vol 1 (Food Safety) & Vol 2 (Sous Vide)"
verification_status: VERIFIED
---

# בישול סו-וויד מבוקר טמפרטורה (Sous-Vide Precision Cooking)

## תיאור הטכניקה (Overview)
בישול מזון ארוז בוואקום באמבט מים מבוקר תרמוסטטית. מאחר שטמפרטורת המים זהה לטמפרטורת היעד של ליבת המזון, לא נוצר בישול-יתר בשכבות החיצוניות.

## דרישות בטיחות קריטיות (Safety & Process Validation)
* **פסטור תלוי זמן, עובי וטמפרטורה**: בטמפרטורות נמוכות מסף ההשמדה המיידי (כגון מתחת ל-74°C בעוף או 63°C בבקר), בטיחות המזון תלויה בזמן ההחזקה בטמפרטורת הליבה בהתאם לעובי הנתח. לכן במערכת `chef_mind`, דיווח טמפרטורה בודד בסו-וויד **אינו** מאשר בטיחות תהליך ללא תוכנית פסטור מאומתת.
