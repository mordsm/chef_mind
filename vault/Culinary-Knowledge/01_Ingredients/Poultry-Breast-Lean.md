---
id: ING-POUL-001
type: INGREDIENT
name: "חזה עוף והודו רזה (Lean Poultry Breast)"
domain: INGREDIENTS
category: "חלבון מן החי"
composition:
  water_pct: 74.0
  protein_pct: 23.0
  fat_pct: 1.5
  carb_pct: 0.0
  ph_level: 5.9
physical_properties:
  density_g_cm3: 1.04
  thermal_conductivity: "MEDIUM"
  cellular_structure: "סיבי שריר לבנים עדינים ודלי קולגן ושומן תוך-שרירי"
sensory_profile:
  dominant_taste: ["MILD_UMAMI"]
  aroma_compounds: ["aldehydes", "lactones"]
  raw_texture: "TENDER_SOFT"
storage_and_safety:
  shelf_life_days_refrigerated: 2
  minimum_internal_temp_c: 74.0
  allergens: []
  kashrut_class: "MEAT"
relationships:
  - type: AFFECTS
    target_id: "SCI-PROT-002"
    target_name: "[[Protein-Denaturation-Coagulation]]"
  - type: REQUIRES
    target_id: "SAF-TEMP-001"
    target_name: "[[Minimum-Internal-Temperatures]]"
  - type: AFFECTS
    target_id: "ING-MEAT-002"
    target_name: "[[Muscle-Fiber-Types-And-Myoglobin-Chemistry]]"
  - type: AFFECTS
    target_id: "TEC-MEAT-002"
    target_name: "[[Whole-Bird-Roasting-And-Crisp-Poultry-Skin]]"
  - type: AFFECTS
    target_id: "RUL-MEAT-003"
    target_name: "[[Rule-Whole-Bird-Breast-Vs-Leg-Thermal-Solutions]]"
  - type: SUPPORTED_BY
    target_id: "SRC-USDA-FSIS-2024"
    target_name: "[[SRC-USDA-FSIS-2024]]"
  - type: SUPPORTED_BY
    target_id: "SRC-MCGEE-2004"
    target_name: "[[SRC-MCGEE-2004]]"
sources:
  - source_id: "SRC-USDA-FSIS-2024"
    citation: "USDA FSIS Safe Minimum Internal Temperature Chart"
  - source_id: "SRC-MCGEE-2004"
    citation: "McGee, On Food and Cooking (2nd Ed., 2004), Chapter 3: Meat"
    book_title: "On Food and Cooking: The Science and Lore of the Kitchen"
    author: "Harold McGee"
    edition: "2nd Edition (Completely Revised and Updated)"
    publication_year: 2004
    chapter: "Chapter 3: Meat"
    printed_pages: "pp. 132-135, 143, 157-160"
    pdf_pages: "pp. 146-149, 157, 171-174"
    claim_type: "DIRECT_SOURCE_CLAIM"
verification_status: VERIFIED
---

# חזה עוף והודו רזה (Lean Poultry Breast)

## תיאור כללי (Description)
נתח חלבון רזה במיוחד המתאפיין באחוז שומן נמוך מאוד (1%–2%) ומיעוט רקמת חיבור. לפי *On Food and Cooking* (`[[SRC-MCGEE-2004]]`, עמ' 132–135 / PDF 146–149):
* **אנטומיית סיבים לבנים מהירים (`DIRECT_SOURCE_CLAIM`, עמ' 134 / PDF 148):** שריר החזה בתרנגולת ובהודו משמש רק להתפרצויות תעופה קצרות ונדירות, ולכן הוא מורכב מ-**90% סיבים לבנים מהירים (Fast-twitch Glycolytic Fibers)** ורק **10% סיבים אדומים איטיים** (לעומת **80% סיבים אדומים** בחזה ברווז ו-**85% סיבים אדומים** בחזה יונה/Squab העפים למרחקים ארוכים; `[[Muscle-Fiber-Types-And-Myoglobin-Chemistry]]`).
* **מחסור במיוגלובין ושומן תוך-תאי:** הסיבים הלבנים מפיקים אנרגיה מפירוק גליקוגן ללא חמצן (אנאירובי), ולכן הם כמעט חסרי מיוגלובין ודלים מאוד בשומן תוך-תאי ובקולגן.
* **צפידת מוות מהירה (Rigor Mortis, עמ' 143 / PDF 157):** בעופות צפידת המוות מתפתחת תוך **פחות משעה אחת** מהשחיטה, ומחייבת הרפיית יישון קצרה של מספר שעות לפני הקפאה או בישול, אחרת החזה נשאר קשיח וצמיגי (`[[Rigor-Mortis-DFD-Meat-And-Aging-Enzymes]]`).

## התנהגות בבישול ודילמת העוף השלם (Cooking Behavior & Whole Bird Dilemma)
* **רגישות לייבוש ודילמת החזה מול השוק (`DIRECT_SOURCE_CLAIM`, עמ' 159–160 / PDF 173–174):** מאחר שאין בחזה שומן תוך-שרירי או קולגן שיתמוסס לג'לטין, חזה עוף והודו מגיע לשיא העסיסיות והרכות סביב **65°C–68°C (150°F–155°F)** ומתחיל להתייבש מעבר לכך, בעוד ששרירי הרגליים והירכיים העובדים (העשירים בקולגן ושומן) נותרים צמיגיים וורודים עד שהם מגיעים ל-**73°C–77°C (165°F–170°F)** (`[[Whole-Bird-Roasting-And-Crisp-Poultry-Skin]]`, `[[Rule-Whole-Bird-Breast-Vs-Leg-Thermal-Solutions]]`).
* **פתרונות קולינריים להאטת חימום החזה או שימור הלחות שלו:** קירור מוקדם של החזה בשקית קרח לשעה לפני הצלייה (Ice-packing), מיסוך החזה בנייר אלומיניום, השריה בתמלחת (Brining של 3%–6% מלח המפחיתה איבוד נוזלים בחצי; `[[Brining-Marinades-And-Protease-Tenderizers]]`), או פירוק ובישול החזה והכרעיים בנפרד.
* **דרישת בטיחות מחייבת**: עקב סיכון לסלמונלה וקמפילובקטר, בתקן המזון הסטנדרטי נדרשת מדידת ליבה של לפחות **74°C** בחלק העבה ביותר (`[[Rule-Poultry-Safe-Core-Temperature]]`), או עמידה בעקומת פסטור זמן-טמפרטורה מאומתת.
