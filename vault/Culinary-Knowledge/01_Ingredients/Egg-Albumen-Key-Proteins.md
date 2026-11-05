---
id: ING-EGG-002
type: INGREDIENT
name: "חלבוני האלבומין המרכזיים בביצה (Key Egg White Proteins: Ovalbumin, Ovotransferrin, Ovomucin)"
title_he: "חלבוני האלבומין המרכזיים בביצה (Key Egg White Proteins)"
domain: INGREDIENTS
category: "חלבון מן החי — תת-רכיבים ביוכימיים"
book_title: "On Food and Cooking: The Science and Lore of the Kitchen"
author: "Harold McGee"
edition: "2nd Edition, Completely Revised and Updated"
publication_year: 2004
chapter: "Chapter 2: Eggs (The White)"
pdf_page: "91-92, 99, 115-117"
printed_page: "77-78, 85, 101-103"
knowledge_type: "INGREDIENT_PROPERTY"
claim_type: "DIRECT_SOURCE_CLAIM"
description: "מערכת שבעת חלבוני האלבומין בביצת תרנגולת, שכל אחד מהם מתאפיין בטמפרטורת דנטורציה שונה, מטען חשמלי ייחודי ותפקיד מבני נפרד בקרישה, בהקצפה ובהגנה אנטי-מיקרוביאלית"
composition:
  water_pct: 89.0
  total_protein_pct: 10.3
  glucose_g_per_egg: 0.25
  albumen_proteins_breakdown_pct:
    ovalbumin: 54.0
    ovotransferrin: 12.0
    ovomucoid: 11.0
    globulins: 8.0
    lysozyme: 3.5
    ovomucin: 1.5
    avidin: 0.06
    others: 10.0
effects:
  molecular_change: "קרישה מדורגת: Ovotransferrin מתמצק ראשון ב-60°C, Lysozyme ב-75°C, ו-Ovalbumin ב-80°C; בהקצפה מכנית גלובולינים ואובטרנספרין מייצבים קצף חי ואובלבומין מקבע אותו באפייה"
  texture_change: "מעבר מנוזל צמיג דו-שכבתי (חלבון סמיך פי 40 מחלבון דליל הודות ל-Ovomucin) לג'ל מוצק או לקצף יציב"
relationships:
  - type: AFFECTS
    target_id: "ING-EGG-001"
    target_name: "[[Egg-Proteins-Yolk-Albumen]]"
    condition: "קובע את תכונות החלבון בביצה השלמה"
    evidence: "McGee 2004, Ch. 2, pp. 77-78 (PDF pp. 91-92)"
    confidence: 99
  - type: ENABLES
    target_id: "SCI-PROT-002"
    target_name: "[[Protein-Denaturation-Coagulation]]"
    condition: "קרישה תרמית מדורגת בין 60°C ל-80°C"
    evidence: "McGee 2004, Ch. 2, pp. 77, 85 (PDF pp. 91, 99)"
    confidence: 99
  - type: ENABLES
    target_id: "SCI-FOAM-001"
    target_name: "[[Egg-Foam-Stability-Disulfide-And-Acid-Copper-Chemistry]]"
    condition: "Globulins ו-Ovotransferrin מייצבים קצף ראשוני; קבוצות הגופרית ב-Ovalbumin יוצרות קשרי S-S ומקבעות קצף בחום"
    evidence: "McGee 2004, Ch. 2, pp. 78, 101-103 (PDF pp. 92, 115-117)"
    confidence: 99
  - type: AFFECTS
    target_id: "FLV-EGG-001"
    target_name: "[[Egg-Sulfur-Volatiles-And-Ferrous-Sulfide-Greening]]"
    condition: "Ovalbumin הוא החלבון היחיד באלבומין בעל קבוצות גופרית ריאקטיביות המשחררות H2S מעל 60°C"
    evidence: "McGee 2004, Ch. 2, pp. 78, 87, 89 (PDF pp. 92, 101, 103)"
    confidence: 99
  - type: AFFECTS
    target_id: "GAP-EGG-001"
    target_name: "[[Egg-Albumen-Biological-And-Adhesion-Unknowns]]"
    condition: "תפקודם הקולינרי של Ovomucoid ו-Avidin ותפקידו הביולוגי המדויק של Ovalbumin מסומנים במקור כבלתי ידועים (?)"
    evidence: "McGee 2004, Ch. 2, pp. 77-78 (PDF pp. 91-92)"
    confidence: 95
  - type: SUPPORTED_BY
    target_id: "SRC-MCGEE-2004"
    target_name: "[[SRC-MCGEE-2004]]"
    note: "Chapter 2, Printed pp. 77-78, 85, 101-103 (PDF pp. 91-92, 99, 115-117)"
sources:
  - source_id: "SRC-MCGEE-2004"
    citation: "Harold McGee, On Food and Cooking (2nd Ed., 2004), Chapter 2: Eggs, Printed pp. 77-78, 85, 101-103 (PDF pp. 91-92, 99, 115-117)"
verification_status: VERIFIED
created_at: 2026-10-21
updated_at: 2026-10-21
---

# חלבוני האלבומין המרכזיים בביצה (`ING-EGG-002`)

## 1. טבלת חלבוני האלבומין ותפקודם הקולינרי
> מקור: *On Food and Cooking* (2004), פרק 2, עמ' מודפס 77–78 (PDF עמ' 91–92) — `DIRECT_SOURCE_CLAIM`:

| שם החלבון (Protein) | אחוז מכלל חלבוני האלבומין | תפקיד ביולוגי טבעי | תכונות קולינריות וטמפרטורת קרישה |
| :--- | :--- | :--- | :--- |
| **Ovalbumin (אובלבומין)** | **54%** | הזנה; חסימת אנזימי עיכול? (לא ידוע בוודאות) | מתמצק בחימום ל-**80°C (180°F)**; החלבון היחיד בעל קבוצות גופרית (`S-H`) ריאקטיביות (מקור טעם, ריח $\text{H}_2\text{S}$ וצבע); עמיד להקצפה מכנית אך מכפיל את חוזק דפנות הקצף באפייה; עמידותו לחום עולה בימים הראשונים לאחר ההטלה; האלרגן המרכזי בביצה |
| **Ovotransferrin (אובטרנספרין)** | **12%** | קשירת אטומי ברזל (מניעתם מחיידקים והובלתם בעובר) | החלבון הראשון שנקרש בחימום — כבר ב-**60°C (140°F)** או בהקצפה מכנית, ולכן קובע את סף ההתמצקות ההתחלתי של החלבון! כשנקשר לברזל מהחלמון עמידותו לחום עולה (לכן ביצה שלמה נקרשת ב-73°C); משנה צבע לזהוב בקערת נחושת או לוורוד בתוספת ברזל |
| **Ovomucoid (אובומוקואיד)** | **11%** | חסימת אנזימי עיכול | לא ידוע (`?` במקור — מתועד ב-`[[Egg-Albumen-Biological-And-Adhesion-Unknowns]]`) |
| **Globulins (גלובולינים)** | **8%** | איטום פגמים בממברנות ובקליפה? | מקציפים בקלות רבה ומייצבים את דפנות הבועות בקצף ביצים חי |
| **Lysozyme (ליזוזים)** | **3.5%** | אנזים המפרק דפנות תאי חיידקים | מתמצק בחימום ל-**75°C (170°F)**; מסייע בייצוב קצף |
| **Ovomucin (אובומוצין)** | **1.5%** | מסמיך את האלבומין; מעכב נגיפים | אחראי לכך שהחלבון הסמיך צמיג **פי 40** מהחלבון הדליל ויוצר מבנה שכבות (Laminations); מתפרק עם התיישנות הביצה והעלייה ב-pH; החלבון העמיד ביותר לחום (מיתרי הכלזה העשויים ממנו נשארים נוזליים במקושקשת גם אחרי ששאר הביצה נקרשה, עמ' 85) |
| **Avidin (אבידין)** | **0.06%** | קושר את הוויטמין ביוטין (מנוטרל בבישול) | לא ידוע (`?` במקור) |
| **אחרים (Others)** | **10%** | קשירת ויטמינים וחסימת אנזימים | לא ידוע (`?` במקור) |

---

## 2. תובנות קולינריות מרכזיות מחלוקת החלבונים
1. **פער של 20°C בין תחילת ההתמצקות להתמצקות מלאה**: מאחר ש-`Ovotransferrin` (12% מהחלבון) נקרש כבר ב-60°C–65°C ואילו `Ovalbumin` (54% מהחלבון) נקרש רק ב-80°C, ניתן לבשל ביצה עלומה או רכה בטמפרטורה של 63°C–68°C ולקבל חלבון יציב, עדין ונימוח מאוד מבלי להקשות את ה-`Ovalbumin` (עמ' מודפס 85 | PDF עמ' 99).
2. **עליית עמידות החום בביצה טרייה מאוד**: עמידותו של `Ovalbumin` לחום עולה במהלך הימים הראשונים לאחר ההטלה, ולכן ביצים שהוטלו באותו יום דורשות מעט פחות בישול לאותו מרקם מאשר ביצים בנות מספר ימים (עמ' מודפס 78 | PDF עמ' 92).
3. **הגנה אנטי-תזונתית המנוטרלת בבישול**: אלבומין נא הוא מגן כימי נגד חיידקים וטורפים (חוסם אנזימי עיכול וקושר ברזל וויטמינים כמו ביוטין), ולכן אכילת ביצה מבושלת חיונית לנטרול חלבוני ההגנה ולהפיכת הביצה למזון זמין ביולוגית (עמ' מודפס 77–78 | PDF עמ' 91–92).

