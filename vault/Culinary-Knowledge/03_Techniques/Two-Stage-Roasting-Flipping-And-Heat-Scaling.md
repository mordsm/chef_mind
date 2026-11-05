---
id: TEC-MEAT-001
type: COOKING_TECHNIQUE
name: "צלייה דו-שלבית, היפוך תכוף של סטייק וחוקי קנה-מידה בהעברת חום (Two-Stage Roasting, Frequent Flipping & Heat Scaling)"
domain: TECHNIQUES
heat_environment: "DRY"
heat_transfer_methods:
  - "CONDUCTION"
  - "CONVECTION"
  - "RADIATION"
recommended_equipment:
  - "מחבת ברזל יצוק כבדה או גריל קורן (לצריבה)"
  - "תנור מבוקר טמפרטורה ומדחום ליבה (Core Probe Thermometer)"
target_foods:
  - "נתחי סטייק עבים, המבורגרים ונתחי צלי רכים דלי קולגן (פילה, סינטה, אנטרקוט, שייטל, צלעות טלה/חזיר)"
conditions:
  surface_temperature_min_c: 140
  cooking_medium: "FAT"
  duration_range: "Proportional to Thickness Squared (L^2) or Weight^(2/3)"
effects:
  primary_outcome: "השחמת מייאר עשירה על פני השטח תוך שמירה על מפל טמפרטורות מתון וליבה אחידה בדרגת מדיום-רייר"
  texture_change: "CRISP_BROWNED_CRUST / UNIFORM_JUICY_INTERIOR"
  moisture_loss_pct_estimate: 12.0
exceptions:
  - "נתחים דקים מאוד (פחות מ-1.5 ס\"מ) מתבשלים בליבתם עוד לפני שפני השטח משחימים — דורשים חום קיצוני וייבוש מוקדם"
  - "כלל 'דקות לקילוגרם' (Minutes per pound) כושל כאשר משנים את צורת הנתח או עוביו"
relationships:
  - type: REQUIRES
    target_id: "SCI-MEAT-001"
    target_name: "[[Meat-Thermal-Progression-And-Doneness-Spectrum]]"
  - type: ENABLES
    target_id: "SCI-CHEM-001"
    target_name: "[[Maillard-Reaction]]"
  - type: AFFECTS
    target_id: "SCI-THERM-002"
    target_name: "[[Heat-Transfer]]"
  - type: AFFECTS
    target_id: "CON-MEAT-001"
    target_name: "[[Searing-Locks-In-Juices-Myth]]"
  - type: ENABLES
    target_id: "RUL-MEAT-002"
    target_name: "[[Rule-Tender-Vs-Tough-Cut-Thermal-Strategy]]"
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
    printed_pages: "pp. 156-159"
    pdf_pages: "pp. 170-173"
    claim_type: "DIRECT_SOURCE_CLAIM"
verification_status: VERIFIED
---

# צלייה דו-שלבית, היפוך תכוף של סטייק וחוקי קנה-מידה בהעברת חום (Two-Stage Roasting, Frequent Flipping & Heat Scaling)

## 1. הפיזיקה של היפוך תכוף וחימום מוקדם בסטייקים והמבורגרים (`DIRECT_SOURCE_CLAIM`, Box p. 156 / PDF p. 170)
בניגוד לכלל המסורתי הגורס כי "יש להפוך סטייק או המבורגר פעם אחת בלבד", המודל הפיזיקלי של העברת חום (שפותח על ידי הפיזיקאי ק. ג'. אוורט ומובא אצל מקג'י בעמ' 156 / PDF 170) מוכיח את ההפך:
* **היפוך תכוף מדי דקה (`Frequent Flipping`):** כאשר הופכים סטייק או המבורגר **בכל 30–60 שניות**, אף צד אינו מספיק לספוג עודף חום קיצוני או להתקרר יתר על המידה באוויר. התוצאה:
  1. הנתח מתבשל **עד 30% מהר יותר**.
  2. השכבה האפורה והמבושלת-יתר מתחת לקרום מצטמצמת למינימום, ופנים הנתח מתבשל באחידות רבה בהרבה.
* **חימום מוקדם מתון של סטייק לפני הצריבה (`Prewarming Steaks`, עמ' 156 / PDF 170):**
  * חימום מוקדם של סטייק ארוז בשקית בתוך מים חמימים (**40°C–50°C / 100°F–120°F**) למשך 30–60 דקות לפני הצריבה (טכניקה המהווה בסיס לסו-וויד ולריברס-סיר) מצמצם את הפרש הטמפרטורות שבין הפנים לחוץ, מזרז ריכוך אנזימטי על ידי `Calpains` ו-`Cathepsins` (`[[Rigor-Mortis-DFD-Meat-And-Aging-Enzymes]]`), ומאפשר צריבה קצרצרה במחבת לוהטת ללא ייבוש השכבות החיצוניות.

---

## 2. צלייה דו-שלבית בתנור (`Two-Stage Roasting`, עמ' 158–159 / PDF 172–173)
בנתחי צלי גדולים (רוסטביף, סינטה, אנטרקוט, שוק טלה), טמפרטורת תנור קבועה אחת יוצרת פשרה: תנור חם מדי (230°C) שורף ומייבש את השליש החיצוני של הנתח לפני שהליבה מגיעה ל-55°C, ואילו תנור נמוך מדי (110°C) אינו משחים את פני השטח (`[[Maillard-Reaction]]`). הפתרון הוא **הפרדת שלב השחמת השטח משלב חימום הליבה** (`DIRECT_SOURCE_CLAIM`, עמ' 158 / PDF 172):
1. **אופציה א' — צריבה בהתחלה ובישול בתנור מתון (`High-to-Low`):**
   * פתיחה בתנור לוהט (**230°C–260°C / 450°F–500°F**) ל-15–20 דקות (או צריבה במחבת) ליצירת קראסט מושחם, ואז הורדת חום התנור ל-**95°C–135°C (200°F–275°F)** להשלמת חימום הליבה במפל טמפרטורות מתון.
2. **אופציה ב' — תנור מתון בהתחלה והשחמה בסיום (`Low-to-High / Reverse Sear`, עמ' 158 / PDF 172):**
   * התחלה בתנור מתון (**95°C–120°C / 200°F–250°F**) עד שהליבה מתקרבת לטמפרטורת היעד, ואז סיום בחום גבוה מאוד (**250°C–260°C / 500°F** או במחבת לוהטת).
   * **היתרון המדעי של השחמה בסיום (`DIRECT_SOURCE_CLAIM`, עמ' 158 / PDF 172):** השהייה בתנור המתון מייבשת ומחממת מראש את פני השטח של הצלי, ולכן שלב ההשחמה הסופי קצר ויעיל יותר ומניב קרום פריך עם מינימום "טבעת אפורה" ומינימום המשך בישול שאריתי (`[[Searing-Locks-In-Juices-Myth]]`, `[[Resting-Carryover-Cooking-And-Carving]]`).

---

## 3. חוקי קנה-המידה של זמן הבישול: מדוע "דקות לקילוגרם" שגוי פיזיקלית (`Box: Cooking Time Depends on Meat Size and Shape`, עמ' 159 / PDF 173)
טבלאות בישול מסורתיות מציינות זמן צלייה ב"דקות לפאונד/קילוגרם", אך מקג'י מראה כי חוק הולכת החום (`[[Heat-Transfer]]`) קובע תלות שונה לחלוטין (`DIRECT_SOURCE_CLAIM`, עמ' 159 / PDF 173):
* **כלל 1 — זמן הבישול פרופורציונלי לריבוע העובי הקצר ביותר ($t \propto L^2$):**
  * בגליל או בנתח שטוח (כגון סטייק או פילה), החום חודר דרך הממד הדק ביותר ($L$). **הכפלת עובי הסטייק (מ-2 ס"מ ל-4 ס"מ) מאריכה את זמן הבישול פי 4 ($2^2 = 4$)!**
  * נתח ארוך וצר במשקל 2 ק"ג יתבשל מהר בהרבה מנתח כדורי ועבה במשקל 2 ק"ג.
* **כלל 2 — בנתחים בעלי צורה תלת-ממדית דומה, זמן הבישול פרופורציונלי למשקל בחזקת שני שלישים ($t \propto W^{2/3}$):**
  * אם שני עופות או שני צלי-בקר דומים בצורתם והאחד שוקל **פי 2** מהשני, עוביו גדול רק פי $\sqrt[3]{2} \approx 1.26$, ולכן זמן הבישול שלו מתארך רק ב-**~60% ($1.26^2 = 2^{2/3} \approx 1.59$)** — **ולא פי 2 (100%)** כפי שמניחה נוסחת "דקות לקילוגרם"!

