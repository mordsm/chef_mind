---
id: SCI-PROT-001
type: SCIENTIFIC_PRINCIPLE
name: "הידרוליזה של קולגן לג'לטין (Collagen Hydrolysis to Gelatin)"
domain: FOOD_SCIENCE
category: "PROTEIN"
description: "פירוק תרמי-הידרוליטי של סלילי הקולגן הקשיחים ברקמת החיבור ליצירת ג'לטין מסיס ונימוח"
conditions:
  temperature_range_c:
    min: 60
    max: 95
  water_activity_aw:
    min: 0.85
    max: 1.0
  ph_range:
    min: 4.0
    max: 7.5
  catalysts: ["water", "time", "mild_acidity"]
effects:
  molecular_change: "פתיחת הסליל המשולש (Triple Helix) של סיבי הקולגן ושבירת קשרי המימן והפפטיד לשרשראות ג'לטין מסיסות במים"
  sensory_consequences:
    taste: ["SAVORY_FULLNESS"]
    aroma: []
    color: "שקוף-מבריק"
    texture: "נימוח, עסיסי ומצפה את החך (Mouthfeel עשיר)"
exceptions:
  - "בחום יבש ומהיר ללא נוזלים או זמן מספק, הקולגן מתכווץ ומתקשה במקום להתמוסס"
relationships:
  - type: AFFECTS
    target_id: "TEX-TEND-001"
    target_name: "[[Collagen-Driven-Tenderness]]"
  - type: ENABLES
    target_id: "TEC-COMB-001"
    target_name: "[[Low-Slow-Braising]]"
  - type: SUPPORTED_BY
    target_id: "SRC-BCCAMPUS-MEAT-2015"
    target_name: "[[SRC-BCCAMPUS-MEAT-2015]]"
sources:
  - source_id: "SRC-BCCAMPUS-MEAT-2015"
    citation: "BCcampus, Meat Cutting and Processing for Food Service, 2015"
    chapter: "Meat Fibres and Tenderness Factors"
    pages: "Chapter 2"
  - source_id: "SRC-MCGEE-2004"
    citation: "McGee, On Food and Cooking, 2004"
    chapter: "Chapter 3: Meat"
    pages: "pp. 147-153"
verification_status: VERIFIED
---

# הידרוליזה של קולגן לג'לטין (Collagen Hydrolysis to Gelatin)

## מנגנון מדעי מפורט (Scientific Mechanism)
קולגן הוא חלבון מבני הבנוי כסליל משולש הדוק (Triple Helix) העוטף את סיבי השריר בנתחים עובדים (`[[Beef-Chuck-Collagen-Rich]]`). כאשר מחממים את הנתח בנוכחות מים לטמפרטורה של 68°C–85°C לאורך זמן, אנרגיית החום מנתקת את קשרי הצילוב בין הסלילים, ומולקולות המים חודרות ומפרידות אותם לשרשראות **ג'לטין** בודדות הקושרות מים ויוצרות תחושת עסיסיות עשירה.

## תנאי סף וטריגרים (Thresholds & Triggers)
* **טמפרטורה וזמן**: תהליך קינטי תלוי-זמן — ב-65°C הוא דורש שעות רבות (כמו ב-`[[Sous-Vide-Precision-Cooking]]`), ב-85°C–90°C (בעבוע עדין ב-`[[Low-Slow-Braising]]`) הוא מושלם תוך 2–3 שעות, ובסיר לחץ (120°C) תוך 35–45 דקות.
* **נוכחות מים**: חיונית לתגובת ההידרוליזה (בקיעת קשרים באמצעות מים).
