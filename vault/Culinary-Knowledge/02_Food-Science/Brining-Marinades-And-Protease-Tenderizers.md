---
id: SCI-MEAT-003
type: SCIENTIFIC_PRINCIPLE
name: "כימיה של השריה בתמלחת (Brining), מרינדות חומציות ואנזימי ריכוך צמחיים (Brining, Marinades & Protease Tenderizers)"
domain: FOOD_SCIENCE
category: "PROTEIN"
description: "השוואה מכניסטית בין השריית בשר בתמלחת (3%-6% מלח הממיס מיוצין ומפחית איבוד נוזלים ב-50%), מרינדות חומציות (חדירה שטחית בלבד) ואנזימי פרוטאז צמחיים (פפאין, ברומלין, פיצין)"
conditions:
  temperature_range_c:
    min: 2
    max: 70
  water_activity_aw:
    min: 0.90
    max: 0.99
  ph_range:
    min: 3.5
    max: 7.0
  catalysts: ["sodium_chloride_3_to_6_pct", "acid", "plant_proteases_papain_bromelain"]
effects:
  molecular_change: "תמלחת 3%-5.5% מלח ממיסה חלקית את חלבוני התמיכה והמיוצין ומרחיקה חוטי חלבון במטען חשמלי; אנזימים צמחיים גוזרים שרשראות חלבון ב-60-70°C"
  sensory_consequences:
    taste: ["SEASONED_CORE_FROM_BRINE", "SURFACE_TANG_FROM_MARINADE"]
    aroma: ["HERB_SPICE_SURFACE_AROMA"]
    color: "בשר מושרה בחומצה הופך לאטום וחיוור על פני השטח"
    texture: "תמלחת מעניקה עסיסיות מוגברת (+10% משקל חי, -50% איבוד בבישול); עודף חומצה או אנזימים יוצר פני שטח דייסתיים/קמחיים (Mealy/Mushy)"
exceptions:
  - "אסור להשתמש באננס, פפאיה, קיווי או תאנים טריים (לא מבושלים) במרינדה ממושכת — האנזימים יהפכו את פני הבשר לדייסה קמחית"
  - "מרינדות חומציות ושמן אינן חודרות לעומק הנתח (מילימטרים ספורים ביום בלבד)"
relationships:
  - type: AFFECTS
    target_id: "ING-POUL-001"
    target_name: "[[Poultry-Breast-Lean]]"
  - type: AFFECTS
    target_id: "FLV-TASTE-001"
    target_name: "[[Salt-Osmosis-And-Perception]]"
  - type: AFFECTS
    target_id: "CON-SALT-001"
    target_name: "[[Pre-Salting-Steak-Timing]]"
  - type: AFFECTS
    target_id: "CNF-MEAT-002"
    target_name: "[[Conflict-Octopus-Corks-Marinades-And-Breading-Myths]]"
  - type: ENABLES
    target_id: "RUL-MEAT-004"
    target_name: "[[Rule-Pre-Cooking-Tenderization-Brine-Marinade-Enzymes]]"
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
    printed_pages: "pp. 154-156"
    pdf_pages: "pp. 168-170"
    claim_type: "DIRECT_SOURCE_CLAIM"
verification_status: VERIFIED
---

# כימיה של השריה בתמלחת (`Brining`), מרינדות חומציות ואנזימי ריכוך צמחיים (Brining, Marinades & Protease Tenderizers)

## 1. השריה בתמלחת (`Brining` — 3% עד 6% מלח, עמ' 155–156 / PDF 169–170)
השריית נתחים רזים הנוטים להתייבש (חזה עוף, הודו שלם, צלעות חזיר) בתמיסת מלח חלשה היא השיטה המדעית היעילה ביותר להגדלת עסיסיות הבשר (`DIRECT_SOURCE_CLAIM`):
* **המנגנון המולקולרי של יוני המלח ($\text{Na}^+, \text{Cl}^-$):**
  1. בריכוז מלח של **~3% (30 גרם לליטר מים)**, המלח ממיס את החלבונים התומכים במבנה סיבי הכיווץ.
  2. בריכוז מלח של **~5.5% (55 גרם לליטר מים)**, המלח **ממיס חלקית את חוטי המיוצין והאקטין עצמם**.
  3. יוני הנתרן והכלור נקשרים לחלבוני השריר, מגדילים את דחיית המטענים החשמליים ביניהם ומרחיקים את החוטים זה מזה כך שיותר מולקולות מים נכנסות ונכלאות ברשת החלבון.
* **התוצאה הכמותית (`DIRECT_SOURCE_CLAIM`, עמ' 155 / PDF 169):**
  * הבשר החי סופג מים ומלח ומגדיל את משקלו ב-**10% או יותר**.
  * בזמן הבישול החלבונים הרפויים מתכווצים פחות, ו**אובדן הלחות בבישול נחתך בחצי (ירידה של ~50% באיבוד הנוזלים)**.
* **הוספת סוכר לתמלחת (1%–3%):** סוכר כמעט אינו משפיע על אגירת המים, אך מאזן את טעם המלח ומאיץ את השחמת פני השטח בתגובת מייאר (`[[Maillard-Reaction]]`).

---

## 2. מרינדות חומציות (`Acid Marinades`, עמ' 155 / PDF 169)
* **קצב חדירה איטי להפליא (`DIRECT_SOURCE_CLAIM`):** מולקולות חומצה, סוכר ותבלינים מסיסי-שמן חודרות לתוך רקמת שריר שלמה בקצב של **מילימטרים ספורים ליממה בלבד**. מרינדה היא אפוא **טיפול פני שטח** ולא טיפול עומק (אלא אם מחוררים את הבשר או פורסים אותו דק).
* **השפעת החומצה על המרקם:** חומצה (יין, חומץ, מיץ לימון, יוגורט) מערערת קשרים בחלבונים ובקולגן בשכבה החיצונית, אך בריכוז גבוה או בהשריה ארוכה מדי החומצה גורמת לחלבוני השטח לעבור דנטורציה חומצית, להצטופף ולסחוט החוצה מים — מה שהופך את השכבה החיצונית של הבשר ל**חמוצה, יבשה ודייסתית (`Sour and Mushy/Pasty`)** (`[[Conflict-Octopus-Corks-Marinades-And-Breading-Myths]]`).
* **יתרון בטיחותי של מרינדות חומציות ועשבי תיבול (עמ' 125 / PDF 139):** מרינדה חומצית המכילה נוגדי חמצון מפחיתה דרמטית יצירת אמינים הטרוציקליים מסרטנים (`HCAs`) בצלייה על גריל לוהט (`[[Meat-Pathogens-Blanch-Grinding-And-Carcinogens]]`).

---

## 3. אנזימי פרוטאז צמחיים ופטרייתיים (`Plant & Fungal Protease Tenderizers`, עמ' 154–155 / PDF 168–169)
פירות וצמחים מסוימים מכילים אנזימי **פרוטאז (`Proteases`)** הגוזרים ביעילות הן את סיבי השריר והן את סיבי הקולגן והאלסטין (`DIRECT_SOURCE_CLAIM`, עמ' 154–155 / PDF 168–169):

| אנזים פרוטאז | מקור צמחי | מאפייני פעילות תרמית והתנהגות בבישול |
| :--- | :--- | :--- |
| **פפאין (`Papain`)** | פפאיה (*Papaya*) — המרכיב הראשי באבקות "מרכך בשר" מסחריות | **שיא פעילות בחימום של 60°C–70°C (140°F–160°F)**! בטמפרטורת החדר או במקרר הוא פועל לאט מאוד, אך בזמן שהבשר מתחמם בתנור/במחבת הוא מפרק חלבונים בקצב מסחרר לפני שהוא עובר דנטורציה מעל 75°C |
| **ברומלין (`Bromelain`)** | אננס טרי (*Fresh Pineapple*) | פעיל מאוד בטווח 50°C–70°C; מיץ אננס חי (לא מפוסטר/משומר) מפרק במהירות את פני הבשר למרקם קמחי |
| **פיצין (`Ficin`)** | תאנים (*Figs*) | מפרק קולגן ואלסטין ביעילות גבוהה ב-60°C–70°C |
| **אקטינידין (`Actinidin`)** | קיווי (*Kiwifruit*) | פרוטאז עדין יותר הפעיל בטמפרטורות מתונות |
| **זינגיבאין (`Zingibain`)** | שורש ג'ינג'ר טרי (*Fresh Ginger*) | מפרק קולגן ושריר (בשימוש מסורתי במוקפצים אסייתיים) |

* **הסכנה המרכזית בשימוש באנזימים צמחיים (`Mealy / Mushy Surface`, עמ' 155 / PDF 169):** מאחר שהאנזימים הם מולקולות חלבון גדולות, הם אינם חודרים לעומק נתח עבה אלא נשארים בשכבה החיצונית (1–2 מ"מ). בזמן הבישול, כאשר הנתח חוצה את טווח 60°C–70°C, השכבה החיצונית מתפרקת ל**עיסה קמחית ומתפוררת (`Mealy/Mushy`)** בעוד פנים הנתח נשאר לא מטופל (`[[Rule-Pre-Cooking-Tenderization-Brine-Marinade-Enzymes]]`).

