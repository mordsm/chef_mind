---
id: TEC-DRY-001
type: COOKING_TECHNIQUE
name: "צריבה במחבת בחום גבוה (High-Heat Pan Searing)"
domain: TECHNIQUES
heat_environment: "DRY"
heat_transfer_methods:
  - "CONDUCTION"
recommended_equipment:
  - "מחבת ברזל יצוק או נירוסטה כבדה בעלת מסה תרמית גבוהה"
target_foods:
  - "נתחי בקר רזים או משוישים (אנטרקוט, סינטה, פילה)"
  - "פילה דג"
  - "חזה עוף"
conditions:
  surface_temperature_min_c: 150
  cooking_medium: "OIL"
  duration_range: "2-6 minutes per side (dependent on thickness)"
effects:
  primary_outcome: "השחמת שטח פנים מהירה ויצירת קראסט עשיר בטעמי מייאר"
  texture_change: "CRISP_EXTERIOR / JUICY_INTERIOR"
  moisture_loss_pct_estimate: 14.0
exceptions:
  - "אינה מתאימה לריכוך שרירים עתירי קולגן (כגון כתף, שוק או קורקבנים) ללא בישול מוקדם"
relationships:
  - type: REQUIRES
    target_id: "SCI-CHEM-001"
    target_name: "[[Maillard-Reaction]]"
  - type: REQUIRES
    target_id: "EQP-PAN-001"
    target_name: "[[Cast-Iron-Vs-Stainless-Thermal-Mass]]"
  - type: ENABLES
    target_id: "TEX-CRUST-001"
    target_name: "[[Surface-Browning]]"
  - type: INHIBITED_BY
    target_id: "RUL-TEC-001"
    target_name: "[[Rule-Pan-Crowding-Steam-Inhibition]]"
sources:
  - source_id: "SRC-MODCUIS-2011"
    citation: "Modernist Cuisine, Vol 2: Traditional Cooking"
  - source_id: "SRC-FOODLAB-2015"
    citation: "The Food Lab, Chapter 3"
verification_status: VERIFIED
---

# צריבה במחבת בחום גבוה (High-Heat Pan Searing)

## תיאור הטכניקה (Overview)
טכניקת חום יבש המבוססת על הולכת חום ישירה (`[[Heat-Transfer]]`) ממשטח מתכת חם אל שטח פני המזון דרך שכבה דקה של שומן. המטרה המרכזית היא אידוי מיידי של לחות חיצונית וחציית סף 140°C להפעלת `[[Maillard-Reaction]]` ויצירת `[[Surface-Browning]]`.

## פרוטוקול ביצוע שלב-אחר-שלב (Execution Protocol)
1. ייבוש יסודי של שטח פני המזון לפני המגע עם המחבת.
2. חימום מוקדם של מחבת בעלת מסה תרמית גבוהה (`[[Cast-Iron-Vs-Stainless-Thermal-Mass]]`).
3. השארת מרווח בין הנתחים למניעת כליאת אדים (`[[Rule-Pan-Crowding-Steam-Inhibition]]`).
4. אימות טמפרטורת ליבה במדחום (`[[Core-Probe-Thermometry]]`) בנפרד מצבע הקראסט.
