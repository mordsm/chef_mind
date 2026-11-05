---
id: ING-EGG-003
type: INGREDIENT
name: "מבנה חלמון הביצה — כדורים, ליפו-פרוטאינים (LDL), לציטין ואנזים עמילאז (Egg Yolk Structure & Amylase)"
title_he: "מבנה חלמון הביצה — כדורים, ליפו-פרוטאינים (LDL), לציטין ואנזים עמילאז"
domain: INGREDIENTS
category: "חלבון ושומן מן החי — מבנה תחליבי ואנזימטי"
book_title: "On Food and Cooking: The Science and Lore of the Kitchen"
author: "Harold McGee"
edition: "2nd Edition, Completely Revised and Updated"
publication_year: 2004
chapter: "Chapter 2: Eggs (The Yolk; Freezing Eggs; Cream Theory and Practice; Yolk Foams)"
pdf_page: "88-91, 97, 112-114, 127-129"
printed_page: "74-77, 83, 98-100, 113-115"
knowledge_type: "INGREDIENT_PROPERTY"
claim_type: "DIRECT_SOURCE_CLAIM"
description: "מבנה היררכי של 'כדורים בתוך כדורים' בחלמון הביצה: תאים כדוריים, גרנולות המתפרקות במלח, חלקיקי LDL עשירי לציטין האחראים ליכולת האמולסיה, מחסור במים חופשיים (2 מ\"ל בלבד לחלמון) ואנזים עמילאז עמיד לחום המפרק עמילן"
composition:
  weight_g: 17.0
  water_pct: 47.0
  free_foamable_water_ml_per_yolk: 2.0
  protein_pct: 15.9
  fat_pct: 35.3
  cholesterol_mg: 213
  pigments: ["xanthophylls (lutein, zeaxanthin)", "beta-carotene and canthaxanthin in duck yolks"]
  active_enzymes: ["heat-resistant amylase (starch-digesting enzyme)"]
effects:
  molecular_change: "הוספת קורט מלח מפרקת את הגרנולות (תתי-הכדורים) למרכיבים קטנים שאינם מסיטים אור — החלמון הופך צלול וסמיך יותר; הקפאה ללא מלח/סוכר גורמת להתלכדות בלתי הפיכה של ליפו-פרוטאינים למשחה צמיגה"
  texture_change: "בישול חלמון שלם יוצר מרקם מתפורר של כדורים רב-פאותיים מוקשים; שבירת החלמון לפני הבישול מונעת גרגיריות; עמילאז שלא הורתח מפרק ג'ל עמילן לנוזל"
exceptions:
  - "תעלת החלמון הלבן הקדמוני (Primordial White Yolk) במרכז החלמון עשירה בברזל, דלילה יותר ואינה נקרשת גם בביצה קשה (McGee p. 74)"
relationships:
  - type: AFFECTS
    target_id: "ING-EGG-001"
    target_name: "[[Egg-Proteins-Yolk-Albumen]]"
    condition: "מספק את כל השומן, הלציטין והברזל בביצה"
    evidence: "McGee 2004, Ch. 2, pp. 75-77, 79 (PDF pp. 89-91, 93)"
    confidence: 99
  - type: ENABLES
    target_id: "SCI-CHEM-002"
    target_name: "[[Caramelization-And-Emulsification]]"
    condition: "אגרגטים של חלבון-שומן-כולסטרול-לציטין (LDL) עוטפים טיפות שמן במיונז ובהולנדז"
    evidence: "McGee 2004, Ch. 2, pp. 76-77 (PDF pp. 90-91)"
    confidence: 99
  - type: INHIBITS
    target_id: "SCI-CARB-001"
    target_name: "[[Starch-Gelatinization-Retrogradation]]"
    condition: "אנזים ה-Amylase שבחלמון שורד חימום מתחת לנקודת הרתיחה ומפרק את רשת העמילן בקרם פטיסייר ופאי"
    evidence: "McGee 2004, Ch. 2, pp. 75, 98-100 (PDF pp. 89, 112-114)"
    confidence: 99
  - type: REQUIRES
    target_id: "RUL-EGG-003"
    target_name: "[[Rule-Starch-Stabilized-Pastry-Cream-Boiling]]"
    condition: "הרתחה מלאה של תערובת חלמון ועמילן להשבתת העמילאז"
    evidence: "McGee 2004, Ch. 2, pp. 98-100 (PDF pp. 112-114)"
    confidence: 99
  - type: ENABLES
    target_id: "TEC-EGG-004"
    target_name: "[[Meringue-Souffle-And-Sabayon-Whipping]]"
    condition: "הוספת לפחות 2 כפיות נוזל וחימום ל-50°C מאפשרים לחלמון להקציף פי 4 בזביונה/סביון"
    evidence: "McGee 2004, Ch. 2, pp. 113-115 (PDF pp. 127-129)"
    confidence: 98
  - type: SUPPORTED_BY
    target_id: "SRC-MCGEE-2004"
    target_name: "[[SRC-MCGEE-2004]]"
    note: "Chapter 2, Printed pp. 74-77, 83, 98-100, 113-115 (PDF pp. 88-91, 97, 112-114, 127-129)"
sources:
  - source_id: "SRC-MCGEE-2004"
    citation: "Harold McGee, On Food and Cooking (2nd Ed., 2004), Chapter 2: Eggs, Printed pp. 74-77, 83, 98-100, 113-115 (PDF pp. 88-91, 97, 112-114, 127-129)"
verification_status: VERIFIED
created_at: 2026-10-21
updated_at: 2026-10-21
---

# מבנה חלמון הביצה — כדורים, ליפו-פרוטאינים (LDL), לציטין ואנזים עמילאז (`ING-EGG-003`)

## 1. ארכיטקטורת "כדורים בתוך כדורים" (Spheres Within Spheres)
החלמון נראה כנוזל אחיד, אך מיקרוסקופ אלקטרונים חושף מבנה תלת-שכבתי מקונן (עמ' מודפס 75–77 | PDF עמ' 89–91):
1. **כדורי החלמון (Yolk Spheres — קוטר ~0.1 מ"מ)**: מדורים כדוריים עטופים בממברנה גמישה הדחוסים זה לצד זה בצורות רב-פאותיות. כאשר מבשלים חלמון שלם (בביצה קשה), כל כדור מתקשה בנפרד ומעניק לחלמון המבושל את **המרקם המתפורר (Crumbly)** האופייני לו. שבירת החלמון וערבובו לפני הבישול משחררת את הכדורים ויוצרת מרקם חלק ופחות גרגירי.
2. **תתי-כדורים / גרנולות (Subspheres / Yolk Granules — קוטר ~0.001 מ"מ)**: צפים במים בתוך כדורי החלמון, עשירים בחלבונים קושרי ברזל וזרחן. הם גדולים מספיק כדי להסיט קרני אור ולכן החלמון הטרי עכור. **אפקט המלח במיונז**: הוספת קורט מלח לחלמון מפרקת כימית את תתי-הכדורים למרכיבים זעירים שאינם מסיטים אור — והחלמון הופך בו-זמנית **צלול יותר וסמיך יותר** (עמ' מודפס 76 | PDF עמ' 90).
3. **תתי-תתי-כדורים — חלקיקי LDL (Low-Density Lipoproteins)**: קטנים פי 40 מהגרנולות; מורכבים מליבת שומן העטופה במעטפת מגן של חלבון, כולסטרול ופוספוליפידים — ובראשם **לציטין (Lecithin)**, מתווך שומן-מים המעניק לחלמון את כושר האמולסיה יוצא הדופן שלו.

---

## 2. שלוש תכונות קריטיות של החלמון במטבח המקצועי
* **א. אנזים העמילאז העמיד לחום (`Yolk Amylase`) — סכנת התנזלות קרמים ופאי**:
  בחלמון קיים אנזים מפרק-עמילן (**Amylase**) בעל עמידות חריגה לחום. אם מכינים קרם פטיסייר או מילוי פאי המעובה בעמילן (קמח/קורנפלור) ומסתפקים בחימום עד הסמכה מתחת לנקודת הרתיחה (או מוסיפים ביצים לאחר הרתיחה כמו ב-*Bouillie* ומאחסנים), העמילאז שורד, מפרק את רשת העמילן תוך מספר שעות, והופך פאי יציב לשלולית נוזלית (`[[Rule-Starch-Stabilized-Pastry-Cream-Boiling]]`, עמ' מודפס 75, 98, 100 | PDF עמ' 89, 112, 114).
* **ב. מחסור במים חופשיים ויציבות יתר בהקצפה (`Zabaglione / Sabayon`)**:
  בחלמון שלם (כף אחת / 15 מ"ל) יש כמחצית מכמות המים שבחלבון, אך כמעט כולם קשורים לליפו-פרוטאינים ונותרים רק **כ-1/3 כפית (2 מ"ל) של מים חופשיים להקצפה**. בנוסף, חלבוני החלמון יציבים מכנית ואינם נפתחים בהקצפה קרה. לכן חלמון לבדו כמעט אינו מקציף; כדי ליצור קצף חלמונים עשיר (זביונה/סביון) חובה להוסיף **נוזל** (לפחות 2 כפיות מים או יין מרסלה) ולבצע את ההקצפה תוך **חימום מבוקר ל-50°C (120°F)** מעל אמבט מים (`[[Meringue-Souffle-And-Sabayon-Whipping]]`, עמ' מודפס 113–115 | PDF עמ' 127–129).
* **ג. התגבשות בלתי הפיכה בהקפאה (`Freezing Gelation`)**:
  הקפאת חלמון נא (או ביצה שלמה מעורבבת) כמות שהיא גורמת לחלבוני החלמון להתלכד למשחה צמיגה וקשה שאינה מתערבבת עוד לאחר ההפשלה. **פתרון מונע**: ערבוב יסודי לפני ההקפאה עם `5 גרם מלח` (כפית), או `15 גרם סוכר` (כף), או `60 מ"ל מיץ לימון` (4 כפות) לכל חצי ליטר חלמונים (ולביצה שלמה — מחצית מהכמויות הללו) מונע את אגרגציית החלבונים ושומר על נזילות החלמון המופשר (עמ' מודפס 83 | PDF עמ' 97).

