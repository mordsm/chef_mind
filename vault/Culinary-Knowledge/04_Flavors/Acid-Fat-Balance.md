---
id: FLV-BAL-001
type: SCIENTIFIC_PRINCIPLE
name: "איזון חומצה-שומן וניגודי טעם (Acid-Fat Sensory Balance)"
domain: FLAVORS
category: "CHEMICAL_REACTION"
description: "שימוש בחומצות אורגניות לאיזון תחושת הכבדות והשמנוניות בחך ולהגברת בהירות הטעם"
conditions:
  temperature_range_c:
    min: 5
    max: 90
  water_activity_aw:
    min: 0.50
    max: 1.0
  ph_range:
    min: 2.2
    max: 5.5
  catalysts: ["citric_acid", "acetic_acid", "lactic_acid", "tartaric_acid"]
effects:
  molecular_change: "גירוי קולטני יוני מימן בחך והגברת הפרשת רוק המפחיתה את צמיגות ציפוי השומן על הלשון"
  sensory_consequences:
    taste: ["BRIGHTNESS", "BALANCED_RICHNESS"]
    aroma: ["FRESH_CITRUS_OR_FERMENTED_NOTES"]
    color: "שמירה על פיגמנטים אדומים (אנתוציאנינים) אך דהייה של כלורופיל ירוק בבישול ממושך"
    texture: "תחושת פה קלילה ונקייה יותר"
exceptions:
  - "חומציות אינה מחטאת חלבון נא (כגון בדגים בסביצ'ה) ואינה מחליפה בישול תרמי לבטיחות מזון"
relationships:
  - type: AFFECTS
    target_id: "DEC-CORR-001"
    target_name: "[[Sauce-Texture-Correction-Matrix]]"
  - type: SUPPORTED_BY
    target_id: "SRC-MCGEE-2004"
    target_name: "[[SRC-MCGEE-2004]]"
sources:
  - source_id: "SRC-MCGEE-2004"
    citation: "McGee, On Food and Cooking, 2004, Chapter 7 & Chapter 11"
    chapter: "Flavor and Seasoning"
    pages: "pp. 270-278"
verification_status: VERIFIED
---

# איזון חומצה-שומן וניגודי טעם (Acid-Fat Sensory Balance)

## מנגנון מדעי מפורט (Scientific Mechanism)
שומנים מצפים את הלשון ומעמעמים את רגישות קולטני הטעם. הוספת חומצה (מיץ לימון, חומץ, יין, עגבניות) בסיום הבישול מעוררת הפרשת רוק ומנקה את ציפוי השומן ("חיתוך שומניות"), מה שמחזיר חדות ובהירות למנות עשירות או כבדות.
* **אזהרת בטיחות קריטית**: דנטורציה חומצית של חלבון (כמו בסביצ'ה) משנה את המרקם לחזות אטומה, אך **אינה** משמידה טפילים או חיידקים באותה ודאות של טיפול תרמי מאומת.
