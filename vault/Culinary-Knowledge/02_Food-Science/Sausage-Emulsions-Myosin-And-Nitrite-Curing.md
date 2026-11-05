---
id: SCI-MEAT-004
type: SCIENTIFIC_PRINCIPLE
name: "תחליבי נקניקיות, מיצוי מיוצין וכבישה בניטריט (Sausage Emulsions, Myosin Extraction & Nitrite Curing)"
domain: FOOD_SCIENCE
category: "PROTEIN"
description: "הכימיה של מיצוי מיוצין במלח בנקניקיות טריות, ספי הטמפרטורה הקריטיים של נקניקיות מתחלבות (≤16°C לחזיר ו-≤21°C לבקר) ופעולת ניטריט הנתרן/תחמוצת החנקן בבשר כבוש"
conditions:
  temperature_range_c:
    min: 0
    max: 70
  water_activity_aw:
    min: 0.75
    max: 0.98
  ph_range:
    min: 5.2
    max: 6.4
  catalysts: ["sodium_chloride", "mechanical_mixing", "ice_cooling", "sodium_nitrite", "staphylococcus_starter"]
effects:
  molecular_change: "מלח ולישה מכנית ממיסים מיוצין ליצירת רשת ג'ל חלבונית הכולאת טיפות שומן ומים; ניטריט (NO2-) הופך ל-NO הקושר ברזל במיוגלובין ומונע חמצון ליפידים"
  sensory_consequences:
    taste: ["SAVORY_CURED_FLAVOR", "CLEAN_NON_RANCID_FAT"]
    aroma: ["SPICED_CURED_AROMA"]
    color: "ורוד-אדום קבוע ויציב לחום (Nitrosomyoglobin)"
    texture: "קפיצי, אחיד ועסיסי (או קמחי/מנוקב שומן אם התחליב נשבר בחימום יתר בזמן הטחינה)"
exceptions:
  - "בפרושוטו די פארמה וסן דניאלה (Parma & San Daniele Hams) מתקבל צבע אדום יציב ללא ניטריט הודות לחיידקי Staphylococcus טבעיים (מנגנון שנחקר כממצא מדעי חדש בעמ' 174)"
relationships:
  - type: AFFECTS
    target_id: "ING-MEAT-002"
    target_name: "[[Muscle-Fiber-Types-And-Myoglobin-Chemistry]]"
  - type: AFFECTS
    target_id: "SCI-PROT-002"
    target_name: "[[Protein-Denaturation-Coagulation]]"
  - type: AFFECTS
    target_id: "SAF-MEAT-001"
    target_name: "[[Meat-Pathogens-Blanch-Grinding-And-Carcinogens]]"
  - type: AFFECTS
    target_id: "GAP-MEAT-002"
    target_name: "[[Meat-Science-And-Cooking-Documented-Unknowns]]"
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
    printed_pages: "pp. 172-178"
    pdf_pages: "pp. 186-192"
    claim_type: "DIRECT_SOURCE_CLAIM"
verification_status: VERIFIED
---

# תחליבי נקניקיות, מיצוי מיוצין וכבישה בניטריט (Sausage Emulsions, Myosin Extraction & Nitrite Curing)

## 1. כימיית נקניקיות טריות: מלח ומיוצין כדבק חלבוני (`DIRECT_SOURCE_CLAIM`, עמ' 172–175 / PDF 186–189)
נקניקייה טרייה או קציצה קפיצית (בעלת **25%–30% שומן** ו-**1.5%–2% מלח ממשקל הבשר**) אינה סתם בשר קצוץ, אלא מערכת חלבונית מקושרת:
* **מיצוי מיוצין (`Myosin Extraction`):** כאשר מערבבים ולשים בשר קצוץ עם מלח (ונוזל קר כגון מים, יין או קרח כתוש), תמיסת המלח המרוכזת ממיסה מתוך תאי השריר את חלבון ה**מיוצין (`Myosin`)**. המיוצין המומס יוצר שכבה דביקה וצמיגה ("דבק חלבוני" / *Sticky Protein Glue*) העוטפת את חלקיקי הבשר ואת כדוריות השומן.
* **קרישה בחימום:** בזמן בישול הנקניקייה (מעל **50°C–60°C**), המיוצין המומס נקרש ל**ג'ל תלת-ממדי אלסטי** הכולא בתוכו את המים ואת השומן המותך ומונע מהם לברוח. ללא מלח ולישה מספקת, השומן והמים ייפרדו מהבשר בבישול והנקניקייה תהיה פירורית ויבשה.

---

## 2. נקניקיות מתחלבות (`Emulsified Batter Sausages`) וסיפי הטמפרטורה הקריטיים (`DIRECT_SOURCE_CLAIM`, עמ' 175–176 / PDF 189–190)
בנקניקיות בעלות מרקם חלק ואחיד כגון פרנקפורטר (*Frankfurters*), מורטדלה (*Mortadella*), בולוניה (*Bologna*) וקנאקוורסט, הבשר, השומן והקרח נטחנים במהירות גבוהה ל**תחליב בשר (`Meat Batter Emulsion`)** שבו מיוצין מומס מצפה מיליוני טיפות שומן מיקרוסקופיות:
* **סכנת חימום מחיכוך הלהבים ושבירת התחליב (`DIRECT_SOURCE_CLAIM`, עמ' 176 / PDF 190):**
  * חיכוך הלהבים המהירים מחמם את התערובת. אם השומן מתחיל להינתך בזמן הטחינה, או אם המיוצין מתחמם ועובר דנטורציה מוקדמת, טיפות השומן מתמזגות והתחליב נשבר (בבישול תיווצר נקניקייה גרגירית העטופה בכיסי שומן מותך וג'לי נפרד).
* **ספי הטמפרטורה המקסימליים המותרים בזמן טחינת הבלילה (`DIRECT_SOURCE_CLAIM`, עמ' 176 / PDF 190):**
  1. **תערובת מבוססת שומן חזיר (`Pork Fat Batter`):** אסור שטמפרטורת התערובת תעלה מעל **16°C (60°F)**! (שומן חזיר רך יותר ומתחיל להינתך מוקדם יותר).
  2. **תערובת מבוססת שומן בקר (`Beef Fat Batter`):** אסור שטמפרטורת התערובת תעלה מעל **21°C (70°F)**! (שומן בקר רווי וקשה יותר; `[[Offal-Organs-And-Animal-Fat-Saturation]]`).
  * לשם כך מקפיאים חלקית את הבשר והשומן מראש ומוסיפים את המים כ**קרח כתוש (`Crushed Ice`)** הסופג את חום החיכוך.

---

## 3. כימיה של כבישה במלח וניטריט (`Salt & Nitrite Curing`, עמ' 173–174, 176–178 / PDF 187–188, 190–192)
כבישת בשר (בייקון, האם, קורנביף, פסטרמה, סלמי) מבוססת על שילוב של **מלח שולחן ($\text{NaCl}$)** ורמות זעירות ומבוקרות של **ניטריט הנתרן (`Sodium Nitrite` — $\text{NaNO}_2$)** או ניטראט ($\text{NaNO}_3$, המומר לניטריט על ידי חיידקים בנקניקים יבשים ארוכי-הבשלה):
* **שלוש הפעולות הביוכימיות של הניטריט ($\text{NO}_2^- \rightarrow \text{NO}$, עמ' 173–174 / PDF 187–188):**
  1. **בטיחות מיקרוביאלית — עיכוב *Clostridium botulinum*:** ניטריט מונע נביטה ושגשוג של נבגי חיידק הבוטוליזם הקטלני בסביבה האנאירובית של נקניקים ובשרים כבושים (`[[Meat-Pathogens-Blanch-Grinding-And-Carcinogens]]`).
  2. **מניעת חמצון שומנים ושינוי הפרופיל הארומטי (`Cured Flavor`):** חנקן חד-חמצני ($\text{NO}$) קושר את אטום הברזל במיוגלובין ומונע ממנו לזרז חמצון שומנים (מונע עיפוש ו-Warmed-Over Flavor; `[[Meat-Flavor-Precursors-Feed-And-Warmed-Over-Flavor]]`), ויוצר את טעם ה"כבוש" המובחן (שהופך בבישול בשר חזיר מטעם צלי לטעם האם/בייקון).
  3. **קיבוע הצבע הוורוד (`Nitrosomyoglobin`):** ה-$\text{NO}$ נקשר לברזל של המיוגלובין ויוצר פיגמנט ורוד-אדום השומר על צבעו גם לאחר בישול (`[[Muscle-Fiber-Types-And-Myoglobin-Chemistry]]`).

> [!NOTE] תעלומת הצבע האדום בפרושוטו די פארמה ללא ניטריט (`Box: Red Ham Without Nitrite`, עמ' 174 / PDF 188)
> בירכי *Prosciutto di Parma* ו-*San Daniele* האיטלקיים המסורתיים נאסר שימוש בניטריט או ניטראט (משתמשים במלח ים בלבד), ובכל זאת הבשר מקבל צבע אדום-ורוד יציב לחום! חוקרים איטלקים גילו כי חיידקי *Staphylococcus* טבעיים על הבשר מייצרים פיגמנט אדום יציב שונה מניטרוזומיוגלובין, אם כי המנגנון הכימי המדויק שלו עדיין נחקר (`[[Meat-Science-And-Cooking-Documented-Unknowns]]`).

