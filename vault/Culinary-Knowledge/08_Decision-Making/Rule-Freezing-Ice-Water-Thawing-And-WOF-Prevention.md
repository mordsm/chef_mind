---
id: RUL-MEAT-005
type: CULINARY_RULE
name: "פרוטוקול הקפאה, הפשרה באמבט מי-קרח (פי 20 מהר מאוויר) ומניעת Warmed-Over Flavor בשאריות (Freezing, Thawing & WOF Prevention)"
domain: DECISION_MAKING
rule_scope: "STORAGE_THAWING_AND_REHEATING"
trigger_conditions:
  food_class: "MEAT"
  observed_problem: "אריזת בשר להקפאה ללא כוויות קור, הפשרה מהירה ובטוחה של בשר קפוא, או מניעת טעם לוואי מעופש (WOF) בחימום חוזר של בשר מבושל"
  cooking_phase: "STORAGE_AND_FINISHING"
recommended_action:
  action_code: "PACKAGE_IMPERMEABLE_THAW_IN_WATER_AND_BLOCK_LIPID_OXIDATION"
  parameters:
    freezing_wrap_material: "PVDC_SARAN_VACUUM_OR_FOIL_NOT_POLYETHYLENE"
    rapid_thaw_medium: "COLD_OR_ICE_WATER_BATH_20X_FASTER_THAN_AIR"
    unthawed_cooking_time_addition_pct: "30_TO_50_PCT"
    wof_inhibitors: ["rosemary", "sage", "thyme", "oregano", "maillard_gravy", "oxygen_exclusion"]
  explanation: "החלף ניילון סופרמרקט (Polyethylene חדיר לחמצן) בעטיפה אטומה (PVDC/ואקום/אלומיניום) לפני הקפאה; הפשר באמבט מים קרים (מוליך חום פי 20 מהר מאוויר); ומנע Warmed-Over Flavor בשאריות עוף/הודו/חזיר באמצעות רוזמרין/מרווה, כיסוי ברוטב מייאר או הגשה קרה."
legitimate_methods_and_tradeoffs:
  - method: "הפשרה באמבט מים קרים / מי קרח (Cold/Ice-Water Bath Thawing — עמ' 147)"
    advantages: "מים מעבירים חום פי 20 מהר יותר מאוויר — מפשיר מהר מאוד (פחות נזק תאי וטפטוף) תוך שמירה על טמפרטורה בטוחה מתחת לאזור הסכנה"
    tradeoffs: "דורש שהבשר יהיה ארוז בשקית אטומה לחלוטין למים"
  - method: "הפשרה איטית באוויר המקרר (Refrigerator Air Thawing — עמ' 147)"
    advantages: "נוחה ופסיבית לחלוטין לנתחים גדולים מאוד (כגון הודו שלם)"
    tradeoffs: "איטית פי 20 ממים (דורשת 24-48 שעות)"
  - method: "בישול ישיר ממצב קפוא ללא הפשרה (Cooking Unthawed — עמ' 147)"
    advantages: "חוסך לחלוטין את זמן ההפשרה בנתחים בעובי בינוני או בצלי קדרה"
    tradeoffs: "מאריך את זמן הבישול ב-30% עד 50% ודורש חום מתון יותר כדי שהחוץ לא יישרף לפני שהליבה מפשירה"
expected_effects:
  moisture_retention: "REDUCED_DRIP_LOSS_AND_NO_FREEZER_BURN"
  reaction_rate: "INHIBITED_IRON_CATALYZED_PHOSPHOLIPID_OXIDATION"
scientific_rationale: "ניילון פוליאתילן חדיר לחמצן ולכן גורם לכוויות קור וחמצון שומן בהקפאה; מים מוליכים חום פי 20 מאוויר; וחימום בשר משחרר ברזל ממיוגלובין המזרז חמצון פוספוליפידים בלתי-רוויים (WOF, חמור במיוחד בעוף/הודו/חזיר) הנבלם בנוגדי חמצון מרוזמרין/מרווה ובתוצרי מייאר (McGee 2004, pp. 145-147, 165-166)."
confidence: 97
verified_on: "2026-10-21"
exceptions:
  - "בשרים כבושים בניטריט (קורנביף, האם, בייקון) אינם סובלים מ-Warmed-Over Flavor משום שהניטריט נועל את הברזל במיוגלובין (עמ' 174)"
relationships:
  - type: SUPPORTED_BY
    target_id: "EQP-MEAT-001"
    target_name: "[[Radiant-Grilling-Smoking-And-Packaging-Permeability]]"
  - type: SUPPORTED_BY
    target_id: "FLV-MEAT-001"
    target_name: "[[Meat-Flavor-Precursors-Feed-And-Warmed-Over-Flavor]]"
  - type: SUPPORTED_BY
    target_id: "ING-MEAT-003"
    target_name: "[[Offal-Organs-And-Animal-Fat-Saturation]]"
  - type: SUPPORTED_BY
    target_id: "SCI-THERM-002"
    target_name: "[[Heat-Transfer]]"
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
    printed_pages: "pp. 145-147, 165-166"
    pdf_pages: "pp. 159-161, 179-180"
    claim_type: "DIRECT_SOURCE_CLAIM"
verification_status: VERIFIED
---

# כלל החלטה: פרוטוקול הקפאה, הפשרה באמבט מי-קרח ומניעת Warmed-Over Flavor בשאריות (`RUL-MEAT-005`)

## 1. הצהרת הכלל המותנה (`IF / THEN / BECAUSE / EXCEPTIONS`)
* **אם (`IF`):** מקפיאים בשר טרי, מפשירים בשר קפוא או מאחסנים ומחממים מחדש שאריות בשר מבושל:
  1. **בהקפאה:** **אז (`THEN`)** יש להסיר את ניילון הסופרמרקט הרגיל (`Polyethylene`) ולעטוף את הבשר ב**סרט אטום לחמצן וללחות (`PVDC / Saran`, שקית ואקום או רדיד אלומיניום עבה)**, ולהקפיא במהירות המקסימלית (עופות וחזיר לתקופה קצרה יותר מבקר).
  2. **בהפשרה:** **אז (`THEN`)** להפשרה מהירה ובטוחה יש לטבול את הבשר (בשקית אטומה) ב**אמבט מים קרים או מי קרח** (ולא להפשיר באוויר החדר או במיקרוגל), או לבשל ישירות ממצב קפוא תוך הוספת **30%–50% לזמן הבישול**.
  3. **באחסון וחימום חוזר של בשר מבושל (ובמיוחד הודו, עוף וחזיר):** **אז (`THEN`)** יש לתבל ב**רוזמרין, מרווה, טימין או אורגנו**, לאחסן את הבשר **מכוסה בנוזל/רוטב צלי עשיר בתוצרי מייאר** (ללא כיסי אוויר), או להגיש את השאריות קרות.
* **משום ש (`BECAUSE`):**
  * ניילון פוליאתילן בחנויות מיוצר בכוונה כחדיר לחמצן (לשמירת צבע `Oxymyoglobin` אדום בדלפק), ולכן במקפיא הוא מאפשר המראת קרח (**כוויות קור / `Freezer Burn`**) וחמצון שומנים (`[[Radiant-Grilling-Smoking-And-Packaging-Permeability]]`, עמ' 145–146 / PDF 159–160).
  * **מים מוליכים חום פי 20 מהר יותר מאוויר**, ולכן אמבט מים קרים מפשיר בשר במהירות גבוהה מבלי לחמם את פני השטח לטמפרטורות מסוכנות (עמ' 147 / PDF 161).
  * בישול משחרר יוני ברזל ($\text{Fe}$) מהמיוגלובין המזרזים חמצון מהיר של פוספוליפידים בלתי-רוויים בממברנות התאים ויוצרים טעם קרטוני מעופש (**`Warmed-Over Flavor`**), הנבלם על ידי נוגדי החמצון שבעשבי התיבול ובתוצרי מייאר (`[[Meat-Flavor-Precursors-Feed-And-Warmed-Over-Flavor]]`, עמ' 165–166 / PDF 179–180).
* **חריגים (`EXCEPTIONS`):**
  * בשר כבוש בניטריט (קורנביף, פסטרמה, האם, בייקון) חסין מ-Warmed-Over Flavor משום שהניטריט קושר את הברזל במיוגלובין ומונע חמצון שומנים (`[[Sausage-Emulsions-Myosin-And-Nitrite-Curing]]`, עמ' 174 / PDF 188).

