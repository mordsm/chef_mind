---
id: SCI-PROT-002
type: SCIENTIFIC_PRINCIPLE
name: "דנטורציה וקרישת חלבונים (Protein Denaturation & Coagulation)"
domain: FOOD_SCIENCE
category: "PROTEIN"
description: "פתיחת המבנה המרחבי של חלבונים בחום או בחומצה ויצירת רשת תלת-ממדית הלוכדת או דוחקת מים"
conditions:
  temperature_range_c:
    min: 50
    max: 85
  water_activity_aw:
    min: 0.70
    max: 1.0
  ph_range:
    min: 3.5
    max: 8.0
  catalysts: ["heat", "acid", "salt", "mechanical_agitation"]
effects:
  molecular_change: "פתיחת הקיפול הטבעי של החלבון (Denaturation) והיקשרות מחדש של שרשראות סמוכות לרשת מוצקה או ג'ל (Coagulation)"
  sensory_consequences:
    taste: []
    aroma: []
    color: "מעבר משקוף לאטום"
    texture: "התמצקות מנוזל/רך למוצק יציב; בחימום יתר — התגבנות ויובש"
exceptions:
  - "חימום מעבר ל-85°C בקרם ביצים גורם לקרישת יתר (Curdling) ולפליטת המים הכלואים (Syneresis)"
relationships:
  - type: AFFECTS
    target_id: "ING-EGG-001"
    target_name: "[[Egg-Proteins-Yolk-Albumen]]"
  - type: AFFECTS
    target_id: "ING-POUL-001"
    target_name: "[[Poultry-Breast-Lean]]"
  - type: SUPPORTED_BY
    target_id: "SRC-BCCAMPUS-PASTRY-2015"
    target_name: "[[SRC-BCCAMPUS-PASTRY-2015]]"
sources:
  - source_id: "SRC-BCCAMPUS-PASTRY-2015"
    citation: "BCcampus, Modern Pastry and Plated Dessert Techniques, 2015"
    chapter: "Coagulation"
    pages: "Chapter 3"
  - source_id: "SRC-MCGEE-2004"
    citation: "McGee, On Food and Cooking, 2004"
    chapter: "Chapter 2 & Chapter 3"
    pages: "pp. 84-91, 148-152"
verification_status: VERIFIED
---

# דנטורציה וקרישת חלבונים (Protein Denaturation & Coagulation)

## מנגנון מדעי מפורט (Scientific Mechanism)
חלבונים במצבם הטבעי מקופלים במבנה תלת-ממדי הדוק. חימום מגביר את התנועה התרמית של האטומים עד לפתיחת הקיפול (**דנטורציה**). כאשר קבוצות הידרופוביות פנימיות נחשפות, מולקולות החלבון נקשרות זו לזו ויוצרות רשת מרחבית (**קרישה / Coagulation**).

## תנאי סף וטריגרים (Thresholds & Triggers)
* **בבשר ודגים**: מיוצין נקרש ב-50°C–55°C (תחילת התמצקות); אקטין מתכווץ ב-66°C–73°C ודוחק נוזלים החוצה מסיבי השריר.
* **בביצים וקרמים (`[[Rule-Custard-Curdling-Rescue]]`)**: קרישה מבוקרת כולאת מים בג'ל חלק ועדין, אך חימום יתר מכווץ את הרשת ופולט נוזל מימי תוך יצירת גושים.
