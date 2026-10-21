---
id: DEC-DIAG-001
type: SCIENTIFIC_PRINCIPLE
name: "אבחון ועצירת כשלים תרמיים בזמן אמת (Real-Time Thermal Rescue)"
domain: DECISION_MAKING
category: "THERMODYNAMICS"
description: "פרוטוקול קבלת החלטות לעצירת חימום יתר, חריכה, התגבנות וסיכוני בטיחות בזמן הבישול"
conditions:
  temperature_range_c:
    min: 60
    max: 250
  water_activity_aw:
    min: 0.10
    max: 1.0
  ph_range:
    min: 3.0
    max: 8.5
  catalysts: ["excess_heat_flux", "moisture_depletion"]
effects:
  molecular_change: "הורדת שטף החום מיידית לפני חציית סף הפירוליזה (שריפה) או קרישת-יתר בלתי הפיכה"
  sensory_consequences:
    taste: ["PREVENTS_ACRID_BURNT_TASTE"]
    aroma: []
    color: []
    texture: "הצלת המרקם בטרם הרס מבני"
exceptions:
  - "חלקים שכבר נשרפו והשחירו אינם מתוקנים בהוספת מים ויש להסירם כדי לא להכתים את טעם המנה"
relationships:
  - type: ENABLES
    target_id: "RUL-VEG-001"
    target_name: "[[Rule-Onion-Browning-Before-Softening]]"
  - type: ENABLES
    target_id: "RUL-EGG-001"
    target_name: "[[Rule-Custard-Curdling-Rescue]]"
  - type: SUPPORTED_BY
    target_id: "SRC-BCCAMPUS-PASTRY-2015"
    target_name: "[[SRC-BCCAMPUS-PASTRY-2015]]"
sources:
  - source_id: "SRC-BCCAMPUS-PASTRY-2015"
    citation: "BCcampus, Modern Pastry and Plated Dessert Techniques, 2015"
verification_status: VERIFIED
---

# אבחון ועצירת כשלים תרמיים בזמן אמת (Real-Time Thermal Rescue)

## עקרונות פעולה בזמן אמת (Real-Time Intervention Rules)
1. **בצל משחים לפני שהתרכך (`[[Rule-Onion-Browning-Before-Softening]]`)**: שטף החום גבוה מקצב הולכת החום לפנים הבצל. פתרון: הפחתת חום לנמוך, הוספת כף-שתיים מים וכיסוי המחבת.
2. **קרם ביצים מתחיל להתגבן (`[[Rule-Custard-Curdling-Rescue]]`)**: עצירה מיידית של החימום והעברה לכלי קר לפני שהרשת החלבונית מתכווצת לחלוטין.
3. **חריכה בתחתית הסיר**: הפחתת חום והעברת תוכן המנה (ללא גירוד השכבה השרופה!) לסיר נקי.
4. **שמן מעשן בכבדות או להבות**: עצירת מקור החום בבטחה; איסור מוחלט על שפיכת מים לשמן חם.
