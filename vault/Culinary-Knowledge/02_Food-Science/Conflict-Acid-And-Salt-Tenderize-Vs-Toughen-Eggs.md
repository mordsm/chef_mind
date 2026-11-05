---
id: CNF-EGG-001
type: CONTRADICTORY_CLAIM
name: "יישוב סתירה: האם חומצה ומלח מקשים חלבוני ביצה או מרככים אותם? (Acid & Salt Tenderize vs. Toughen Eggs)"
title_he: "יישוב סתירה: האם חומצה ומלח מקשים חלבוני ביצה או מרככים אותם?"
domain: FOOD_SCIENCE
category: "CONFLICT_RESOLUTION"
book_title: "On Food and Cooking: The Science and Lore of the Kitchen"
author: "Harold McGee"
edition: "2nd Edition, Completely Revised and Updated"
publication_year: 2004
chapter: "Chapter 2: Eggs (Acids and Salt Tenderize; Salt in Egg Foams; Pickled Eggs)"
pdf_page: "100-101, 118, 130"
printed_page: "86-87, 104, 116"
knowledge_type: "CONTRADICTION_AND_CONDITIONAL_DIFFERENCE"
claim_type: "DIRECT_SOURCE_CLAIM"
description: "בירור הסתירה בין האמונה הרווחת במטבח שלפיה מלח וחומצה 'מקשים' ביצים לבין הממצא הכימי של מקג'י שלפיו מלח וחומצה מרככים ביצים מבושלות (אך מחלישים קצף חלבון חי ומקשים ביצים כבושות בחומץ ללא מלח)"
effects:
  molecular_change: "בבישול תרמי (מקושקשת/קסטרד): חומצה ומלח מנטרלים את המטען השלילי של חלבוני הביצה ולכן גורמים להם להיקשר בטמפרטורה נמוכה יותר בעודם מקופלים חלקית וללא קשרי גופרית הדוקים — התוצאה רכה יותר; בקצף חלבון חי: יוני מלח מתחרים על אתרי קשירה ומחלישים את הקצף"
  texture_change: "ריכוך מרקם בביצה מקושקשת ובקסטרד; החלשת יציבות בקצף מרנג חי; התקשות בביצה קשה המושרית שבועות בחומץ ללא מלח מספק"
relationships:
  - type: AFFECTS
    target_id: "SCI-PROT-002"
    target_name: "[[Protein-Denaturation-Coagulation]]"
    condition: "שינוי סף הטמפרטורה וצפיפות הקשרים ברשת החלבונית"
    evidence: "McGee 2004, Ch. 2, p. 86 (PDF p. 100)"
    confidence: 99
  - type: AFFECTS
    target_id: "SCI-FOAM-001"
    target_name: "[[Egg-Foam-Stability-Disulfide-And-Acid-Copper-Chemistry]]"
    condition: "ניגוד תפקודי: חומצה מייצבת קצף חלבון בעוד מלח מחליש קצף חלבון"
    evidence: "McGee 2004, Ch. 2, pp. 103-104 (PDF pp. 117-118)"
    confidence: 99
  - type: SUPPORTED_BY
    target_id: "SRC-MCGEE-2004"
    target_name: "[[SRC-MCGEE-2004]]"
    note: "Chapter 2, Printed pp. 86-87, 104, 116 (PDF pp. 100-101, 118, 130)"
sources:
  - source_id: "SRC-MCGEE-2004"
    citation: "Harold McGee, On Food and Cooking (2nd Ed., 2004), Chapter 2: Eggs, Printed pp. 86-87, 104, 116 (PDF pp. 100-101, 118, 130)"
verification_status: RECONCILED
created_at: 2026-10-21
updated_at: 2026-10-21
---

# יישוב סתירה: האם חומצה ומלח מקשים חלבוני ביצה או מרככים אותם? (`CNF-EGG-001`)

## 1. הצגת הסתירה (The Conflict)
* **הטענה המסורתית בספרי בישול (Claim A)**: "אין להוסיף מלח או חומצה לביצים לפני הבישול, משום שהם 'מקשים' (Toughen) את חלבוני הביצה וגורמים להפרדת נוזלים."
* **הממצא המדעי של מקג'י (Claim B — עמ' מודפס 86 | PDF עמ' 100)**: *"There's no truth to the common saying that acidity and salt 'toughen' egg proteins... Acids and salt make eggs thicken and coagulate at a lower cooking temperature, but actually produce a more tender texture."*

---

## 2. ההסבר המנגנוני והפרדת התנאים (Conditional Reconciliation)
מקג'י מראה כי הפרדוקס נובע מהבלבול בין **הקדמת זמן הקרישה** לבין **צפיפות הרשת הסופית**, וכן מהבדלים מותנים בין 4 סביבות קולינריות שונות:

| הקשר קולינרי | השפעת מלח ($\text{NaCl}$) | השפעת חומצה (לימון / חומץ / קרם טרטר) | המנגנון הכימי המדויק (לפי McGee Ch. 2) |
| :--- | :--- | :--- | :--- |
| **1. ביצה מקושקשת, חביתה וקסטרד (חימום תרמי)** | **מרכך את המרקם** ומוריד טמפרטורת קרישה | **מרכך מאוד את המרקם** ומוריד טמפרטורת קרישה | מיסוך המטען השלילי גורם לחלבונים להיקשר מוקדם יותר בחימום — **בעודם עדיין מגולגלים חלקית (Balled up)** ולפני שהם נפתחים לגמרי ומתפתלים בצפיפות; בנוסף חומצה מדכאת קשרי גופרית ($\text{S}-\text{S}$) (עמ' 86) |
| **2. קצף חלבון ביצה חי (Egg-White Foam)** | **מחליש את הקצף** ומאריך זמן הקצפה | **מייצב מאוד את הקצף** ומונע התגרגרות | יוני המלח מתחרים על אתרי קשירה בחלבונים הפתוחים ומחלישים את שלד הקצף (עמ' 104); לעומת זאת יוני $\text{H}^+$ מהחומצה מונעים קשרי $\text{S}-\text{S}$ עודפים בלי לפגוע בקשרים האחרים (עמ' 103) |
| **3. מי שליקה של ביצה עלומה (Poaching Water)** | מאיץ קרישה חיצונית (ומגביר צפיפות מים) | מאיץ קרישה חיצונית אך יוצר סיבים וקרום מחוספס | הוספת מלח וחומץ למי השליקה מאיצה את התמצקות החלבון החיצוני, אך יוצרת שרוכים וקרום לא אחיד על פני הביצה העלומה (אלא אם משתמשים בטכניקת ה"ריחוף" המקצועית בסיר עמוק, עמ' 90) |
| **4. ביצים קשות כבושות בחומץ (Pickled Eggs, 1–3 שבועות)** | **מרכך** את החלבון הכבוש | **מקשה** את החלבון המבושל למרקם גומיי | השריית ביצה קשה בחומץ בלבד למשך שבועות מורידה את ה-pH ומהדקת את הרשת שכבר נקרשה; הוספת **מלח רב** לתחמיץ רותח ממתנת את ההתקשות ויוצרת מרקם רך יותר (עמ' 116) |

---

## 3. דוגמאות היסטוריות ומעשיות מהפרק (עמ' מודפס 86–87 | PDF עמ' 100–101)
* **מטבח מרוקאי וערבי**: פאולה וולפרט וקלאודיה רודן מתעדות טריפת ביצים עם מיץ לימון או חומץ לפני בישול ארוך למניעת מרקם עורי/גומיי; הבסיסיות הטבעית של הביצה מנטרלת חלק מהחומצה האצטית הנדיפה כך שהטעם נשאר עדין להפתיע.
* **צרפת של המאה ה-17 (*Le Patissier françois*, 1690)**: ביצים מקושקשות עם מלח ומיץ ענבים חמוץ (*Verjus*) או מיץ לימון/תפוז — אבותיו הקולינריים של ה-`Lemon Curd`.

