---
id: SCI-CHEM-002
type: SCIENTIFIC_PRINCIPLE
name: "קרמליזציה ויציבות תחליבים (Caramelization & Emulsion Stability)"
domain: FOOD_SCIENCE
category: "CHEMICAL_REACTION"
description: "פירוק תרמי של סוכרים טהורים בחום גבוה וייצוב פיזיקלי של מערכות שמן-במים"
conditions:
  temperature_range_c:
    min: 110
    max: 185
  water_activity_aw:
    min: 0.10
    max: 0.90
  ph_range:
    min: 3.0
    max: 8.0
  catalysts: ["heat", "shear_force", "emulsifiers_lecithin_starch"]
effects:
  molecular_change: "בקרמליזציה: איזומריזציה, דה-הידרציה ופילמור של מולקולות סוכר; בתחליב: ציפוי טיפות שומן מיקרוסקופיות במולקולות אמפיפיליות"
  sensory_consequences:
    taste: ["COMPLEX_SWEET", "SLIGHTLY_BITTER_ACIDIC"]
    aroma: ["diacetyl_buttery", "furans_nutty"]
    color: "ענברי עד חום עמוק"
    texture: "חלק, קרמי ומבריק"
exceptions:
  - "נוכחות גבישי סוכר לא מומסים בשולי הסיר גורמת להתגבשות מחדש של הסירופ"
  - "מעבר מעל 190°C שורף את הקרמל למרירות בלתי הפיכה"
relationships:
  - type: AFFECTS
    target_id: "TEX-VISC-001"
    target_name: "[[Starch-And-Emulsion-Viscosity]]"
  - type: SUPPORTED_BY
    target_id: "SRC-BCCAMPUS-PASTRY-2015"
    target_name: "[[SRC-BCCAMPUS-PASTRY-2015]]"
sources:
  - source_id: "SRC-BCCAMPUS-PASTRY-2015"
    citation: "BCcampus, Modern Pastry and Plated Dessert Techniques, 2015"
    chapter: "Crystallization"
    pages: "Chapter 4"
  - source_id: "SRC-MCGEE-2004"
    citation: "McGee, On Food and Cooking, 2004"
    chapter: "Chapter 11 & Chapter 12"
    pages: "pp. 625-633, 656-662"
verification_status: VERIFIED
---

# קרמליזציה ויציבות תחליבים (Caramelization & Emulsion Stability)

## מנגנון מדעי מפורט (Scientific Mechanism)
1. **קרמליזציה ובקרת התגבשות**: בשונה מתגובת מייאר (`[[Maillard-Reaction]]`), קרמליזציה מתרחשת בסוכרים בלבד ללא חלבונים (פרוקטוז מ-110°C, סוכרוז וגלוקוז ב-160°C–180°C). במהלך הרתחת סירופ סוכר, גבישים שנותרו על דופן הסיר עלולים לשמש כגרעין להתגבשות שרשרתית; הימנעות מערבוב מיותר ושמירה על דפנות נקיות מונעות זאת.
2. **תחליבים (Emulsions)**: פיזור יציב של טיפות שומן במים דורש כוח גזירה (טריפה) ומייצבים (לציטין מחלמון `[[Egg-Proteins-Yolk-Albumen]]`, חרדל, או מים עמילניים `[[Starch-Cornstarch-Flour]]`).
