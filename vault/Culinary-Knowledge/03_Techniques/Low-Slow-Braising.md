---
id: TEC-COMB-001
type: COOKING_TECHNIQUE
name: "צלי קדרה ובישול ארוך בנוזל (Low-and-Slow Braising)"
domain: TECHNIQUES
heat_environment: "COMBINATION"
heat_transfer_methods:
  - "CONDUCTION"
  - "CONVECTION"
recommended_equipment:
  - "סיר כבד עם מכסה אטום (Dutch Oven)"
target_foods:
  - "נתחי שריר עתירי קולגן (כתף, שוק, אסאדו, קורקבנים)"
  - "ירקות שורש קשים"
conditions:
  surface_temperature_min_c: 80
  cooking_medium: "WATER"
  duration_range: "90-240 minutes (until collagen hydrolyzes)"
effects:
  primary_outcome: "הידרוליזה מלאה של קולגן לג'לטין וריכוך סיבי שריר עבים"
  texture_change: "FORK_TENDER / GELATINOUS_SUCCULENCE"
  moisture_loss_pct_estimate: 20.0
exceptions:
  - "אסור ליישם על נתחים רזים ודלי קולגן (כגון חזה עוף או פילה בקר) שכן הם יתייבשו לחלוטין"
relationships:
  - type: REQUIRES
    target_id: "SCI-PROT-001"
    target_name: "[[Collagen-Hydrolysis-Gelatin]]"
  - type: ENABLES
    target_id: "TEX-TEND-001"
    target_name: "[[Collagen-Driven-Tenderness]]"
  - type: ALTERNATIVE_TO
    target_id: "TEC-PREC-001"
    target_name: "[[Sous-Vide-Precision-Cooking]]"
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
    printed_pages: "pp. 161-163"
    pdf_pages: "pp. 175-177"
    claim_type: "DIRECT_SOURCE_CLAIM"
verification_status: VERIFIED
---

# צלי קדרה ובישול ארוך בנוזל (Low-and-Slow Braising)

## תיאור הטכניקה (Overview)
טכניקה משולבת הכוללת (אופציונלית) השחמה ראשונית בחום יבש לפיתוח תוצרי `[[Maillard-Reaction]]`, ולאחריה בישול איטי ומכוסה בנוזל מתון (80°C–90°C) לשם פירוק קולגן לג'לטין (`[[Collagen-Hydrolysis-Gelatin]]`, `[[Succulent-Braising-Stewing-And-Liquid-Cooling]]`).

## פרוטוקול ביצוע שלב-אחר-שלב (Execution Protocol)
1. זיהוי שהנתח אכן עשיר ברקמת חיבור (`[[Rule-Collagen-Cut-Moist-Heat]]`, `[[Beef-Chuck-Collagen-Rich]]`).
2. הוספת נוזל (ציר, מים, יין) וכיסוי הסיר (`[[Covered-Vs-Uncovered-Evaporation]]`).
3. **בקרת טמפרטורה דו-שלבית (`[[SRC-MCGEE-2004]]`, עמ' 162–163 / PDF 176–177):** התחלה בתנור מתון של **95°C–120°C (200°F–250°F)** למשך שעה–שעתיים לניצול שיא פעילות אנזימי ה-Cathepsins (עד 50°C), ולאחר מכן העלאה לבעבוע תת-רתיחתי עדין כך שטמפרטורת הבשר הפנימית תישמר סביב **80°C (180°F)** — לעולם לא ברתיחה סוערת (100°C) המייבשת ומכווצת את סיבי השריר.
4. **קירור בנוזל וספיגה חוזרת (`DIRECT_SOURCE_CLAIM`, עמ' 163 / PDF 177):** בסיום הבישול, הניחו לבשר להתקרר **בתוך נוזל הבישול** עד **50°C (120°F)** (או ללילה במקרר) כדי שיספוג מחדש את הנוזל הג'לטיני; הוציאו את הבשר מהסיר לפני צמצום הרוטב ברתיחה.
5. בדיקת רכות מכנית לצד מדידת טמפרטורת בטיחות (`[[Minimum-Internal-Temperatures]]`).
