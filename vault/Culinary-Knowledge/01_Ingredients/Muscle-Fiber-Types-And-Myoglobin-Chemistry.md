---
id: ING-MEAT-002
type: INGREDIENT
name: "סוגי סיבי שריר (אדומים מול לבנים) וכימיית מיוגלובין (Muscle Fiber Types & Myoglobin Chemistry)"
domain: INGREDIENTS
category: "חלבון מן החי"
composition:
  water_pct: 75.0
  protein_pct: 20.0
  fat_pct: 3.0
  carb_pct: 1.0
  ph_level: 5.5
physical_properties:
  density_g_cm3: 1.05
  thermal_conductivity: "MEDIUM"
  cellular_structure: "סיבי שריר משורטטים (Actin & Myosin) המסווגים לסיבים לבנים מהירים (גליקוליטיים) וסיבים אדומים איטיים (חמצוניים עתירי מיוגלובין)"
sensory_profile:
  dominant_taste: ["UMAMI", "IRON_MINERAL", "SAVORY"]
  aroma_compounds: ["lactones", "sulfur_heterocycles", "lipid_oxidation_volatiles"]
  raw_texture: "ELASTIC_FIBROUS"
storage_and_safety:
  shelf_life_days_refrigerated: 3
  minimum_internal_temp_c: 63.0
  allergens: []
  kashrut_class: "MEAT"
relationships:
  - type: AFFECTS
    target_id: "ING-MEAT-001"
    target_name: "[[Beef-Chuck-Collagen-Rich]]"
  - type: AFFECTS
    target_id: "ING-POUL-001"
    target_name: "[[Poultry-Breast-Lean]]"
  - type: AFFECTS
    target_id: "SCI-MEAT-001"
    target_name: "[[Meat-Thermal-Progression-And-Doneness-Spectrum]]"
  - type: AFFECTS
    target_id: "SCI-MEAT-004"
    target_name: "[[Sausage-Emulsions-Myosin-And-Nitrite-Curing]]"
  - type: AFFECTS
    target_id: "FLV-MEAT-001"
    target_name: "[[Meat-Flavor-Precursors-Feed-And-Warmed-Over-Flavor]]"
  - type: AFFECTS
    target_id: "EQP-MEAT-001"
    target_name: "[[Radiant-Grilling-Smoking-And-Packaging-Permeability]]"
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
    printed_pages: "pp. 129-136, 148-149"
    pdf_pages: "pp. 143-150, 162-163"
    claim_type: "DIRECT_SOURCE_CLAIM"
verification_status: VERIFIED
---

# סוגי סיבי שריר (אדומים מול לבנים) וכימיית מיוגלובין (Muscle Fiber Types & Myoglobin Chemistry)

## 1. הרכב תא השריר ומערכת הכיווץ (`DIRECT_SOURCE_CLAIM`, עמ' 129–130 / PDF 143–144)
שריר שלד רזה מורכב בממוצע מ-**75% מים**, **20% חלבון**, **3% שומן** וכ-**2% פחמימות (גליקוגן), מינרלים וחומצות אמינו חופשיות**. מערכת הכיווץ הפנימית בנויה משני חלבונים עיקריים:
* **מיוצין (`Myosin`):** חלבון מנועי גדול המסודר בחוטים עבים; מתחיל לעבור דנטורציה ולהיקרש סביב **50°C–55°C (120°F–130°F)**, והוא גם החלבון המסיס במלח היוצר את הדבק החלבוני בנקניקיות (`[[Sausage-Emulsions-Myosin-And-Nitrite-Curing]]`).
* **אקטין (`Actin`):** חלבון כדורי המסודר בחוטים דקים המחליקים לאורך המיוצין; עמיד יותר לחום ועובר דנטורציה וקרישה רק סביב **66°C–80°C (150°F–180°F)**, שלב שבו התאים מתכווצים בצפיפות ומאבדים את שארית המים החופשיים (`[[Meat-Thermal-Progression-And-Doneness-Spectrum]]`).

---

## 2. סיבים לבנים (Fast-Twitch) מול סיבים אדומים (Slow-Twitch) (`DIRECT_SOURCE_CLAIM`, עמ' 132–135 / PDF 146–149)
היחס בין שני סוגי סיבי השריר קובע את הצבע, תכולת השומן הפנימית, העסיסיות והטעם של כל נתח:

| מאפיין ביוכימי וקולינרי | סיבי שריר לבנים (`White / Fast-Twitch Glycolytic`) | סיבי שריר אדומים (`Red / Slow-Twitch Oxidative`) |
| :--- | :--- | :--- |
| **תפקיד פיזיולוגי** | התפרצויות כוח קצרות ומהירות (כגון בריחה של תרנגולת) | פעילות אירובית ממושכת, עמידה, הליכה ותעופה ארוכה |
| **מקור אנרגיה בתא** | **גליקוגן (פחמימה)** המפורק אנאירובית בתוך התא ללא צורך בחמצן | **חומצות שומן (טיפות שומן תוך-תאיות)** הנשרפות אירובית בנוכחות חמצן |
| **תכולת מיוגלובין וברזל** | **נמוכה מאוד** — צבע חיוור/לבן | **גבוהה מאוד** — צבע אדום עמוק עד כהה |
| **קוטר הסיב ורקמת חיבור** | סיבים **רחבים/עבים** יותר עם מעט קולגן ושומן | סיבים **דקים** יותר העשירים בטיפות שומן תוך-תאיות ולעיתים קרובות ביותר קולגן |
| **השלכה קולינרית וטעם** | מתבשל מהר, טעם עדין, מתייבש בקלות מעל 68°C (`[[Poultry-Breast-Lean]]`) | טעם בשרי עשיר ומורכב (עקב ריבוי שומנים וברזל המזרז חמצון; `[[Meat-Flavor-Precursors-Feed-And-Warmed-Over-Flavor]]`) |
| **דוגמאות מובהקות (עמ' 134)** | חזה תרנגולת והודו (**90% סיבים לבנים / 10% אדומים**), מותן חזיר ועגל צעיר | חזה ברווז בר (**80% סיבים אדומים**), חזה יונה/Squab (**85% סיבים אדומים**), שוקי עוף, בקר וטלה |

> [!NOTE] מדוע חזה ברווז וחזה יונה הם "בשר אדום" בעוד חזה עוף הוא לבן? (`DIRECT_SOURCE_CLAIM`, עמ' 134 / PDF 148)
> תרנגולות והודו כמעט אינם עפים ולכן שרירי החזה שלהם מכילים רק **10% סיבים אדומים**. ברווזים ויונים עפים למרחקים ארוכים, ולכן שרירי החזה שלהם מורכבים מ-**80%–85% סיבים אדומים** עתירי מיוגלובין ושומן, המתנהגים בצלייה כמו סטייק בקר (מוגשים במיטבם בדרגת מדיום-רייר).

---

## 3. ארבעת מצבי הצבע של פיגמנט המיוגלובין (`DIRECT_SOURCE_CLAIM`, עמ' 135–136, 148–149 / PDF 149–150, 162–163)
הפיגמנט המעניק לבשר את צבעו הוא **מיוגלובין (`Myoglobin`)** — חלבון אוגר חמצן המכיל אטום **ברזל (`Fe`)** במרכז טבעת הֶם (*Heme*). צבע הבשר החי והמבושל נקבע על ידי מצב החמצון של אטום הברזל והמולקולה הקשורה אליו:

1. **סגול-אדמדם כהה (`Deoxymyoglobin` — $\text{Fe}^{2+}$ ללא חמצן):**
   * מופיע בפנים נתח בשר טרי שזה עתה נחתך או בבשר הארוז **באריזת ואקום אטומה לחמצן** (`[[Radiant-Grilling-Smoking-And-Packaging-Permeability]]`). אטום הברזל במצב מחוזר ($\text{Fe}^{2+}$) ואינו קשור לחמצן.
2. **אדום בוהק (`Oxymyoglobin` — $\text{Fe}^{2+} + \text{O}_2$):**
   * כאשר פני הבשר נחשפים לאוויר (או נארזים בניילון חדיר לחמצן בחנות), מולקולת חמצן ($\text{O}_2$) נקשרת לברזל ($\text{Fe}^{2+}$) ויוצרת בתוך דקות גוון אדום דובדבן בוהק ("פריחה" / *Bloom*).
3. **חום-אפרפר (`Metmyoglobin` — $\text{Fe}^{3+} + \text{H}_2\text{O}$):**
   * בחשיפה ממושכת לאחוזי חמצן נמוכים, לאור, לטמפרטורה חמימה או למלח, אטום הברזל מאבד אלקטרון ומתחמצן מ-$\text{Fe}^{2+}$ ל-**$\text{Fe}^{3+}$**, הקושר מולקולת מים במקום חמצן והופך לחום-אפור.
   * בבישול רגיל סביב **60°C–65°C (140°F–150°F)**, חלבון המיוגלובין עובר דנטורציה, הברזל מתחמצן ל-$\text{Fe}^{3+}$ ויוצר פיגמנט חום-בז' של בשר עשוי (*Hemichrome*).
4. **ורוד יציב לחום (`Nitrosomyoglobin` / `Carboxymyoglobin` — $\text{Fe}^{2+} + \text{NO}$ או $\text{CO}$):**
   * כאשר אטום הברזל נקשר ל**תחמוצת החנקן ($\text{NO}$)** (מניטריט בכבישת קורנביף/נקניקים או מגזי בעירה בתנור גז/מעשנה) או ל**פחמן חד-חמצני ($\text{CO}$)** (בעישון עץ/פחמים), נוצר קומפלקס ורוד-אדום יציב שאינו הופך לחום גם בבישול מלא מעל 74°C — זהו המקור ל**"טבעת העשן" הוורודה (*Smoke Ring*)** בברביקיו ולגוון ורוד בעוף צלוי למרות שהגיע לטמפרטורת בטיחות מלאה (עמ' 149, 174 / PDF 163, 188; `[[Rule-Poultry-Safe-Core-Temperature]]`).

