---
id: TEX-EGG-001
type: SCIENTIFIC_PRINCIPLE
name: "טרנספורמציות מרקם בביצים — ג'לים, רשתות קסטרד, שלבי קצף וכשלי מרנג (Egg Texture Transformations)"
title_he: "טרנספורמציות מרקם בביצים — ג'לים, רשתות קסטרד, שלבי קצף וכשלי מרנג"
domain: TEXTURES
category: "GEL_AND_FOAM_RHEOLOGY"
book_title: "On Food and Cooking: The Science and Lore of the Kitchen"
author: "Harold McGee"
edition: "2nd Edition, Completely Revised and Updated"
publication_year: 2004
chapter: "Chapter 2: Eggs (The Yolk; Protein Coagulation; Custards; Egg Foams; Meringues)"
pdf_page: "90, 98-100, 108-109, 119-123"
printed_page: "76, 84-86, 94-95, 105-109"
knowledge_type: "CULINARY_PRINCIPLE"
claim_type: "DIRECT_SOURCE_CLAIM"
description: "מיפוי מבני של מרקמי הביצה: ג'ל אלבומין אלסטי ומבריק מול ג'ל חלמון מתפורר או קרמי, רשת קסטרד עדינה לחילוץ מתבנית, ואבחון כשלי מרקם במרנג (הזעת סירופ Weeping, חרוזי סוכר Beading וגרגיריות Grittiness)"
conditions:
  temperature_range_c:
    min: 60
    max: 120
  catalysts: ["albumen_vs_yolk_ratio", "sugar_dissolution", "ambient_humidity", "oven_temperature"]
effects:
  molecular_change: "רשת חלבונים חופשיים באלבומין יוצרת ג'ל חזק ומבריק; חלקיקי LDL בחלמון יוצרים רשת רכה וקרמית הדורשת ריכוז גבוה יותר (3 חלמונים ל-250 מ\"ל) כדי לעמוד בפני עצמה; גבישי סוכר לא מומסים במרנג מושכים מים היגרוסקופית ויוצרים טיפות סירופ"
  sensory_consequences:
    taste: ["עשירות שומנית בחלמון מול ניטרליות באלבומין"]
    aroma: []
    color: "מבריק וצחור במרנג תקין; צהבהב וסדוק במרנג שנאפה בחום גבוה מדי"
    texture: "ג'ל חלק או מתפורר, קצף קטיפתי או פריך-זכוכיתי, או כשלי נזילה וגרגיריות"
exceptions:
  - "אבקת סוכר (Powdered/Confectioner's Sugar) מכילה 10% קורנפלור למניעת התגיישות — חלק מהשפים נמנעים ממנה במרנג ואחרים מעדיפים אותה כביטוח סופג-לחות (McGee p. 106)"
relationships:
  - type: REQUIRES
    target_id: "SCI-PROT-002"
    target_name: "[[Protein-Denaturation-Coagulation]]"
    condition: "צפיפות הקשרים ברשת החלבונית קובעת את המרקם מרך ועד גומיי"
    evidence: "McGee 2004, Ch. 2, pp. 84-86 (PDF pp. 98-100)"
    confidence: 99
  - type: REQUIRES
    target_id: "SCI-FOAM-001"
    target_name: "[[Egg-Foam-Stability-Disulfide-And-Acid-Copper-Chemistry]]"
    condition: "איזון בין לכידת אוויר, סיכוך נוזלי והמסת סוכר במרנג"
    evidence: "McGee 2004, Ch. 2, pp. 105-109 (PDF pp. 119-123)"
    confidence: 99
  - type: AFFECTS
    target_id: "TEC-EGG-003"
    target_name: "[[Custard-Water-Bath-Baking-And-Cream-Stirring]]"
    condition: "יחס ביצים שלמות לחלמונים קובע אם קסטרד יוכל לעמוד יציב בחילוץ מהתבנית"
    evidence: "McGee 2004, Ch. 2, pp. 94-95 (PDF pp. 108-109)"
    confidence: 99
  - type: SUPPORTED_BY
    target_id: "SRC-MCGEE-2004"
    target_name: "[[SRC-MCGEE-2004]]"
    note: "Chapter 2, Printed pp. 76, 84-86, 94-95, 105-109 (PDF pp. 90, 98-100, 108-109, 119-123)"
sources:
  - source_id: "SRC-MCGEE-2004"
    citation: "Harold McGee, On Food and Cooking (2nd Ed., 2004), Chapter 2: Eggs, Printed pp. 76, 84-86, 94-95, 105-109 (PDF pp. 90, 98-100, 108-109, 119-123)"
verification_status: VERIFIED
created_at: 2026-10-21
updated_at: 2026-10-21
---

# טרנספורמציות מרקם בביצים — ג'לים, רשתות קסטרד, שלבי קצף וכשלי מרנג (`TEX-EGG-001`)

## 1. השוואת מרקם הג'ל: חלבון (Albumen) מול חלמון (Yolk) בקסטרדים
כאשר מתכננים מרקם של קסטרד (עמ' מודפס 94–95 | PDF עמ' 108–109):
* **אלבומין (חלבונים חופשיים)**: יוצר ג'ל **מוצק יותר, גמיש ומבריק (Glossier & Firmer)**.
* **חלמון (חלבונים קשורים לחלקיקי LDL ושומן)**: יוצר ג'ל **עדין, רך וקרמי יותר (More tender & creamier)**, אך מכיוון שחלבוני ה-LDL פחות יעילים ביצירת רשת מרחבית מחלבוני האלבומין החופשיים, קסטרד המיועד לחילוץ מהתבנית (*Unmolding*, כגון קרם קרמל) חייב להכיל **חלבון ביצה או לפחות 3 חלמונים לכל כוס (250 מ"ל) נוזל**.
* **החלפת חלב בשמנת**: שמנת מכילה 20%–40% פחות מים מחלב, ולכן חלבוני הביצה מדוללים פחות ונדרש שיעור קטן יותר של ביצים להשגת אותה מוצקות (עמ' מודפס 95 | PDF עמ' 109).

---

## 2. מטריצת אבחון ומניעת כשלי מרקם במרנג (Meringue Texture Troubleshooting)
> מקור: *On Food and Cooking* (2004), פרק 2, עמ' מודפס 108–109 (PDF עמ' 122–123) — `DIRECT_SOURCE_CLAIM`:

| תופעת הכשל במרנג | הסיבה הפיזיקלית-כימית המדויקת | פרוטוקול מניעה ופתרון |
| :--- | :--- | :--- |
| **1. חרוזי סירופ על פני המרנג (`Beading`) או שלוליות (`Weeping`)** | א. הקצפת-חסר או הקצפת-יתר.<br>ב. **גבישי סוכר שלא נמסו במלואם**: הגבישים הנותרים מושכים מים מסביבתם ויוצרים כיסים של סירופ מרוכז.<br>ג. **תנור חם מדי**: מכווץ את החלבונים הנקרשים ודוחק מהם מים מהר יותר מקצב האידוי שלהם. | שימוש בסוכר דק מאוד (*Superfine*) או אבקת סוכר במרנג קשה (יחס 2:1 סוכר לחלבון הוא גבול המסיסות בטמפרטורת החדר — 67%!); ואפייה איטית בתנור נמוך (`93°C / 200°F`). |
| **2. מרקם גרגירי וחולי (`Grittiness`)** | סוכר שלא נמס (כולל גבישים מיקרוסקופיים בסירופ של מרנג איטלקי שבושל פחות מדי והמשיכו לגדול בקירור). | המסה מלאה של הסוכר ובישול סירופ למרנג איטלקי בדיוק ל-`115°C–120°C` (`240°F–250°F`). |
| **3. הזעת סירופ והחלקת מרנג על גבי פאי (`Weeping Pie Topping`)** | מתרחשת משתי סיבות הפוכות:<br>א. **תת-בישול של תחתית הקצף** (כשהמלית קרה והתנור לוהט).<br>ב. **בישול-יתר של תחתית הקצף** (כשהמלית לוהטת והתנור מתון). | פיזור שכבת פירורים סופגת-סירופ על מלית הפאי לפני הנחת המרנג, או שילוב מעט עמילן או ג'לטין בקצף לקשירת הלחות (עמ' 109). |
| **4. התרככות ודביקות לאחר האפייה (`Stickiness`)** | משטח הסוכר של המרנג הוא היגרוסקופי וסופח לחות מהאוויר (במיוחד במזג אוויר לח). | העברת מרנג מיובש **ישירות מהתנור לכלי אטום לאוויר** והגשה מיד עם הוצאתו מהכלי. |

