---
id: TEC-MEAT-004
type: COOKING_TECHNIQUE
name: "מנוחת הבשר, בישול שאריתי (Carryover Cooking) ופריסה נגד הסיבים (Resting, Carryover Cooking & Carving)"
domain: TECHNIQUES
heat_environment: "NONE"
heat_transfer_methods:
  - "CONDUCTION"
recommended_equipment:
  - "סכין פריסה ארוכה, דקה וחדה מאוד (Slicing / Carving Knife) ומדחום ליבה"
target_foods:
  - "כל נתחי הבשר והעוף הצלויים (סטייקים, רוסטביף, שוק טלה, עוף והודו שלמים)"
conditions:
  surface_temperature_min_c: 50
  cooking_medium: "AIR"
  duration_range: "5-10 minutes for steaks; 15-30 minutes for large roasts"
effects:
  primary_outcome: "השוואת מפל הטמפרטורות בנתח (Carryover 3-10°C), קירור המיצים ל-50°C להגדלת צמיגותם ומניעת שפיכתם על הקרש, וקיצור מכני של סיבי השריר בפריסה נגד הסיבים"
  texture_change: "JUICY_RETAINED / SHORT_TENDER_FIBERS"
  moisture_loss_pct_estimate: 3.0
exceptions:
  - "בנתחים דקים מאוד או בנתחים בעלי עור פריך במיוחד, כיסוי הדוק בנייר אלומיניום בזמן המנוחה ירכך את הקראסט באדים"
relationships:
  - type: AFFECTS
    target_id: "SCI-MEAT-001"
    target_name: "[[Meat-Thermal-Progression-And-Doneness-Spectrum]]"
  - type: AFFECTS
    target_id: "SCI-THERM-002"
    target_name: "[[Heat-Transfer]]"
  - type: AFFECTS
    target_id: "TEX-MEAT-001"
    target_name: "[[Two-Phase-Juiciness-And-Fiber-Compaction]]"
  - type: ENABLES
    target_id: "RUL-SAF-001"
    target_name: "[[Rule-Poultry-Safe-Core-Temperature]]"
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
    printed_pages: "p. 165"
    pdf_pages: "p. 179"
    claim_type: "DIRECT_SOURCE_CLAIM"
verification_status: VERIFIED
---

# מנוחת הבשר, בישול שאריתי (`Carryover Cooking`) ופריסה נגד הסיבים (Resting, Carryover Cooking & Carving)

## 1. בישול שאריתי ("Afterheat" / `Carryover Cooking`, עמ' 165 / PDF 179)
כאשר מוציאים בשר ממקור החום, השכבה החיצונית שלו חמה בהרבה ממרכזו (למשל 100°C–150°C בחוץ לעומת 52°C במרכז). על פי חוקי הולכת החום (`[[Heat-Transfer]]`), אנרגיית החום ממשיכה לזרום מהשכבה החיצונית הן אל האוויר והן **פנימה אל מרכז הנתח** (`DIRECT_SOURCE_CLAIM`, עמ' 165 / PDF 179):
* **בסטייקים ונתחים דקים:** טמפרטורת הליבה עולה במנוחה ב-**2°C–3°C (4°F–6°F)**.
* **בצלי בקר גדול או הודו שלם שנצלו בחום גבוה:** טמפרטורת הליבה עולה במנוחה בעד **10°C (20°F)**!
* **כלל מעשי:** חובה להוציא את הנתח ממקור החום כאשר טמפרטורת הליבה שלו **נמוכה ב-3°C עד 10°C** מטמפרטורת היעד הסופית (`[[Meat-Thermal-Progression-And-Doneness-Spectrum]]`). בצלייה דו-שלבית בתנור נמוך (`[[Two-Stage-Roasting-Flipping-And-Heat-Scaling]]`), מפל הטמפרטורות קטן בהרבה ולכן גם העלייה השאריתית קטנה יותר (1°C–3°C).

---

## 2. מדוע מנוחה של 10–20 דקות מונעת בריחת מיצים בחיתוך? (`DIRECT_SOURCE_CLAIM`, עמ' 165 / PDF 179)
אם פורסים צלי או סטייק מיד ביציאתו מהתנור/מחבת (כשפנים הנתח ב-60°C–70°C), שלולית גדולה של מיצים זורמת החוצה אל קרש החיתוך והבשר נותר יבש. כאשר מניחים לבשר לנוח עד שטמפרטורת הפנים שלו יורדת לכיוון **50°C (120°F)**:
1. **עליית צמיגות הנוזל והתמוססות חלבונים:** ככל שהמים והחלבונים המומסים בתוך הסיבים מתקררים מ-65°C ל-50°C, הנוזל הופך סמיך וצמיג יותר וזורם הרבה יותר לאט.
2. **הרפיית הלחץ התוך-סיבי:** השוואת הטמפרטורות מרפה את הלחץ המכני של השכבות החיצוניות על ליבת הנתח, וכושר אחזקת המים של השריר עולה משמעותית.

---

## 3. אומנות הפריסה (`Carving Across the Grain`, עמ' 165 / PDF 179)
* **חיתוך בניצב לסיבים (`Across the Grain`):** סיבי השריר ומעטפות הקולגן שלהם עמידים מאוד לקריעה לאורכם אך נפרדים בקלות לרוחבם. חיתוך בניצב לכיוון הסיבים (או באלכסון של 45° בנתחים דקים) מקצר מכנית את הסיבים לאורך של מילימטרים ספורים, כך שהשיניים מפרידות בין צרורות הסיבים במקום ללעוס סיבים ארוכים (`[[Two-Phase-Juiciness-And-Fiber-Compaction]]`).
* **סכין חדה ודקה:** סכין קהה או משוננת קורעת ומועכת את תאי השריר כמו ספוג נסחט ומשחררת מיצים על הקרש; להב חלק וחד חותך מבלי לסחוט.
* **ניצול מיצי הקרש (`Jus`):** איסוף המיצים שניגרו על קרש החיתוך, טריפתם עם מעט שמן זית או חמאה מומסת ויציקתם חזרה על הפרוסות מחזירים לבשר לחות ושומן עתירי טעם (עמ' 165 / PDF 179).

