---
id: EQP-SENS-001
type: SCIENTIFIC_PRINCIPLE
name: "מדידת טמפרטורת ליבה ומיקום חיישן (Core Probe Thermometry)"
domain: EQUIPMENT
category: "THERMODYNAMICS"
description: "מדידה פיזיקלית של המרכז התרמי של המזון באמצעות מדחום ליבה לאימות בטיחות ודרגת עשייה"
conditions:
  temperature_range_c:
    min: -20
    max: 250
  water_activity_aw:
    min: 0.0
    max: 1.0
  ph_range:
    min: 1.0
    max: 14.0
  catalysts: ["geometric_center_placement"]
effects:
  molecular_change: "איתור הנקודה הקרה ביותר במזון (Thermal Center) שבה קצב השמדת הפתוגנים הוא האיטי ביותר"
  sensory_consequences:
    taste: []
    aroma: []
    color: "מונע הסתמכות שגויה על צבע הבשר או המיצים"
    texture: "מונע בישול יתר הנובע מניחוש זמן"
exceptions:
  - "מגע של קצה המדחום בעצם, בשומן עבה או בתחתית המחבת מציג קריאה שגויה וגבוהה מהליבה האמיתית"
relationships:
  - type: ENABLES
    target_id: "SAF-TEMP-001"
    target_name: "[[Minimum-Internal-Temperatures]]"
  - type: SUPPORTED_BY
    target_id: "SRC-USDA-FSIS-2024"
    target_name: "[[SRC-USDA-FSIS-2024]]"
sources:
  - source_id: "SRC-USDA-FSIS-2024"
    citation: "USDA FSIS, Food Thermometers Guide"
verification_status: VERIFIED
---

# מדידת טמפרטורת ליבה ומיקום חיישן (Core Probe Thermometry)

## פרוטוקול מדידה תפעולי (Operating Protocol)
לפי הנחיות `[[SRC-USDA-FSIS-2024]]`, יש להחדיר את מדחום המזון לחלק העבה ביותר של הנתח, הרחק מעצם, שומן או סחוס. בנתחים דקים או שטוחים יש להחדיר מהצד (אופקית). כאשר מבשלים מספר נתחים, יש למדוד בכמה חלקים עבים לפני אישור מוכנות.
