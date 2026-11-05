---
id: REPORT-FLB-2015-001
type: INGESTION_REPORT
name: דוח חילוץ ידע מכל תשעת פרקי The Food Lab
verification_status: PRELIMINARY
evidence_cutoff_date: "2026-10-25"
---

# דוח חילוץ ידע מכל תשעת פרקי The Food Lab

## תוצאה והיקף

עובדו כל תשעת הפרקים הממוספרים לשכבה ראשונה של ידע מובנה: **36 טענות מקור נבחרות, 9 ניסוחי כלל מותנה, 9 מפות פרק ו־21 מושגים קיימים שאליהם קושרו הראיות**. זהו חילוץ סלקטיבי של עקרונות ליבה מכל פרק, ולא טענה שכל משפט, מתכון, איור או טענה מספרית בספר קודדו ונבדקו. קובצי המבוא, האינדקס והנספחים נסרקו מבנית; לא נוצר מהם פרק נוסף של טענות.

זוהו 11 עקרונות קולינריים, 6 עקרונות מדעיים, 8 תכונות חומרי גלם, 5 תצפיות ניסוי מטבח, 4 טכניקות ו־2 תכונות ציוד. תשעת הכללים הם **פרשנות מותנית** של הראיות; לא הוצגו כציטוטים. לא נוצרו השערות מדעיות חדשות. קישור מושגי מסומן כפרשנות, ולא כהוכחה לסיבתיות.

## ספר ומהדורה

The Food Lab: Better Home Cooking Through Science, J. Kenji López-Alt, First Edition, W. W. Norton & Company, 2015. פורמט המקור בפועל הוא EPUB; אין PDF מצורף של הספר הזה. ISBN אלקטרוני: `9780393249866`. מידע הכותרת נבדק ב־`content.opf`, ומהדורה וזכויות ב־`text/part0458.html`. [[FoodLab-2015-Source-Audit]] מתעד את הבדיקה. הספר האחר, On Food and Cooking של McGee, לא עובד מחדש במסגרת משימה זו.

מקור מקומי: `C:\Users\lenovo\Downloads\J. Kenji López-Alt - The Food Lab_ Better Home Cooking Through Science (2015, W. W. Norton & Company) - libgen.li.epub`

חתימת המקור: `9457a6e8f889baf3740e5e82bd136089c5ce255225d77eeb8069f11a12510a54`

## שיטת העבודה והכיסוי

מופו **459 קובצי HTML פנימיים**, מהם 441 משויכים לפרקים 1–9 לפי תוכן העניינים. הסריקה מדדה מבנה, מספר פסקאות, כמות טקסט וחתימות. אין להסיק מכך שנערכה ביקורת מהותית לכל כ־1,575,285 תווי טקסט בפרקים. בפועל נבחרו ונבדקו 36 פסקאות ראיה, ועוד פסקאות נקודתיות לצורך ביקורת פערים והקשר.

| פרק | שם לפי תוכן העניינים | טענות | כללים | קבצים במיפוי המבני |
|---|---|---:|---:|---:|
| 1 | Eggs, Dairy, and the Science of Breakfast | 4 | 1 | 51 |
| 2 | Soups, Stews, and the Science of Stock | 4 | 1 | 53 |
| 3 | Steaks, Chops, Chicken, Fish, and the Science of Fast-Cooking Foods | 4 | 1 | 66 |
| 4 | Blanching, Searing, Braising, Glazing, Roasting, and the Science of Vegetables | 4 | 1 | 61 |
| 5 | Balls, Loaves, Links, Burgers, and the Science of Ground Meat | 4 | 1 | 32 |
| 6 | Chickens, Turkeys, Prime Rib, and the Science of Roasts | 4 | 1 | 53 |
| 7 | Tomato Sauce, Macaroni, and the Science of Pasta | 4 | 1 | 61 |
| 8 | Greens, Emulsions, and the Science of Salads | 4 | 1 | 41 |
| 9 | Batter, Breadings, and the Science of Frying | 4 | 1 | 23 |

לכל טענה מזהה יציב `CLM-FLB-CHxx-nnn`, רשומת ראיה `EVD-FLB-CHxx-nnn`, נתיב פנימי, מספר פסקה וחתימת הפסקה. אין עימוד EPUB אמין בעותק: `pdf_page` ו־`printed_page` הם `UNKNOWN`. שיטת המיקום ניתנת לשחזור ומוגדרת במניפסט ובביקורת המקור. לא הומצאו עמודים.

## שילוב, כפילויות וקשרים

הראיות פוזרו בתיקיות התחום הקיימות, וכל כלל בתיקיית `12_Rules`. נוצרו 36 **רשומות ראיה**, ולא 36 מושגי ליבה חלופיים. נעשה שימוש חוזר ב־21 מזהי מושג קיימים וב־`SRC-FOODLAB-2015`; 3 מהכללים מציינים במפורש מזהי כלל קנוניים קיימים (`RUL-MEAT-001`, `RUL-MEAT-002`, `RUL-MEAT-003`). 6 האחרים הם כללי טיוטה חדשים בהקשר מוגדר. אין אומדן מומצא של מספר כפילויות מילוליות שנמנעו: הנתון המדיד הוא 36 מיפויי ראיה ל־21 יעדים קיימים.

נוצרו **90 קשרים מובנים ב־YAML** ברשומות הראיה והכללים: ביסוס במקור, מיפוי למושג קיים וביסוס כלל בראיה. קשרי המיפוי הם מותנים ופרשניים. החיבור לשמונת התחומים, כולל מגבלות הבטיחות והטעם, מוצג ב־[[FoodLab-2015-Domain-Map]]. גלוטן ופקטין אינם ממוזגים עם עמילן: אלה פערים בטקסונומיה המתועדים לבחינה.

## סתירות, תנאים ואי־ודאות

[[FoodLab-2015-Conflicts-And-Gaps]] כולל 9 ממצאי ביקורת. שניים הם אי־התאמות מפורשות: שיוך פסטה לפרק 9 ברשומה הישנה מול פרק 7 בפועל, ותיאור שדה מגנטי מול שדה חשמלי בשני מקומות בספר. יתר הממצאים מפרידים הבדלי תחולה, גבולות ניסוי ופערי אימות; אין להציג את כל תשעתם כסתירות מוכחות.

כל 36 הטענות נבדקו מול פסקת המקור שסומנה, אך **לא אומתו עצמאית מול מחקרים חיצוניים או ניסויים חדשים**. כל הרשומות החדשות מסומנות `PRELIMINARY`; רמת העקיבות גבוהה, וההכללה מותנית. Confidence מתאר ביטחון בייחוס ובהתאמה, לא הסתברות מדעית. חסרים נתוני מדגם, סמיות וסטטיסטיקה לחלק ממבחני המטבח (`UNKNOWN`). לא נבדקו errata של המו״ל או מהדורות אחרות.

טמפרטורות, חיי מדף ותהליכי בטיחות לא נגזרו אוטומטית מהעדפות המרקם בספר. מספרים שלא נבדקו בהקשר מתאים אינם מוצגים כקבועים אוניברסליים. אין כאן חיבור חדש למנוע השף, הפעלת טיוטות, שינוי בממשק או הבטחה למנוע הסקה אוטומטי.

## שאלות בדיקה

[[FoodLab-2015-Five-Questions]] מציג חמש שאלות, תשובות מוגבלות ושרשראות ראיה: בשר יבש בתבשיל לח, מרקם בשר טחון, נפח מים בירקות לעומת פסטה, יציבות ויניגרט, ופרישת עוף/מאוורר תנור. אלה בדיקות ידניות של הידע וקשריו.

## בקרת איכות ושימור

תוצאות הבדיקה נרשמות ב־`FoodLab-2015-validation.json`: מזהים חדשים ייחודיים, YAML תקין, קישורים חדשים פתירים, מזהי קשר תואמים ליעדיהם, עקיבות לכל פסקת ראיה, 9 פרקים ו־8 תחומים, אי־שינוי המקור, אי־שינוי קובצי הידע הקודמים ואי־שינוי קובצי היישום. בדיקות Chef אינן נדרשות כאן כי קוד היישום לא השתנה. אין הסתמכות על קישור שאינו פתיר או על מספר עמוד מומצא.

תוצאת הבדיקה בפועל: **PASS**. אומתו 59 רשומות Markdown, 90 קשרים ו־36 חתימות פסקה; 125 קובצי ידע קודמים ו־56 קובצי יישום נשארו ללא שינוי.

## קבצים

נוצרו 59 קובצי Markdown חדשים; כולל 36 רשומות ראיה, 9 כללים, 9 מפות פרק, ביקורת מקור, ביקורת סתירות ופערים, מפת תחומים, חמש שאלות והדוח הזה. נוסף מניפסט JSON, דוח בדיקות JSON ושני סקריפטי שחזור/אימות, כולם בתוך אזור הידע הקיים. **לא שונה אף קובץ ידע שהיה קיים לפני העבודה; לא שונה יישום השף.**

- `01_Ingredients/FoodLab-CH01-Yolk-Lecithin.md`
- `01_Ingredients/FoodLab-CH02-Corn-Sugar-Storage.md`
- `01_Ingredients/FoodLab-CH03-Salmon-Fat-Variation.md`
- `01_Ingredients/FoodLab-CH04-Sweet-Potato-Enzymes.md`
- `01_Ingredients/FoodLab-CH06-Cranberry-Pectin.md`
- `01_Ingredients/FoodLab-CH08-Yolk-Mayo-Emulsifier.md`
- `01_Ingredients/FoodLab-CH09-Eggplant-Porosity.md`
- `02_Food-Science/FoodLab-CH01-Biscuit-Cold-Fat.md`
- `02_Food-Science/FoodLab-CH01-Enriched-Dough.md`
- `02_Food-Science/FoodLab-CH02-Stock-Gelatin-Time.md`
- `02_Food-Science/FoodLab-CH05-Meatloaf-Gelatin.md`
- `02_Food-Science/FoodLab-CH07-Pasta-Hydration-Separate.md`
- `02_Food-Science/FoodLab-CH09-Frying-Coating-Set.md`
- `03_Techniques/FoodLab-CH01-Poaching-Acid.md`
- `03_Techniques/FoodLab-CH04-Blanch-Water-Volume.md`
- `03_Techniques/FoodLab-CH04-Vegetable-Braising.md`
- `03_Techniques/FoodLab-CH05-Cold-Grinding.md`
- `03_Techniques/FoodLab-CH06-Spatchcock-Geometry.md`
- `03_Techniques/FoodLab-CH07-Cheese-Starch-Sauce.md`
- `03_Techniques/FoodLab-CH08-Cabbage-Water.md`
- `03_Techniques/FoodLab-CH09-Batter-Heat-Barrier.md`
- `04_Flavors/FoodLab-CH03-Pan-Fond.md`
- `04_Flavors/FoodLab-CH03-Steak-Salt-Drying.md`
- `04_Flavors/FoodLab-CH07-Butter-Oil-Burning.md`
- `05_Textures/FoodLab-CH02-Braising-Moisture.md`
- `05_Textures/FoodLab-CH04-Mash-Potato-Type.md`
- `05_Textures/FoodLab-CH05-Burger-Handling.md`
- `05_Textures/FoodLab-CH05-Sausage-Moisture.md`
- `05_Textures/FoodLab-CH08-Mustard-Vinaigrette.md`
- `06_Equipment/FoodLab-CH02-Oven-Stovetop-Braise.md`
- `06_Equipment/FoodLab-CH06-Convection-Surface-Drying.md`
- `06_Equipment/FoodLab-CH07-Pasta-Water-Energy.md`
- `07_Food-Safety/FoodLab-CH08-Dairy-Dressing.md`
- `08_Decision-Making/FoodLab-CH03-Tender-Tough-Method.md`
- `08_Decision-Making/FoodLab-CH06-Bone-Insulation-Test.md`
- `08_Decision-Making/FoodLab-CH09-Fries-Crispness-Tradeoff.md`
- `09_Sources/FoodLab-2015/FoodLab-2015-Chapter-01.md`
- `09_Sources/FoodLab-2015/FoodLab-2015-Chapter-02.md`
- `09_Sources/FoodLab-2015/FoodLab-2015-Chapter-03.md`
- `09_Sources/FoodLab-2015/FoodLab-2015-Chapter-04.md`
- `09_Sources/FoodLab-2015/FoodLab-2015-Chapter-05.md`
- `09_Sources/FoodLab-2015/FoodLab-2015-Chapter-06.md`
- `09_Sources/FoodLab-2015/FoodLab-2015-Chapter-07.md`
- `09_Sources/FoodLab-2015/FoodLab-2015-Chapter-08.md`
- `09_Sources/FoodLab-2015/FoodLab-2015-Chapter-09.md`
- `09_Sources/FoodLab-2015/FoodLab-2015-Domain-Map.md`
- `09_Sources/FoodLab-2015/FoodLab-2015-Five-Questions.md`
- `09_Sources/FoodLab-2015/FoodLab-2015-manifest.json`
- `09_Sources/FoodLab-2015/FoodLab-2015-Report-HE.md`
- `09_Sources/FoodLab-2015/FoodLab-2015-Source-Audit.md`
- `09_Sources/FoodLab-2015/FoodLab-2015-validation.json`
- `09_Sources/FoodLab-2015/ingest_foodlab.py`
- `09_Sources/FoodLab-2015/validate_foodlab.py`
- `11_Conflicts/FoodLab-2015-Conflicts-And-Gaps.md`
- `12_Rules/FoodLab-CH01-Rule-Egg-Poaching-Choices.md`
- `12_Rules/FoodLab-CH02-Rule-Braise-Heat-Source.md`
- `12_Rules/FoodLab-CH03-Rule-Cut-Method-Choice.md`
- `12_Rules/FoodLab-CH04-Rule-Vegetable-Water-Choice.md`
- `12_Rules/FoodLab-CH05-Rule-Ground-Meat-Texture.md`
- `12_Rules/FoodLab-CH06-Rule-Bird-Geometry.md`
- `12_Rules/FoodLab-CH07-Rule-Pasta-Hydration-Choice.md`
- `12_Rules/FoodLab-CH08-Rule-Vinaigrette-Stability.md`
- `12_Rules/FoodLab-CH09-Rule-Fries-Effort-Crispness.md`

## מדוע העבודה נעצרת ומה מומלץ הלאה

הסתיים מעבר החילוץ המובנה המוגדר מכל תשעת הפרקים, והתקבלו ראיות, כללים וקשרים שניתנים לבדיקה. לא הוכרזה רוויה מדעית או סקירה ממצה של הספר. נותרו מתכונים, איורים וטענות נוספות שלא נותחו מהותית; הם ניתנים לאיתור דרך המניפסט.

מומלץ לבדוק ידנית תחילה את תשעת הכללים ואת שתי אי־ההתאמות, להחליט כיצד לתקן את הפניות הפסטה בלי לאבד היסטוריה, להשלים מקור לפיזיקת המיקרוגל ולמנגנון הלציטין, ולהפריד גלוטן ופקטין בטקסונומיה. לפני שימוש אוטומטי נדרשת סקירת התוכן ובטיחות התהליכים. ההרחבה העתידית תהיה לפי שאלות בעלות ערך, ולא באמצעות הכרזה שכל הספר כבר אומת.
