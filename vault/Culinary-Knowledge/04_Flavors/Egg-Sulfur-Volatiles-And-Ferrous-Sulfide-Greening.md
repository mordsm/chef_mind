---
id: FLV-EGG-001
type: SCIENTIFIC_PRINCIPLE
name: "כימיה של טעם הביצה — מימן גופרי (H2S), הירקרקות ברזל גופרי (FeS) וטרימתילאמין (Egg Flavor & Greening Chemistry)"
title_he: "כימיה של טעם הביצה — מימן גופרי (H2S), הירקרקות ברזל גופרי (FeS) וטרימתילאמין"
domain: FLAVORS
category: "AROMA_AND_COLOR_REACTIONS"
book_title: "On Food and Cooking: The Science and Lore of the Kitchen"
author: "Harold McGee"
edition: "2nd Edition, Completely Revised and Updated"
publication_year: 2004
chapter: "Chapter 2: Eggs (The Chemistry of Egg Flavor; Green Yolks; Green Eggs in the Chafing Dish)"
pdf_page: "101, 103, 107"
printed_page: "87, 89, 93"
knowledge_type: "SCIENTIFIC_FACT"
claim_type: "DIRECT_SOURCE_CLAIM"
description: "מנגנוני יצירת הארומה והצבע בביצים: שחרור גז מימן גופרי (H2S) מאובלבומין מעל 60°C, תגובת גופרית-ברזל ליצירת ברזל גופרי (FeS) ירוק-אפור בביצים קשות ובמקושקשת מוחזקת בחום, וריח דגי מטרימתילאמין בזני ביצים חומות"
conditions:
  temperature_range_c:
    min: 60
    max: 100
  ph_range:
    min: 6.0
    max: 9.5
  catalysts: ["heat_above_60c", "alkaline_ph_above_8", "prolonged_holding_heat", "rapeseed_or_soy_choline_feed"]
effects:
  molecular_change: "מעל 60°C אובלבומין נפתח ומשחרר אטומי גופרית המגיבים עם יוני מימן ליצירת גז H2S; בממשק חלבון-חלמון גופרית מגיבה עם ברזל מהחלמון ליצירת ברזל גופרי (FeS) ירוק-אפור; חומצה (מיץ לימון/חומץ) מדכאת שחרור H2S ו-FeS"
  sensory_consequences:
    taste: ["חלמון מעניק טעם מתקתק-חמאתי; חלבון מעניק תו גופריתי אומאמי"]
    aroma: ["100–200 תרכובות ארומה בביצה מבושלת ובראשן H2S ואמוניה זעירה; ריח דגי מ-Triethylamine בתרנגולות ביצים חומות הניזונות מלפתית/סויה"]
    color: "טבעת ירוקה-אפורה (FeS) סביב חלמון ביצה קשה או כתמים ירוקים במקושקשת על פלטת חימום"
    texture: "ללא שינוי מרקמי ישיר (FeS אינו מזיק לבריאות אך מעיד על בישול-יתר או בסיסיות גבוהה)"
exceptions:
  - "מכיוון שמימן גופרי (H2S) הוא גז נדיף, ביצים קשות מאבדות את חריפותן הגופריתית והופכות עדינות יותר בטעמן במהלך אחסון במקרר (McGee p. 87)"
relationships:
  - type: REQUIRES
    target_id: "ING-EGG-002"
    target_name: "[[Egg-Albumen-Key-Proteins]]"
    condition: "Ovalbumin הוא המקור הבלעדי לקבוצות הגופרית הריאקטיביות בחלבון הביצה"
    evidence: "McGee 2004, Ch. 2, pp. 78, 87 (PDF pp. 92, 101)"
    confidence: 99
  - type: AFFECTS
    target_id: "ING-EGG-004"
    target_name: "[[Egg-Aging-Alkalinization-And-Grades]]"
    condition: "ביצים ישנות בעלות pH גבוה (9.2) או תוספת סודה לשתייה למי הבישול מאיצות דרמטית יצירת H2S ו-FeS"
    evidence: "McGee 2004, Ch. 2, pp. 87-89 (PDF pp. 101-103)"
    confidence: 99
  - type: INHIBITED_BY
    target_id: "FLV-BAL-001"
    target_name: "[[Acid-Fat-Balance]]"
    condition: "הוספת חצי כפית (2g) מיץ לימון או חומץ לכל ביצה מונעת לחלוטין הירקרקות במקושקשת המוחזקת בחום"
    evidence: "McGee 2004, Ch. 2, p. 93 (PDF p. 107)"
    confidence: 99
  - type: SUPPORTED_BY
    target_id: "SRC-MCGEE-2004"
    target_name: "[[SRC-MCGEE-2004]]"
    note: "Chapter 2, Printed pp. 87, 89, 93 (PDF pp. 101, 103, 107)"
sources:
  - source_id: "SRC-MCGEE-2004"
    citation: "Harold McGee, On Food and Cooking (2nd Ed., 2004), Chapter 2: Eggs, Printed pp. 87, 89, 93 (PDF pp. 101, 103, 107)"
verification_status: VERIFIED
created_at: 2026-10-21
updated_at: 2026-10-21
---

# כימיה של טעם הביצה — מימן גופרי ($\text{H}_2\text{S}$), הירקרקות ברזל גופרי ($\text{FeS}$) וטרימתילאמין (`FLV-EGG-001`)

## 1. יצירת הארומה האופיינית של ביצה מבושלת (`Hydrogen Sulfide — H2S`)
בביצה מבושלת זוהו בין **100 ל-200 תרכובות ארומה**, שהדומיננטית שבהן היא גז **מימן גופרי ($\text{H}_2\text{S}$)** (עמ' מודפס 87 | PDF עמ' 101):
* **סף הטמפרטורה (`60°C / 140°F`)**: $\text{H}_2\text{S}$ נוצר בעיקר בחלבון (Albumen) כאשר חלבוני ה-`Ovalbumin` נפתחים בטמפרטורות מעל **60°C (140°F)** ומשחררים אטומי גופרית המגיבים עם מולקולות אחרות.
* **שלושת המאיצים של ריח גופריתי חזק**:
  1. שהייה ממושכת בטמפרטורה גבוהה.
  2. **גיל הביצה ורמת ה-pH**: ככל שהביצה ישנה יותר וה-pH שלה בסיסי יותר (או כאשר מוסיפים סודה לשתייה למי הבישול כדי להקל על הקילוף, עמ' 88), נוצר הרבה יותר $\text{H}_2\text{S}$.
* **דיכוי בחומצה**: הוספת מיץ לימון או חומץ מפחיתה את ייצור ה-$\text{H}_2\text{S}$ ואת ריחו.

---

## 2. מנגנון הירקרקות בחלמון ביצה קשה ובמקושקשת בחימום (`Ferrous Sulfide — FeS`)
הצבע הירוק-אפור המופיע לעיתים על פני חלמון ביצה קשה או ככתמים ירוקים בביצה מקושקשת וחביתות המוחזקות במגש חימום (*Chafing Dish / Steam Table*) הוא תרכובת בלתי מזיקה של ברזל וגופרית — **ברזל גופרי ($\text{FeS}$)** (עמ' מודפס 89, 93 | PDF עמ' 103, 107):
1. **המנגנון הכימי**: תנאים בסיסיים בחלבון מזרזים קריעת אטומי גופרית מחלבוני האלבומין שנפתחו בחום; הגופרית מגיבה עם הברזל שבשכבת הפנים של החלמון ליצירת $\text{FeS}$.
2. **מניעה בביצה קשה (עמ' 89)**: שימוש בביצים טריות (pH נמוך יותר), בישול קצר ועדין ככל האפשר (80–85°C), **וקירור מהיר במי קרח מיד בתום הבישול** (העוצר את נדידת הגופרית לכיוון החלמון החם).
3. **מניעה במקושקשת על פלטת חימום (עמ' 93)**: בביצה מקושקשת המוחזקת בחום עולה ה-pH בכחצי יחידת pH; הוספת **1/2 כפית (2 גרם) מיץ לימון או חומץ לכל ביצה** מונעת לחלוטין את ההירקרקות (ומחצית מהכמות — 1 גרם לביצה — מאטה אותה מאוד עם השפעה מינימלית על הטעם).

---

## 3. השפעת גנטיקה ותזונת התרנגולת על טעמי לוואי (`Choline -> Triethylamine`)
בדרך כלל לגיל הביצה ולתנאי האחסון יש השפעה גדולה יותר על הטעם מאשר לתזונת התרנגולת, אך מקג'י מתעד חריג ביוכימי מרתק (עמ' מודפס 87 | PDF עמ' 101):
* **רגישות זני ביצים חומות לכולין (Choline)**: תרנגולות מזנים המטילים ביצים חומות חסרות את היכולת המטבולית לפרק מרכיב חסר ריח בשם **כולין (Choline)** המצוי בכוספת לפתית (Rapeseed/Canola meal) ובכוספת סויה; חיידקי המעי שלהן הופכים אותו למולקולה בעלת **טעם וריח דגי מובהק — טרימתילאמין (Triethylamine)** — העוברת אל הביצה!

