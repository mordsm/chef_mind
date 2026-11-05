"""Rebuild source-anchored Hebrew culinary notes, distinct from raw page capture."""

import hashlib
import json
from pathlib import Path

from build_book_network import DEST, SCRATCH, VAULT, write_note

# folder, title, page, source anchor, specific query aliases, Hebrew interpretation,
# existing canonical concept. Anchors are checked against the actual extracted page.
NOTES = [
    ("04_Flavors", "המרת מלח לפי משקל ולא לפי נפח", 44, "almost twice as salty by volume", ["מלח כשר", "kosher salt", "Diamond Crystal", "Morton"],
     "מותגי מלח שונים נבדלים בצפיפות. אין להחליף אותה כמות נפח בין Diamond Crystal ל־Morton בלי התאמה; השתמש במשקל או בהמרה המתאימה לסוג המלח.", "FLV-TASTE-001"),
    ("04_Flavors", "המלחה והפחתת מרירות", 47, "salt masks bitterness", ["מרירות", "אשכולית", "bitter"],
     "כשמנה מוכנה לטעימה מרגישה מרה, נסה מעט מלח בכף נפרדת לפני שינוי כל הסיר. מלח משנה את תפיסת המרירות; הוא אינו מסלק את החומר המר.", "FLV-TASTE-001"),
    ("02_Food-Science", "פיזור מלח אל פנים המזון", 50, "the salt will have begun to move inward", ["המלחה מראש", "דיפוזיה", "presalting"],
     "היעלמות גבישי המלח מהמשטח אינה אומרת שכל הנתח מתובל באופן אחיד. פיזור המלח פנימה זקוק לזמן; גודל הנתח והרכבו משנים את הקצב.", "FLV-TASTE-001"),
    ("03_Techniques", "המסה של מלח לפני הוספת שומן", 54, "dissolve salt in water", ["ויניגרט", "מיונז", "חמאה מתובלת", "vinaigrette", "mayonnaise"],
     "להמלחה אחידה ברוטב שמן, המס את המלח תחילה בחלק המימי, בחומץ או במיץ הלימון, ואז הוסף את השומן. אל תמהר להוסיף עוד מלח לפני שהראשון התמוסס.", "SCI-CHEM-002"),
    ("03_Techniques", "תזמון מלח בתערובות ביצים", 54, "Add a pinch of salt to eggs destined", ["מקושקשת", "אומלט", "פריטטה", "scrambled eggs", "omelette"],
     "המחברת ממליצה להמליח תערובות למקושקשת, אומלט ופריטטה לפני החימום. אין להחיל זאת אוטומטית על ביצה מטוגנת או בקליפה, שאותן היא מתבלת בהגשה.", "ING-EGG-001"),
    ("02_Food-Science", "מלח ומבנה בצק", 56, "salt aids in strengthening gluten", ["בצק לחם", "בצק פיצה", "גלוטן", "bread dough"],
     "מלח משפיע על חוזק רשת הגלוטן ולא רק על הטעם. שינוי סדר ההוספה עשוי לשנות את התחושה בזמן הלישה; תן לבצק זמן מנוחה לפי המתכון.", "SCI-PROT-002"),
    ("04_Flavors", "מלח במנות שסופגות את כל הנוזל", 56, "all of the cooking water will be absorbed", ["ספיגת נוזלים", "אורז בספיגה", "absorption rice"],
     "כאשר כל נוזל הבישול נספג במזון, גם המלח נשאר במנה. תבל את הנוזל במתינות רבה יותר מאשר מי חליטה שנשפכים בסיום.", "FLV-TASTE-001"),
    ("03_Techniques", "טחינת תבלינים סמוך לשימוש", 70, "Purchase whole spices", ["תבלינים", "טחינת תבלינים", "spices"],
     "לטעם מודגש, טחן תבלינים שלמים סמוך לשימוש. הטחינה והחימום משחררים ארומות, ולכן אחסון ממושך לאחר הטחינה משנה את עוצמתם.", "FLV-AROMA-001"),
    ("04_Flavors", "מלח בקינוחים", 70, "salt will also improve a sweet dessert", ["עוגיות", "קינוח", "בצק מתוק", "cookies"],
     "גם בצק או קרם מתוק זקוקים לאיזון. ערבב מלח דק בתערובת להמסה אחידה; מלח פתיתים מעל קינוח מוסיף גם מרקם, ולכן אינו תחליף אוטומטי למלח שבתוכו.", "FLV-TASTE-001"),
    ("08_Decision-Making", "דילול מנה שהומלחה יתר על המידה", 76, "Add more unseasoned ingredients", ["מלוח מדי", "המלחת יתר", "oversalted"],
     "למנה מלוחה מדי אפשר להוסיף מרכיבים לא מומלחים. אם המלח התרכז בעקבות אידוי, החזר נוזל לא מומלח; אם הכמות תהיה גדולה מדי, תקן רק חלק מהמנה.", "DEC-CORR-001"),
    ("08_Decision-Making", "בדיקת איזון לפני תיקון מלח", 76, "Doctor up a spoonful", ["טעם מלוח", "איזון מלח", "salt balance"],
     "לפני דילול סיר שלם, בדוק בכף נפרדת אם מעט חומצה או שומן משפרים את האיזון. הם משנים את תפיסת הטעם, אך אינם מוציאים מלח מהמנה.", "FLV-BAL-001"),
    ("08_Decision-Making", "שינוי תפקיד של מזון מלוח מדי", 77, "Shred an oversalted piece of meat", ["בשר מלוח מדי", "oversalted meat"],
     "בשר מבושל ומלוח מדי יכול להפוך למרכיב קטן במנה גדולה יותר, כמו מרק או מילוי. נוזל בישול מלוח אינו חייב לעבור יחד איתו למנה החדשה.", "DEC-CORR-001"),
    ("08_Decision-Making", "בחירת תפקיד השומן במנה", 85, "identify the primary role", ["בחירת שומן", "שומן לבישול", "cooking fat"],
     "בחר שומן לפי תפקידו: חומר גלם שמשנה טעם ומרקם, אמצעי להעברת חום, או תוספת סיום. שומן שמתאים לתפקיד אחד אינו בהכרח מתאים לאחר.", "FLV-AROMA-001"),
    ("01_Ingredients", "הערכת שמן זית באמצעות טעם וריח", 89, "taste, not price", ["שמן זית", "olive oil"],
     "צבע ומחיר אינם מספיקים להערכת שמן זית. טעם והריח הם כלי ההשוואה שמציעה המחברת; בחר שמן שמתאים למנה ולא רק לתווית.", "FLV-AROMA-001"),
    ("06_Equipment", "אחסון שמן זית במקום יציב וחשוך", 91, "store it somewhere reliably cool and dark", ["אחסון שמן זית", "olive oil storage"],
     "אחסן שמן זית במקום קריר וחשוך, הרחק משינויי חום ליד הכיריים. כלי כהה או אטום לאור מפחית חשיפה לאור כשאין ארון מתאים.", "FLV-AROMA-001"),
    ("03_Techniques", "חמאה מזוקקת ובחירת שומן לחימום", 92, "yield clariﬁed butter", ["חמאה מזוקקת", "גהי", "clarified butter", "ghee"],
     "זיקוק מפריד את מוצקי החלב מהשומן ומשנה את התנהגות החמאה בחימום. השתמש בו כאשר רוצים טעם חמאה וחימום שמתאים פחות לחמאה רגילה.", "ING-DAI-001"),
    ("03_Techniques", "חימום מחבת ושומן עם חריגי שום וחמאה", 101, "exceptions to the preheating rule", ["חימום מחבת", "שום בחמאה", "preheat pan"],
     "בצריבה מחממים תחילה את המחבת ואת השומן, אך שום וחמאה דורשים חימום עדין יותר כדי שלא יישרפו. התאם את הסדר למרכיבים ולכלי.", "TEC-DRY-001"),
    ("03_Techniques", "רינדור שומן בחום מתון", 102, "rendered , or cooked over gentle heat", ["רינדור", "שומן ברווז", "rendering"],
     "להמסה הדרגתית של שומן מוצק השתמש בחימום מתון; השחמה חיצונית מהירה אינה מבטיחה שהשומן הספיק להינמס. כמות קטנה של מים יכולה למתן את תחילת החימום.", "ING-MEAT-003"),
    ("05_Textures", "שמירת פריכות לאחר הטיגון", 104, "do not cover or pile up crisp foods", ["טיגון", "פריכות", "fried food"],
     "אל תערום ואל תכסה מזון פריך בעודו חם. האדים המשתחררים נלכדים, מתעבים ומרככים את המעטפת. השאר מקום לאדים לצאת.", "TEX-CRUST-001"),
    ("02_Food-Science", "תחליב ויציבות רוטב לסלט", 106, "Mustard often plays the role", ["ויניגרט", "חרדל בויניגרט", "vinaigrette"],
     "ערבוב מפזר נוזל אחד בטיפות קטנות בתוך האחר; חרדל יכול לסייע ליציבות ויניגרט. רוטב שהתפרק עשוי לתבל עלים בצורה לא אחידה, ולכן ערבב לפני ההגשה.", "SCI-CHEM-002"),
    ("03_Techniques", "הוספת שמן מדורגת למיונז", 108, "adding in the oil one drop at a time", ["הכנת מיונז", "מיונז", "mayonnaise"],
     "במיונז מתחילים בהוספת שמן איטית מאוד תוך טריפה. אחרי שנוצר בסיס יציב אפשר להגביר את הקצב. אם התערובת סמיכה מדי, מתקנים במעט נוזל מתאים.", "SCI-CHEM-002"),
    ("03_Techniques", "סיום רוטב עם חמאה קרה", 110, "very cold butter", ["רוטב חמאה", "פסטה בחמאה", "butter sauce"],
     "ברוטב חמאה נחוץ גם נוזל מימי. הוסף חמאה קרה וערבב תוך שליטה בחום; כשהרוטב מתחיל להסמיך, החום השיורי יכול להשלים את ההמסה.", "ING-DAI-001"),
    ("08_Decision-Making", "עצירה ושיקום של מיונז שנשבר", 111, "stop adding fat", ["מיונז נשבר", "מיונז התפרק", "broken mayonnaise"],
     "אם מיונז מפסיק להסמיך, עצור את הוספת השמן. לשיקום, צור בסיס מימי קטן בקערה נקייה וטרוף לתוכו את התערובת השבורה בהדרגה; חלמון חדש הוא אפשרות נוספת.", "DEC-CORR-001"),
    ("05_Textures", "בצק פריך מול בצק מתפורר", 114, "fat prevents them from sticking", ["בצק פריך", "shortbread", "גלוטן"],
     "ערבוב שומן בקמח מגביל יצירת רשת גלוטן ומשנה את המרקם. ערבוב אינטימי מתאים למרקם מתפורר; למרקם עלעלי יש לשמר חלק מהשומן כחתיכות נפרדות.", "SCI-PROT-002"),
    ("03_Techniques", "חתיכות חמאה קרות לבצק עלעלי", 115, "fat must be very cold", ["בצק פאי", "בצק עלעלי", "pie dough"],
     "לבצק פאי עלעלי שמור חתיכות חמאה קרות ונפרדות יחסית. החימום בתנור והאדים מסייעים להפריד שכבות; ערבוב יתר או המסה מוקדמת משנים את התוצאה.", "ING-DAI-001"),
    ("03_Techniques", "בקרת טמפרטורה בזמן הכנת בצק", 120, "Don’t overmix", ["בצק פאי חם", "קירור בצק", "pastry dough"],
     "אם החמאה מתרככת במהלך העבודה, עצור וצנן את הבצק והכלים. עבוד מהר ואל תערבב יתר על המידה; הכנס מאפה מורכב וקר לתנור שחומם מראש.", "ING-DAI-001"),
    ("03_Techniques", "הקצפת חמאה וסוכר ליצירת אווריריות", 123, "creaming", ["הקצפת חמאה", "עוגת חמאה", "creaming butter"],
     "הקצפת חמאה וסוכר לוכדת בועות אוויר. חמאה רכה מדי אינה מחזיקה אותן היטב, וקרה מדי מקשה על פיזורן; עקוב אחר המרקם והטמפרטורה, ולא רק זמן ההקצפה.", "TEC-EGG-004"),
    ("03_Techniques", "קיפול עדין ושמירת האוויר בבלילה", 124, "folding", ["קיפול בלילה", "בלילת עוגה", "folding batter"],
     "לאחר יצירת קצף או תערובת מוקצפת, חבר אותה לשאר המרכיבים בתנועות קיפול עדינות. ערבוב אגרסיבי יכול לאבד אוויר שכבר הוכנס.", "TEC-EGG-004"),
    ("05_Textures", "עצירת הקצפת שמנת בזמן", 124, "Overwhip cream", ["קצפת", "הקצפת שמנת", "whipped cream"],
     "הקצף שמנת קרה ועקוב אחר המרקם. הקצפת יתר מאחדת את השומן ובהמשך מפרידה את התערובת לשומן ולנוזל; עצור כשמתקבל המרקם הדרוש למנה.", "ING-DAI-001"),
    ("03_Techniques", "ריכוך ירקות לפני רוטב חומצי", 143, "cook onions until they’re tender", ["בצל ברוטב עגבניות", "שעועית בעגבניות", "ירקות ברוטב עגבניות"],
     "חומצה יכולה להאט ריכוך של ירקות וקטניות. אם נדרשת תוצאה רכה ברוטב עגבניות, רכך קודם את המרכיב המתאים לפני הוספת העגבניות.", "FLV-BAL-001"),
    ("03_Techniques", "חלב ומנה חומצית", 145, "dairy should only be added", ["חלב ברוטב", "רוטב חומצי וחלב", "dairy acid"],
     "חומצה יכולה להקריש חלבוני חלב. הוסף רכיב חלבי מתאים בשלב מאוחר ובחימום מבוקר; מוצרים שונים, ובהם שמנת עתירת שומן, אינם מתנהגים באותו אופן.", "SCI-PROT-002"),
    ("02_Food-Science", "זמן השריה בחומצה ומרקם חלבון", 146, "continues to sit in acid", ["מרינדה חומצית", "סביצ׳ה", "acid marinade", "ceviche"],
     "השריה ממושכת בחומצה יכולה לשנות מרקם ולהוציא מים מחלבונים. התאמה דורשת סוג מרכיב, ריכוז וזמן; שינוי מרקם בדג אינו אישור בטיחות.", "SCI-MEAT-003"),
    ("04_Flavors", "חומצה בסיום לעומת חומצה בבישול", 151, "Garnishing acids", ["סיום בלימון", "תיבול בחומץ", "finishing acid"],
     "חומצה שמוסיפים בסיום מדגישה רעננות וארומה, בעוד חומצה שמתבשלת במנה משתלבת אחרת. בחר את תזמון ההוספה לפי התוצאה הרצויה וטעם בהדרגה.", "FLV-BAL-001"),
    ("04_Flavors", "אומאמי במינון שמתאים למנה", 158, "a little umami", ["אומאמי", "umami"],
     "רכיבי אומאמי רבים מביאים איתם גם מלח וחומצה. בחר תוספת שמתאימה למנה ובדוק את האיזון הכולל במקום לצרף כמה מקורות חזקים ללא הבחנה.", "FLV-BAL-001"),
    ("04_Flavors", "איזון ארוחה שלמה", 162, "a good meal should also be balanced", ["תכנון תפריט", "סלט לצד מאפה", "menu balance"],
     "שפוט תיבול גם ביחס לשאר הארוחה. סלט שנלווה למנה עשירה יכול להזדקק לחדות חומצית רבה יותר מאותו סלט שמוגש לבדו.", "FLV-BAL-001"),
    ("06_Equipment", "צפיפות בתבנית ותנועת אדים", 176, "Choose your cooking vessel", ["צפיפות בתבנית", "ירקות בתנור", "roasting vegetables"],
     "כמות המזון וצורת הכלי משנות את יציאת האדים. פיזור מאפשר השחמה; צפיפות ולכידת לחות עשויות להתאים כשמבקשים קודם ריכוך של ירק צפוף.", "EQP-ENV-001"),
    ("02_Food-Science", "מים חום ומרקם עמילן", 179, "correct amount of water and heat", ["בישול עמילנים", "אורז קשה", "פסטה רכה מדי", "starch cooking"],
     "עמילנים צריכים שילוב מתאים של מים וחימום. חוסר מים או חימום משאיר מרכז קשה; עודף מים או בישול ממושך מדי עלולים לתת מרקם רך מדי.", "SCI-CARB-001"),
    ("02_Food-Science", "פקטין בריבות", 183, "gelling agent when combined with sugar and acid", ["ריבה", "מרמלדה", "פקטין", "jam"],
     "פקטין יכול ליצור ג׳ל בנוכחות התנאים המתאימים של סוכר, חומצה וחימום. פרי, קליפה וגרעינים תורמים כמויות שונות; אין יחס אחד שמתאים לכל ריבה.", "SCI-CARB-001"),
    ("08_Decision-Making", "שמירת רכות מול יצירת רכות", 191, "preserving innate tenderness", ["בחירת שיטת בישול", "נתח רך", "נתח קשה", "tender cut"],
     "שאל אם מטרת החימום היא לשמור על רכות שכבר קיימת או ליצור רכות בחומר גלם קשה. הבחירה הזאת קודמת לקביעת זמן ועוצמת חום.", "DEC-PLAN-001"),
    ("06_Equipment", "מחזורי תרמוסטט ותנור ביתי", 192, "miscalibrated", ["תנור ביתי", "כיול תנור", "oven temperature"],
     "הטמפרטורה בתנור משתנה במהלך מחזורי החימום ופתיחת הדלת. ההגדרה היא נקודת ייחוס; עקוב אחר השחמה, התייצבות ומדידה מתאימה למזון.", "SCI-HEAT-001"),
    ("03_Techniques", "אמבט מים וחום שיורי בקסטרד", 201, "residual heat", ["קסטרד", "קרם קרמל", "עוגת גבינה", "custard"],
     "אמבט מים ממתן את החימום אך אינו מונע בישול יתר. הבא בחשבון המשך התייצבות אחרי ההוצאה והוצא את הכלים בזהירות מהאמבט לפי המתכון.", "TEC-EGG-003"),
    ("03_Techniques", "קערה מעל אדים לחימום עדין", 202, "a large bowl over a pot", ["בן מארי", "המסת שוקולד", "הולנדז", "double boiler"],
     "קערה מעל סיר עם מים מבעבעים בעדינות מאפשרת חימום מבוקר של שוקולד או רוטב עדין. החום עקיף, ועדיין נדרשים ערבוב ומעקב אחר המרקם.", "SCI-HEAT-001"),
    ("03_Techniques", "נפח מים ועומס בחליטה", 208, "too much food to too little water", ["חליטת ירקות", "בישול פסטה", "blanching"],
     "הוספת כמות גדולה של מזון מורידה את טמפרטורת המים. בחליטה שדורשת רתיחה פעילה, התאם את גודל הסיר ואת הכמות בכל סבב כדי לאפשר בישול אחיד.", "TEC-MOIST-001"),
    ("03_Techniques", "עומס טיגון ובקרת טמפרטורת השמן", 216, "always let oil temperature return", ["טיגון עמוק", "שמן מתקרר", "deep frying"],
     "מזון קר או כמות גדולה מורידים את חום השמן. טגן בסבבים והמתן שהשמן יחזור לטווח שנדרש במתכון לפני הסבב הבא; בדוק במדחום מתאים.", "SCI-HEAT-001"),
    ("03_Techniques", "הוצאת אגוזים מתבנית קלייה חמה", 223, "remove them from their hot trays", ["קליית אגוזים", "קליית תבלינים", "toasting nuts"],
     "בסיום קלייה, העבר אגוזים או תבלינים מהתבנית החמה לכלי מתאים. החום השיורי ממשיך להשחים אותם גם אחרי הוצאת התבנית מהתנור.", "TEC-MEAT-004"),
    ("03_Techniques", "אורז בספיגה ומנוחה מכוסה", 348, "Let it rest covered for 10 minutes", ["אורז בספיגה", "אורז בסמטי", "אורז יסמין", "steamed rice"],
     "בשיטת הספיגה מבשלים בעדינות ובכיסוי ביחס נוזל שמתאים לזן. לאחר ספיגת הנוזל וריכוך הגרגרים, הספר מציע מנוחה מכוסה של עשר דקות לפני אוורור במזלג.", "SCI-CARB-001"),
    ("03_Techniques", "ערבוב הדרגתי של נוזל בריזוטו", 351, "add stock gradually", ["ריזוטו", "risotto"],
     "בריזוטו מוסיפים ציר בהדרגה תוך ערבוב, ומחכים לספיגה לפני הוספה נוספת. בדוק רכות עם מרכז נגיס והתאם את הנוזל כדי לשמור על מרקם זורם.", "TEX-VISC-001"),
    ("03_Techniques", "הוספת פולנטה בזרם תוך טריפה", 351, "Add polenta or grits in a thin stream", ["פולנטה", "גריטס", "polenta", "grits"],
     "הוסף פולנטה לנוזל הרותח בזרם דק תוך טריפה, ולא כגוש אחד. המשך ערבוב ובדוק רכות; הוסף נוזל לפי הצורך במקום להסתמך רק על זמן.", "SCI-CARB-001"),
]


def build():
    pages = {row["pdf_page"]: row for row in json.loads((SCRATCH / "nosrat-pages.json").read_text(encoding="utf-8"))}
    records = []
    for i, (folder, title, page, anchor, aliases, tip, concept) in enumerate(NOTES, 1):
        raw = Path(pages[page]["text_path"]).read_text(encoding="utf-8")
        normalized = " ".join(raw.split())
        if " ".join(anchor.split()) not in normalized:
            raise ValueError(f"Source anchor not found: page {page}, {anchor!r}")
        node_id = f"EVD-NOS-FULL-{i:03}"
        meta = {"id": node_id, "type": "EVIDENCE_RECORD", "name": title,
                "domain": folder.split("_", 1)[1].upper(), "verification_status": "PRELIMINARY",
                "source_text_checked": True, "claim_type": "INTERPRETATION",
                "scientific_validation": "NOT_INDEPENDENTLY_VALIDATED", "description": tip, "claim": tip,
                "chef_tip": tip, "target_foods": aliases, "tags": aliases,
                "conditions": {"method_id": ""}, "checkpoints": [],
                "step_keywords": ["תיבול", "המלח", "ערבב", "בישול", "חימום", "הכנת", "תנור", "רוטב"],
                "recommended_equipment": [], "runtime_use": "EXPLANATION_ONLY",
                "sources": [{"source_id": "SRC-NOSRAT-2017", "citation": f"Nosrat, Salt, Fat, Acid, Heat (2017), PDF {page}",
                             "pdf_pages": [page], "split_page": [page],
                             "split_filename": pages[page]["source_filename"], "pdf_sha256": pages[page]["source_sha256"],
                             "evidence_anchor": anchor, "anchor_sha256": hashlib.sha256(anchor.encode()).hexdigest()}],
                "relationships": [{"type": "SUPPORTED_BY", "target_id": f"PAGE-NOSRAT-{page:03}"},
                                  {"type": "SUPPORTED_BY", "target_id": "SRC-NOSRAT-2017"},
                                  {"type": "MENTIONS", "target_id": concept}]}
        body = f"# {title}\n\n{tip}\n\nמקור: [[nosrat-page-{page:03}]] מתוך [[SRC-NOSRAT-2017]].\n\n"
        body += "הערה מעובדת בעברית עם עוגן טקסט שנבדק במקור. אין כאן אימות מדעי עצמאי או פרוטוקול בטיחות.\n"
        path = VAULT / folder / f"{node_id}.md"
        write_note(path, meta, body)
        records.append({"id": node_id, "path": path.relative_to(VAULT).as_posix(), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
    manifest_path = DEST / "reviewed-manifest.json"
    existing = json.loads(manifest_path.read_text(encoding="utf-8"))["records"] if manifest_path.exists() else []
    records = [row for row in existing if not row["id"].startswith("EVD-NOS-FULL-")] + records
    manifest_path.write_text(json.dumps({"records": records, "scope": "chef_mind"}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Built {len(records)} source-anchored Hebrew notes")


if __name__ == "__main__":
    build()
