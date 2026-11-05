---
id: RUL-MEAT-004
type: CULINARY_RULE
name: "בחירת שיטת ריכוך והעשרת לחות לפני בישול: תמלחת (Brining) מול מרינדה מול אנזימים (Pre-Cooking Tenderization Matrix)"
domain: DECISION_MAKING
rule_scope: "PRE_COOKING_TREATMENT"
trigger_conditions:
  food_class: "MEAT"
  observed_problem: "בחירה בין תמלחת מלח (Brine), המלחה יבשה (Dry Brine), מרינדה חומצית או אנזימי פירות לשיפור עסיסיות, רכות וטעם"
  cooking_phase: "PREPARATION"
recommended_action:
  action_code: "SELECT_BRINE_OR_SHALLOW_MARINADE"
  parameters:
    brine_salt_concentration_pct: "3_TO_6_PCT"
    expected_moisture_loss_reduction_pct: 50
    protease_active_temp_range_c: "60_TO_70C"
  explanation: "לשיפור עסיסיות וריכוך עומק בנתחים רזים השתמש בתמלחת (3%-6% מלח) או המלחה מוקדמת; השתמש במרינדה חומצית רק לתיבול פני שטח ולמניעת HCAs בגריל; הימנע מהשריה ארוכה באנזימי פירות טריים (אננס/פפאיה) ההופכים את פני הבשר לדייסה קמחית."
legitimate_methods_and_tradeoffs:
  - method: "השריה בתמלחת מלח רטובה (Wet Brining 3%-6% מלח — עמ' 155-156)"
    advantages: "מוסיפה ~10% למשקל הבשר החי ומפחיתה איבוד נוזלים בבישול ב-50% על ידי המסת מיוצין חלקית"
    tradeoffs: "מרטיבה את פני השטח ומדללת מעט את ריכוז הטעם הטבעי של הבשר (ניתן לפצות בציר/תבלינים בתמלחת וייבוש במקרר)"
  - method: "המלחה יבשה מוקדמת (Dry Salting / Koshering — עמ' 143, 155)"
    advantages: "ממיסה מיוצין ומשפרת אגירת מים מבלי להוסיף מים חיצוניים, ומייבשת את פני השטח להשחמה מעולה"
    tradeoffs: "אינה מוסיפה תוספת מים של 10% כמו תמלחת רטובה בחזה עוף/הודו רזה במיוחד"
  - method: "מרינדה חומצית עם עשבי תיבול ושמן זית (Acid-Antioxidant Marinade — עמ' 125, 155)"
    advantages: "מעניקה טעם עשיר לפני השטח ומפחיתה בעד 90% יצירת אמינים הטרוציקליים מסרטנים (HCAs) בצלייה על גריל"
    tradeoffs: "חודרת רק מילימטרים ספורים ליממה; השריה ארוכה מדי בחומצה חזקה הופכת את פני השטח לחמוצים ודייסתיים"
expected_effects:
  moisture_retention: "INCREASED_BY_50_PCT_WITH_BRINE"
  reaction_rate: "MYOSIN_SOLUBILIZATION_AND_HCA_INHIBITION"
scientific_rationale: "מלח בריכוז 3%-5.5% ממיס חלקית את חוטי המיוצין והאקטין ומגדיל אגירת מים; חומצה ואנזימי פירות (פפאין/ברומלין) חודרים רק לפני השטח וגורמים לפירוק-יתר קמחי בשכבה החיצונית (McGee 2004, pp. 125, 154-156)."
confidence: 96
verified_on: "2026-10-21"
exceptions:
  - "בנתחים דקים מאוד (מוקפץ/שיפודים) או נתחים מחוררים, מרינדה ואנזימי ג'ינג'ר/קיווי קצרי-מועד (15-30 דקות בלבד) יעילים משום שיחס שטח-הפנים לנפח גבוה"
relationships:
  - type: SUPPORTED_BY
    target_id: "SCI-MEAT-003"
    target_name: "[[Brining-Marinades-And-Protease-Tenderizers]]"
  - type: SUPPORTED_BY
    target_id: "CNF-MEAT-002"
    target_name: "[[Conflict-Octopus-Corks-Marinades-And-Breading-Myths]]"
  - type: SUPPORTED_BY
    target_id: "CON-SALT-001"
    target_name: "[[Pre-Salting-Steak-Timing]]"
  - type: SUPPORTED_BY
    target_id: "SAF-MEAT-001"
    target_name: "[[Meat-Pathogens-Blanch-Grinding-And-Carcinogens]]"
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
    printed_pages: "pp. 125, 154-156"
    pdf_pages: "pp. 139, 168-170"
    claim_type: "DIRECT_SOURCE_CLAIM"
verification_status: VERIFIED
---

# כלל החלטה: בחירת שיטת ריכוך והעשרת לחות לפני בישול — תמלחת מול מרינדה מול אנזימים (`RUL-MEAT-004`)

## 1. הצהרת הכלל המותנה (`IF / THEN / BECAUSE / EXCEPTIONS`)
* **אם (`IF`):** מבקשים לשפר את העסיסיות, הרכות או הטעם של בשר/עוף לפני הבישול:
  * **לשימור עסיסיות לעומק בנתחים עבים ורזים (עוף, הודו, צלעות חזיר):** **אז (`THEN`)** יש להשתמש ב**תמלחת (`Brining` של 3%–6% מלח, 30–60 גרם מלח לליטר מים)** או בהמלחה מוקדמת (`Dry Brining`), ולא במרינדה חומצית נטולת מלח.
  * **לתיבול פני שטח והגנה מפני חומרים מסרטנים בצלייה על גריל (`Grilling`):** **אז (`THEN`)** יש להשתמש במרינדה קצרה המשלבת חומצה מתונה, שמן זית ועשבי תיבול נוגדי חמצון (`[[Meat-Pathogens-Blanch-Grinding-And-Carcinogens]]`).
  * **לגבי אנזימי פירות טריים (`Papain`, `Bromelain`, `Ficin` מפפאיה, אננס או תאנים):** **אז (`THEN`)** יש להימנע מהשריה ממושכת של נתחים עבים במיץ פירות חי או באבקת פפאין.
* **משום ש (`BECAUSE`):**
  1. יוני המלח בתמלחת (3%–5.5%) חודרים לנתח, ממיסים חלקית את חוטי המיוצין והאקטין וחותכים ב-**50%** את אובדן הלחות בבישול (`[[Brining-Marinades-And-Protease-Tenderizers]]`, עמ' 155 / PDF 169).
  2. חומצות ומולקולות ארומה במרינדה חודרות רק **מילימטרים ספורים ליממה**, ועודף חומצה גורם לדנטורציה חומצית הסוחטת מים והופכת את פני השטח לחמוצים ודייסתיים (`[[Conflict-Octopus-Corks-Marinades-And-Breading-Myths]]`, עמ' 155 / PDF 169).
  3. אנזימי פפאין וברומלין מגיעים לשיא פעילותם ב-**60°C–70°C** בזמן החימום ומפרקים את השכבה החיצונית של הבשר ל**מרקם קמחי ומתפורר (`Mealy/Mushy`)** (עמ' 154–155 / PDF 168–169).
* **חריגים (`EXCEPTIONS`):**
  * בפרוסות דקות מאוד (מוקפץ/פاهיטס) השריה קצרה (15–30 דקות) במרינדה או בג'ינג'ר/קיווי יעילה משום שכל הנתח הוא "פני שטח".
  * אם משתמשים במחית אננס או קיווי במרינדה ארוכה רק לשם הטעם, **הרתחה קצרה של הפרי מראש** משביתה את אנזימי הפרוטאז ומונעת פגיעה במרקם הבשר.

