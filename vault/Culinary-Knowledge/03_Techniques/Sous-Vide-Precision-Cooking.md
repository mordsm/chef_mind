---
id: TEC-PREC-001
type: COOKING_TECHNIQUE
name: "בישול סו-וויד מבוקר טמפרטורה (Sous-Vide Precision Cooking)"
domain: TECHNIQUES
heat_environment: "PRECISION"
heat_transfer_methods:
  - "CONVECTION"
  - "CONDUCTION"
recommended_equipment:
  - "סירקולטור תרמי מדויק ושקית אטומה בוואקום"
target_foods:
  - "נתחי בקר, עוף, דגים (למעט דגים עתירי פרוטאזות) וביצים"
conditions:
  surface_temperature_min_c: 50
  cooking_medium: "WATER"
  duration_range: "20 minutes (fish) to 48 hours (tough meat; requires validated time-temperature schedule)"
effects:
  primary_outcome: "שיווי משקל תרמי מדויק בכל עובי הנתח ללא גרדיאנט בישול-יתר חיצוני"
  texture_change: "EDGE_TO_EDGE_UNIFORM_TENDERNESS"
  moisture_loss_pct_estimate: 5.0
exceptions:
  - "מדידת טמפרטורה בודדת אינה מאמתת פסטור בסו-וויד; נדרשת טבלת זמן-טמפרטורה ועובי מאומתת"
  - "דגים ופירות ים עתירי אנזימי פרוטאז בשריר (סרדין, הרינג, מקרל, טונה, סלמון צ'אם, בקלה/פולאק, אמנון/טילפיה, שרימפס ולובסטר) הופכים לדייסתיים ומתפוררים (Mushy) בבישול איטי או בהחזקה ב-55°C–60°C (McGee 2004, pp. 211-212, 220)"
relationships:
  - type: REQUIRES
    target_id: "SAF-TEMP-001"
    target_name: "[[Minimum-Internal-Temperatures]]"
  - type: ALTERNATIVE_TO
    target_id: "TEC-COMB-001"
    target_name: "[[Low-Slow-Braising]]"
  - type: AFFECTS
    target_id: "SCI-FISH-001"
    target_name: "[[Fish-Thermal-Progression-Proteases-And-Sarcoplasmic-Glue]]"
  - type: AFFECTS
    target_id: "CNF-FISH-001"
    target_name: "[[Conflict-Fish-Slow-Cooking-Cephalopod-Dual-Window-And-Shells]]"
  - type: SUPPORTED_BY
    target_id: "SRC-MODCUIS-2011"
    target_name: "[[SRC-MODCUIS-2011]]"
  - type: SUPPORTED_BY
    target_id: "SRC-MCGEE-2004"
    target_name: "[[SRC-MCGEE-2004]]"
sources:
  - source_id: "SRC-MODCUIS-2011"
    citation: "Modernist Cuisine, Vol 1 (Food Safety) & Vol 2 (Sous Vide)"
  - source_id: "SRC-MCGEE-2004"
    citation: "McGee, On Food and Cooking (2nd Ed., 2004), Chapter 4: Fish and Shellfish"
    book_title: "On Food and Cooking: The Science and Lore of the Kitchen"
    author: "Harold McGee"
    edition: "2nd Edition (Completely Revised and Updated)"
    publication_year: 2004
    chapter: "Chapter 4: Fish and Shellfish"
    printed_pages: "pp. 211-212, 220"
    pdf_pages: "pp. 225-226, 234 (Part 1 PDF p. 225; Part 2 PDF pp. 1, 9)"
    claim_type: "DIRECT_SOURCE_CLAIM"
verification_status: VERIFIED
---

# בישול סו-וויד מבוקר טמפרטורה (Sous-Vide Precision Cooking)

## 1. תיאור הטכניקה (Overview)
בישול מזון ארוז בוואקום באמבט מים מבוקר תרמוסטטית. מאחר שטמפרטורת המים זהה לטמפרטורת היעד של ליבת המזון, לא נוצר בישול-יתר בשכבות החיצוניות.

## 2. דרישות בטיחות וחריג הפרוטאזות בדגים ופירות ים (`Safety & Fish Protease Exception`)
* **פסטור תלוי זמן, עובי וטמפרטורה**: בטמפרטורות נמוכות מסף ההשמדה המיידי (כגון מתחת ל-74°C בעוף או 63°C בבקר), בטיחות המזון תלויה בזמן ההחזקה בטמפרטורת הליבה בהתאם לעובי הנתח. לכן במערכת `chef_mind`, דיווח טמפרטורה בודד בסו-וויד **אינו** מאשר בטיחות תהליך ללא תוכנית פסטור מאומתת.
* **מלכודת 55°C–60°C בדגים ופירות ים עתירי פרוטאזות (`Mush-Prone Fish & Shellfish`, `[[SRC-MCGEE-2004]]`, עמ' 211–212, 220):** בעוד שסלמון אטלנטי מפתח בבישול איטי ב-50°C מרקם קסטרדי קטיפתי, במינים רבים של דגים וסרטנאים (**סרדין, הרינג, מקרל, טונה, סלמון צ'אם, בקלה/פולאק, וייטינג, אמנון/טילפיה, שרימפס ולובסטר**) מצויים בשריר אנזימי פרוטאז פעילים מאוד המגיעים לשיא פעילותם ב-**55°C–60°C (130°F–140°F)** ומפרקים את סיבי השריר למרקם דייסתי ומתפורר (`Mushy`) אם מבשלים אותם לאט או מחזיקים אותם בטווח טמפרטורות זה (`[[Fish-Thermal-Progression-Proteases-And-Sarcoplasmic-Glue]]`, `[[Rule-Fish-Target-Temperature-And-Protease-Management]]`).
