"""Reproducible, additive chapter evidence extraction; never changes Chef code."""
import hashlib
import json
import re
import zipfile
from pathlib import Path
import xml.etree.ElementTree as ET

import yaml

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
BOOK = next(Path('C:/Users/lenovo/Downloads').glob('*Food Lab*.epub'))
SOURCE = 'SRC-FOODLAB-2015'
BOOK_HASH = hashlib.sha256(BOOK.read_bytes()).hexdigest()

# Each paraphrase is scoped to a specific paragraph of the supplied edition.
# Canonical concepts are reused rather than recreated under new concept IDs.
ROWS = [
 (1,18,'The yolk  is the nutritive source','Yolk-Lecithin','חלמון כמקור לחומר מתחלב','המחבר מתאר חלמון כמערכת המכילה מים, חלבונים ושומן, ובה לציטין המסייע לשילוב השומן במים.','INGREDIENT_PROPERTY','01_Ingredients','Egg-Yolk-Lipoproteins-And-Amylase','אין להסיק מכאן יחס שמן קבוע לכל רוטב.'),
 (1,23,'Yes, … sort of.','Poaching-Acid','חומצה ושליקת ביצים','המחבר מדווח שחומץ עשוי לזרז התייצבות חלבונים, אך אינו פתרון מיידי לסידור הלבן ועלול להקשיח ולהוסיף טעם חומצי.','CULINARY_PRINCIPLE','03_Techniques','Poaching-Scrambling-And-French-Omelet-Control','התוצאה תלויה בריכוז ובזמן; אין להכליל לכל מערכת חלבון.'),
 (1,57,'First off, biscuits','Biscuit-Cold-Fat','שומן קר ומבנה בצק ביסקוויט','הספר מבחין בין חמאה מומסת בבלילה לבין פיסות חמאה קרות בבצק; שילוב השומן לפני הנוזל יוצר אזורים הנבדלים בספיחת מים וביצירת גלוטן.','CULINARY_PRINCIPLE','02_Food-Science','Starch-Cornstarch-Flour','ההבחנה מתייחסת לבצקי ביסקוויט מול בלילות; אין יחס החלפה אוניברסלי.'),
 (1,61,'Sticky buns are made','Enriched-Dough','שומן ובניית גלוטן בבצק מועשר','המחבר מסביר ששומן בבצק מועשר מגביל קישור הדוק בין חלבוני הקמח, לעומת רשת חזקה יותר בבצק רזה.','SCIENTIFIC_PRINCIPLE','02_Food-Science','Starch-Cornstarch-Flour','שינוי בכמות שומן משנה גם טיפול בבצק; אין כאן הבטחת נפח.'),
 (2,69,'Remember how collagen','Stock-Gelatin-Time','זמן מיצוי ויכולת הסמכה של ציר','הספר מתאר המרת רקמת חיבור לג׳לטין במהלך הכנת ציר, ומזהיר שמיצוי ממושך מעבר להמרה עלול לפרק גם את הג׳לטין ולצמצם הסמכה.','SCIENTIFIC_PRINCIPLE','02_Food-Science','Collagen-Hydrolysis-Gelatin','הזמנים שבפסקה נוגעים לציר העוף שבדיון; אינם טבלת ריכוך לקורקבנים.'),
 (2,98,'Pot roast is essentially','Braising-Moisture','סביבה לחה אינה מבטיחה עסיסיות','המחבר מבחין בין פירוק קולגן בתבשיל לח לבין אובדן נוזלים בסיבי הבשר; גם בתוך נוזל הבשר יכול לאבד לחות.','CULINARY_PRINCIPLE','05_Textures','Two-Phase-Juiciness-And-Fiber-Compaction','יש להבחין בין רכות רקמת חיבור לעסיסיות השריר.'),
 (2,115,'On the stovetop, the stew cooks only','Oven-Stovetop-Braise','סיר בתנור לעומת חימום מתחתית','הספר משווה חימום מקומי מלמטה בכיריים לחימום מכמה כיוונים בתנור מבוקר תרמוסטט, ומעדיף תנור לתבשילים סמיכים וארוכים להפחתת חריכת תחתית.','EQUIPMENT_PROPERTY','06_Equipment','Covered-Vs-Uncovered-Evaporation','אין להסיק שכל תנור אחיד או שכל גודל סיר מתבשל באותו קצב בפועל.'),
 (2,83,'Because of the result','Corn-Sugar-Storage','מתיקות תירס לאחר הקטיף','המחבר מציין שבתירס מתוק מתחיל אובדן מתיקות לאחר הקטיף עקב שינוי סוכרים לעמילן, ושהטמפרטורה בזמן ההמתנה משפיעה על הקצב.','INGREDIENT_PROPERTY','01_Ingredients','Starch-Cornstarch-Flour','האחוזים המופיעים במקור אינם אומדן לכל זן ותנאי אחסון.'),
 (3,131,'First, as the steak sits','Steak-Salt-Drying','המלחה מוקדמת וייבוש פני סטייק','המחבר מתאר חדירת מלח ושינוי בחלבונים בעת מנוחה לאחר המלחה, לצד ייבוש השכבה החיצונית המסייע להשחמה מהירה.','CULINARY_PRINCIPLE','04_Flavors','Pre-Salting-Steak-Timing','יש להתאים לעובי ולתנאי קירור; אין להמיר מנוחה בקירור להשהיה לא מבוקרת בחוץ.'),
 (3,142,'You see, as meat cooks','Pan-Fond','משקעי השחמה כבסיס לרוטב','הספר מזהה משקעי מיצי בשר שהתייבשו והשחימו במחבת כבסיס טעם לרוטב מחבת.','CULINARY_PRINCIPLE','04_Flavors','Maillard-Reaction','משקע שחום אינו שקול למשקע חרוך; לא כל מחבת מייצרת אותה כמות משקע.'),
 (3,121,'Fast-cooking methods include','Tender-Tough-Method','מטרת בישול מהיר לעומת איטי','המחבר מבחין בין חימום נתחים רכים לטמפרטורת הגשה לבין החזקת נתחים עתירי רקמת חיבור בחימום מתאים לפירוקה.','CULINARY_PRINCIPLE','08_Decision-Making','Cut-To-Method-Matching','בחירת השיטה תלויה בנתח ובמטרה; צלייה ורתיחה אינן שיטות בלעדיות לקבוצה אחת.'),
 (3,168,'Depending on the species, the time of year','Salmon-Fat-Variation','שונות בשומן תת־עורי בסלמון','הספר מתאר שונות בעובי השומן התת־עורי בסלמון לפי מין, עונה ותנאים נוספים.','INGREDIENT_PROPERTY','01_Ingredients','Finfish-Muscle-Myotomes-Fat-And-Pigments','אין לנבא את מידת השומן של פילה יחיד לפי שם המין בלבד.'),
 (4,193,'I cooked a half pound','Blanch-Water-Volume','נפח מים ותוצאת חליטת ירקות','בניסוי המתואר בשעועית ירוקה, מעט מים איבדו יותר טמפרטורה לאחר הוספת הירק, ונצפו ריכוך איטי יותר וגוון פחות ירוק מאשר במנות מים גדולות.','EMPIRICAL_OBSERVATION','03_Techniques','Heat-Transfer','זהו ניסוי מטבח במזון ובעומס מוגדרים; אין להעתיק את מסקנת נפח המים לפסטה.'),
 (4,220,'Braising is a slow','Vegetable-Braising','ברייז לירקות לעומת בשר','הספר מבחין בין ריכוך ירקות הקשור בפקטין לבין ריכוך בשר הקשור בקולגן, ולכן אין להעתיק ביניהם באופן אוטומטי זמן ועוצמת חימום.','CULINARY_PRINCIPLE','03_Techniques','Low-Slow-Braising','הטמפרטורה האחידה לכל הירקות שבניסוח המקור דורשת זהירות; זן, חיתוך וחומציות משנים תוצאה.'),
 (4,235,'Now, sweet potatoes contain','Sweet-Potato-Enzymes','אנזימים ומתיקות בטטה','המחבר קושר עלייה במתיקות בטטה לפעילות אנזימטית הממירה עמילן למלטוז, ומשווה חימום ישיר לשלב חימום מקדים.','SCIENTIFIC_PRINCIPLE','01_Ingredients','Starch-Gelatinization-Retrogradation','מסקנת המתיקות אינה הוראת בטיחות לשהייה ארוכה בחום פושר.'),
 (4,239,'Potato type','Mash-Potato-Type','זן תפוח אדמה ומרקם מחית','הספר מתאר שתפוחי אדמה קמחיים מתפרקים ביתר קלות ודורשים פחות עבודה למחית, בעוד זנים שעוותיים דורשים יותר עיבוד ומניבים מרקם שונה.','INGREDIENT_PROPERTY','05_Textures','Starch-And-Emulsion-Viscosity','הכינוי המסחרי אינו מדידה של עמילן; עיבוד יתר עשוי לשנות את התוצאה.'),
 (5,253,'Keep everything cold','Cold-Grinding','קירור בשר וציוד בטחינה','המחבר קושר חימום בזמן טחינה למריחת הבשר והשומן במקום חיתוך נקי, וממליץ לשמור את הבשר וחלקי הטחינה קרים.','COOKING_TECHNIQUE','03_Techniques','Sausage-Emulsions-Myosin-And-Nitrite-Curing','זוהי הנחיית איכות; טמפרטורת ציוד אינה תחליף לנוהלי בטיחות בשר נא.'),
 (5,256,'OK, maybe a bit','Sausage-Moisture','נקניק מלוח עדיין רגיש לבישול יתר','הספר מתאר יתרון באחזקת נוזלים בבשר שהומלח, אך מדגיש שגם נקניק אינו חסין מבישול יתר ושמעטפת וצורה משנות את השיטה המתאימה.','CULINARY_PRINCIPLE','05_Textures','Two-Phase-Juiciness-And-Fiber-Compaction','לא הועתקו טמפרטורות ההגשה שבמתכוני המקור כהוראות בטיחות.'),
 (5,271,'Despite outward appearances','Burger-Handling','עיבוד בשר טחון וצפיפות המבורגר','המחבר מתאר שלישה וטיפול עודף בבשר טחון מגבירים קישור בין חלבונים ויוצרים המבורגר צפוף ומהודק יותר.','CULINARY_PRINCIPLE','05_Textures','Sausage-Emulsions-Myosin-And-Nitrite-Curing','מבנה צפוף הוא יעד אפשרי בנקניק, אך לא בהכרח בהמבורגר רך.'),
 (5,265,'The difference between veal','Meatloaf-Gelatin','ג׳לטין ושמירת נוזלים בקציץ בשר','המחבר מסביר את תרומת הג׳לטין בקציץ כרשת המסייעת לאחזקת מים, במסגרת ההשוואה בין עגל, בקר וחזיר.','SCIENTIFIC_PRINCIPLE','02_Food-Science','Collagen-Hydrolysis-Gelatin','ההשוואה תלויה בהרכב התערובת; אין להסיק שכל עגל מכיל אותה כמות ג׳לטין זמין.'),
 (6,283,'Butterflying the bird','Spatchcock-Geometry','גאומטריית עוף פרוש וחשיפת השוקיים','הספר מסביר שפרישת העוף משנה את חשיפת הירכיים והשוקיים לחום ומסייעת לתאם את הבשלת הבשר הכהה והבהיר.','COOKING_TECHNIQUE','03_Techniques','Whole-Bird-Roasting-And-Crisp-Poultry-Skin','זו חלופה לצלייה שלמה, עם מחיר בהצגה ובמבנה; נדרשת מדידה בחלקים שונים.'),
 (6,285,'In a regular oven,','Convection-Surface-Drying','מאוורר תנור וייבוש פני שטח','המחבר מתאר זרימת אוויר מאולצת המספקת חום ומסלקת לחות מפני המזון, ולכן עשויה להאיץ בישול והשחמה.','EQUIPMENT_PROPERTY','06_Equipment','Heat-Transfer','תנור ביתי אינו בהכרח אחיד; יש לעקוב אחר ההשחמה ולא להניח המרת זמן קבועה.'),
 (6,313,'Tasted side by side','Bone-Insulation-Test','עצם: בידוד לעומת טענת העברת טעם','במבחן הטעימה המתואר לא הובחן הבדל בין חלק מהתנאים עם ובלי הפרדת עצם ברדיד, והמחבר מפרש את ההבדל במרקם כתרומת בידוד תרמי.','EMPIRICAL_OBSERVATION','08_Decision-Making','Heat-Transfer','אי־זיהוי במבחן המטבח המתואר אינו הוכחה שאין העברת טעם בשום שיטה.'),
 (6,306,'Here’s why to make','Cranberry-Pectin','פקטין טבעי בחמוציות','הספר מתאר את הפקטין שבחמוציות כבסיס ליצירת ג׳ל ברוטב עם סוכר ומים, ללא צורך אוטומטי בתוספת פקטין.','INGREDIENT_PROPERTY','01_Ingredients','Starch-And-Emulsion-Viscosity','כמות הסוכר, הריכוז והחומציות עדיין משנים את הג׳ל; אין להכליל לכל פרי.'),
 (7,334,'To solve this mystery','Pasta-Water-Energy','רתיחה, הספק ונפח מים לפסטה','המחבר מנתח מאזן אנרגיה בשני נפחי מים רותחים על מבערים זהים, ומפריד בין חימום, איבוד חום ואנרגיית אידוי.','SCIENTIFIC_PRINCIPLE','06_Equipment','Heat-Transfer','המודל מניח תנאים מסוימים; מים רותחים אינם מבטיחים טמפרטורה זהה בכל גובה.'),
 (7,356,'See, as the evaporated','Cheese-Starch-Sauce','עמילן וחלב מרוכז ברוטב גבינה','הספר מתאר התנפחות עמילן ותוספת חלבוני חלב כמסייעות לרוטב גבינה חלק, ומציע לפזר את העמילן דרך הגבינה המגוררת לפני החיבור.','COOKING_TECHNIQUE','03_Techniques','Starch-And-Emulsion-Viscosity','ההסבר מתייחס לתערובת הנדונה; אינו מבטיח יציבות בכל גבינה ויחס נוזל.'),
 (7,378,'But who’s to say','Pasta-Hydration-Separate','הידרציה נפרדת מחימום פסטה','הספר מציג השריית פסטה יבשה כדרך להפריד את ספיחת המים מחלק מתהליך הבישול בחום, במסגרת דיון בפסטה אפויה.','CULINARY_PRINCIPLE','02_Food-Science','Starch-Gelatinization-Retrogradation','השריה אינה בישול מלא או אימות בטיחות; אין משך אחסון גורף שניתן להסיק מכך.'),
 (7,387,'First off: Butter','Butter-Oil-Burning','שמן אינו מבטל חריכת מוצקי חמאה','המחבר מדווח שתוספת שמן לחמאה אינה מונעת את חריכת מוצקי החלב שבה, ומבחין בין בחירת טעם לבין מנגנון החריכה.','EMPIRICAL_OBSERVATION','04_Flavors','Dairy-Butter-Emulsion','אין כאן טמפרטורת עשן אחידה לכל שמן וחמאה; יש להבחין בחמאה מזוקקת.'),
 (8,397,'The container on the left','Mustard-Vinaigrette','חרדל והאטת הפרדת ויניגרט','בהשוואת המטבח המתוארת, ויניגרט עם מעט חרדל נפרד לאט יותר מתערובת שמן וחומץ ללא חרדל.','EMPIRICAL_OBSERVATION','05_Textures','Caramelization-And-Emulsification','הניסוי אינו מבטיח יציבות קבועה לכל חרדל, יחס שמן או זמן אחסון.'),
 (8,413,'Normally when you mix','Yolk-Mayo-Emulsifier','מתחלבים בחלמון ומיונז','הספר מזהה לציטין וחומרים מתחלבים בחלמון כמסייעים להשהיית טיפות שמן במערכת מימית.','INGREDIENT_PROPERTY','01_Ingredients','Egg-Yolk-Lipoproteins-And-Amylase','התיאור המולקולרי בפסקאות הסמוכות דורש בדיקה נפרדת; לא מחלצים ממנו כיווניות ראש וזנב אוטומטית.'),
 (8,420,'Osmosis is the transfer','Cabbage-Water','המלחה וניקוז כרוב לסלט','המחבר מציע המלחה, מנוחה וסחיטה להפחתת הנוזלים המשתחררים מכרוב לתוך רוטב קולסלאו.','COOKING_TECHNIQUE','03_Techniques','Salt-Osmosis-And-Perception','המלחה משנה גם תיבול ומרקם; ההגדרה הפיזיקלית המקוצרת לאוסמוזה במקור אינה מועתקת כהגדרה מדעית מלאה.'),
 (8,424,'These dressings are','Dairy-Dressing','מוצרי חלב כבסיס רוטב מתחלב','הספר מתאר מוצרי חלב כבסיס שמגיע כבר במבנה מתחלב להכנת רטבים קרמיים, ומזהיר שחיי המדף קצרים יחסית.','INGREDIENT_PROPERTY','07_Food-Safety','Microbial-Danger-Zone-Cooling','אין לפרש את ההשוואה כהוראת חיי מדף או כהבטחה שרוטב חלבי לעולם לא ייפרד.'),
 (9,435,'Protein coagulation','Frying-Coating-Set','התייצבות חלבוני ציפוי בטיגון','הספר מתאר קרישת חלבונים בבלילה או בפירורים כמנגנון היוצר שלד מוצק לציפוי המטוגן.','SCIENTIFIC_PRINCIPLE','02_Food-Science','Protein-Denaturation-Coagulation','סוג הציפוי וההרכב משנים את המבנה; צבע הציפוי אינו מדידת מוכנות הפנים.'),
 (9,444,'This is why you want','Batter-Heat-Barrier','בלילה כחוצץ להעברת חום','המחבר מתאר בלילה כחוצץ בין שמן חם לדג, המאפשר לפנים להתבשל באופן מתון יחסית בזמן שהציפוי מתייצב ומתייבש.','CULINARY_PRINCIPLE','03_Techniques','Heat-Transfer','אין להסיק שציפוי מונע כל בישול יתר או מוכיח טמפרטורת ליבה.'),
 (9,442,'Salting, resting, and pressing','Eggplant-Porosity','הוצאת מים ודחיסת חציל','הספר משווה טיפול בהמלחה וסחיטה בחציל להפחתת מים ואוויר, אך מציין שונות בין חלקי הפרוסה וסיכון להמלחת יתר.','INGREDIENT_PROPERTY','01_Ingredients','Salt-Osmosis-And-Perception','מסקנת ההתאמה משתנה בין חציל פרמזן לבין בישול ארוך ברוטב.'),
 (9,453,'The problem, however,','Fries-Crispness-Tradeoff','הכנה פשוטה מול פריכות צ׳יפס','המחבר משווה שיטה פשוטה יותר לצ׳יפס להכנה הכוללת חליטה וטיגון חוזר, ומציג פשרה בין מאמץ לבין פריכות ומבנה עמילני.','EMPIRICAL_OBSERVATION','08_Decision-Making','Starch-Gelatinization-Retrogradation','דירוגי הטעם והמאמץ הם העדפת המחבר; אינם מדידה אובייקטיבית כללית.'),
]

RULES = [
 (1,'Egg-Poaching-Choices','שליקת ביצה: חומצה מול עדינות טעם',2,'אם רוצים ביצה שלוקה ולבן עדין','אפשר לבחור מעט חומצה כשמקבלים את השפעתה על הטעם והמרקם, או להימנע ממנה כשעדינות טעם חשובה יותר','לפי התיאור במקור, האצה בהתייצבות אינה בהכרח יתרון מיידי ויכולה להוביל להתייצבות יתר','התאמה לריכוז, זמן וטריות הביצה; אין ערובה שכל שיטה תייצר אותה צורה','עם חומצה: שינוי בהתייצבות ובטעם; ללא חומצה: שמירת טעם עדין, עם צורך בטיפול אחר בלבן','Poaching-Scrambling-And-French-Omelet-Control'),
 (2,'Braise-Heat-Source','תבשיל סמיך: תנור או כיריים',3,'אם תבשיל סמיך נדרש לחימום ממושך','אפשר להשתמש בתנור עם סיר מתאים, או בכיריים עם בקרה וערבוב לפי הצורך','המקור מבחין בחימום תחתית מקומי לעומת חימום מכמה כיוונים','יש לוודא התאמת הסיר והמכסה לתנור; אין להסיק זמן בישול זהה','תנור מפחית צורך בבקרת תחתית אך דורש כלי מתאים; כיריים נגישות לבדיקה אך מחייבות מעקב','Covered-Vs-Uncovered-Evaporation'),
 (3,'Cut-Method-Choice','נתח רך או עתיר רקמת חיבור',3,'אם בוחרים שיטת הכנה לנתח מזוהה','בחר חימום מהיר מבוקר לנתח רך כשזו מטרת המנה; שקול בישול ממושך מתאים לנתח עתיר רקמת חיבור','חימום לטמפרטורת יעד ופירוק רקמת חיבור הן מטרות שונות','חיתוך, טחינה ויעד קולינרי משנים התאמה; נדרש נוהל בטיחות נפרד','צריבה מדגישה השחמה; בישול לח ממושך נותן זמן לריכוך קולגן','Cut-To-Method-Matching'),
 (4,'Vegetable-Water-Choice','חליטה: נפח מים לפי יעד ותנאים',1,'אם רוצים שעועית ירוקה רכה־פריכה וירוקה','אפשר להשתמש במסת מים שממתנת את ירידת הטמפרטורה, או לבחון חלופה מותאמת לעומס ולציוד','בניסוי המתואר מעט מים התקררו יותר לאחר הוספת השעועית','אין להחיל את ממצאי השעועית על פסטה או על כל ירק','יותר מים דורשים חימום ראשוני גדול; פחות מים מחייבים התאמת עומס ובדיקת צבע ורכות','Heat-Transfer'),
 (5,'Ground-Meat-Texture','בשר טחון: מבנה רך או מלוכד',3,'אם מרקם הבשר הטחון הוא יעד ההכנה','להמבורגר רך צמצם לישה מיותרת; למוצר שמבנהו המלוכד רצוי אפשר לבחור עיבוד מכוון','המקור מתאר התהדקות עם טיפול עודף; ההרחבה למוצר מלוכד היא פרשנות קולינרית','יש להפריד טחינה קרה ובטיחות מאפקט הלישה; אין כלל אחד לכל מתכון נקניק','פחות עיבוד שומר פירור רך; עיבוד מכוון משפר אחידות אך עלול ליצור מרקם קפיצי','Sausage-Emulsions-Myosin-And-Nitrite-Curing'),
 (6,'Bird-Geometry','עוף שלם: פרישה מול צלייה שלמה',1,'אם רוצים לתאם בישול חזה וירכיים','אפשר לפרוש את העוף לשינוי חשיפת החלקים, או לשמור צורה שלמה ולבקר את החלקים בנפרד','הספר מסביר שהפרישה חושפת יותר את הבשר הכהה','אין לאמץ טמפרטורות בטיחות מקוצרות בלי נוהל מאומת; בדיקה בכמה נקודות נדרשת','פרישה משנה הצגה ומקום בתבנית; צורה שלמה שומרת הצגה אך מקשה על אחידות','Whole-Bird-Roasting-And-Crisp-Poultry-Skin'),
 (7,'Pasta-Hydration-Choice','פסטה אפויה: השריה או בישול מקדים',3,'אם מכינים פסטה הממשיכה להתבשל ברוטב בתנור','אפשר להשתמש בהשריה מותאמת או בבישול מקדים מותאם, ולכוון נוזל ברוטב בהתאם','המקור מפריד ספיחת מים משלב הבישול בחום','השריה אינה בישול מלא; תנאי זמן ושמירה חייבים להגיע מהמתכון המתאים','השריה משנה תזמון וספיחת רוטב; בישול מקדים מוסיף שלב ועלול להביא לבישול יתר','Starch-Gelatinization-Retrogradation'),
 (8,'Vinaigrette-Stability','ויניגרט: יציבות מול טעם נקי',1,'אם רוטב שמן וחומץ צריך להמתין לפני ההגשה','אפשר להוסיף חרדל כשמתאים לטעם ולרגישויות, או לבחור רוטב ללא חרדל ולערבב סמוך להגשה','בניסוי המתואר חרדל האט את ההפרדה','חרדל הוא רכיב בעל השלכות טעם ורגישות; אין הבטחת יציבות בלתי מוגבלת','יציבות ארוכה יותר משנה טעם; פחות תוספים מצריכים ערבוב חוזר','Caramelization-And-Emulsification'),
 (9,'Fries-Effort-Crispness','צ׳יפס: פשטות מול פריכות מרבית',4,'אם בוחרים שיטת צ׳יפס בהתאם לזמן ולמרקם המבוקש','אפשר לבחור שיטה פשוטה או שיטה רב־שלבית עם חליטה וטיגון חוזר לפי מתכון מלא','המחבר מציג תוצאת פריכות שונה ופשרה במאמץ','אין כאן פרוטוקול טיגון עצמאי; נדרשים מתכון מלא וציוד בטוח','פחות שלבים חוסכים מאמץ; יותר שלבים מאפשרים שליטה במבנה ובפריכות','Starch-Gelatinization-Retrogradation'),
]


def paragraphs(raw):
    body = ET.fromstring(raw).find('{*}body')
    return [' '.join(e.itertext()).strip() for e in body.iter() if e.tag.rsplit('}',1)[-1] == 'p'] if body is not None else []


def write_note(path, meta, body):
    text = '---\n' + yaml.safe_dump(meta, allow_unicode=True, sort_keys=False, width=110) + '---\n\n' + body + '\n'
    if path.exists():
        if path.read_text(encoding='utf-8') != text:
            raise RuntimeError(f'Refusing to overwrite existing content: {path}')
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8')


def main():
    originals = {}
    app_root=ROOT.parents[1]/'backend'
    application_hashes={str(p.relative_to(app_root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in app_root.rglob('*') if p.is_file() and p.suffix in ('.py','.js','.css','.html','.yaml','.json')}
    nodes = {}
    for p in ROOT.rglob('*.md'):
        if 'FoodLab-2015' in str(p) or p.stem.startswith('FoodLab-CH'):
            continue
        originals[str(p.relative_to(ROOT))] = hashlib.sha256(p.read_bytes()).hexdigest()
        text = p.read_text(encoding='utf-8-sig')
        if text.startswith('---'):
            m = yaml.safe_load(text.split('---',2)[1])
            if isinstance(m,dict) and m.get('id'): nodes[p.stem] = m['id']
    inventory = []
    with zipfile.ZipFile(BOOK) as z:
        nav = ET.fromstring(z.read('nav.xhtml'))
        chapters = []
        for a in nav.iter():
            label = ' '.join(a.itertext()).strip() if a.tag.endswith('}a') else ''
            if re.match(r'^[1-9] ',label): chapters.append((int(re.search(r'part(\d+)',a.attrib['href']).group(1)),label))
        for name in sorted(z.namelist()):
            if not re.match(r'text/part\d+\.html$',name): continue
            raw = z.read(name); ps = paragraphs(raw)
            i = int(re.search(r'part(\d+)',name).group(1))
            chapter = next((k+1 for k,(lo,_) in enumerate(chapters) if lo <= i < (chapters[k+1][0] if k+1<len(chapters) else 455)), None)
            inventory.append({'internal_path':name,'chapter':chapter,'sha256':hashlib.sha256(raw).hexdigest(),'paragraph_count':len(ps),'characters':sum(map(len,ps)), 'coverage':'STRUCTURAL_SCAN; SELECTED_CLAIMS_ONLY' if chapter else 'OUTSIDE_NUMBERED_CHAPTERS'})
        records = []
        counts = {}
        for ch,part,needle,slug,title,claim,kind,folder,canonical,limits in ROWS:
            counts[ch] = counts.get(ch,0)+1; n=counts[ch]
            name=f'text/part{part:04d}.html'; ps=paragraphs(z.read(name))
            matches=[(j+1,t) for j,t in enumerate(ps) if needle.casefold() in t.casefold() and len(t)>150]
            if len(matches)!=1: raise RuntimeError((name,needle,len(matches)))
            j,paragraph=matches[0]
            eid=f'EVD-FLB-CH{ch:02d}-{n:03d}'
            cid=f'CLM-FLB-CH{ch:02d}-{n:03d}'
            stem=f'FoodLab-CH{ch:02d}-{slug}'
            canonical_id=nodes[canonical]
            locator={'internal_path':name,'paragraph_index':j,'paragraph_selector':'body descendant p; 1-based; includes empty p; itertext joined with a space then stripped','paragraph_sha256':hashlib.sha256(paragraph.encode()).hexdigest(),'anchor_status':'UNKNOWN','pdf_page':'UNKNOWN','printed_page':'UNKNOWN'}
            meta={'id':eid,'type':'EVIDENCE_RECORD','name':title,'domain':folder.split('_',1)[1].upper(),'knowledge_type':kind,'claim_id':cid,'claim_type':'SOURCE_SUPPORTED_CLAIM','claim':claim,'canonical_concept_id':canonical_id,'verification_status':'PRELIMINARY','source_text_checked':True,'scientific_validation':'NOT_INDEPENDENTLY_VALIDATED','confidence':{'source_traceability':'HIGH','generalizability':'CONDITIONAL','score_is_probability':False},'conditions':[limits],'sources':[{'source_id':SOURCE,'book_title':'The Food Lab: Better Home Cooking Through Science','author':'J. Kenji López-Alt','edition':'First Edition','year':2015,'chapter':chapters[ch-1][1],'epub_sha256':BOOK_HASH,**locator}],'relationships':[{'type':'SUPPORTED_BY','target_id':SOURCE,'target_name':'[[SRC-FOODLAB-2015]]','evidence':cid,'confidence':'HIGH_FOR_SOURCE_ATTRIBUTION'},{'type':'SUPPORTS','target_id':canonical_id,'target_name':f'[[{canonical}]]','conditions':limits,'confidence':'CONDITIONAL_INTERPRETIVE_MAPPING'}]}
            body=f'# {title}\n\n{claim}\n\nתנאים ומגבלות: {limits}\n\nהטענה נתמכת בפסקה שצוינה בספר; היא אינה אימות מדעי חיצוני. שיוך הטענה למושג הקיים [[{canonical}]] הוא מיפוי פרשני.\n\nמקור: [[SRC-FOODLAB-2015]], {chapters[ch-1][1]}, `{name}`, פסקה {j}. אין מספר עמוד PDF או עמוד מודפס זמין בעותק זה.\n\nלמפת הפרק: [[FoodLab-2015-Chapter-{ch:02d}]].'
            write_note(ROOT/folder/(stem+'.md'),meta,body)
            records.append({'id':eid,'claim_id':cid,'stem':stem,'chapter':ch,'canonical':canonical,'canonical_id':canonical_id,'path':str((Path(folder)/(stem+'.md')).as_posix()),'locator':locator,'kind':kind})
        for ch,slug,title,which,if_,then,because,exceptions,tradeoffs,canonical in RULES:
            evidence=[r for r in records if r['chapter']==ch][which-1]
            rid=f'RUL-FLB-CH{ch:02d}-001';stem=f'FoodLab-CH{ch:02d}-Rule-{slug}'
            reuse={2:'RUL-MEAT-001',3:'RUL-MEAT-002',6:'RUL-MEAT-003'}
            meta={'id':rid,'canonical_rule_id':reuse.get(ch,'NEW_DRAFT_RULE'),'type':'CULINARY_RULE','name':title,'domain':'RULES','verification_status':'PRELIMINARY','claim_type':'INTERPRETATION','if':if_,'then':then,'because':because,'exceptions':[exceptions],'tradeoffs':tradeoffs,'source_claim_ids':[evidence['claim_id']],'sources':[{'source_id':SOURCE,'edition':'First Edition','book_title':'The Food Lab: Better Home Cooking Through Science','author':'J. Kenji L\u00f3pez-Alt','year':2015,'knowledge_type':'CONDITIONAL_RULE_INTERPRETATION','chapter':chapters[ch-1][1],**evidence['locator']}],'relationships':[{'type':'SUPPORTED_BY','target_id':evidence['id'],'target_name':f"[[{evidence['stem']}]]",'confidence':'CONDITIONAL','evidence':evidence['claim_id']},{'type':'SUPPORTED_BY','target_id':nodes[canonical],'target_name':f'[[{canonical}]]','conditions':'השוואת בחירות בתוך ההקשר בלבד; אינה סתירה גורפת','confidence':'INTERPRETIVE'}]}
            write_note(ROOT/'12_Rules'/(stem+'.md'),meta,f'# {title}\n\n**IF:** {if_}\n\n**THEN:** {then}\n\n**BECAUSE:** {because}\n\n**EXCEPTIONS:** {exceptions}\n\nפשרות וחלופות: {tradeoffs}\n\nכלל פרשני, ולא ציטוט או פרוטוקול מלא מהספר. ביסוס: [[{evidence["stem"]}]]. המושג הקיים נשמר: [[{canonical}]]. אין הפעלה אוטומטית במנוע השף.')
        for ch,(_,title) in enumerate(chapters,1):
            rs=[r for r in records if r['chapter']==ch]
            rule=next(x for x in RULES if x[0]==ch)
            listing='\n'.join(f'- [[{r["stem"]}]] → [[{r["canonical"]}]] — `{r["claim_id"]}`' for r in rs)
            write_note(OUT/f'FoodLab-2015-Chapter-{ch:02d}.md',{'id':f'SRC-FLB-CH{ch:02d}','type':'CHAPTER_EVIDENCE_MAP','name':title,'source_id':SOURCE,'verification_status':'PRELIMINARY','coverage':'SELECTIVE_STRUCTURED_EXTRACTION_NOT_EXHAUSTIVE','claim_count':len(rs),'rule_count':1},f'# {title}\n\n{listing}\n\nכלל מותנה: [[FoodLab-CH{ch:02d}-Rule-{rule[1]}]].\n\nכל קובצי הפרק מופו במניפסט; חילוץ הטענות ממוקד בעקרונות ליבה ואינו העתקה או קידוד של כל מתכון.\n\n[[FoodLab-2015-Report-HE]]')
    manifest={'source_id':SOURCE,'book_path':str(BOOK),'book_sha256':BOOK_HASH,'edition':'First Edition','year':2015,'format':'EPUB','ebook_isbn':'9780393249866','chapter_boundaries':chapters,'chapter_end_exclusive':455,'pagination':'UNKNOWN; NO_PAGE_LIST_OR_PAGEBREAKS_FOUND','files':inventory,'records':records,'existing_knowledge_hashes':originals,'application_hashes':application_hashes,'original_pdf_modified':False,'chef_application_modified':False}
    mp=OUT/'FoodLab-2015-manifest.json'
    if mp.exists(): raise RuntimeError('Manifest already exists; review before rerun')
    mp.write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'records':len(records),'rules':len(RULES),'chapters':len(chapters),'files_scanned':len(inventory),'source_sha256':BOOK_HASH}))


if __name__ == '__main__':
    main()
