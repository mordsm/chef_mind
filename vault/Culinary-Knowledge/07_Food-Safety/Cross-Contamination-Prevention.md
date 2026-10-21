---
id: SAF-CONT-001
type: SCIENTIFIC_PRINCIPLE
name: "מניעת זיהום צולב במטבח (Cross-Contamination Prevention)"
domain: FOOD_SAFETY
category: "PROTEIN"
description: "הפרדת כלים, משטחים ונוזלים שבאו במגע עם חלבון נא ממזון מבושל או מוכן לאכילה"
conditions:
  temperature_range_c:
    min: 0
    max: 60
  water_activity_aw:
    min: 0.50
    max: 1.0
  ph_range:
    min: 4.0
    max: 8.5
  catalysts: ["shared_cutting_boards", "unwashed_tongs", "raw_marinade_reuse"]
effects:
  molecular_change: "העברת פתוגנים פעילים מחומר גלם נא אל מזון שכבר עבר בישול תרמי ולא יעבור חימום נוסף"
  sensory_consequences:
    taste: []
    aroma: []
    color: []
    texture: []
exceptions:
  - "מרינדה שבה הושרה בשר או עוף נא מותרת לשימוש כרוטב רק אם הורתחה היטב בנפרד"
relationships:
  - type: SUPPORTED_BY
    target_id: "SRC-USDA-FSIS-2024"
    target_name: "[[SRC-USDA-FSIS-2024]]"
sources:
  - source_id: "SRC-USDA-FSIS-2024"
    citation: "USDA FSIS Safe Food Handling: Cross-Contamination"
verification_status: VERIFIED
---

# מניעת זיהום צולב במטבח (Cross-Contamination Prevention)

## פרוטוקול הפרדה תפעולי (Separation Protocol)
1. **הפרדת כלי עבודה והגשה**: לעולם אין להחזיר עוף, בשר או דג מבושלים לצלחת או לקרש החיתוך שבהם הונחו כשהיו נאים, ואין להשתמש באותם מלקחיים ללא שטיפה יסודית במים חמים וסבון.
2. **הימנעות משטיפת עוף נא בכיור**: שטיפת עוף נא מתיזה טיפות מים מזוהמות בקמפילובקטר וסלמונלה על משטחי המטבח; השמדת החיידקים מתבצעת בבישול ל-74°C (`[[Minimum-Internal-Temperatures]]`).
