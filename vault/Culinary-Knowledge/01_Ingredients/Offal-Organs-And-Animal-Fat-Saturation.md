---
id: ING-MEAT-003
type: INGREDIENT
name: "איברים פנימיים (חלקי פנים) ומדרג רוויית שומן מן החי (Offal Organs & Animal Fat Saturation)"
domain: INGREDIENTS
category: "חלבון ושומן מן החי"
composition:
  water_pct: 70.0
  protein_pct: 18.0
  fat_pct: 10.0
  carb_pct: 2.0
  ph_level: 6.0
physical_properties:
  density_g_cm3: 1.04
  thermal_conductivity: "MEDIUM"
  cellular_structure: "חלוקה מבנית בין שרירים לא-שלדיים עתירי קולגן (קורקבן, לב, לשון, קיבה) לבין איברים בלוטיים/תאיים דלי קולגן (כבד, שקדים, מוח)"
sensory_profile:
  dominant_taste: ["UMAMI", "IRON_MINERAL", "SWEET_GLYCOGEN", "FATTY_RICH"]
  aroma_compounds: ["aldehydes", "pyrazines", "skatole", "unsaturated_lipid_volatiles"]
  raw_texture: "VARIES_BY_ORGAN"
storage_and_safety:
  shelf_life_days_refrigerated: 2
  minimum_internal_temp_c: 71.0
  allergens: []
  kashrut_class: "MEAT"
relationships:
  - type: AFFECTS
    target_id: "ING-MEAT-001"
    target_name: "[[Beef-Chuck-Collagen-Rich]]"
  - type: AFFECTS
    target_id: "SCI-PROT-001"
    target_name: "[[Collagen-Hydrolysis-Gelatin]]"
  - type: AFFECTS
    target_id: "FLV-MEAT-001"
    target_name: "[[Meat-Flavor-Precursors-Feed-And-Warmed-Over-Flavor]]"
  - type: AFFECTS
    target_id: "RUL-MEAT-001"
    target_name: "[[Rule-Collagen-Cut-Moist-Heat]]"
  - type: AFFECTS
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
    printed_pages: "pp. 131-132, 136-141, 145-146, 166-171"
    pdf_pages: "pp. 145-146, 150-155, 159-160, 180-185"
    claim_type: "DIRECT_SOURCE_CLAIM"
verification_status: VERIFIED
---

# איברים פנימיים (חלקי פנים) ומדרג רוויית שומן מן החי (Offal Organs & Animal Fat Saturation)

## 1. סיווג מבני של איברים פנימיים (`Offal / Variety Meats`, עמ' 166–171 / PDF 180–185)
הרולד מקג'י מחלק את חלקי הפנים לקבוצות מבניות מובחנות המתנהגות בחום באופן הפוך לחלוטין (`DIRECT_SOURCE_CLAIM`):

### א. שרירים לא-שלדיים ושרירים חלקים (Nonskeletal & Smooth Muscles — עתירי קולגן)
* **קורקבנים (`Gizzard`), לב (`Heart`), לשון (`Tongue`) וקיבה (`Tripe / Stomach`):**
  * **מבנה:** איברים המבצעים עבודה מכנית בלתי פוסקת ומכילים **עד פי 3 יותר קולגן** משריר שלד רגיל (עמ' 166, 169–170 / PDF 180, 183–184). הקיבה (*Tripe*) והקורקבן בנויים משריר חלק (*Smooth Muscle*) דק-סיבים המשובץ ברשת קולגן צפופה במיוחד.
  * **השלכה קולינרית:** בדומה לכתף ושוק (`[[Beef-Chuck-Collagen-Rich]]`), איברים אלו מחייבים **בישול לח וממושך** להמסת הקולגן לג'לטין (`[[Rule-Collagen-Cut-Moist-Heat]]`), למעט לב טרי שניתן גם לפרוס דק ולצרוב במהירות לדרגת מדיום-רייר לפני שהקולגן מתכווץ (עמ' 169 / PDF 183). הלשון עשירה גם בשומן (15%–25%) המעניק לה מרקם קטיפתי לאחר בישול ארוך וקילוף העור החיצוני.

### ב. איברים בלוטיים ותאיים (Glandular & Cellular Organs — דלי קולגן)
* **כבד (`Liver`, עמ' 166–168 / PDF 180–182):**
  * **מבנה:** איבר מטבולי המורכב מתאים כדוריים עתירי ברזל, ויטמינים וגליקוגן (סוכר כבד המעניק מתיקות קלה ומאיץ השחמת מייאר), עם **מעט מאוד קולגן וסיבי כיווץ**.
  * **השלכה קולינרית:** מאחר שאין בכבד קולגן שיתמוסס בבישול ארוך, חימום מעבר לדרגת מדיום-רייר/מדיום (60°C–65°C) גורם לחלבוני התאים להיקרש לצפיפות גירית, יבשה ומרירה. **כבד חייב להתבשל במהירות ובקצרה** (צריבה/טיגון קצר או אפיית פטה מתונה באמבט מים).
* **כבד אווז/ברווז שמן (`Foie Gras`, עמ' 167–168 / PDF 181–182):**
  * **מבנה:** מכיל **50%–65% שומן** האגור בטיפות בתוך תאי הכבד, הנמס בטווח של **45°C–70°C (115°F–160°F)**.
  * **השלכה קולינרית:** דורש אחד משני קצוות תרמיים — או בישול עדין מאוד לטרין (**50°C–60°C / 120°F–140°F**) כך שהשומן נשאר כלוא בתוך רשת החלבון העדינה, או צריבה לוהטת וקצרצרה של פרוסות עבות במחבת יבשה (דקה מכל צד) ליצירת קרום מייאר לפני שליבת השומן ניתכת לחלוטין.
* **שקדי עגל/טלה (`Sweetbreads` — בלוטת התימוס או הלבלב, עמ' 168 / PDF 182):**
  * בלוטה עדינה עשירה בחלבונים ורשת קולגן צעירה ועדינה; דורשת השריה במים קרים, חליטה מוקדמת במים מתובלים עם חומצה קלה למיצוק, הסרת הקרום, וצריבה מהירה בחמאה.
* **מוח (`Brains`, עמ' 168–169 / PDF 182–183):**
  * רקמה עצבית רכה במיוחד המורכבת מ-**80% מים, 10% שומן ורק 10% חלבון** (ללא קולגן כלל). מתפרק בקלות ודורש שליקה עדינה מתחת לסף הרתיחה לפני ציפוי וטיגון.
* **כליות (`Kidneys`, עמ' 169 / PDF 183):**
  * מחייבות **או הקפצה/צריבה מהירה מאוד בחום גבוה** (כדי שלא יתכווצו ויתקשו) **או בישול איטי וממושך** המרכך מחדש את מבנה הצינוריות הצפוף.

---

## 2. מדרג רוויית השומן מן החי ורגישות לחמצון (`DIRECT_SOURCE_CLAIM`, עמ' 131–132, 145–146 / PDF 145–146, 159–160)
רקמת השומן בבעלי חיים שונים נבדלת ביחס שבין חומצות שומן **רוויות (Saturated — מוצקות בטמפ' החדר ובעלות טמפ' התכה גבוהה)** לבין חומצות שומן **בלתי-רוויות (Unsaturated — רכות/נוזליות ורגישות מאוד לחמצון ועיפוש)**:

| סוג בעל החיים | אופי השומן וטמפרטורת התכה | רגישות לחמצון שומנים (`Rancidity`) ו-"Warmed-Over Flavor" |
| :--- | :--- | :--- |
| **בקר וטלה (`Beef & Lamb Tallow`)** | **הרווי והקשה ביותר** — מכיל חיידקי כרס (*Rumen bacteria*) ההופכים חומצות שומן בלתי-רוויות מהמזון לשומן רווי ומוצק (ועשיר בחומצה סטארית) | **הנמוכה ביותר** — חיי מדף ארוכים יותר בקירור ובהקפאה (אפשרות ליישון יבש של 30 יום בבקר; `[[Rigor-Mortis-DFD-Meat-And-Aging-Enzymes]]`) |
| **חזיר (`Pork Lard`)** | **ביניים** — בעל קיבה אחת, ולכן הרכב השומן משקף את תזונתו; רך ונמס בפה מהר יותר משומן בקר | **בינונית** — מתחמצן מהר יותר מבקר וטלה |
| **עופות (`Poultry Fat`)** | **בלתי-רווי ורך/נוזלי יחסית** — עשיר בחומצות שומן חד- ורב-בלתי-רוויות | **גבוהה** — נוטה להתעפש במהירות בקירור ובהקפאה ומפתח טעם לוואי מחומצן בחימום חוזר |
| **דגים (`Fish Oils`)** | **הכי רב-בלתי-רווי (אומגה-3)** — נוזלי גם בטמפרטורות קרות | **הגבוהה ביותר** |

* **כלל מדרג הרגישות לחמצון שומנים (`DIRECT_SOURCE_CLAIM`, עמ' 145 / PDF 159):**
  $$\text{Fish} > \text{Poultry} > \text{Pork} > \text{Lamb} > \text{Beef}$$
  משום כך שומן עוף וחזיר מתקלקלים בהקפאה מהר בהרבה משומן בקר, ומועדים במיוחד לטעם לוואי של חימום חוזר (`[[Meat-Flavor-Precursors-Feed-And-Warmed-Over-Flavor]]`, `[[Rule-Freezing-Ice-Water-Thawing-And-WOF-Prevention]]`).

