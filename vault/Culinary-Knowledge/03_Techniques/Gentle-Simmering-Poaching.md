---
id: TEC-MOIST-001
type: COOKING_TECHNIQUE
name: "בישול עדין ובעבוע מבוקר (Gentle Simmering & Poaching)"
domain: TECHNIQUES
heat_environment: "MOIST"
heat_transfer_methods:
  - "CONVECTION"
  - "CONDUCTION"
recommended_equipment:
  - "סיר בעל תחתית עבה ומדחום נוזלים"
target_foods:
  - "ביצים וקרמים"
  - "דגים עדינים ופירות ים"
  - "קורקבנים, מרקים, קטניות ודגנים"
conditions:
  surface_temperature_min_c: 65
  cooking_medium: "WATER"
  duration_range: "Variable by ingredient (5-15 min for fish fillets; <=60 min for fish stock)"
effects:
  primary_outcome: "העברת חום אחידה ומתונה ללא פירוק מכני מאגרסיביות בועות הרתיחה"
  texture_change: "UNIFORM_TENDER_SET"
  moisture_loss_pct_estimate: 8.0
exceptions:
  - "אינו מייצר השחמת מייאר או קראסט פריך עקב מחסום ה-100°C של המים"
  - "במרק הדגים הפרובנסאלי בויאבז (Bouillabaisse) מבצעים רתיחה סוערת מכוונת של 10 דקות כדי לתחלב שמן זית בתוך ג'לטין הדגים (McGee 2004, p. 216)"
relationships:
  - type: REQUIRES
    target_id: "SCI-HEAT-001"
    target_name: "[[Heat-Transfer]]"
  - type: AFFECTS
    target_id: "SCI-PROT-002"
    target_name: "[[Protein-Denaturation-Coagulation]]"
  - type: INHIBITS
    target_id: "TEX-CRUST-001"
    target_name: "[[Surface-Browning]]"
  - type: AFFECTS
    target_id: "TEC-FISH-002"
    target_name: "[[Fish-Poaching-Fumet-Bouillabaisse-And-Steaming]]"
  - type: SUPPORTED_BY
    target_id: "SRC-MCGEE-2004"
    target_name: "[[SRC-MCGEE-2004]]"
sources:
  - source_id: "SRC-MCGEE-2004"
    citation: "McGee, On Food and Cooking (2nd Ed., 2004), Chapter 4: Fish and Shellfish & Chapter 14"
    book_title: "On Food and Cooking: The Science and Lore of the Kitchen"
    author: "Harold McGee"
    edition: "2nd Edition (Completely Revised and Updated)"
    publication_year: 2004
    chapter: "Chapter 4: Fish and Shellfish"
    printed_pages: "pp. 215-216"
    pdf_pages: "pp. 229-230 (Part 2 PDF pp. 4-5)"
    claim_type: "DIRECT_SOURCE_CLAIM"
verification_status: VERIFIED
---

# בישול עדין ובעבוע מבוקר (Gentle Simmering & Poaching)

## 1. תיאור הטכניקה (Overview)
בישול בנוזל בטמפרטורה מתחת לנקודת הרתיחה הסוערת (Poaching: **65°C–80°C**; Simmering: **85°C–94°C**). מונע התפרקות מכנית של חלבונים עדינים (כגון דגים וביצים) ומאפשר מיצוי טעמים צלול בצירים (`[[In-Shell-Egg-Simmering-And-Steaming]]`, `[[Fish-Poaching-Fumet-Bouillabaisse-And-Steaming]]`).

## 2. שליקת דגים וציר דגים לפי *On Food and Cooking* (`[[SRC-MCGEE-2004]]`, עמ' 215–216 / PDF 229–230)
* **פרוטוקול השליקה הדו-שלבי לדגים (`DIRECT_SOURCE_CLAIM`, עמ' 216):** הכנסת פילה דג לנוזל רותח-כמעט (לחיטוי מיידי של חיידקי פני השטח), הסרת הסיר מהאש והוספת נוזל קר להורדת הטמפרטורה ל-**65°C–70°C (150°F–160°F)** לבישול עדין ואחיד. קירור הדג כשהוא שקוע בנוזל השליקה מונע אידוי לחות מפני השטח ומשאיר אותו עסיסי יותר.
* **שליקה בשמן, חמאה או תחליב חמאה (`Oil / Beurre Monté Poaching`, עמ' 215–216):** מעניקה הולכת חום איטית ומתונה יותר ממים ומונעת לחלוטין קירור אידוי.
* **מגבלת 60 הדקות בציר דגים (`Fumet`, עמ' 215):** ציר מעצמות וראשי דגים (ללא זימים) מבושל בסיר גלוי במשך **עד שעה אחת בלבד** — בישול ארוך יותר ממיס מלחי סידן מעצמות הדג העדינות, המעכירים את הציר ומעניקים לו טעם גירי (`Chalky taste`).
