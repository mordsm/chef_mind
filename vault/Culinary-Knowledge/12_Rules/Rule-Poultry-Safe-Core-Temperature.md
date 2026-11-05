---
id: RUL-SAF-001
type: CULINARY_RULE
name: "אימות טמפרטורת ליבה בעוף ובשר במדחום (Safe Core Temperature Verification)"
domain: RULES
rule_scope: "FOOD_SAFETY"
trigger_conditions:
  food_class: "MEAT"
  observed_problem: "יש מדחום מזון מתאים ויודעים מהו סוג הבשר"
  cooking_phase: "FINISHING"
recommended_action:
  action_code: "MEASURE_THICKEST_PART_CORE"
  parameters:
    heat_adjustment: "MAINTAIN_UNTIL_SAFE_THRESHOLD"
    liquid_addition_ml: 0
    cover_vessel: false
  explanation: "מדוד בחלק העבה ביותר של הבשר או העוף, הרחק מעצם, שומן וסחוס, והשווה לסף הבטוח (74°C לעוף/קורקבנים, 71°C לבשר טחון מסחרי, 63°C עם 3 דקות מנוחה לנתח בקר שלם)."
expected_effects:
  moisture_retention: "OPTIMAL_WITHOUT_OVERCOOKING"
  reaction_rate: "PATHOGEN_LOG_REDUCTION"
scientific_rationale: "צבע הבשר וצבע המיצים אינם מדדים אמינים להשמדת פתוגנים (מיוגלובין עשוי להישאר ורוד עקב תחמוצת החנקן/פחמן חד-חמצני או להשחים מוקדם בבשר מיושן/טחון); רק מדידה במרכז התרמי של החלק העבה מאמתת הגעה לסף הבטיחות."
observations:
  - "דווח את סוג הבשר ואת הטמפרטורה הנמוכה ביותר שנמדדה בחלקים העבים"
safety_notes:
  - "אין לאשר שהבשר או העוף בטוחים להגשה ללא מדידת טמפרטורה שעומדת בסף של סוג החלבון"
tags:
  - "מדחום"
  - "טמפרטורה"
  - "בטיחות"
  - "עוף"
  - "בשר"
  - "thermometer"
  - "safety"
confidence: 95
verified_on: "2026-10-21"
exceptions:
  - "בהכנה ביתית של המבורגר מנתח בקר שלם שחוטא בחליטה במים רותחים ל-30–60 שניות לפני טחינה בכלים נקיים, פנים הנתח סטרילי מ-E. coli O157:H7 וניתן לבשלו לדרגת מדיום-רייר (McGee p. 154)"
relationships:
  - type: SUPPORTED_BY
    target_id: "SAF-TEMP-001"
    target_name: "[[Minimum-Internal-Temperatures]]"
  - type: SUPPORTED_BY
    target_id: "EQP-SENS-001"
    target_name: "[[Core-Probe-Thermometry]]"
  - type: SUPPORTED_BY
    target_id: "SAF-MEAT-001"
    target_name: "[[Meat-Pathogens-Blanch-Grinding-And-Carcinogens]]"
  - type: SUPPORTED_BY
    target_id: "SRC-USDA-FSIS-2024"
    target_name: "[[SRC-USDA-FSIS-2024]]"
  - type: SUPPORTED_BY
    target_id: "SRC-MCGEE-2004"
    target_name: "[[SRC-MCGEE-2004]]"
sources:
  - source_id: "SRC-USDA-FSIS-2024"
    citation: "USDA FSIS Food Thermometers & Safe Minimum Internal Temperature Chart"
  - source_id: "SRC-MCGEE-2004"
    citation: "McGee, On Food and Cooking (2nd Ed., 2004), Chapter 3: Meat"
    book_title: "On Food and Cooking: The Science and Lore of the Kitchen"
    author: "Harold McGee"
    edition: "2nd Edition (Completely Revised and Updated)"
    publication_year: 2004
    chapter: "Chapter 3: Meat"
    printed_pages: "pp. 125-126, 148-154"
    pdf_pages: "pp. 139-140, 162-168"
    claim_type: "DIRECT_SOURCE_CLAIM"
verification_status: VERIFIED
---

# כלל החלטה: אימות טמפרטורת ליבה בעוף ובשר במדחום (`RUL-SAF-001`)

## הצהרת הכלל המותנה (Conditional Rule Statement — `IF / THEN / BECAUSE / EXCEPTIONS`)
* **אם (`IF`):** בודקים מוכנות ובטיחות מיקרוביאלית של עוף, הודו, קורקבנים, בשר בקר/חזיר/טלה שלם או בשר טחון,
* **אז (`THEN`):** יש למדוד במדחום מזון (`[[Core-Probe-Thermometry]]`) בחלק העבה ביותר הרחק מעצם ושומן ולהתחשב בעליית החום השאריתית במנוחה (`[[Resting-Carryover-Cooking-And-Carving]]`),
* **משום ש (`BECAUSE`):** צבע הבשר וצבע המיצים אינם מדדים אמינים לבטיחות — מיוגלובין מחומצן למטמיוגלובין ($\text{Fe}^{3+}$) בבשר טחון משחים כבר ב-**60°C (140°F)** לפני השמדת *E. coli* O157:H7 (הדורש **68°C / 155°F** למספר שניות או **71°C / 160°F** מיידית), ומנגד עופות ונתחי בשר עשויים להישאר ורודים גם לאחר בישול מלא עקב תגובה עם גזי $\text{NO}$ או $\text{CO}$ בתנור או בגריל (`[[Muscle-Fiber-Types-And-Myoglobin-Chemistry]]`, `[[Meat-Pathogens-Blanch-Grinding-And-Carcinogens]]`, `[[SRC-MCGEE-2004]]`, עמ' 148–154 / PDF 162–168; `[[SRC-USDA-FSIS-2024]]`),
* **חריגים (`EXCEPTIONS`):**
  1. **פסטור זמן-טמפרטורה מבוקר:** השמדת חיידקים תלויה בשילוב של טמפרטורה וזמן החזקה (למשל *Trichina spiralis* בחזיר מושמד ב-**58°C / 137°F**, או בהקפאה של 20 יום ב-$\le -15^\circ\text{C} / 5^\circ\text{F}$; עמ' 126, 152 / PDF 140, 166).
  2. **שיטת החליטה-וטחינה להמבורגר מדיום-רייר בטוח (`DIRECT_SOURCE_CLAIM`, עמ' 154 / PDF 168):** בנתח בקר שלם החיידקים נמצאים על פני השטח החיצוניים בלבד; חליטת נתח שלם במים רותחים למשך **30–60 שניות** לפני טחינתו במטחנה נקייה משמידה את זיהום פני השטח ומאפשרת הכנת המבורגר בדרגת רייר/מדיום-רייר בבטיחות מוגברת.
