---
id: ING-EGG-004
type: INGREDIENT
name: "התיישנות הביצה, עליית בסיסיות (pH) ודירוג איכות (Egg Aging, Alkalinization & Grading)"
title_he: "התיישנות הביצה, עליית בסיסיות (pH) ודירוג איכות"
domain: INGREDIENTS
category: "חלבון מן החי — דינמיקת אחסון וטריות"
book_title: "On Food and Cooking: The Science and Lore of the Kitchen"
author: "Harold McGee"
edition: "2nd Edition, Completely Revised and Updated"
publication_year: 2004
chapter: "Chapter 2: Eggs (Egg Quality, Handling, and Safety; Basic Egg Dishes)"
pdf_page: "94-97, 102-103"
printed_page: "80-83, 88-89"
knowledge_type: "SCIENTIFIC_FACT"
claim_type: "DIRECT_SOURCE_CLAIM"
description: "תהליכי ההתיישנות הכימיים והפיזיקליים בביצה מהרגע שהוטלה: בריחת גז CO2 המעלה את ה-pH של החלבון מ-7.7 ל-9.2, דילול האובומוצין, נדידת מים אוסמוטית לחלמון והתרחבות תא האוויר"
conditions:
  temperature_range_c:
    min: 0
    max: 25
  ph_range:
    min: 6.0
    max: 9.5
  catalysts: ["CO2_outgassing_through_10000_pores", "osmotic_pressure_gradient", "moisture_evaporation"]
effects:
  molecular_change: "איבוד פחמן דו-חמצני מומס (חומצה פחמתית) דרך הקליפה מעלה את ה-pH של האלבומין מ-7.7 ל-9.2+ ושל החלמון מ-6.0 ל-6.6; דחייה חשמלית בין חלבונים בסביבה בסיסית מפרקת את מבנה ה-Ovomucin"
  texture_change: "החלבון העכור והסמיך הופך שקוף ודליל (יחס סמיך:דליל יורד מ-60:40 לפחות מ-50:50); החלמון סופג 5 מ\"ג מים ליום במקרר, מתנפח והממברנה שלו נחלשת; תא האוויר מתרחב עקב אובדן 4 מ\"ג מים ליום באידוי"
exceptions:
  - "היתרון הקולינרי המובהק היחיד של ביצה ישנה (pH ~9.2) הוא קילוף קל וחלק של הקליפה בביצה קשה (McGee pp. 82, 88)"
relationships:
  - type: AFFECTS
    target_id: "ING-EGG-001"
    target_name: "[[Egg-Proteins-Yolk-Albumen]]"
    condition: "משנה את ה-pH, הצמיגות והצפיפות של הביצה לאורך חיי המדף"
    evidence: "McGee 2004, Ch. 2, pp. 80-82 (PDF pp. 94-96)"
    confidence: 99
  - type: AFFECTS
    target_id: "ING-EGG-002"
    target_name: "[[Egg-Albumen-Key-Proteins]]"
    condition: "פירוק הדרגתי של Ovomucin בסביבה בסיסית (pH 9.2)"
    evidence: "McGee 2004, Ch. 2, pp. 78, 81 (PDF pp. 92, 95)"
    confidence: 99
  - type: AFFECTS
    target_id: "FLV-EGG-001"
    target_name: "[[Egg-Sulfur-Volatiles-And-Ferrous-Sulfide-Greening]]"
    condition: "בסיסיות גבוהה בביצה ישנה מאיצה שחרור מימן גופרי (H2S) והיווצרות טבעת ירוקה-אפורה (FeS) סביב החלמון"
    evidence: "McGee 2004, Ch. 2, pp. 87, 89 (PDF pp. 101, 103)"
    confidence: 99
  - type: ENABLES
    target_id: "RUL-EGG-002"
    target_name: "[[Rule-Egg-Age-And-Grade-Selection-Matrix]]"
    condition: "התאמת גיל ודירוג הביצה (Grade AA מול ביצה בת שבוע+) למשימה הקולינרית"
    evidence: "McGee 2004, Ch. 2, pp. 80-82, 88, 105 (PDF pp. 94-96, 102, 119)"
    confidence: 98
  - type: SUPPORTED_BY
    target_id: "SRC-MCGEE-2004"
    target_name: "[[SRC-MCGEE-2004]]"
    note: "Chapter 2, Printed pp. 80-83, 88-89 (PDF pp. 94-97, 102-103)"
sources:
  - source_id: "SRC-MCGEE-2004"
    citation: "Harold McGee, On Food and Cooking (2nd Ed., 2004), Chapter 2: Eggs, Printed pp. 80-83, 88-89 (PDF pp. 94-97, 102-103)"
verification_status: VERIFIED
created_at: 2026-10-21
updated_at: 2026-10-21
---

# התיישנות הביצה, עליית בסיסיות (pH) ודירוג איכות (`ING-EGG-004`)

## 1. שלושת מנגנוני ההתיישנות בביצה שלמה (Deterioration Mechanisms)
ברגע שהביצה עוזבת את גוף התרנגולת, מתרחשים בה שלושה תהליכים כימיים-פיזיקליים מקבילים (עמ' מודפס 81–82 | PDF עמ' 95–96):
1. **איבוד $\text{CO}_2$ ועליית בסיסיות (Alkalinization)**:
   - הביצה הטרייה מכילה פחמן דו-חמצני מומס בצורת חומצה פחמתית ($\text{H}_2\text{CO}_3$). הגז בורח בהדרגה דרך 10,000 נקבוביות הקליפה.
   - כתוצאה מכך, ה-pH של החלבון מזנק מ-**7.7** בביצה טרייה ל-**9.2 ומעלה** לאחר מספר ימי קירור, וה-pH של החלמון עולה מ-**6.0** ל-**6.6**.
   - **השלכה ויזואלית ומרקמית**: ב-pH 7.7 חלבוני האלבומין נוטים להתקבץ בצברים המפזרים אור ולכן חלבון טרי נראה עכור-לבן; ב-pH 9.2 החלבונים טעונים שלילית ודוחים זה את זה, ולכן חלבון של ביצה ישנה הוא **שקוף ודליל**, ורשת ה-`Ovomucin` מתפרקת כך שיחס החלבון הסמיך לדליל צונח מ-**60:40** אל מתחת ל-**50:50**.
2. **נדידת מים אוסמוטית מהחלבון לחלמון (Osmotic Swelling)**:
   - ריכוז המולקולות המומסות בחלמון גבוה מזה שבחלבון, מה שיוצר לחץ אוסמוטי.
   - בטמפרטורת מקרר, כ-**5 מיליגרם מים** חוצים מדי יום מהחלבון דרך ממברנת החלמון לתוך החלמון. החלמון מתנפח, נעשה דליל ומימי יותר, והממברנה העוטפת אותו נמתחת ונחלשת (נוטה להיקרע בפתיחת הביצה).
3. **אידוי מים והתרחבות תא האוויר (Moisture Loss & Air Cell Expansion)**:
   - אפילו ביצה משומנת במקרר לח מאבדת כ-**4 מיליגרם מים ליום** באידוי דרך הקליפה.
   - **מבחן הציפה במים**: בביצה טרייה תא האוויר קטן מ-3 מ"מ (1/8 אינץ'), צפיפות הביצה גבוהה מצפיפות המים והיא שוקעת לתחתית. ככל שתא האוויר מתרחב הביצה מזדקפת, וביצה שצפה על פני המים היא ישנה מאוד ויש להשליכה (עמ' מודפס 81–82 | PDF עמ' 95–96).

---

## 2. כלל קצב ההתיישנות ואחסון אופטימלי
* **יחס טמפרטורה-זמן (`1:4`)**: איכות הביצה מידרדרת ב**יום אחד בטמפרטורת החדר** באותה מידה שהיא מידרדרת ב-**4 ימים במקרר**, ובמקביל חיידקי *Salmonella* מתרבים מהר בהרבה בטמפרטורת החדר (עמ' מודפס 82 | PDF עמ' 96).
* **מיקום במקרר ותנוחת אחסון**:
  - יש לאחסן במדף פנימי במקרר ולא בדלת (טלטול מדלל את החלבון הסמיך).
  - מחקרים משנות ה-60 וה-70 הראו שתנוחת האחסון אינה משפיעה על איכות האלבומין, אך **אחסון ביצים על צידן** מניב חלמונים ממורכזים יותר בביצים קשות מאחר ששני מיתרי הכלזה פועלים באופן שווה נגד כוח הכבידה (עמ' מודפס 82, 88 | PDF עמ' 96, 102).
* **צבע הקליפה ודירוג USDA**:
  - צבע הקליפה (לבן ב-Leghorn, חום ב-Rhode Island Red, כחול ב-Araucana) נקבע גנטית בלבד ואינו משפיע כלל על הטעם או הערך התזונתי (עמ' מודפס 75 | PDF עמ' 89).
  - ביצה טרייה בדירוג `Grade A` עדיפה על ביצה ישנה בדירוג `Grade AA` — גיל הביצה בפועל חשוב מהדירוג הראשוני בבית האריזה (עמ' מודפס 80–81 | PDF עמ' 94–95).

