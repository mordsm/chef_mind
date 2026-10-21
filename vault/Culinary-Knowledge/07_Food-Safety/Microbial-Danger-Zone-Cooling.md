---
id: SAF-ZONE-001
type: SCIENTIFIC_PRINCIPLE
name: "אזור הסכנה המיקרוביאלי וקירור בטוח (Microbial Danger Zone & Safe Chilling)"
domain: FOOD_SAFETY
category: "THERMODYNAMICS"
description: "מניעת התרבות חיידקים ויצירת רעלנים בטווח הטמפרטורות 4°C עד 60°C"
conditions:
  temperature_range_c:
    min: 4
    max: 60
  water_activity_aw:
    min: 0.85
    max: 1.0
  ph_range:
    min: 4.6
    max: 9.0
  catalysts: ["time_above_2_hours", "warm_ambient_temperature"]
effects:
  molecular_change: "הכפלה מהירה של אוכלוסיית החיידקים (כל 20 דקות בתנאים אופטימליים) והفرשת אנטרוטוקסינים עמידים לחום"
  sensory_consequences:
    taste: []
    aroma: ["פתוגנים אינם גורמים בהכרח לריח או טעם מקולקל"]
    color: []
    texture: []
exceptions:
  - "חימום מחדש של מזון ששהה מעל שעתיים באזור הסכנה אינו מנטרל רעלנים יציבים לחום (כגון Staphylococcus aureus או Bacillus cereus)"
relationships:
  - type: SUPPORTED_BY
    target_id: "SRC-USDA-FSIS-2024"
    target_name: "[[SRC-USDA-FSIS-2024]]"
sources:
  - source_id: "SRC-USDA-FSIS-2024"
    citation: "USDA FSIS Danger Zone (40°F - 140°F)"
verification_status: VERIFIED
---

# אזור הסכנה המיקרוביאלי וקירור בטוח (Microbial Danger Zone & Safe Chilling)

## כללי בטיחות מחייבים (Mandatory Safety Rules)
1. **טווח הסכנה (4°C–60°C)**: אין להשאיר מזון מתכלה מחוץ למקרר יותר משעתיים (או שעה אחת בטמפרטורת סביבה מעל 32°C).
2. **הפשרה בטוחה**: יש להפשיר בשר, עוף ודגים במקרר, לא על השיש בטמפרטורת החדר.
3. **חוסר מהימנות של בדיקת ריח/מראה**: מזון המזוהם בפתוגנים מסוכנים עשוי להיראות ולהריח תקין לחלוטין.
