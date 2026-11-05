---
id: SCI-CHEM-003
type: SCIENTIFIC_PRINCIPLE
name: "כימיה של שימור ביצים במלח, חומצה ובסיס חזק — Pidan וביצים מומלחות (Alkali, Acid & Salt Egg Curing Chemistry)"
title_he: "כימיה של שימור ביצים במלח, חומצה ובסיס חזק (Pidan & Salted Eggs)"
domain: FOOD_SCIENCE
category: "INORGANIC_PROTEIN_TRANSFORMATION"
book_title: "On Food and Cooking: The Science and Lore of the Kitchen"
author: "Harold McGee"
edition: "2nd Edition, Completely Revised and Updated"
publication_year: 2004
chapter: "Chapter 2: Eggs (Pickled and Preserved Eggs)"
pdf_page: "129-131"
printed_page: "115-117"
knowledge_type: "SCIENTIFIC_FACT"
claim_type: "DIRECT_SOURCE_CLAIM"
description: "טרנספורמציות כימיות של חלבוני הביצה ללא בישול תרמי: קרישת חלמון בלבד בתמיסת מלח רוויה (35%), ו'תסיסה אי-אורגנית' בבסיס חזק (pH 12+) ההופכת את האלבומין לג'ל חום-שקוף ואת החלמון לקרם ירוק-כהה בביצי אלף השנים (Pidan)"
conditions:
  temperature_range_c:
    min: 15
    max: 70
  ph_range:
    min: 3.5
    max: 12.5
  catalysts: ["35_pct_salt_brine", "strong_alkali_ash_lime_lye_ph_12", "acetic_acid_vinegar"]
effects:
  molecular_change: "בתמיסת מלח 35% יוני Na+/Cl- ממסכים את חלבוני האלבומין ומונעים את קרישתם (החלבון נשאר נוזלי!) אך מצמידים את חלקיקי החלמון למוצק; ב-Pidan (pH 12+) הבסיס הקיצוני פותח חלבונים ויוצר עם יוני המלח ג'ל שקוף-חום (תגובת מייאר עם הגלוקוז) וברזל גופרי בחלמון"
  sensory_consequences:
    taste: ["מלוח-עשיר בביצים מומלחות; בסיסי, אומאמי וגופריתי ב-Pidan; חמוץ בביצים כבושות"]
    aroma: ["אמוניה ומימן גופרי ב-Pidan (מתמתנים באוורור לאחר קילוף)"]
    color: "ב-Pidan: חלבון בגוון תה/ענבר שקוף (ולעיתים גבישי 'פרחי אורן' לבנים ב-Songhuadan) וחלמון ירוק-ירקן כהה"
    texture: "חלבון ג'לטיני שקוף ואלסטי וחלמון קרמי ב-Pidan; חלבון קשיח/גומיי בכבישת חומץ (מתרכך בתוספת מלח ונוזל רותח)"
exceptions:
  - "בשיטת Nouveaux Pidan הטאיוואנית (8 ימים ב-5% מלח ו-4.2% סודה קאוסטית NaOH + חימום של 10 דקות ב-70°C), מתקבל ג'ל חלבון שקוף וחסר צבע לחלוטין עם חלמון זהוב ללא השחמה או הירקרקות (McGee p. 117)"
relationships:
  - type: AFFECTS
    target_id: "ING-EGG-001"
    target_name: "[[Egg-Proteins-Yolk-Albumen]]"
    condition: "שינוי מבנה החלבון והחלמון באמצעות יונים ו-pH קיצוני"
    evidence: "McGee 2004, Ch. 2, pp. 116-117 (PDF pp. 130-131)"
    confidence: 99
  - type: REQUIRES
    target_id: "SCI-PROT-002"
    target_name: "[[Protein-Denaturation-Coagulation]]"
    condition: "דנטורציה כימית במקום תרמית"
    evidence: "McGee 2004, Ch. 2, pp. 116-117 (PDF pp. 130-131)"
    confidence: 99
  - type: ENABLES
    target_id: "SCI-CHEM-001"
    target_name: "[[Maillard-Reaction]]"
    condition: "בסיסיות קיצונית (pH 12) מאיצה תגובת מייאר בטמפרטורת החדר בין חלבוני האלבומין ל-0.25g גלוקוז"
    evidence: "McGee 2004, Ch. 2, p. 117 (PDF p. 131)"
    confidence: 99
  - type: AFFECTS
    target_id: "SAF-EGG-001"
    target_name: "[[Egg-Salmonella-Pasteurization-And-Lead-Pidan-Hazards]]"
    condition: "סכנת הרעלת עופרת ב-Pidan מסורתי שהוכן עם תחמוצת עופרת (Lead Oxide)"
    evidence: "McGee 2004, Ch. 2, p. 117 (PDF p. 131)"
    confidence: 99
  - type: SUPPORTED_BY
    target_id: "SRC-MCGEE-2004"
    target_name: "[[SRC-MCGEE-2004]]"
    note: "Chapter 2, Printed pp. 115-117 (PDF pp. 129-131)"
sources:
  - source_id: "SRC-MCGEE-2004"
    citation: "Harold McGee, On Food and Cooking (2nd Ed., 2004), Chapter 2: Eggs, Printed pp. 115-117 (PDF pp. 129-131)"
verification_status: VERIFIED
created_at: 2026-10-21
updated_at: 2026-10-21
---

# כימיה של שימור ביצים במלח, חומצה ובסיס חזק (`SCI-CHEM-003`)

## 1. ביצים מומלחות (*Salted Eggs — Hulidan / Xiandan*): מדוע החלמון מתמצק והחלבון נשאר נוזלי?
בהשריית ביצים (בעיקר ביצי ברווז) בתמיסת מלח רוויה של **35% מלח** או במעטפת בוץ ומלח למשך 20–30 יום עד לשיווי משקל כימי, מתרחשת תופעה מפתיעה (עמ' מודפס 116 | PDF עמ' 130):
* **החלבון (Albumen) נשאר נוזלי לחלוטין**: הריכוז הגבוה מאוד של יוני נתרן ($\text{Na}^+$) וכלוריד ($\text{Cl}^-$) יוצר מעטפת מיסוך צפופה סביב חלבוני האלבומין המונעת מהם להיקשר זה לזה.
* **החלמון (Yolk) מתמצק לכדור מוצק וגרגירי**: המלח שואב מים מכדורי החלמון וגורם לחלקיקי ה-LDL להתלכד למסה מוצקה. ביצים אלו מבושלות לפני האכילה.

---

## 2. ביצי "אלף השנים" בכבישה בסיסית (*Pidan / Songhuadan*): "תסיסה אי-אורגנית"
בניגוד לשמן העממי, ביצי *Pidan* מיוצרות מזה כ-500 שנה בלבד ומבשילות תוך **1 עד 6 חודשים** בתערובת של **מלח וחומר בסיסי חזק** (אפר עצים, סיד $\text{CaO}$, סודה לכביסה $\text{Na}_2\text{CO}_3$ או סודה קאוסטית $\text{NaOH}$, לרוב עם תה ובוץ) המעלה את ה-pH של הביצה מ-9 ל-**12 ומעלה** (עמ' מודפס 116–117 | PDF עמ' 130–131):
1. **ג'ל חלבון שקוף בצבע חום-ענבר**: ה-pH הקיצוני פותח את חלבוני האלבומין ומעניק להם מטען שלילי חזק הדוחה אותם זה מזה, בעוד יוני המלח ממתנים את הדחייה בדיוק במידה המאפשרת יצירת **רשת ג'ל עדינה ושקופה לחלוטין** (בניגוד לג'ל האטום של ביצה מבושלת בחום). הצבע החום נוצר מהאצת **תגובת מייאר** בטמפרטורת החדר בין חלבוני האלבומין ל-0.25 גרם הגלוקוז שבחלבון!
2. **גבישי "פרחי אורן" (*Songhuadan*)**: בזן המובחר *Songhuadan*, הג'ל השקוף מנוקד בפרחים לבנים דמויי פתיתי שלג — אלו הם **גבישים של חומצות אמינו מותמרות** שהבסיס החזק פירק משרשראות האלבומין.
3. **חלמון קרמי בגוון ירוק-ירקן (Jade)**: הבסיס הקיצוני הורס את המבנה הכדורי של החלמון ומונע גרגיריות, ומאיץ תגובה בין גופרית מהחלבונים לברזל בחלמון ליצירת **ברזל גופרי ($\text{FeS}$)** בכל נפח החלמון (ולא רק על פני השטח כמו בביצה קשה).
4. **אזהרת בטיחות — תחמוצת עופרת ($\text{PbO}$)**: בעבר הוסיפו תחמוצת עופרת לתערובת הכבישה כדי שתיצור משקע שחור של עופרת גופריתית ($\text{PbS}$) האוטם בהדרגה את נקבוביות הקליפה ומעדן את הטעם; מכיוון שעופרת היא רעלן עצבי מסוכן, יש להשתמש אך ורק בביצים המסומנות `"No Lead Oxide"` או כאלו שהוכנו עם **אבץ (Zinc)** כתחליף בטוח (עמ' מודפס 117 | PDF עמ' 131).

