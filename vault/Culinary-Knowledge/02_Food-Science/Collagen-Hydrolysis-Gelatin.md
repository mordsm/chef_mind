---
id: SCI-PROT-001
type: SCIENTIFIC_PRINCIPLE
name: "הידרוליזה של קולגן לג'לטין (Collagen Hydrolysis to Gelatin)"
domain: FOOD_SCIENCE
category: "PROTEIN"
description: "פירוק תרמי-הידרוליטי של סלילי הקולגן הקשיחים ברקמת החיבור ליצירת ג'לטין מסיס ונימוח"
conditions:
  temperature_range_c:
    min: 60
    max: 95
  water_activity_aw:
    min: 0.85
    max: 1.0
  ph_range:
    min: 4.0
    max: 7.5
  catalysts: ["water", "time", "mild_acidity", "cathepsin_enzymes"]
effects:
  molecular_change: "פתיחת הסליל המשולש (Triple Helix) של סיבי הקולגן ושבירת קשרי המימן והפפטיד לשרשראות ג'לטין מסיסות במים"
  sensory_consequences:
    taste: ["SAVORY_FULLNESS"]
    aroma: []
    color: "שקוף-מבריק"
    texture: "נימוח, עסיסי ומצפה את החך (Mouthfeel עשיר)"
exceptions:
  - "בחום יבש ומהיר ללא נוזלים או זמן מספק, הקולגן מתכווץ ומתקשה במקום להתמוסס"
  - "אלסטין (Elastin) אינו קולגן ואינו מתפרק לג'לטין בשום טמפרטורת בישול"
relationships:
  - type: AFFECTS
    target_id: "TEX-TEND-001"
    target_name: "[[Collagen-Driven-Tenderness]]"
  - type: ENABLES
    target_id: "TEC-COMB-001"
    target_name: "[[Low-Slow-Braising]]"
  - type: AFFECTS
    target_id: "SCI-MEAT-001"
    target_name: "[[Meat-Thermal-Progression-And-Doneness-Spectrum]]"
  - type: ENABLES
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
    chapter: "Meat Fibres and Tenderness Factors"
    pages: "Chapter 2"
  - source_id: "SRC-MCGEE-2004"
    citation: "McGee, On Food and Cooking (2nd Ed., 2004), Chapter 3: Meat"
    book_title: "On Food and Cooking: The Science and Lore of the Kitchen"
    author: "Harold McGee"
    edition: "2nd Edition (Completely Revised and Updated)"
    publication_year: 2004
    chapter: "Chapter 3: Meat"
    printed_pages: "pp. 130-131, 147-153, 162-163"
    pdf_pages: "pp. 144-145, 161-167, 176-177"
    claim_type: "DIRECT_SOURCE_CLAIM"
verification_status: VERIFIED
---

# הידרוליזה של קולגן לג'לטין (Collagen Hydrolysis to Gelatin)

## מנגנון מדעי מפורט (Scientific Mechanism)
קולגן הוא חלבון מבני הבנוי כסליל משולש הדוק (Triple Helix) העוטף את סיבי השריר בנתחים עובדים (`[[Beef-Chuck-Collagen-Rich]]`), ומהווה כשליש מכלל החלבון בגוף בעל החיים (`[[SRC-MCGEE-2004]]`, עמ' 130 / PDF 144). בבישול בשר מתרחשים שני שלבים תרמיים מנוגדים ברקמת הקולגן (`[[Meat-Thermal-Progression-And-Doneness-Spectrum]]`, עמ' 148–152 / PDF 162–166):
1. **שלב ההתכווצות והסחיטה (סביב 60°C / 140°F):** מעטפות הקולגן מתכווצות לאורך הסיבים ולוחצות בעוצמה על תאי השריר, מה שגורם להפרשה פתאומית ומסיבית של מיצים החוצה ולהקשיית הנתח.
2. **שלב ההמסה לג'לטין (החל מ-60°C–70°C / 140°F–160°F ובקצב מהיר ב-80°C–90°C / 180°F–200°F):** בחימום ממושך בנוכחות מים, אנרגיית החום מנתקת את קשרי המימן וחלק מקשרי הצילוב בין הסלילים, ומולקולות המים מפרידות אותם לשרשראות **ג'לטין (Gelatin)** מסיסות הקושרות מים, מסמיכות את נוזלי הבישול ומעניקות תחושת עסיסיות עשירה בפה (`[[Collagen-Driven-Tenderness]]`).

## תנאי סף, השפעת גיל בעל החיים וטריגרים (Thresholds & Animal Age)
* **קשרי צילוב ותלות בגיל בעל החיים (`DIRECT_SOURCE_CLAIM`, עמ' 130–131 / PDF 144–145):** בבעלי חיים צעירים (עגל, טלה, עוף פטם) קשרי הצילוב בין סלילי הקולגן הם רופפים ורגישים לחום, ולכן הקולגן מתמוסס במהירות לג'לטין שופע (זו הסיבה שציר עגל מתקרש לג'ל חזק במיוחד). עם התבגרות בעל החיים, קשרי הצילוב הופכים לקוולנטיים וצפופים יותר — הקולגן מתכווץ בעוצמה רבה יותר ב-60°C ודורש שעות בישול ארוכות בהרבה כדי להתפרק (`[[Collagen-Time-Curve-By-Animal-Age]]`). בדגים, לעומת זאת, הקולגן דל בקשרי צילוב ומתמוסס כבר ב-**50°C–55°C (120°F–130°F)**.
* **החלשה אנזימטית ביישון (`[[Rigor-Mortis-DFD-Meat-And-Aging-Enzymes]]`):** אנזימי ה-**Cathepsins** בבשר מיושן מחלישים חלק מקשרי הצילוב של הקולגן (פעילותם מגיעה לשיא עד **50°C / 122°F** לפני שהם עוברים דנטורציה).
* **טמפרטורה וזמן**: תהליך קינטי תלוי-זמן — ב-60°C–65°C הוא דורש שעות רבות (כמו ב-`[[Sous-Vide-Precision-Cooking]]`), ב-**80°C–90°C (180°F–195°F)** בבישול קדרה מבוקר (`[[Low-Slow-Braising]]`, `[[Succulent-Braising-Stewing-And-Liquid-Cooling]]`) הוא מושלם תוך 2–3 שעות, ובסיר לחץ (120°C) תוך 35–45 דקות.
* **נוכחות מים**: חיונית לתגובת ההידרוליזה (בקיעת קשרים באמצעות מים).
