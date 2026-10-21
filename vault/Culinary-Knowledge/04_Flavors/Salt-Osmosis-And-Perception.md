---
id: FLV-TASTE-001
type: SCIENTIFIC_PRINCIPLE
name: "מליחות, אוסמוזה והמלחה מוקדמת (Salt Osmosis & Dry Brining)"
domain: FLAVORS
category: "PROTEIN"
description: "השפעת נתרן כלורי על תפיסת הטעם, דיפוזיה אוסמוטית ושינוי מבנה חלבוני השריר לשמירת עסיסיות"
conditions:
  temperature_range_c:
    min: 2
    max: 25
  water_activity_aw:
    min: 0.70
    max: 1.0
  ph_range:
    min: 5.0
    max: 7.5
  catalysts: ["sodium_chloride", "time_above_40_min"]
effects:
  molecular_change: "שאיבת מים אוסמוטית ראשונית, המסת מיוצין ליצירת ג'ל חלבוני, וספיגה חוזרת של הנוזלים לתוך סיבי השריר"
  sensory_consequences:
    taste: ["ENHANCED_SAVORY", "SUPPRESSED_BITTERNESS"]
    aroma: ["INCREASED_VOLATILE_RELEASE"]
    color: "אדום עמוק ויבש יותר על פני השטח (לאחר מנוחה בקירור)"
    texture: "עסיסיות משופרת ופחות איבוד נוזלים בצלייה"
exceptions:
  - "המלחה בטווח של 3 עד 35 דקות לפני צריבה משאירה שלולית נוזלים על פני השטח ופוגעת בהשחמה"
relationships:
  - type: ENABLES
    target_id: "TEX-CRUST-001"
    target_name: "[[Surface-Browning]]"
  - type: AFFECTS
    target_id: "CON-SALT-001"
    target_name: "[[Pre-Salting-Steak-Timing]]"
  - type: SUPPORTED_BY
    target_id: "SRC-FOODLAB-2015"
    target_name: "[[SRC-FOODLAB-2015]]"
sources:
  - source_id: "SRC-FOODLAB-2015"
    citation: "The Food Lab, 2015, Chapter 3: Steaks"
    chapter: "Chapter 3"
    pages: "pp. 200-206"
verification_status: VERIFIED
---

# מליחות, אוסמוזה והמלחה מוקדמת (Salt Osmosis & Dry Brining)

## מנגנון מדעי מפורט (Scientific Mechanism)
המלח ($\text{NaCl}$) מדגיש טעמי אומאמי ומתיקות ומדכא מרירות. ברמת הרקמה, המלחה מוקדמת (Dry Brining) פועלת בשני שלבים: בדקות הראשונות אוסמוזה מושכת טיפות מים אל פני השטח; לאחר 40 דקות ומעלה (ובמיטבו אחרי 12–24 שעות במקרר), המלח ממיס חלקית את חלבוני המיוצין והתמיסה נספגת חזרה פנימה, תוך השארת שטח פנים יבש המוכן לצריבה (`[[Pre-Salting-Steak-Timing]]`).
