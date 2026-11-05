---
id: ING-MEAT-001
type: INGREDIENT
name: "נתחי שריר עתירי קולגן (כתף, שוק, קורקבנים)"
domain: INGREDIENTS
category: "חלבון מן החי"
composition:
  water_pct: 71.0
  protein_pct: 21.0
  fat_pct: 7.0
  carb_pct: 0.0
  ph_level: 5.6
physical_properties:
  density_g_cm3: 1.05
  thermal_conductivity: "MEDIUM"
  cellular_structure: "סיבי שריר עבים העטופים ברשת צפופה של רקמת חיבור (קולגן ואלסטין)"
sensory_profile:
  dominant_taste: ["UMAMI", "SAVORY"]
  aroma_compounds: ["thiazoles", "thiophenes"]
  raw_texture: "TOUGH_FIBROUS"
storage_and_safety:
  shelf_life_days_refrigerated: 3
  minimum_internal_temp_c: 63.0
  allergens: []
  kashrut_class: "MEAT"
relationships:
  - type: REQUIRES
    target_id: "SCI-PROT-001"
    target_name: "[[Collagen-Hydrolysis-Gelatin]]"
  - type: ENABLES
    target_id: "TEX-TEND-001"
    target_name: "[[Collagen-Driven-Tenderness]]"
  - type: AFFECTS
    target_id: "ING-MEAT-002"
    target_name: "[[Muscle-Fiber-Types-And-Myoglobin-Chemistry]]"
  - type: AFFECTS
    target_id: "SCI-MEAT-001"
    target_name: "[[Meat-Thermal-Progression-And-Doneness-Spectrum]]"
  - type: AFFECTS
    target_id: "TEC-MEAT-003"
    target_name: "[[Succulent-Braising-Stewing-And-Liquid-Cooling]]"
  - type: SUPPORTED_BY
    target_id: "SRC-BCCAMPUS-MEAT-2015"
    target_name: "[[SRC-BCCAMPUS-MEAT-2015]]"
  - type: SUPPORTED_BY
    target_id: "SRC-MCGEE-2004"
    target_name: "[[SRC-MCGEE-2004]]"
sources:
  - source_id: "SRC-BCCAMPUS-MEAT-2015"
    citation: "BCcampus, Meat Cutting and Processing for Food Service, 2015"
  - source_id: "SRC-MCGEE-2004"
    citation: "McGee, On Food and Cooking (2nd Ed., 2004), Chapter 3: Meat"
    book_title: "On Food and Cooking: The Science and Lore of the Kitchen"
    author: "Harold McGee"
    edition: "2nd Edition (Completely Revised and Updated)"
    publication_year: 2004
    chapter: "Chapter 3: Meat"
    printed_pages: "pp. 129-136, 150-154, 162-163"
    pdf_pages: "pp. 143-150, 164-168, 176-177"
    claim_type: "DIRECT_SOURCE_CLAIM"
verification_status: VERIFIED
---

# נתחי שריר עתירי קולגן (Collagen-Rich Working Muscles)

## תיאור כללי (Description)
נתחים שמקורם בשרירים עובדים הנושאים משקל או מבצעים פעולה מתמדת (כגון כתף בקר, שוק/אוסובוקו, אסאדו, צוואר וקורקבני עוף). שרירים אלו מתאפיינים במעטפת עבה של רקמת חיבור חלבונית מסוג קולגן. לפי *On Food and Cooking* (`[[SRC-MCGEE-2004]]`, עמ' 129–136 / PDF 143–150):
* **הרכב שריר בקר רזה ממוצע (`DIRECT_SOURCE_CLAIM`, עמ' 129 / PDF 143):** כ-**75% מים**, **20% חלבון**, **3% שומן** וכ-2% מינרלים, פחמימות וחומצות אמינו חופשיות.
* **סוג סיבי השריר (`[[Muscle-Fiber-Types-And-Myoglobin-Chemistry]]`):** שרירי תנועה ויציבה בבקר וטלה מורכבים ברובם מ**סיבים אדומים איטיים (Slow-twitch Oxidative Fibers)** העשירים במיוגלובין ($\text{Fe}^{2+}$) ובטיפות שומן תוך-תאיות המזינות פעילות אירובית ממושכת, ולכן הם עתירי טעם בשרי עמוק יותר מנתחי מותן (Loin).
* **שני חלבוני רקמת החיבור — קולגן מול אלסטין (`DIRECT_SOURCE_CLAIM`, עמ' 130–131 / PDF 144–145):**
  1. **קולגן (Collagen):** סליל משולש של שרשראות חלבון המחוברות בקשרי צילוב (Cross-links). סביב **60°C (140°F)** מעטפות הקולגן מתכווצות וסוחטות מיצים מתאי השריר, אך החל מ-**60°C–70°C (140°F–160°F)** ובקצב מהיר ב-**80°C–90°C (180°F–200°F)** בנוכחות מים, הקולגן מתמוסס ל**ג'לטין (Gelatin)** (`[[Collagen-Hydrolysis-Gelatin]]`).
  2. **אלסטין (Elastin):** חלבון גומי אלסטי מצהוב ועד לבן המצוי בדפנות כלי דם וברצועות צוואר/כתף (*Silverskin* / *Ligamentum nuchae*). **אלסטין אינו מתפרק ואינו מתרכך בשום טמפרטורת בישול במטבח**, ולכן חובה להסירו בסכין (Trimming) או לטחון/לקצוץ אותו מכנית לפני הבישול.

## התנהגות בבישול (Cooking Behavior)
* **חום יבש ומהיר**: גורם להתכווצות סיבי השריר ולאיבוד נוזלים עוד לפני שהקולגן מספיק להתפרק, מה שמניב מרקם קשה וסיבי (`[[Meat-Thermal-Progression-And-Doneness-Spectrum]]`).
* **חום רטוב וממושך (`[[Low-Slow-Braising]]`, `[[Succulent-Braising-Stewing-And-Liquid-Cooling]]`)**: בנוכחות מים ובטמפרטורה מעל 68°C (ובאופן מיטבי בטמפרטורת בשר פנימית של **80°C / 180°F** ללא רתיחה אגרסיבית) לאורך זמן, סלילי הקולגן עוברים הידרוליזה לג'לטין (`[[Collagen-Hydrolysis-Gelatin]]`), המעניק עסיסיות ומרקם נימוח (`[[Collagen-Driven-Tenderness]]`). קירור הבשר בתוך נוזל הבישול ל-**50°C (120°F)** מאפשר לנתח לספוג מחדש חלק ניכר ממיצי הג'לטין.
* **הבחנה בין בטיחות למרקם**: סף הבטיחות המיקרוביאלי (63°C בבקר שלם עם מנוחה, 74°C בעוף/קורקבנים) מושג זמן רב לפני שהנתח מתרכך קולינרית.
