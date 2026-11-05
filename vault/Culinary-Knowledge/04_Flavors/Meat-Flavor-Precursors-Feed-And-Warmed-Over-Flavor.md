---
id: FLV-MEAT-001
type: SCIENTIFIC_PRINCIPLE
name: "קודמני טעם בבשר, השפעת מרעה מול דגנים (Skatole & Terpenes) וטעם לוואי של חימום חוזר (Meat Flavor, Feed & Warmed-Over Flavor)"
domain: FLAVORS
category: "PROTEIN"
description: "הכימיה של יצירת טעם הבשר (תגובת מייאר של חלבוני שריר מול חמצון שומנים ספציפי למין החיה), השפעת תזונת עשב מול דגנים, ומנגנון Warmed-Over Flavor (WOF) בחימום חוזר"
conditions:
  temperature_range_c:
    min: 4
    max: 180
  water_activity_aw:
    min: 0.50
    max: 0.99
  ph_range:
    min: 5.4
    max: 6.2
  catalysts: ["free_iron_from_myoglobin", "oxygen", "unsaturated_phospholipids", "rumen_microbes", "rosemary_antioxidants"]
effects:
  molecular_change: "מייאר בחלבונים יוצר את ליבת הטעם ה'בשרי' (Meaty); חמצון שומנים יוצר את חותמת המין (בקר/טלה/חזיר/עוף); ברזל חופשי ממיוגלובין מזרז חמצון פוספוליפידים בקירור וחימום חוזר (WOF)"
  sensory_consequences:
    taste: ["UMAMI_GLUTAMATE_IMP", "LACTIC_TANG", "METALLIC_IRON"]
    aroma: ["SPECIES_SPECIFIC_LIPID_VOLATILES", "GRASSY_SKATOLE_TERPENES", "CARDBOARD_WARMED_OVER_FLAVOR"]
    color: "ללא שינוי ישיר"
    texture: "ללא שינוי ישיר"
exceptions:
  - "בשר כבוש בניטריט (קורנביף, האם, בייקון) אינו מפתח Warmed-Over Flavor משום שהניטריט נועל את אטום הברזל במיוגלובין"
relationships:
  - type: AFFECTS
    target_id: "ING-MEAT-002"
    target_name: "[[Muscle-Fiber-Types-And-Myoglobin-Chemistry]]"
  - type: AFFECTS
    target_id: "ING-MEAT-003"
    target_name: "[[Offal-Organs-And-Animal-Fat-Saturation]]"
  - type: AFFECTS
    target_id: "SCI-CHEM-001"
    target_name: "[[Maillard-Reaction]]"
  - type: AFFECTS
    target_id: "SCI-MEAT-004"
    target_name: "[[Sausage-Emulsions-Myosin-And-Nitrite-Curing]]"
  - type: ENABLES
    target_id: "RUL-MEAT-005"
    target_name: "[[Rule-Freezing-Ice-Water-Thawing-And-WOF-Prevention]]"
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
    printed_pages: "pp. 131-132, 136-141, 145-146, 165-166"
    pdf_pages: "pp. 145-146, 150-155, 159-160, 179-180"
    claim_type: "DIRECT_SOURCE_CLAIM"
verification_status: VERIFIED
---

# קודמני טעם בבשר, השפעת מרעה מול דגנים (`Skatole & Terpenes`) וטעם לוואי של חימום חוזר (Meat Flavor, Feed & Warmed-Over Flavor)

## 1. החלוקה הדו-רכיבית של טעם וארומת הבשר (`DIRECT_SOURCE_CLAIM`, עמ' 131–132, 147–148 / PDF 145–146, 161–162)
בשר נא הוא בעל ארומה חלשה מאוד וטעם של חומצה לקטית, מלחים, ברזל מיוגלובין וחומצות אמינו/נוקלאוטידים אומאמיים (גלוטמט ו-`IMP` — *Inosine Monophosphate*). בבישול נוצרים שני ערוצי ארומה משלימים:
1. **ליבת הטעם ה"בשרי" האוניברסלית (`Meaty Core` — מתאי השריר הרזים):**
   * חימום חומצות אמינו, פפטידים (ובמיוחד ציסטאין המכיל גופרית) וסוכרים (גלוקוז/ריבוז מפירוק גליקוגן ו-ATP) בתאי השריר מפעיל את `[[Maillard-Reaction]]` (מעל 130°C–140°C) ויוצר תרכובות הטרוציקליות גופרתיות וחנקניות המעניקות את הארומה הבשרית הצלויה המשותפת לבקר, טלה, חזיר ועוף.
2. **חותמת המין הספציפית (`Species Character` — מרקמת השומן והפוספוליפידים):**
   * ההבדל הארומטי המובהק שבין בקר, כבש/טלה, חזיר ועוף נובע מ**חמצון תרמי של חומצות השומן וממולקולות מסיסות-שומן האגורות ברקמת השומן** (`[[Offal-Organs-And-Animal-Fat-Saturation]]`). לכן שריר רזה לחלוטין של בקר, חזיר וטלה דומה מאוד בטעמו, בעוד השומן שלהם נושא את חותמת המין הייחודית (למשל חומצות שומן מסועפות-שרשרת המקנות לכבש/טלה את הארומה האופיינית לו; עמ' 139 / PDF 153).

---

## 2. השפעת תזונת בעל החיים: מרעה עשב מול דגנים (`Forage/Pasture vs. Grain Diet`, עמ' 137–139 / PDF 151–153)
תזונת הבקר והצאן מעצבת באופן ישיר את הרכב השומן ואת מולקולות הריח הנאגרות בו (`DIRECT_SOURCE_CLAIM`):

| פרמטר ביוכימי וקולינרי | תזונת מרעה ועשב (`Grass / Forage-Fed`) | תזונת דגנים ותירס (`Grain-Fed`) |
| :--- | :--- | :--- |
| **תרכובות ארומה בשומן (`Skatole` & `Terpenes`, עמ' 137 / PDF 151)** | חיידקי הכרס מפרקים כלורופיל מהעשב ל**טרפנים (`Terpenes` / *Phytenes*)** עשבוניים, ומפרקים את חומצת האמינו טריפטופן ל**סקטול (`Skatole`)** — מולקולה ארומטית עזה המקנה לבשר ניחוח "מרעה/ציד" (*Grassy / Gamey / Barnyard*) | דגנים דלים בכלורופיל ומעודדים אוכלוסיית חיידקים שונה בכרס המייצרת מעט מאוד סקטול וטרפנים — ארומה **מתונה, נקייה וחמאתית** יותר |
| **הרכב חומצות השומן וצבע השומן** | יותר חומצות שומן **אומגה-3** רב-בלתי-רוויות ו**בטא-קרוטן** צהוב מהעשב (שומן בגוון קרם-צהבהב) | יותר שומן חד-בלתי-רווי ורווי, שיוש תוך-שרירי (*Marbling*) עשיר ושומן לבן בוהק |
| **פעילות גופנית וסיבי שריר** | תנועה מרובה במרעה $\rightarrow$ יותר מיוגלובין, יותר קולגן וטעם בשרי מרוכז יותר | תנועה מועטה $\rightarrow$ סיבים רכים יותר ופחות קשרי צילוב בקולגן |

* **ריח חזיר לא מסורס (`Boar Taint`, עמ' 139 / PDF 153):** בחזירים זכרים בוגרים לא מסורסים מצטברות בשומן שתי מולקולות נדיפות — **סקטול (`Skatole`)** מהמעי והורמון ה**אנדרוסטנון (`Androstenone`)** — היוצרות בעת החימום ריח חריף של זיעה ושתן (שאחוז ניכר מהאוכלוסייה רגיש אליו גנטית במיוחד).

---

## 3. טעם לוואי של חימום חוזר (`Warmed-Over Flavor — WOF`, עמ' 165–166 / PDF 179–180)
אחת התופעות המוכרות והמתסכלות במטבח היא שבשר צלוי (ובמיוחד הודו, עוף וחזיר) שהיה עסיסי ונהדר ביום הכנתו מפתח לאחר יום–יומיים במקרר וחימום חוזר **טעם וריח מעופשים, קרטוניים או דגיים (`Stale, Cardboard, Painty or Fishy Warmed-Over Flavor`)**:
* **המנגנון הכימי המדויק (`DIRECT_SOURCE_CLAIM`, עמ' 165–166 / PDF 179–180):**
  1. במהלך הבישול הראשון, החום שובר את חלבון המיוגלובין ומשחרר **יוני ברזל חופשיים ($\text{Fe}$)** אל תוך רקמת השריר.
  2. במקביל, החום פוגע בממברנות התאים העשירות ב**פוספוליפידים רב-בלתי-רוויים (`Unsaturated Membrane Phospholipids`)**.
  3. בזמן האחסון במקרר (וביתר שאת בעת החימום החוזר בנוכחות חמצן), הברזל החופשי פועל כקטליזטור המזניק **חמצון שומנים מהיר** של הפוספוליפידים לתרכובות אלדהידיות וקטוניות בעלות ריח קרטון ועיפוש.
  4. **מדוע עוף, הודו וחזיר נפגעים הכי קשה?** משום שהממברנות והשומן שלהם עשירים בהרבה בחומצות שומן רב-בלתי-רוויות לעומת בקר וטלה (`[[Offal-Organs-And-Animal-Fat-Saturation]]`).

### 5 שיטות מוכחות למניעת `Warmed-Over Flavor` (`DIRECT_SOURCE_CLAIM`, עמ' 166 / PDF 180; `[[Rule-Freezing-Ice-Water-Thawing-And-WOF-Prevention]]`):
1. **שימוש בעשבי תיבול נוגדי חמצון (`Antioxidant Herbs`):** הוספת **רוזמרין (`Rosemary`), מרווה (`Sage`), טימין (`Thyme`) או אורגנו (`Oregano`)** לבשר או לרוטב בולמת את חמצון השומנים על ידי הברזל החופשי.
2. **ציפוי ברוטב עשיר בתוצרי מייאר (`Maillard Reaction Products`):** תוצרי ההשחמה של תגובת מייאר בציר מצומצם או ברוטב צלי פועלים בעצמם כנוגדי חמצון חזקים ובו-זמנית מבודדים את פני הבשר מחמצן האוויר.
3. **עיטוף הדוק ללא אוויר או טבילה בנוזל/שומן (`Oxygen Exclusion`):** אריזת שאריות הבשר כשהן מכוסות ברוטב/ציר (כמו בצלי קדרה) או בניילון צמוד המוציא כיסי אוויר.
4. **צמצום השימוש במלח לפני אחסון ארוך:** מלח מאיץ חמצון שומנים (עמ' 143 / PDF 157).
5. **הגשת שאריות חזה עוף/הודו או רוסטביף קרות:** טמפרטורה קרה מדכאת את התנדפות מולקולות הריח המחומצנות ומונעת את האצת החמצון שמתרחשת בחימום החוזר.

