---
id: SAF-EGG-001
type: SCIENTIFIC_PRINCIPLE
name: "בטיחות מזון בביצים — השמדת סלמונלה, פסטור מרנג ורעילות עופרת ב-Pidan (Egg Safety & Salmonella Protocols)"
title_he: "בטיחות מזון בביצים — השמדת סלמונלה, פסטור מרנג ורעילות עופרת ב-Pidan"
domain: FOOD_SAFETY
category: "MICROBIAL_AND_TOXICOLOGICAL_SAFETY"
book_title: "On Food and Cooking: The Science and Lore of the Kitchen"
author: "Harold McGee"
edition: "2nd Edition, Completely Revised and Updated"
publication_year: 2004
chapter: "Chapter 2: Eggs (Egg Allergies; Egg Safety: The Salmonella Problem; Safe Poached Eggs; Cream Theory; Cooked Meringues; Pidan)"
pdf_page: "94, 96-97, 105, 113, 122, 131"
printed_page: "80, 82-83, 91, 99, 108, 117"
knowledge_type: "SCIENTIFIC_FACT"
claim_type: "DIRECT_SOURCE_CLAIM"
description: "פרוטוקולי בטיחות מזון בביצים לפי מקג'י: משטרי זמן-טמפרטורה להשמדת Salmonella enteritidis (60°C ל-5 דקות או 70°C לדקה אחת), פסטור ביצה עלומה ב-65°C ל-15 דקות, אי-כשירות מרנג איטלקי להשמדת סלמונלה (מגיע רק ל-55–58°C) לעומת מרנג שווייצרי (75–78°C), מניעת נדידת פלסטיסייזרים לקרם חם, ואיסור תחמוצת עופרת ב-Pidan"
storage_and_safety:
  minimum_internal_temp_c: 70.0
  pasteurization_schedules:
    - "60°C (140°F) held for 5 minutes (runny yolk preserved)"
    - "70°C (160°F) held for 1 minute (hardened yolk)"
    - "65°C (150°F) water bath held for 15 minutes (never below 63°C/145°F) for safe poached eggs"
    - "55°C–60°C (130°F–140°F) controlled commercial in-shell/liquid pasteurization"
    - "75°C–78°C (170°F–175°F) Swiss meringue over water bath"
  chemical_hazards:
    - "Lead oxide (PbO) in traditional Pidan is a potent nerve toxin — use only 'no lead oxide' or zinc-cured eggs"
    - "Plastic wrap directly on warm fat-rich pastry creams leaches plasticizing chemicals — use waxed paper or buttered parchment"
  allergens:
    - "Ovalbumin in egg white — pediatricians recommend avoiding egg whites in infants under 1 year old (yolks are far less allergenic)"
effects:
  molecular_change: "השמדה תרמית של חיידקי Salmonella enteritidis מתחת או מעל סף קרישת החלמון בהתאם למשך ההחזקה"
  texture_change: "בפסטור של 55°C–60°C או החזקה ב-60°C ל-5 דקות החלמון נשאר נוזלי; ב-70°C לדקה החלמון מתמצק"
exceptions:
  - "במרנג איטלקי, למרות שסירופ הסוכר מורתח ל-115°C–120°C (240°F–250°F), איבוד החום לקערה, למטרפה ולאוויר גורם לכך שמסת הקצף מגיעה רק ל-55°C–58°C (130°F–135°F) — טמפרטורה שאינה מספיקה להשמדת סלמונלה! (McGee p. 108)"
relationships:
  - type: AFFECTS
    target_id: "ING-EGG-001"
    target_name: "[[Egg-Proteins-Yolk-Albumen]]"
    condition: "הגדרת תנאי אחסון וטיפול תרמי בטוח בביצים"
    evidence: "McGee 2004, Ch. 2, pp. 80, 82-83 (PDF pp. 94, 96-97)"
    confidence: 99
  - type: AFFECTS
    target_id: "TEC-EGG-002"
    target_name: "[[Poaching-Scrambling-And-French-Omelet-Control]]"
    condition: "פרוטוקול אמבט מים ב-65°C ל-15 דקות לביצה עלומה בטוחה"
    evidence: "McGee 2004, Ch. 2, p. 91 (PDF p. 105)"
    confidence: 99
  - type: AFFECTS
    target_id: "TEC-EGG-004"
    target_name: "[[Meringue-Souffle-And-Sabayon-Whipping]]"
    condition: "הבחנת בטיחות קריטית בין מרנג איטלקי (לא מפוסטר) למרנג שווייצרי (מפוסטר ב-75–78°C)"
    evidence: "McGee 2004, Ch. 2, p. 108 (PDF p. 122)"
    confidence: 99
  - type: COMPLEMENTARY_TO
    target_id: "SAF-TEMP-001"
    target_name: "[[Minimum-Internal-Temperatures]]"
    condition: "משלים את טבלאות הבטיחות של USDA עם משטרי זמן-טמפרטורה של מקג'י"
    evidence: "McGee 2004, Ch. 2, pp. 83, 91, 108"
    confidence: 99
  - type: SUPPORTED_BY
    target_id: "SRC-MCGEE-2004"
    target_name: "[[SRC-MCGEE-2004]]"
    note: "Chapter 2, Printed pp. 80, 82-83, 91, 99, 108, 117 (PDF pp. 94, 96-97, 105, 113, 122, 131)"
sources:
  - source_id: "SRC-MCGEE-2004"
    citation: "Harold McGee, On Food and Cooking (2nd Ed., 2004), Chapter 2: Eggs, Printed pp. 80, 82-83, 91, 99, 108, 117 (PDF pp. 94, 96-97, 105, 113, 122, 131)"
verification_status: VERIFIED
created_at: 2026-10-21
updated_at: 2026-10-21
---

# בטיחות מזון בביצים — השמדת סלמונלה, פסטור מרנג ורעילות עופרת ב-Pidan (`SAF-EGG-001`)

## 1. בקרת *Salmonella enteritidis* ומשטרי זמן-טמפרטורה בביצים
החל משנת 1985 זוהה החיידק *Salmonella enteritidis* כגורם תחלואה מרכזי בביצים, היכול להימצא גם בתוך ביצים שלמות, נקיות ומדורגות `Grade A` (עמ' מודפס 83 | PDF עמ' 97). מקג'י מפרט את משטרי הפסטור המדויקים (במיוחד עבור ילדים, קשישים ובעלי מערכת חיסון מוחלשת):

| שיטת בישול / הכנה | טמפרטורה ומשך החזקה | מצב החלמון / הקצף | האם משמיד *Salmonella*? | מקור בפרק 2 |
| :--- | :--- | :--- | :--- | :--- |
| **בישול מהיר למוצקות מלאה** | **`70°C` (`160°F`) למשך דקה אחת** | החלמון מתקשה (Hardens) | **כן — בטוח** | עמ' מודפס 83 (PDF 97) |
| **החזקה תרמית בחלמון נוזלי** | **`60°C` (`140°F`) למשך 5 דקות** | החלמון נשאר נוזלי (Runny) | **כן — בטוח** | עמ' מודפס 83 (PDF 97) |
| **פרוטוקול "ביצה עלומה בטוחה" (Safe Poached Egg)** | העברה לאחר השליקה לאמבט מים ב-**`65°C` (`150°F`) למשך 15 דקות** (לא מתחת ל-`63°C`) | החלמון נשאר רך ונוזלי | **כן — בטוח** | עמ' מודפס 91 (PDF 105) |
| **ביצה מפוסטרת מסחרית בקליפה / נוזל** | חימום מבוקר ב-**`55°C–60°C` (`130°F–140°F`)** | נאה (ירידה קלה בכושר הקצפה ואמולסיה) | **כן — מפוסטר** | עמ' מודפס 83–84 (PDF 97–98) |
| **מרנג איטלקי (Syrup-Cooked Meringue)** | סירופ ב-`115°C–120°C`, אך הקצף מגיע רק ל-**`55°C–58°C` (`130°F–135°F`)** | קצף יציב ומבריק | **לא! אינו מספיק להשמדת סלמונלה** | עמ' מודפס 108 (PDF 122) |
| **מרנג שווייצרי (Swiss / Meringue Cuite)** | חימום הקצף עם סוכר וחומצה באמבט מים ל-**`75°C–78°C` (`170°F–175°F`)** | קצף צפוף ויציב לזילוף | **כן — מפסטר את החלבונים** | עמ' מודפס 108 (PDF 122) |

---

## 2. סיכונים כימיים ואלרגניים נוספים בפרק 2
1. **אלרגיה לחלבון ביצה בתינוקות (Egg Allergies — עמ' מודפס 80 | PDF עמ' 94)**: החלבון `Ovalbumin` שבחלבון הביצה (Albumen) הוא הגורם המרכזי לאלרגיה לביצים; מערכת העיכול של תינוקות מתחת לגיל שנה טרם הבשילה במלואה ולכן רופאי ילדים ממליצים להימנע ממתן חלבון ביצה עד גיל שנה, בעוד **חלמון הביצה אלרגני הרבה פחות** ובטוח לרוב התינוקות.
2. **נדידת פלסטיסייזרים מניילון נצמד לקרם חם (עמ' מודפס 99 | PDF עמ' 113)**: כדי למנוע היווצרות קרום יבש על קרם פטיסייר חם, יש להצמיד לפניו **נייר שעווה (Waxed paper) או נייר אפייה משומן בחמאה** — **ולהימנע מניילון נצמד (Plastic wrap)**, משום שהכימיקלים המרככים בפלסטיק (Plasticizers) נוטים לנדוד לתוך מזונות עשירים בשומן!
3. **רעילות עופרת בביצי *Pidan* (עמ' מודפס 117 | PDF עמ' 131)**: אין לצרוך ביצי אלף השנים שהוכנו עם תחמוצת עופרת ($\text{PbO}$, רעלן עצבי חזק); יש לוודא כיתוב `"No Lead Oxide"` או שימוש באבץ ($\text{Zn}$).

