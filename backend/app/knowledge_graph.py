"""Adapted culinary graph with immutable source provenance and separate safety policy.

The supplied YAML is data, never an instruction or a source of automatic safety clearance.
Original times/temperatures remain in the archive; only curated adaptations are activated.
"""

import hashlib
import re
from copy import deepcopy
from functools import lru_cache
from pathlib import Path

import yaml
from pydantic import Field

from app.schemas import StrictModel

SOURCE = Path(__file__).with_name("data") / "culinary_graph_source.yaml"
SAFETY = "https://www.foodsafety.gov/food-safety-charts/safe-minimum-internal-temperatures"
SEAFOOD = (
    "https://www.fda.gov/food/buy-store-serve-safe-food/selecting-and-serving-fresh-and-frozen-seafood-safely"
)

# Editorial adaptations: remove universal ratios, fixed cooking times, unsafe targets,
# compulsory brining, and claims that color/texture/acid alone establishes safety.
PREP = {
    "chicken_breast": "אפשר להשוות עובי כדי לעזור להכנה אחידה. לפני צריבה ניתן לייבש בעדינות; השתמש בכלים נקיים והימנע מזיהום צולב.",
    "chicken_thighs_boneless": "פרוס לעובי דומה לפי המנה, ובדוק אם נשארו עצמות או גידים. סבילות למרקם אינה סיבה להתעלם מטמפרטורת הליבה.",
    "chicken_thighs_bone_in": "לנתח עם עצם בדוק את החלק העבה בלי לגעת בעצם. רכות וצבע סביב העצם אינם אישור מוכנות.",
    "chicken_wings": "אפשר להפריד במפרק אם זה מתאים למנה. לפני צלייה בחום יבש ניתן לייבש את העור בעדינות.",
    "chicken_giblets": "יש להבחין בין קורקבן לכבד: הם דורשים שיטות הכנה שונות. שניהם עדיין דורשים בדיקת בטיחות של עוף.",
    "chicken_whole": "בדוק מוכנות בכמה חלקים עבים של העוף. הכנת העור והקשירה הן אפשרויות קולינריות, לא תחליף למדידה.",
    "turkey_breast": "חזה הודו רזה; עקוב אחר מדידה והימנע מבישול יתר. המלחה מוקדמת היא אפשרות לפי המתכון, לא חובה.",
    "turkey_thigh": "בירך הודו בדוק גידים ועובי. בחר בין פריסה להכנה קצרה יחסית לבין הכנה ארוכה יותר בהתאם למתכון ולגודל.",
    "duck_breast": "יש לאמת אם הנתח הוא חזה ברווז או חזה אווז. טכניקת המסת שומן אינה מאפשרת להשתמש בדרגת עשייה ורודה כאישור בטיחות.",
    "duck_leg": "יש לאמת אם מדובר בשוק ברווז או אווז. קונפי דורש מתכון מתאים ובקרת חום; טמפרטורת מרקם גבוהה אינה סף הבטיחות המינימלי.",
    "beef_ribeye": "אפשר לייבש בעדינות לפני צריבה ולפרוס בניצב לסיבים. תכנון מנוחה קולינרית נפרד ממנוחת הבטיחות הנדרשת.",
    "beef_tenderloin": "פילה רזה; עקוב אחר טמפרטורה והתאם את השיטה לעובי. חמאה או השקיה בשומן הן אפשרויות בלבד בהתאם לתזונה.",
    "beef_sirloin": "אפשר לטפל בשכבת שומן חיצונית ולפרוס בניצב לסיבים. אל תשתמש בטמפרטורת מדיום־רר שבמסמך כאישור בטיחות.",
    "beef_short_ribs": "אסאדו מתאים לעיתים לבישול ממושך בנוזל או בחום עקיף. בדוק רכות בנפרד מטמפרטורת הבטיחות.",
    "beef_ground": "עבד בשר טחון בעדינות אם רצוי מרקם פחות דחוס. אחוז השומן הוא בחירת מתכון; הבטיחות שונה מנתח שלם.",
    "beef_shank": "שוק בקר מתאים לבישול ממושך בנוזל. קימוח וקשירה הם אפשרויות, ויש להתחשב באלרגנים ובשיטת ההכנה.",
    "beef_flank": "בדוק את כיוון הסיבים לפני הפריסה. דרגת עשייה קולינרית אינה מגדירה את סף הבטיחות.",
    "beef_brisket": "בריסקט דורש התאמה לעובי, לשומן ולשיטת ההכנה. יעד רכות עשוי להיות גבוה מסף הבטיחות.",
    "lamb_chops": "בחר שיטת הכנה לפי עובי הצלע. דרגת מדיום־רר היא העדפת מרקם ולא אישור בטיחות.",
    "lamb_shoulder": "כתף טלה יכולה להתאים להכנה ארוכה ומכוסה. רכות ומידת התפרקות הן בדיקות מרקם נפרדות.",
    "fish_salmon_fillet": "בדוק עצמות וייבש בעדינות אם המטרה צריבה. עור פריך או מרכז מבריק אינם תחליף לבדיקת מוכנות.",
    "fish_tuna_loin": "יש להבחין בין טונה מבושלת לטונה המיועדת להגשה נאה. צריבה חיצונית קצרה אינה מאשרת בטיחות של מרכז נא.",
    "fish_sea_bass_whole": "בדוק שהדג נוקה והוסרו קשקשים ועצמות מסוכנות לפי הצורך. התאם את ההכנה לגודל הדג.",
    "fish_sea_bream_fillet": "בדוק עצמות ועובי הפילה. מגע עור רציף במחבת יכול לסייע להשחמה; אין זמן קבוע לכל פילה.",
    "fish_cod_fillet": "בשר בקלה עדין; הפוך בעדינות כדי לשמור על שלמותו. בדוק מוכנות בנפרד מצורת הפתיתים.",
    "fish_sardines_fresh": "הכן דג נקי ומזוהה, והתאם את ההכנה לגודלו. חמיצות היא תיבול ואינה חיטוי.",
    "seafood_shrimp": "נקה לפי הצורך ובדוק בישול מתאים. צורת C או O היא תצפית מרקם, לא הוכחת בטיחות.",
    "seafood_calamari": "זמן ההכנה תלוי בחיתוך ובשיטה. כלל שתי הדקות או ארבעים הדקות אינו חוק בטיחות או תחליף למתכון מתאים.",
    "seafood_scallops": "אפשר לייבש בעדינות לפני צריבה. אין להסתמך על שניות לכל צד או על טמפרטורת מרקם נמוכה כאישור בטיחות.",
    "veg_onion_yellow": "לריכוך בלי השחמה אפשר לבחור חום מתון. גודל חיתוך דומה מסייע להכנה אחידה.",
    "veg_onion_red": "אפשר להשתמש נא, כבוש או מבושל לפי המנה. מידת ההשחמה והחמיצות הן בחירות טעם.",
    "veg_garlic_cloves": "מידת הקיצוץ משנה את אופי השום. עקוב אחר הצבע והריח בזמן טיגון והפחת חום אם הוא נחרך.",
    "veg_shallot": "בחר קיצוץ וגודל בהתאם לרוטב או לתבשיל. בדוק צבע ורכות במקום לקבוע שהוא תמיד מתקרמל מהר יותר מבצל.",
    "veg_leek": "פתח ושטוף בין השכבות כדי להסיר חול. בחר אילו חלקים להשתמש לפי מידת הסיביות והמנה.",
    "veg_eggplant": "בחר בין צלייה, צריבה ובישול לפי התוצאה הרצויה. המלחה מוקדמת היא אפשרות ולא דרישה לכל חציל.",
    "veg_tomato_round": "קילוף לאחר חליטה מתאים לרטבים שבהם רצוי מרקם חלק. אין צורך לקלף בכל מנה.",
    "veg_tomato_cherry": "אפשר לצלות שלמות או לחצות. עקוב אחר ריכוך ושחרור נוזלים לפי המנה.",
    "veg_bell_pepper_red": "אפשר להסיר גרעינים ומחיצות. חריכה וקילוף הם אפשרות לטעם ולמרקם, לא פעולה מחייבת.",
    "veg_chili_fresh": "טפל בפלפל חריף בזהירות והימנע ממגע בעיניים. הוסף בהדרגה ובדוק את החריפות הרצויה.",
    "veg_broccoli": "חלק לתפרחות בגודל דומה והתאם את הכנת הגבעול לעוביו. אל תניח שגבעול ותפרחת מתרככים באותו זמן.",
    "veg_cauliflower": "בחר תפרחות או פרוסות בגודל דומה. בדוק רכות במרכז והשחמה מבחוץ בנפרד.",
    "veg_cabbage_white": "הסר ליבה קשה לפי הצורך. חיתוך דק מתאים לסלט, וחיתוך עבה יותר יכול להתאים לצלייה.",
    "veg_cabbage_red": "אפשר להוסיף מעט חמיצות לפי המנה ולבדוק צבע וטעם. אין זמן בישול קבוע ביחס לכרוב לבן.",
    "veg_brussels_sprouts": "אפשר לחצות לקבלת שטח השחמה. בדוק רכות של הגדולים יותר ולא רק את צבע העלים.",
    "veg_potato_russet": "בחר זן לפי המרקם הדרוש; צבע הקליפה אינו קובע את תכולת העמילן. השיטה לפירה שונה מזו לצלייה או לטיגון.",
    "veg_sweet_potato": "בחר גודל חיתוך ושיטה לפי התוצאה הרצויה. בדוק רכות וטעם במקום להחיל זמן או טווח אנזימטי אחיד.",
    "veg_carrot": "חתוך לחלקים בגודל דומה. זיגוג הוא אפשרות, ואין צורך להוסיף סוכר בכל מנה.",
    "veg_beetroot": "אפשר לצלות בקליפה או להכין לאחר קילוף. המתן לטיפול בטוח בחום לפני הקילוף.",
    "veg_celeriac": "קלף את החלק החיצוני הקשה. ניתן לשלב במחית או בצלי; חמאה ושמנת אינן חובה.",
    "veg_parsnip": "בדוק אם קיימת ליבה סיבית בשורש גדול. חיתוך דומה עוזר לקבלת מרקם אחיד.",
    "veg_fennel": "לסלט אפשר לפרוס דק; לבישול אפשר להשאיר פלחים. השתמש במגן יד אם בוחרים במנדולינה.",
    "veg_zucchini": "קישוא משחרר נוזלים. התאם צפיפות במחבת וחום למטרה של ריכוך או השחמה.",
    "veg_butternut_squash": "קלף והסר גרעינים לפי הצורך. בחר גודל חיתוך לפי צלייה או מרק.",
    "veg_spinach": "שטוף היטב להסרת חול, ובדוק ריכוך ושחרור נוזלים. אין אחוז איבוד נפח אחיד לכל זן.",
    "veg_kale": "הסר שדרה קשה לפי הצורך. להכנה נאה או מבושלת מתאימים טיפולים שונים; גם קייל יכול להתרכך יתר על המידה.",
    "veg_asparagus_green": "חתוך או קלף חלק בסיס סיבי לפי הצורך. בדוק מרקם רצוי לפי עובי הגבעולים.",
    "veg_green_beans": "קטום קצוות לפי הצורך. חליטה, אידוי או הקפצה הן אפשרויות בהתאם למרקם הרצוי.",
    "veg_mushrooms_cremini": "ההנחיה מתייחסת לפטריות מאכל מזוהות בלבד. הימנע מעומס במחבת אם המטרה השחמה; אין להשתמש בה לזיהוי פטריות בר.",
    "legume_chickpeas": "ברר אם החומוס יבש, משומר או כבר מבושל. השריה ובישול של יבש שונים מחימום של מוצר מוכן.",
    "legume_lentils_brown": "ברור ושטוף. בדוק הוראות אריזה ומרקם; לעדשים שלמות ולעדשים מפוצלות התנהגות שונה.",
    "legume_lentils_red": "עדשים כתומות עשויות להתפרק ולהסמיך מרק. התאם נוזלים לפי מצב הסיר והוראות האריזה.",
    "legume_white_beans": "ברר אם השעועית יבשה או מוכנה. השריה לבדה אינה בישול; פעל לפי הוראות בישול בטוחות של היצרן, לא חימום איטי בלבד.",
    "grain_rice_basmati": "בדוק הוראות יצרן לסוג האורז. שטיפה ומנוחה הן אפשרויות בהתאם למנה ולאריזה, לא יחס מים אחיד לכל אורז.",
    "grain_rice_arborio": "בריזוטו רוצים לשמר עמילן למרקם קרמי; אין להחיל אוטומטית את שטיפת הבסמטי. הוסף נוזל בהדרגה ובדוק מרקם.",
    "grain_quinoa": "בדוק אם הקינואה שטופה מראש ומה הוראות האריזה. אין יחס נוזלים יחיד שמתאים לכל מוצר ושיטה.",
    "grain_pasta_durum": "בדוק את הוראות האריזה ושמור מעט ממי הבישול אם מתאים לרוטב. המלחה ודרגת מרקם נתונות לבחירתך.",
    "dairy_butter": "עקוב אחר מוצקי החלב כדי למנוע חריכה. שילוב חמאה ברוטב הוא אפשרות בהתאם לאלרגיות ולהפרדת בשר וחלב.",
    "dairy_heavy_cream": "שמור בקירור לפי האריזה. גם שמנת עשירה עלולה להיפרד בתנאים מסוימים; חום ושומן אינם מבטיחים יציבות.",
    "dairy_parmigiano": "גירור דק והוספה מבוקרת יכולים לסייע להשתלבות ברוטב. בדוק התאמה לאלרגיות ולפרופיל התזונה.",
    "dairy_mozzarella_fresh": "אם יש עודף נוזל, אפשר לסנן בקירור לפי צורכי המנה. בחר את שלב ההוספה בהתאם לאפייה ולמרקם הרצוי.",
    "dairy_halloumi": "ייבש בעדינות לפני צריבה אם זה מתאים למנה. בדוק מליחות והתאמה למרכיבים האחרים.",
    "herb_rosemary": "רוזמרין בעל טעם חזק; הוסף בהדרגה. הסר גבעולים מעוצים כשאינם מיועדים לאכילה.",
    "herb_thyme": "אפשר לשלב טימין בבישול ממושך או בתיבול, לפי המנה. הסר גבעולים קשים לפני ההגשה.",
    "herb_parsley": "שטוף וייבש. עלים יכולים להתאים לתוספת בסוף; גבעולים נקיים יכולים להתאים לבישול בהתאם למנה.",
    "herb_basil": "שטוף וייבש בעדינות והוסף לפי המנה. אין להחיל כלל אחסון גורף שאוסר קירור על כל מוצר בזיליקום.",
}

EXTRA_ALIASES = {
    "chicken_breast": ["חזה עוף"],
    "chicken_thighs_boneless": ["פרגיות", "פרגית"],
    "chicken_thighs_bone_in": ["כרעיים", "שוקי עוף", "שוקיים עוף"],
    "chicken_whole": ["עוף שלם"],
    "chicken_giblets": [
        "קורקבנים",
        "קורקבן",
        "קוקבנים",
        "קוקבן",
        "gizzard",
        "gizzards",
        "כבד עוף",
        "כבדי עוף",
    ],
    "turkey_thigh": ["ירך הודו", "שווארמה הודו"],
    "duck_breast": ["חזה ברווז", "חזה אווז", "מגרט"],
    "duck_leg": ["שוק ברווז", "שוק אווז"],
    "beef_ribeye": ["אנטרקוט", "אנטריקוט", "ribeye"],
    "beef_tenderloin": ["פילה בקר"],
    "beef_short_ribs": ["אסאדו", "שפונדרה"],
    "beef_flank": ["פלנק"],
    "beef_brisket": ["בריסקט"],
    "beef_ground": ["בקר טחון", "בשר טחון", "המבורגר"],
    "beef_shank": ["אוסובוקו"],
    "fish_salmon_fillet": ["סלמון", "salmon"],
    "fish_tuna_loin": ["טונה", "tuna"],
    "fish_sea_bass_whole": ["לברק"],
    "fish_sea_bream_fillet": ["דניס"],
    "fish_cod_fillet": ["בקלה", "קוד", "cod"],
    "seafood_shrimp": ["שרימפס", "shrimp"],
    "seafood_calamari": ["קלמארי", "דיונון"],
    "seafood_scallops": ["סקאלופס"],
    "veg_onion_yellow": ["בצל", "onion"],
    "veg_onion_red": ["בצל סגול"],
    "veg_garlic_cloves": ["שום", "garlic"],
    "veg_leek": ["כרישה", "לוף"],
    "veg_tomato_round": ["עגבנייה", "עגבניה"],
    "veg_tomato_cherry": ["עגבניות שרי", "עגבנית שרי"],
    "veg_bell_pepper_red": ["גמבה"],
    "veg_chili_fresh": ["פלפל חריף"],
    "veg_brussels_sprouts": ["כרוב ניצנים"],
    "veg_potato_russet": ["תפוח אדמה", "תפוחי אדמה"],
    "veg_parsnip": ["פסטרנק"],
    "veg_zucchini": ["קישוא", "זוקיני"],
    "veg_spinach": ["תרד"],
    "veg_asparagus_green": ["אספרגוס"],
    "veg_green_beans": ["שעועית ירוקה"],
    "veg_mushrooms_cremini": ["פטריות", "שמפיניון", "פורטובלו"],
    "legume_chickpeas": ["חומוס", "גרגרי חומוס"],
    "legume_lentils_brown": ["עדשים ירוקות", "עדשים חומות"],
    "grain_rice_arborio": ["ריזוטו", "ארבוריו", "קרנרולי"],
    "grain_pasta_durum": ["פסטה", "pasta"],
    "dairy_butter": ["חמאה", "butter"],
    "dairy_heavy_cream": ["שמנת", "cream"],
    "dairy_parmigiano": ["פרמזן", "פרמז'ן"],
    "dairy_mozzarella_fresh": ["מוצרלה"],
    "dairy_halloumi": ["חלומי"],
    "herb_rosemary": ["רוזמרין"],
    "herb_thyme": ["טימין", "קורנית"],
    "herb_parsley": ["פטרוזיליה"],
    "herb_basil": ["בזיליקום"],
}

METHODS = {
    "pan_sear": (
        "צריבה במחבת",
        ["צריבה במחבת", "צריבה", "pan sear"],
        "צריבה מתאימה כשרוצים השחמה. התאם חום לכלי ולמזון; אין צורך להביא שמן לעשן.",
        ["הכנה וייבוש לפני צריבה", "צריבה ובדיקת השחמה"],
    ),
    "oven_roast": (
        "צלייה בתנור",
        ["תנור", "צלייה בתנור", "oven roast"],
        "בחר חום ומיקום תבנית לפי מתכון מתאים ובדוק מוכנות בפועל. חימום מוקדם תלוי במתכון ובתנור.",
        ["הכנת התבנית והתנור", "צלייה ובדיקת מצב"],
    ),
    "grill_direct": (
        "גריל ישיר",
        ["גריל", "מנגל", "grill direct"],
        "תכנן אזורי חום בהתאם לגריל. עקוב אחר להבות שומן; סימני רשת אינם בדיקת מוכנות.",
        ["הכנת אזורי חום", "צלייה ובדיקת מצב"],
    ),
    "deep_fry": (
        "טיגון עמוק",
        ["טיגון עמוק", "deep fry"],
        "השתמש בכלי מתאים ובמדידת שמן לפי המתכון. ייבש מזון לפני הכנסתו לשמן; טמפרטורת השמן אינה טמפרטורת הליבה.",
        ["הכנת כלי ושמן לפי המתכון", "טיגון בנגלות ובדיקת מוכנות"],
    ),
    "stir_fry": (
        "הקפצה בווק",
        ["ווק", "הקפצה", "מוקפץ", "מוקפצת", "stir fry"],
        "הכן חיתוך מתאים מראש ועבוד בנגלות לפי הצורך. אין לחייב עשן כבד או רוטב על דפנות לוהטות.",
        ["הכנת חיתוך ומרכיבים", "הקפצה לפי סדר שבחרת"],
    ),
    "sous_vide": (
        "סו־וויד",
        ["סו וויד", "סו-וויד", "sous vide"],
        "נדרשת תוכנית זמן–טמפרטורה מאומתת שמתחשבת בעובי, במזון ובקירור. טמפרטורת אמבט לבדה אינה אישור פסטור.",
        ["בחירת תוכנית סו־וויד מאומתת", "בדיקת ציוד ותוכנית טיפול לאחר הבישול"],
    ),
    "steam": (
        "אידוי",
        ["אידוי", "מאודה", "steaming"],
        "בדוק מפלס מים, כלי מתאים וזרימת אדים. פתח מכסה בזהירות והרחיק פנים וידיים מנתיב האדים.",
        ["הכנת כלי האידוי", "אידוי ובדיקת מצב"],
    ),
    "braise": (
        "בישול ארוך בנוזל",
        ["בישול ארוך", "קדירה", "קדרה", "ברייז", "braise"],
        "בחר רמת נוזל וחום לפי נתח ומתכון מתאים. בדוק רכות בנפרד מבטיחות; השחמה מקדימה היא בחירה קולינרית.",
        ["השחמה מקדימה אם בחרת", "בישול מבוקר בנוזל", "בדיקת רכות ומדידה בנפרד"],
    ),
    "boil_simmer": (
        "בישול בנוזל",
        ["בישול בנוזל", "הרתחה", "בעבוע", "boil simmer"],
        "התאם רתיחה או בעבוע למרכיב. מלח, מכסה ויחס נוזלים אינם כלל אחיד לכל מזון.",
        ["בחירת נוזל ושיטת חימום", "בישול ובדיקת מרקם"],
    ),
    "raw_cure": (
        "נא וכבישה קרה",
        ["ללא חימום", "כבישה", "נא", "טרטר", "סביצ׳ה", "סביצ'ה", "raw cure"],
        "כבישה בחומצה או המלחה אינן אישור חיטוי. נדרשים זיהוי חומר גלם, מקור ותהליך מתאימים; העץ אינו מאשר הגשת חלבון נא.",
        ["בירור חומר גלם ותהליך מאומת לפני הכנה נאה"],
    ),
}

NUDGES = {
    "surface_wet": (
        "שטח הפנים רטוב",
        "אם המזון עדיין מחוץ למחבת, אפשר לייבש בעדינות לפני הצריבה. אל תכניס נייר סופג למחבת חמה או לשמן חם.",
        "info",
    ),
    "pan_crowded": (
        "המחבת עמוסה",
        "אם המטרה השחמה, אפשר לחלק לנגלות כדי להפחית הצטברות נוזלים. זו הצעה לשיטה שבחרת.",
        "info",
    ),
    "oil_smoking_heavily": (
        "השמן מעשן בכבדות",
        "הפסק חימום אם אפשר בבטחה. אל תוסיף מים ואל תנסה להזיז כלי מסוכן; אם יש אש, טפל בסיכון לפני המשך.",
        "safety",
    ),
    "oven_cold": (
        "התנור טרם הגיע לחום שבחרתי",
        "בדוק מה דורש המתכון. חימום מוקדם יכול להשפיע על תזמון והכנה, אך אין לקבוע אוטומטית שהמזון ייהרס.",
        "info",
    ),
    "skin_rubbery": (
        "העור עדיין אינו פריך",
        "בדוק רטיבות, צפיפות וסוג הכיסוי. התאמת השחמה היא בחירה; אין העלאה אוטומטית לחום ולזמן קבועים.",
        "info",
    ),
    "flare_up": (
        "נוצרו להבות שומן בגריל",
        "עצור וטפל בסיכון לפי הוראות הגריל. אל תוסיף מים לשומן בוער ואל תנסה להעביר מזון דרך להבות מסוכנות.",
        "safety",
    ),
    "meat_sticking": (
        "המזון נדבק לרשת",
        "אל תמשוך בכוח. בדוק בעדינות, התאם חום והשתמש בכלי מתאים; שחרור טבעי אינו מובטח בכל כלי ומזון.",
        "info",
    ),
    "temp_below_160": (
        "מדדתי שמן מתחת לטווח שבמתכון",
        "השווה לטווח של שלב הטיגון במתכון. שלב מקדים עשוי להיות בטמפרטורה נמוכה יותר; אין סף אחיד של 160°C לכל טיגון.",
        "info",
    ),
    "draining_on_paper": (
        "אני מנקז אחרי הטיגון",
        "אפשר להשתמש ברשת מתאימה כדי להפחית הצטברות אדים, בזהירות משמן חם.",
        "info",
    ),
    "ingredients_uneven": (
        "החיתוך אינו אחיד",
        "אפשר להפריד גדלים ולשנות את סדר ההוספה. אל תנסה לחתוך מזון בתוך כלי חם.",
        "info",
    ),
    "sauce_burning": (
        "הרוטב נחרך בווק",
        "הפחת חום אם בטוח לעשות זאת ובדוק חריכה. אל תוסיף רוטב לדפנות לוהטות כפתרון אוטומטי.",
        "info",
    ),
    "bag_floating": (
        "שקית הסו־וויד צפה",
        "בדוק איטום ושקיעה בטוחה לפי הוראות הציוד. אם תנאי התוכנית לא התקיימו, אין לאשר פסטור או מוכנות.",
        "review",
    ),
    "no_sear_finish": (
        "המזון יצא חיוור מהשקית",
        "צריבה יכולה להוסיף צבע וטעם אם בחרת בכך; היא אינה חובה ואינה מתקנת תוכנית פסטור לא מאומתת.",
        "review",
    ),
    "water_dry": (
        "הסיר מתחת לאידוי יבש",
        "הפסק חימום אם בטוח לעשות זאת. אל תשפוך מים לכלי יבש ולוהט באופן שעלול ליצור התזה או אדים; פעל לפי הוראות הכלי.",
        "safety",
    ),
    "oversteaming_veg": (
        "הירק מתרכך יותר משרציתי",
        "בדוק מרקם רצוי והפסק את ההכנה אם הושג. צבע הוא מידע על המנה, לא הוכחה לבטיחות.",
        "info",
    ),
    "boiling_vigorously": (
        "הנוזל רותח בחוזקה",
        "אם בחרת בבישול עדין, אפשר להפחית לבעבוע שמתאים למתכון.",
        "info",
    ),
    "liquid_evaporated": (
        "נוזל הבישול התאדה",
        "בדוק חום וכיסוי. אם בטוח ומתאים לכלי ולמנה, אפשר להשלים מעט נוזל מתאים בהדרגה.",
        "info",
    ),
    "water_unsalted": (
        "מי הבישול לא הומלחו",
        "המלחה היא בחירת טעם ותזונה. אפשר להתאים תיבול גם בהמשך; אין חובה להוסיף מלח.",
        "info",
    ),
    "scum_forming": (
        "יש קצף על הנוזל",
        "אם המטרה ציר צלול, אפשר לקפות בעדינות. קצף לבדו אינו קובע קלקול או בטיחות.",
        "info",
    ),
    "acid_too_long": (
        "חומר הגלם נמצא בחומצה",
        "בדוק את התהליך והמרקם, ואל תסיק שהחומצה הפכה חלבון נא לבטוח. אין המלצת הגשה אוטומטית אחרי זמן קבוע.",
        "review",
    ),
    "knife_dull": (
        "הסכין אינה חותכת היטב",
        "עצור ובחר כלי חד ומתאים או טפל בו לפי הוראות היצרן, הרחק ממקור חום ומסביבה לא יציבה.",
        "info",
    ),
}

PREPARATIONS = {
    "brining_wet": "השריה במלח היא אפשרות לפי מתכון, הרכב ותזונה. שמור חומר גלם מתכלה בקירור ואל תשתמש ביחס גורף לכל מוצר.",
    "brining_dry": "המלחה יבשה היא אפשרות ולא חובה; בחר כמות וזמן לפי המתכון ושמור בקירור לפי הנדרש.",
    "blanching": "חליטה יכולה להתאים לריכוך חלקי או להכנה מקדימה. קירור לאחריה תלוי בשימוש המתוכנן, ולא כל חומר גלם דורש אותה.",
    "deglazing": "אפשר לשחרר משקעים לא שרופים בנוזל מתאים, בזהירות מהתזה. יין אינו חובה ומשקע שרוף אינו בסיס רצוי לרוטב.",
    "sweating": "ריכוך בחום מתון בלי השחמה מתאים למנות מסוימות; בחר בו רק אם זו התוצאה הרצויה.",
}


class GraphIngredient(StrictModel):
    id: str
    name: str
    category: str
    tip: str
    aliases: list[str]
    minimum_temperature: float | None = None
    rest_seconds: int = 0
    food_class: str = "unknown"
    allergens: list[str] = Field(default_factory=list)
    clarification: str = ""
    source_id: str
    archetype_ref: str = ""
    inherited_advice: str = ""
    inherited_warning: str = ""
    domain_source_id: str = ""


class GraphObservation(StrictModel):
    id: str
    label: str
    message: str
    severity: str
    source_id: str


class GraphMethod(StrictModel):
    id: str
    name: str
    advice: str
    suggestions: list[str]
    observations: list[GraphObservation]
    requires_validated_process: bool = False


class GraphPath(StrictModel):
    id: str
    title: str
    ingredient_ref: str
    method_ref: str
    suggestions: list[str]
    selectable: bool
    reason: str = ""
    source_id: str
    aliases: list[str] = Field(default_factory=list)
    introduced_allergens: list[str] = Field(default_factory=list)
    meat_dairy: bool = False
    archetype_ref: str = ""
    detailed_steps: list[dict] = Field(default_factory=list, max_length=8)
    domain_source_id: str = ""


class GraphContext(StrictModel):
    source_sha256: str
    domain_sha256: str = ""
    ingredients: list[GraphIngredient] = Field(default_factory=list, max_length=16)
    method: GraphMethod | None = None
    preparations: list[dict[str, str]] = Field(default_factory=list, max_length=5)
    paths: list[GraphPath] = Field(default_factory=list, max_length=20)
    minimum_temperature: float | None = None
    rest_seconds: int = 0


def tokens(value):
    return re.findall(r"[^\W_]+", value.lower())


def phrase_spans(text, aliases):
    words = tokens(text)
    spans = []
    for alias in aliases:
        part = tokens(alias)
        if not part:
            continue
        for index in range(len(words) - len(part) + 1):
            fragment = words[index : index + len(part)]
            first_matches = fragment[0] == part[0] or (
                len(part[0]) >= 3 and re.fullmatch(r"[בלמהו]" + re.escape(part[0]), fragment[0]) is not None
            )
            if (
                first_matches
                and fragment[1:] == part[1:]
                and not set(words[max(0, index - 2) : index]) & {"ללא", "בלי", "לא", "without", "no"}
            ):
                spans.append((index, index + len(part), len(" ".join(part))))
    return spans


def minimum_for(key):
    if key.startswith(("chicken_", "turkey_", "duck_")):
        return 74.0, 0
    if key == "beef_ground":
        return 71.0, 0
    if key.startswith(("beef_", "lamb_")):
        return 63.0, 180
    if key.startswith(("fish_", "seafood_")):
        return 63.0, 0
    return None, 0


def ingredient_metadata(key):
    if key.startswith(("chicken_", "turkey_", "duck_", "beef_", "lamb_")):
        return "meat", []
    if key.startswith("dairy_"):
        return "dairy", ["milk"]
    if key.startswith("fish_"):
        return "pareve", ["fish"]
    if key.startswith("seafood_"):
        return "unknown", ["shellfish"]
    if key == "grain_pasta_durum":
        return "pareve", ["wheat"]
    if key == "veg_celeriac":
        return "pareve", ["celery"]
    return "pareve", []


@lru_cache(maxsize=1)
def graph():
    raw_bytes = SOURCE.read_bytes()
    data = yaml.safe_load(raw_bytes.decode("utf-8-sig"))
    if set(data) != {"base_ingredients", "cooking_methods", "preparations", "recipe_paths"}:
        raise ValueError("Unexpected culinary graph sections")
    if set(data["base_ingredients"]) != set(PREP) or set(data["cooking_methods"]) != set(METHODS):
        raise ValueError("Every graph node requires an explicit editorial adaptation")
    nodes = {}
    for key, entry in data["base_ingredients"].items():
        aliases = [entry["name"], key.replace("_", " "), *EXTRA_ALIASES.get(key, [])]
        aliases += [part.strip() for part in re.split(r"[/()]", entry["name"]) if len(part.strip()) >= 3]
        minimum, rest = minimum_for(key)
        food_class, allergens = ingredient_metadata(key)
        clarification = (
            "יש לאמת אם מדובר בברווז או באווז; המזהה והשם במסמך אינם תואמים."
            if key.startswith("duck_")
            else "האם מדובר בקורקבן או בכבד? שיטת ההכנה שונה."
            if key == "chicken_giblets"
            else ""
        )
        nodes[key] = GraphIngredient(
            id=key,
            name=entry["name"],
            category=entry["category"],
            tip=PREP[key],
            aliases=list(dict.fromkeys(aliases)),
            minimum_temperature=minimum,
            rest_seconds=rest,
            food_class=food_class,
            allergens=allergens,
            clarification=clarification,
            source_id=f"base_ingredients/{key}",
        ).model_dump()
    methods = {}
    for key, entry in data["cooking_methods"].items():
        name, aliases, advice, suggestions = METHODS[key]
        observations = []
        for rule in entry["nudge_rules"]:
            condition = rule["condition"]
            label, message, severity = NUDGES[condition]
            observations.append(
                GraphObservation(
                    id=condition,
                    label=label,
                    message=message,
                    severity=severity,
                    source_id=f"cooking_methods/{key}/nudge_rules/{condition}",
                ).model_dump()
            )
        methods[key] = GraphMethod(
            id=key,
            name=name,
            advice=advice,
            suggestions=suggestions,
            observations=observations,
            requires_validated_process=key in ("raw_cure", "sous_vide"),
        ).model_dump()
    paths = []
    for index, entry in enumerate(data["recipe_paths"]):
        ingredient, method = entry["ingredient_ref"], entry["method_ref"]
        if ingredient not in nodes or method not in methods:
            raise ValueError("Dangling recipe path")
        if ingredient == "grain_rice_arborio":
            method = "boil_simmer"
        text = " ".join([entry["title"], *[item["action"] for item in entry["specific_steps"]]])
        allergens = []
        for allergen, phrases in [
            ("milk", ["חמאה", "גבינה", "פרמז"]),
            ("soy", ["סויה"]),
            ("sesame", ["טחינה", "שומשום"]),
            ("wheat", ["קמח", "פסטה", "לחמנייה"]),
        ]:
            if any(phrase in text for phrase in phrases):
                allergens.append(allergen)
        allergens = list(dict.fromkeys(nodes[ingredient]["allergens"] + allergens))
        restricted = method in ("raw_cure", "sous_vide") or bool(nodes[ingredient]["clarification"])
        reason = "נדרש בירור חומר גלם ותהליך מאומת לפני הפעלת מתווה זה." if restricted else ""
        paths.append(
            GraphPath(
                id=f"path_{index:02d}",
                title=entry["title"],
                ingredient_ref=ingredient,
                method_ref=method,
                suggestions=[
                    f"הכנת {nodes[ingredient]['name']}",
                    *methods[method]["suggestions"],
                    "בדיקת תוצאה לפי השיטה וחומר הגלם",
                ],
                selectable=not restricted,
                reason=reason,
                source_id=f"recipe_paths/{index}",
                introduced_allergens=allergens,
                meat_dairy=nodes[ingredient]["food_class"] == "meat" and "milk" in allergens,
            ).model_dump()
        )
    from app.culinary_domain import ARCHETYPES, ID_MAP, domain_graph

    domain = domain_graph()
    for raw_key, entry in domain["raw"]["base_ingredients"].items():
        key = ID_MAP.get(raw_key, raw_key)
        if key not in nodes:
            raise ValueError("Unmapped domain ingredient")
        parent = domain["inheritance"][key]
        _, advice, warning = ARCHETYPES[parent]
        nodes[key].update(
            archetype_ref=parent,
            inherited_advice=advice,
            inherited_warning=warning,
            domain_source_id=f"domain/base_ingredients/{raw_key}",
        )
        nodes[key]["aliases"] = list(dict.fromkeys(nodes[key]["aliases"] + [entry["name"]]))
    for extension in domain["paths"]:
        path = next(
            (
                item
                for item in paths
                if item["ingredient_ref"] == extension["ingredient_ref"]
                and item["method_ref"] == extension["method_ref"]
            ),
            None,
        )
        if path is None:
            raise ValueError("Domain path must extend an existing path")
        parent = extension["archetype_ref"]
        _, advice, warning = ARCHETYPES[parent]
        path.update(archetype_ref=parent, domain_source_id=extension["source_id"])
        path["aliases"].append(extension["title"])
        path["detailed_steps"] = [
            {
                "title": f"פעולה {index + 1}",
                "instruction": action,
                "why": advice,
                "successCriteria": [extension["checkpoints"][index]],
                "commonMistakes": [warning],
                "recoveryActions": ["אם התוצאה שונה, דווח מה השתנה לפני בחירת תיקון."],
                "chefQuestions": ["מה המצב בפועל? " + extension["checkpoints"][index]],
                "next_step_prep": extension["steps"][index + 1]
                if index + 1 < len(extension["steps"])
                else "בדוק תוצאה, מדידה ותיבול לפי הצורך לפני סיום.",
                "source_id": f"{extension['source_id']}/steps/{index}",
                "origin": "USER_GRAPH_ADAPTED",
            }
            for index, action in enumerate(extension["steps"])
        ]
    return {
        "domain_sha256": domain["sha256"],
        "sha256": hashlib.sha256(raw_bytes).hexdigest(),
        "raw": data,
        "ingredients": nodes,
        "methods": methods,
        "paths": paths,
    }


def match_ingredients(*texts):
    data = graph()
    found = {}
    for text in texts:
        candidates = []
        for key, node in data["ingredients"].items():
            candidates.extend((span, key) for span in phrase_spans(text, node["aliases"]))
        occupied = set()
        for (start, end, length), key in sorted(candidates, key=lambda item: (-item[0][2], item[0][0])):
            positions = set(range(start, end))
            if not positions & occupied:
                found.setdefault(key, data["ingredients"][key])
                occupied |= positions
    return list(found.values())[:16]


def match_method(method, title=""):
    text = method or title
    found = []
    for key, (_, aliases, _, _) in METHODS.items():
        for span in phrase_spans(text, [key.replace("_", " "), *aliases]):
            found.append((span[2], key))
    return graph()["methods"][max(found)[1]] if found else None


def graph_context(title, method="", ingredients=()):
    data = graph()
    nodes = match_ingredients(title, *ingredients)
    selected = match_method(method, title)
    if not nodes:
        # Recipe titles can identify the ingredient even when the name is e.g. "רוסטביף".
        for path in data["paths"]:
            if phrase_spans(title, [path["title"], *path["aliases"]]):
                nodes = [data["ingredients"][path["ingredient_ref"]]]
                selected = selected or data["methods"][path["method_ref"]]
                break
    keys = {node["id"] for node in nodes}
    paths = [
        deep
        for deep in data["paths"]
        if deep["ingredient_ref"] in keys and (not selected or deep["method_ref"] == selected["id"])
    ]
    categories = {node["category"] for node in nodes}
    preparations = []
    for key, entry in data["raw"]["preparations"].items():
        if categories & set(entry["applicable_categories"]):
            preparations.append(
                {
                    "id": key,
                    "name": entry["name"],
                    "advice": PREPARATIONS[key],
                    "source_id": f"preparations/{key}",
                }
            )
    values = [node["minimum_temperature"] for node in nodes if node["minimum_temperature"] is not None]
    return GraphContext(
        domain_sha256=data["domain_sha256"],
        source_sha256=data["sha256"],
        ingredients=nodes,
        method=selected,
        preparations=preparations,
        paths=paths,
        minimum_temperature=max(values) if values else None,
        rest_seconds=max((node["rest_seconds"] for node in nodes), default=0),
    ).model_dump()


def observation_reply(context, condition):
    method = context.get("method")
    if method:
        return next((rule for rule in method["observations"] if rule["id"] == condition), None)
    return None


def dietary_paths(context, allergies=(), forbid_meat_dairy=True):
    result = deepcopy(context)
    aliases = {
        "milk": {"milk", "dairy", "חלב"},
        "fish": {"fish", "דג", "דגים"},
        "shellfish": {"shellfish", "שרימפס", "פירות ים"},
        "wheat": {"wheat", "gluten", "חיטה", "גלוטן"},
        "sesame": {"sesame", "שומשום", "טחינה"},
        "soy": {"soy", "סויה"},
    }
    avoided = {value.strip().lower() for value in allergies}
    for path in result["paths"]:
        if forbid_meat_dairy and path["meat_dairy"]:
            path["selectable"] = False
            path["reason"] = "המתווה המקורי כולל בשר וחלב ואינו מתאים להפרדה שבחרת."
        if any(avoided & aliases.get(allergen, {allergen}) for allergen in path["introduced_allergens"]):
            path["selectable"] = False
            path["reason"] = "המתווה המקורי מציג מרכיב שאינו מתאים לרשימת ההימנעות שלך."
    return result


def audit_graph():
    data = graph()
    changes = []
    for key, entry in data["raw"]["base_ingredients"].items():
        if "safety_temp" in entry:
            changes.append(
                {
                    "source_id": f"base_ingredients/{key}/safety_temp",
                    "original": entry["safety_temp"],
                    "safety_minimum": data["ingredients"][key]["minimum_temperature"],
                    "rest_seconds": data["ingredients"][key]["rest_seconds"],
                    "classification": "ORIGINAL_NOT_USED_FOR_SAFETY",
                    "policy_source": SEAFOOD if key.startswith("seafood_") else SAFETY,
                }
            )
    from app.culinary_domain import ID_MAP, domain_graph

    domain = domain_graph()
    return {
        "domain_doneness_changes": [
            {
                "source_id": f"domain/base_ingredients/{key}/target_doneness",
                "original": entry["target_doneness"],
                "safety_minimum": data["ingredients"][ID_MAP.get(key, key)]["minimum_temperature"],
                "rest_seconds": data["ingredients"][ID_MAP.get(key, key)]["rest_seconds"],
                "classification": "ORIGINAL_NOT_USED_FOR_SAFETY",
                "policy_source": SAFETY,
            }
            for key, entry in domain["raw"]["base_ingredients"].items()
            if "target_doneness" in entry
        ],
        "domain_source_sha256": domain["sha256"],
        "domain_archetypes": len(domain["raw"]["archetypes"]),
        "domain_ingredients": len(domain["raw"]["base_ingredients"]),
        "domain_recipe_paths": len(domain["paths"]),
        "domain_adapted_steps": sum(len(item["steps"]) for item in domain["paths"]),
        "source_sha256": data["sha256"],
        "source_file": SOURCE.name,
        "ingredients": len(data["ingredients"]),
        "methods": len(data["methods"]),
        "preparations": len(data["raw"]["preparations"]),
        "recipe_paths": len(data["paths"]),
        "safety_changes": changes,
        "editorial_policy": "All active rules are curated adaptations; original recipe times and low-temperature processes are not activated.",
        "evidence_cutoff_date": "2026-10-19",
    }
