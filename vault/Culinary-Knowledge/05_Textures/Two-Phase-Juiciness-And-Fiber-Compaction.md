---
id: TEX-MEAT-001
type: SCIENTIFIC_PRINCIPLE
name: "תפיסת העסיסיות הדו-שלבית, דחיסת סיבי השריר והצלת מרקם בפירוק (Two-Phase Juiciness & Fiber Compaction)"
domain: TEXTURES
category: "PROTEIN"
description: "המודל הסנסורי הדו-שלבי של עסיסיות בשר (מים חופשיים בלעיסות הראשונות מול שומן מותך וג'לטין בלעיסה מתמשכת) וטכניקות מכניות להתמודדות עם סיבים צפופים"
conditions:
  temperature_range_c:
    min: 50
    max: 90
  water_activity_aw:
    min: 0.85
    max: 0.99
  ph_range:
    min: 5.4
    max: 6.2
  catalysts: ["intracellular_water", "intramuscular_marbling_fat", "hydrolyzed_gelatin", "saliva_flow", "mechanical_shredding"]
effects:
  molecular_change: "50-55°C שחרור מים חופשיים בתוך הסיבים (שלב 1 של עסיסיות); 60-80°C סחיטת המים ודחיסת אקטין/מיוצין; 80-90°C המסת שומן תוך-שרירי וקולגן לג'לטין המצפים את הסיבים (שלב 2 של עסיסיות)"
  sensory_consequences:
    taste: ["SAVORY_RELEASE_IN_SALIVA"]
    aroma: ["FAT_CARRIED_VOLATILES"]
    color: "מבריק מעטיפת שומן וג'לטין"
    texture: "עסיסיות ראשונית שופעת במדיום-רייר; עסיסיות מתמשכת וקטיפתית בצלי קדרה עשיר בג'לטין ושיוש שומן"
exceptions:
  - "נתח רזה ודל קולגן (כגון חזה עוף או פילה בקר) המבושל ל-80°C יאבד את עסיסיות שלב 1 מבלי שיהיו לו שומן או ג'לטין לספק את עסיסיות שלב 2"
relationships:
  - type: AFFECTS
    target_id: "SCI-MEAT-001"
    target_name: "[[Meat-Thermal-Progression-And-Doneness-Spectrum]]"
  - type: AFFECTS
    target_id: "SCI-PROT-001"
    target_name: "[[Collagen-Hydrolysis-Gelatin]]"
  - type: AFFECTS
    target_id: "TEX-TEND-001"
    target_name: "[[Collagen-Driven-Tenderness]]"
  - type: AFFECTS
    target_id: "TEC-MEAT-003"
    target_name: "[[Succulent-Braising-Stewing-And-Liquid-Cooling]]"
  - type: AFFECTS
    target_id: "TEC-MEAT-004"
    target_name: "[[Resting-Carryover-Cooking-And-Carving]]"
  - type: SUPPORTED_BY
    target_id: "SRC-MCGEE-2004"
    target_name: "[[SRC-MCGEE-2004]]"
sources:
  - source_id: "SRC-MCGEE-2004"
    citation: "McGee, On Food and Cooking (2nd Ed., 2004), Chapter 3: Meat"
    book_title: "On Food and Cooking: The Science and Lore of the Kitchen"
    author: "Harold McGee"
    edition: "2nd Edition (Completely Revised and Updated)"
    publication_year: 2004
    chapter: "Chapter 3: Meat"
    printed_pages: "pp. 131, 148-154, 163, 165"
    pdf_pages: "pp. 145, 162-168, 177, 179"
    claim_type: "DIRECT_SOURCE_CLAIM"
verification_status: VERIFIED
---

# תפיסת העסיסיות הדו-שלבית, דחיסת סיבי השריר והצלת מרקם בפירוק (Two-Phase Juiciness & Fiber Compaction)

## 1. המודל הדו-שלבי של תפיסת העסיסיות בפה (`Two-Phase Juiciness Perception`, עמ' 131, 148–151 / PDF 145, 162–165)
הרולד מקג'י מראה כי תחושת ה"עסיסיות" (*Juiciness*) בעת אכילת בשר אינה תכונה בודדת, אלא חוויה תחושתית דו-שלבית הנובעת משני מקורות פיזיקליים שונים לחלוטין (`DIRECT_SOURCE_CLAIM`):

1. **שלב א' — רטיבות ראשונית מיידית (`Initial Wetness` — מים חופשיים בתוך תאי השריר):**
   * מורגשת בנגיסות הראשונות ונובעת מכמות **המים החופשיים (Intracellular Juice)** הפורצים מתוך סיבי השריר כאשר השיניים חותכות אותם.
   * מגיעה לשיאה בדרגת **רייר עד מדיום-רייר (50°C–58°C / 125°F–135°F)** ונעלמת מעל **65°C–70°C** לאחר שמעטפות הקולגן והאקטין מתכווצות וסוחטות את המים החוצה (`[[Meat-Thermal-Progression-And-Doneness-Spectrum]]`).
2. **שלב ב' — עסיסיות מתמשכת (`Sustained Juiciness` — שומן משויש מותך, ג'לטין והפרשת רוק):**
   * מורגשת לאורך המשך הלעיסה ונובעת מ**שומן תוך-שרירי מותך (*Marbling Fat*)**, **ג'לטין מומס מקולגן** (`[[Collagen-Hydrolysis-Gelatin]]`) ו**עידוד הפרשת רוק בפה** על ידי שומן וחומצות אמינו אומאמיות.
   * השומן והג'לטין מצפים את הלשון ואת סיבי השריר היבשים, משמנים אותם ומעניקים תחושת עסיסיות קטיפתית מתמשכת גם בבשר שהתבשל בישול ארוך ל-**80°C–90°C** ואיבד מזמן את המים התוך-תאיים שלו (`[[Collagen-Driven-Tenderness]]`).

---

## 2. ארבע התערבויות מכניות לשיפור רכות ועסיסיות (`Mechanical Tenderization & Recovery`, עמ' 154, 163, 165 / PDF 168, 177, 179)
כאשר סיבי השריר ארוכים, עבים או התכווצו בבישול, ניתן לשנות את חוויית המרקם באמצעות שבירה או קיצור מכני של הסיבים (`DIRECT_SOURCE_CLAIM`):

1. **דיקור, שיטוח וטחינה לפני הבישול (`Pounding, Cubing & Grinding`, עמ' 154 / PDF 168):**
   * פטיש שניצלים, סכיני דיקור (*Jaccard*) או מטחנת בשר קורעים מכנית את מעטפות הקולגן ומקצרים את סיבי השריר עוד לפני החימום. (זהירות: דיקור מחדיר חיידקי פני שטח לעומק הנתח ומחייב בישול מלא יותר; `[[Meat-Pathogens-Blanch-Grinding-And-Carcinogens]]`).
2. **פריסה דקה בניצב לסיבים (`Slicing Thin Across the Grain`, עמ' 154, 165 / PDF 168, 179):**
   * קיצור אורך הסיבים למילימטרים ספורים לפני הבישול (כמו במוקפץ סיני) או לאחר הצלייה (`[[Resting-Carryover-Cooking-And-Carving]]`) הופך גם נתח סיבי ללעיס ורך.
3. **קירור בנוזל הצלייה ל-50°C (`Cooling in Braising Liquid`, עמ' 163 / PDF 177):**
   * מאפשר לחללים הקפילריים שבין צרורות הסיבים לשאוב חזרה נוזל ג'לטיני עשיר (`[[Succulent-Braising-Stewing-And-Liquid-Cooling]]`).
4. **פירוק הבשר לסיבים וערבובו ברוטב מרוכז ופושר (`Shredding & Coating`, עמ' 163 / PDF 177):**
   * הפרדת בשר מבושל לחוטים/סיבים וערבובם בנוזלי הצלייה שהוסמכו בג'לטין ובשומן יוצרת מעטפת רוטב צמיגה סביב כל סיב בודד ומחזירה עסיסיות עשירה לבשר שהתייבש.

