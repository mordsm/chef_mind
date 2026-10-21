---
id: SAF-TEMP-001
type: SCIENTIFIC_PRINCIPLE
name: "טמפרטורות ליבה מינימליות ומנוחת בטיחות (Safe Minimum Internal Temperatures)"
domain: FOOD_SAFETY
category: "PROTEIN"
description: "ספי טמפרטורה וזמן מנוחה מחייבים להשמדת פתוגנים בחלבונים מן החי לפי תקן USDA"
conditions:
  temperature_range_c:
    min: 63
    max: 74
  water_activity_aw:
    min: 0.85
    max: 1.0
  ph_range:
    min: 5.0
    max: 7.5
  catalysts: ["core_temperature", "holding_rest_time"]
effects:
  molecular_change: "דנטורציה בלתי הפיכה של חלבוני אנזימים וממברנות בתאי חיידקים פתוגניים (סלמונלה, ליסטריה, E. coli)"
  sensory_consequences:
    taste: []
    aroma: []
    color: "צבע אינו מדד אמין לבטיחות"
    texture: "משתנה לפי סוג הנתח"
exceptions:
  - "בשיטות טמפרטורה נמוכה (כגון סו-וויד) נדרשת תוכנית זמן-טמפרטורה מאומתת בנפרד"
relationships:
  - type: REQUIRES
    target_id: "EQP-SENS-001"
    target_name: "[[Core-Probe-Thermometry]]"
  - type: ENABLES
    target_id: "RUL-SAF-001"
    target_name: "[[Rule-Poultry-Safe-Core-Temperature]]"
  - type: SUPPORTED_BY
    target_id: "SRC-USDA-FSIS-2024"
    target_name: "[[SRC-USDA-FSIS-2024]]"
sources:
  - source_id: "SRC-USDA-FSIS-2024"
    citation: "USDA FSIS Safe Minimum Internal Temperature Chart"
verification_status: VERIFIED
---

# טמפרטורות ליבה מינימליות ומנוחת בטיחות (Safe Minimum Internal Temperatures)

## טבלת ספי בטיחות מחייבים במערכת (`[[SRC-USDA-FSIS-2024]]`)
| קטגוריית מזון | טמפרטורת ליבה מינימלית | דרישת מנוחה מחייבת (Rest Time) |
| :--- | :---: | :---: |
| **עופות (עוף, הודו, ברווז, אווז, קורקבנים, כבד)** | **74°C** | ללא דרישת מנוחת בטיחות |
| **בשר בקר וטלה טחונים (המבורגר, קציצות)** | **71°C** | ללא דרישת מנוחת בטיחות |
| **נתחי בקר, עגל וטלה שלמים (סטייק, צלי)** | **63°C** | **3 דקות מנוחה (180 שניות)** |
| **דגים ופירות ים** | **63°C** | ללא דרישת מנוחת בטיחות |
| **מנות ביצים ותערובות ביצים** | **71°C** (או עד התייצבות חלבון וחלמון) | ללא דרישת מנוחת בטיחות |
