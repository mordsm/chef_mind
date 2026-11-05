"""Add source-checked evidence from the three owner-supplied PDF excerpts."""
import hashlib
import json
from pathlib import Path
import re
import unicodedata

import fitz
import yaml

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
DOWNLOADS = Path('C:/Users/lenovo/Downloads')
SOURCE = 'SRC-MCGEE-2004'

# Printed page, chapter, anchor, stable slug, Hebrew paraphrase, folder,
# canonical concept, and explicit limits. No raw PDF instructions are executed.
ROWS = [
 (265,5,'Water and walls determine texture','Plant-Turgor','מים ודפנות התא קובעים פריכות','הספר מבחין בין תא צמחי מלא מים שנשבר בפריכות לבין רקמה שאיבדה לחץ מים ונעשית רפויה ולעיסה.','05_Textures','Starch-And-Emulsion-Viscosity','השריית ירק רפוי יכולה לשנות מרקם; אינה הוכחה לטריות או בטיחות.'),
 (283,5,'precooking vegetables in plain water','Acid-Vegetable-Softening','חומציות וריכוך ירקות','הספר מציע בישול מקדים במים לפני הוספה לרוטב עגבניות כשחומציות הסביבה מעכבת את הריכוך; גם קשיות המים יכולה להשפיע.','03_Techniques','Low-Slow-Braising','אין זמן אחיד לכל ירק; אין להחיל מכאן מינון סודה אוטומטי.'),
 (280,5,'excessively alkaline conditions','Greens-Alkalinity-Tradeoff','ירקות ירוקים: צבע מול מרקם','הספר מזהיר שסביבה בסיסית מדי עשויה לשמור על ירוק אך לרכך יתר על המידה ולהשאיר טעם סבוני.','04_Flavors','Acid-Fat-Balance','לא מועתקת ההצעה להוסיף מתכות למי בישול; זו אינה הוראת תוסף או מינון.'),
 (277,5,'traps the gas ethylene','Produce-Ethylene','אתילן ואחסון תוצרת','הספר מתאר שאריזה סגורה יכולה ללכוד אתילן ולהאיץ הבשלה או הזדקנות של רקמות צמחיות.','01_Ingredients','Allium-Onion-Sulfur-Sugars','זהו מנגנון כללי; מין הפרי והירק קובע תגובה. אין להסיק חיי מדף מדויקים.'),
 (303,6,'neighboring cells cohere','Waxy-Potato-Structure','תפוח אדמה ששומר צורה','הספר מתאר זנים שעוותיים שתאיהם נשארים מלוכדים לאחר הבישול ומתאימים יותר לחתיכות שלמות בסלטים ובגרטנים.','01_Ingredients','Starch-Cornstarch-Flour','צבע הקליפה אינו לבדו זיהוי אמין של תכונת הזן.'),
 (303,6,'Mashed and Pureed Potatoes','Potato-Mash-Processing','מחית תפוחי אדמה','הספר מתאר הכנת מחית כשילוב פירוק תפוח אדמה מבושל לחלקיקים והוספת מים ושומן לשינוי המרקם והעושר.','05_Textures','Starch-And-Emulsion-Viscosity','אין יחס שומן אחד המתאים לכל זן ולכל מרקם יעד.'),
 (311,6,'Chopping, pound','Allium-Cutting-Aroma','חיתוך ושינוי ארומת בצל ושום','הספר מתאר יצירת חומרי ארומה גופרתיים לאחר פגיעה ברקמת משפחת הבצל; עוצמת הפגיעה, חמצן וזמן משנים את תערובת הארומות.','04_Flavors','Allium-Onion-Sulfur-Sugars','ההשפעה תלויה במין ובשיטת החיתוך; אין כלל שקובע שכל כתישה עדיפה.'),
 (353,7,'ethylene, a simple hydrocarbon gas','Fruit-Ethylene-Ripening','אתילן והפעלת הבשלה','הספר מתאר אתילן כגורם המפעיל מערכות אנזימים הקשורות להבשלת פירות בוגרים שטרם הבשילו.','02_Food-Science','Fat-Soluble-Volatile-Aromas','התוצאה תלויה בפרי ובבגרותו; אין המלצה לחשיפה לגז תעשייתי.'),
 (353,7,'Nonclimacteric','Ripening-Styles','שני דפוסי הבשלה','הספר מבחין בין פירות המגיבים לאתילן בהאצה עצמית של תהליך ההבשלה לבין פירות שאינם מציגים תגובה כזו; לכן אי אפשר להניח שכל פרי משתבח באותה דרך אחרי קטיף.','08_Decision-Making','Cut-To-Method-Matching','מיפוי למושג תכנון קיים הוא אנלוגיה בלבד, לא זהות בין פירות לנתחי בשר.'),
 (398,8,'toward the end of cooking','Herb-Addition-Time','מועד הוספת עשבי תיבול','הספר מציע הוספת חלק מעשבי התיבול או התמצית לקראת סיום כדי לשמר רכיבי ארומה טריים שעלולים להשתנות או להתנדף בחימום ממושך.','03_Techniques','Fat-Soluble-Volatile-Aromas','הוספה מוקדמת יכולה להיות רצויה לפיתוח טעם אחר; אין מועד מיטבי אחיד לכל תבלין.'),
 (399,8,'pestle pounding in a mortar','Herb-Processing-Oxygen','כתישה, חיתוך וחשיפה לחמצן','הספר משווה בין כלי עיבוד עשבי תיבול לפי פגיעה בתאים, יצירת חום והחדרת אוויר, ומסביר מדוע תוצאה ארומטית עשויה להשתנות ביניהם.','06_Equipment','Fat-Soluble-Volatile-Aromas','אין להסיק שמעבד מזון תמיד נחות; היעד, הכמות והמרקם קובעים.'),
 (399,8,'Oils and fats dissolve more aroma','Aroma-Medium','שומן ומים במיצוי ארומה','הספר מסביר ששומן ממיס רכיבי ארומה רבים ומשנה גם את קצב שחרורם באכילה; בחירת המדיום משנה את פרופיל הטעם.','04_Flavors','Fat-Soluble-Volatile-Aromas','אין להניח שכל תרכובת ארומה מסיסה באותה מידה בשומן.'),
 (443,8,'bitterness increases','Coffee-Roast-Balance','קליית קפה ומאזן טעמים','הספר מתאר שינוי בחומציות, עפיצות ומרירות עם התקדמות הקלייה, והיחלשות אפשרית של ארומות זן בקלייה כהה.','04_Flavors','Maillard-Reaction','זו מגמה תיאורית; זן, קלייה וחליטה משנים את התוצאה. לא נגזרת המלצה בריאותית.'),
 (446,8,'more particles, the more bitterness','Coffee-Particles-Extraction','חלקיקי קפה והמשך מיצוי','ההקדמה לטבלת החליטה קושרת שארית חלקיקי קפה במשקה להמשך מיצוי מרירות ועפיצות בכוס או בקנקן.','06_Equipment','Heat-Transfer','הטבלה הרב־עמודתית לא הומרה ליחסי זמן וטמפרטורה אוטומטיים.'),
 (454,9,'seeds that are especially rich in protein','Legume-Seed-Composition','קטניות והרכב הזרע','הספר מתאר קטניות כזרעים עשירים יחסית בחלבון ומקשר זאת לסימביוזה של הצמח עם חיידקים מספקי חנקן.','01_Ingredients','Starch-Cornstarch-Flour','זה אינו אומדן תזונתי למנה מסוימת; אין הסקת תועלת רפואית.'),
 (454,9,'store their energy not in starch but in oil','Nut-Seed-Oil','שמן כחומר תשמורת באגוזים','הספר מתאר אגוזים רבים כזרעים שעיקר תשמורת האנרגיה שלהם בשמן ולא בעמילן, בניגוד למספר קבוצות זרעים אחרות.','01_Ingredients','Dairy-Butter-Emulsion','הקישור לשומן הוא בין־תחומי בלבד; אגוז וחמאה אינם אותו חומר גלם.'),
 (456,9,'moist grain and bean dishes','Cooked-Seeds-Storage','תבשילי דגן וקטניות לאחר בישול','הספר מדגיש שתבשילי דגן וקטניות לחים דורשים תשומת לב לאחסון לאחר הבישול, בניגוד ליציבות היחסית של זרעים יבשים.','07_Food-Safety','Microbial-Danger-Zone-Cooling','הוראות חימום חוזר ונתוני בריאות משנת 2004 לא מופעלים כנוהל עדכני; ריח תקין אינו הוכחת בטיחות.'),
 (688,12,'Intentionally Crystalline Hard Candies','Candy-Crystallization','גבישים ומרקם ממתק','הספר מבחין בין ממתקים שבהם גבישים הם פגם לבין ממתקים שבהם גבישים קטנים מכוונים יוצרים מרקם פריך ומתפורר.','05_Textures','Caramelization-And-Emulsification','נדרש מתכון מלא; אין כאן טמפרטורת עבודה או הוראת טיפול בסירופ חם.'),
 (694,12,'fermentation and roasting','Chocolate-Aroma-Development','פיתוח טעם שוקולד','הספר מייחס את מורכבות טעם השוקולד לשילוב תהליכי תסיסה וקלייה של זרעי הקקאו.','04_Flavors','Maillard-Reaction','הראיה אינה מפרטת כאן פרוטוקול תסיסה או קלייה לשימוש ביתי.'),
 (706,12,'Some recipes rely','Cocoa-Leavening','קקאו טבעי מול קקאו בסיסי','הספר מזהיר שהחלפת קקאו טבעי בקקאו שעבר הבססה משנה מתכון המסתמך על חומציות הקקאו לתגובה עם סודה לשתייה.','08_Decision-Making','Acid-Fat-Balance','יש לבדוק את מערכת ההתפחה כולה; אבקת אפייה וסודה אינן זהות ואין יחס החלפה אוטומטי.'),
 (707,12,'small amount of water','Chocolate-Seizing','שוקולד שנתפס לאחר תוספת מים','הספר מסביר שמעט מים בשוקולד מומס יכולים ליצור גשרים דביקים בין חלקיקי הסוכר והקקאו; תוספת נוזל מספקת יכולה ליצור תערובת נוזלית אחרת.','03_Techniques','Caramelization-And-Emulsification','תיקון בעזרת נוזל משנה את המוצר; התערובת אינה בהכרח מתאימה עוד לטמפרור או לציפוי קשיח.'),
 (715,13,'YEASTS AND ALCOHOLIC FERMENTATION','Yeast-Fermentation','שמרים ותסיסה אלכוהולית','הספר מציג שמרי Saccharomyces כקבוצת אורגניזמים המשמשת לייצור אלכוהול במזון ובמשקאות.','02_Food-Science','Fat-Soluble-Volatile-Aromas','הטקסט אינו מספק פרוטוקול תסיסה בטוח או ייעוץ בריאותי על שתייה.'),
 (720,13,'small traces boost their volatility','Alcohol-Aroma','אלכוהול ומיצוי ארומה','הספר מסביר שאלכוהול מספק מדיום נוסף למיצוי טעם, ושהריכוז שלו יכול לשנות את שחרור הארומות.','04_Flavors','Fat-Soluble-Volatile-Aromas','אין להסיק שכל האלכוהול נעלם בבישול או שתבשיל מתאים למי שחייב להימנע מאלכוהול.'),
 (773,13,'Alcohol + oxygen','Acetic-Fermentation','תסיסה אצטית ודרישת חמצן','הספר מתאר יצירת חומצה אצטית מאלכוהול בנוכחות חמצן באמצעות חיידקים מתאימים.','02_Food-Science','Acid-Fat-Balance','מנגנון אינו מתכון בטוח להכנת חומץ ואינו הוכחה להתאמה לשימור או לכבישה.'),
 (781,14,'One of the most important variables is the thickness','Thickness-Heat-Time','עובי וזמן חימום המרכז','הספר מסביר שחום מגיע למרכז מזון מוצק בהולכה וששינוי עובי וצורה משנה את זמן החימום באופן שאינו יחס ישר פשוט.','08_Decision-Making','Heat-Transfer','אין להכפיל זמן אוטומטית כשמכפילים עובי; נדרשת בדיקת מוכנות.'),
 (790,14,'line copper utensils with stainless steel','Copper-Lining','כלי נחושת וציפוי','הספר מתאר יתרון הולכת חום בנחושת לצד תגובתיות עם מזון, ואת השימוש בציפוי נירוסטה או בדיל להפרדה.','06_Equipment','Cast-Iron-Vs-Stainless-Thermal-Mass','אין לפרש נחושת חשופה כמתאימה לכל מזון; הוראות היצרן והמצב הפיזי של הציפוי קובעים.'),
 (789,14,'damaged by quenching a hot pan','Enamel-Thermal-Shock','אמייל ושינוי טמפרטורה חד','הספר מזהיר שקירור פתאומי של כלי אמייל חם במים קרים עלול לפגוע בשכבת הזכוכית.','06_Equipment','Cast-Iron-Vs-Stainless-Thermal-Mass','יש להבחין בין חומרי כלי שונים ולפעול לפי הוראות היצרן.'),
 (793,15,'hydrogen bond','Water-Polarity','קוטביות מים וקשרי מימן','הספר מסביר שקוטביות מולקולת המים מאפשרת משיכות וקשרי מימן זמניים בין מולקולות, ותכונה זו עומדת בבסיס כמה מתכונות המים בבישול.','02_Food-Science','Heat-Transfer','זהו הסבר מולקולרי; אינו קובע זמן או טמפרטורה לתהליך מסוים.'),
 (802,15,'water-soluble at the head','Emulsifier-Orientation','מתחלבים: ראש מימי וזנב שומני','הספר מתאר מולקולות מתחלב בעלות ראש מסיס במים וזנב מסיס בשומן, המסייעות להפרדת טיפות שומן במערכת מימית.','02_Food-Science','Caramelization-And-Emulsification','המנגנון אינו מבטיח יציבות לכל רוטב; ההרכב ויחסי הפאזות קובעים.'),
 (804,15,'linear chain called amylose','Starch-Structure','עמילוז, עמילופקטין וגרגרי עמילן','הספר מבחין בין שרשרת עמילוז ליניארית לבין עמילופקטין מסועף, ומתאר התנפחות גרגרים בחימום עם מים וקישור מחדש בקירור.','02_Food-Science','Starch-Gelatinization-Retrogradation','תכונות העמילן משתנות בין מקורות; לא מוסקים מכאן יחסי הסמכה אחידים.'),
 (808,15,'Denaturation is not a change in composition','Protein-Denaturation-Structure','דנטורציה כשינוי במבנה חלבון','הספר מבחין בין פירוק המבנה המרחבי של חלבון לבין שינוי בהרכבו, ומסביר שמבנה משתנה גורר התנהגות שונה.','02_Food-Science','Protein-Denaturation-Coagulation','דנטורציה אינה הוכחת חיטוי, אינה תמיד קרישה ואינה טמפרטורה אחת לכל חלבון.'),
]

RULES = [
 (5,2,'Acid-Softening','ירק שאינו מתרכך ברוטב חומצי','אם ירק נשאר קשה ברוטב עגבניות','אפשר לבשלו תחילה במים ולהוסיף לרוטב בהמשך, או לשמור את הבישול ברוטב כשמרקם יציב רצוי','חומציות וקשיות מים משנות את פירוק חומרי דופן התא','בישול נפרד מוסיף כלי ושלב; בישול ברוטב שומר רצף עבודה אך עשוי לעכב ריכוך'),
 (6,1,'Potato-Shape','בחירת תפוח אדמה לפי מרקם','אם צריך חתיכות תפוח אדמה ששומרות צורה','אפשר לבחור זן שעוותי לסלט או גרטן, או זן המתפרק בקלות למרקם מחיתי','לכידות התאים אחרי בישול שונה בין זנים','שמירת צורה ומחית חלקה הן מטרות שונות; אין זן אחד המיטבי לכולן'),
 (7,2,'Fruit-Ripening','פרי שנקטף: ציפייה להבשלה','אם בוחרים פרי לפי מה שצפוי להשתנות אחרי הקטיף','יש לזהות את סוג הפרי ולא להניח שכל פרי קשה יהפוך מתוק בהמתנה','הספר מבחין בדפוסי הבשלה שונים','קנייה בשלה מתאימה לשימוש מיידי; המתנה מתאימה רק למין ולשלב שבהם היא מועילה'),
 (8,1,'Herb-Time','עשבי תיבול מוקדם או בסיום','אם רוצים ארומה רעננה בתבשיל ממושך','אפשר להוסיף חלק בסיום; אפשר להוסיף מוקדם לפיתוח טעם מבושל או לפצל בין הזמנים','חימום משנה ומנדף חלק מרכיבי הארומה','הוספה מוקדמת משתלבת בטעם התבשיל; מאוחרת מדגישה רעננות'),
 (9,3,'Cooked-Seeds','זרע יבש לעומת תבשיל לח','אם עוברים מאחסון דגן או קטנייה יבשים לתבשיל מבושל','יש לעבור גם לנוהל אחסון המתאים למזון לח, ולא לשמר את הנחות האחסון של חומר הגלם היבש','לחות לאחר בישול משנה את תנאי הגידול של מיקרואורגניזמים','זהו כלל אבחנה בלבד; זמני קירור וחימום מגיעים מנוהל בטיחות עדכני ולא מהספר לבדו'),
 (12,4,'Chocolate-Goal','שוקולד שנתפס: תיקון לפי שימוש','אם שוקולד מומס נעשה משחתי לאחר מעט מים','אפשר להפוך אותו לרוטב באמצעות נוזל מתאים, או להתחיל מחדש כשנדרש ציפוי קשיח','מעט מים מדביקים חלקיקים בעוד מערכת עם די נוזל מתנהגת אחרת','תיקון לרוטב מציל חומר אך אינו משחזר בהכרח מוצר המתאים לטמפרור'),
 (13,2,'Alcohol-Choice','בחירת אלכוהול לפי יעד המנה','אם רוצים להשתמש במשקה אלכוהולי לטעם','אפשר להשתמש בו כשמתאים לסועדים, או לבחור חלופה נטולת אלכוהול ולהתאים טעם בנפרד','אלכוהול משנה מיצוי ושחרור ארומות, לא רק טעם המשקה','חלופה אינה בהכרח משחזרת אותו פרופיל; בישול אינו הבטחה להסרת כל האלכוהול'),
 (14,1,'Thickness','שינוי עובי ואומדן זמן','אם עובי המזון שונה מהמתכון','יש להתאים את נקודות הבדיקה, במקום להכפיל זמן באופן ליניארי','מרחק ההולכה וצורת המזון משנים את קצב חימום המרכז','אומדן זמן מסייע לתכנון; בדיקת המרכז מסייעת להחלטת המשך'),
 (15,4,'Protein-Endpoint','מבנה חלבון מול בטיחות','אם שינוי מרקם מצביע על התייצבות חלבון','אפשר להשתמש בו להערכת המרקם אך יש לבדוק בטיחות בנפרד לפי חומר הגלם והתהליך','דנטורציה מתארת שינוי מבני ולא אישור חיטוי','השלמת מרקם ובדיקת בטיחות הן מטרות נפרדות; אין להסיק טמפרטורה אחת לכל חלבון'),
]


def norm(t):
    t=re.sub(r'(?<=\w)[-\u00ad]\s*\n\s*(?=\w)','',t)
    t=unicodedata.normalize('NFKC',t).replace('\u00ad','')
    return re.sub(r'\s+',' ',t).strip()


def sha(data):return hashlib.sha256(data).hexdigest()


def note(path,meta,body):
    content='---\n'+yaml.safe_dump(meta,allow_unicode=True,sort_keys=False,width=110)+'---\n\n'+body+'\n'
    if path.exists() and path.read_text(encoding='utf-8')!=content:raise RuntimeError(f'Existing file differs: {path}')
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(content,encoding='utf-8')


def main():
    files=[]
    for folder,lo,hi in [('ilovepdf_split-range (4)',226,400),('ilovepdf_split-range (4)',401,500),('ilovepdf_split-range (3)',701,898)]:
        matches=list((DOWNLOADS/folder).glob(f'*{lo}-{hi}.pdf'))
        if len(matches)!=1:raise RuntimeError((folder,lo,len(matches)))
        files.append((matches[0],lo,hi,fitz.open(matches[0])))
    full=next(DOWNLOADS.glob('On Food and Cooking*.pdf'));whole=fitz.open(full)
    originals={str(p.relative_to(ROOT)):sha(p.read_bytes()) for p in ROOT.rglob('*.md') if 'McGee-2004-Supplied-Ranges' not in str(p) and not p.stem.startswith('McGee-Ranges-')}
    nodes={}
    for p in ROOT.rglob('*.md'):
        t=p.read_text(encoding='utf-8-sig')
        if t.startswith('---'):
            m=yaml.safe_load(t.split('---',2)[1])
            if isinstance(m,dict) and m.get('id'):nodes[p.stem]=m['id']
    pages=[]
    for path,lo,hi,d in files:
        if len(d)!=hi-lo+1:raise RuntimeError('Unexpected split length')
        for k,page in enumerate(d):
            global_page=lo+k;text=norm(page.get_text())
            if text!=norm(whole[global_page-1].get_text()):raise RuntimeError(f'Full-book mapping failed: {path.name}/{k+1}')
            pages.append({'split_filename':path.name,'split_page':k+1,'pdf_page':global_page,'normalized_text_sha256':sha(text.encode()),'characters':len(text)})
    # Validate all anchors before writing notes.
    for printed,ch,anchor,*_ in ROWS:
        if norm(anchor).casefold() not in norm(whole[printed+13].get_text()).casefold():raise RuntimeError((printed,anchor))
        if not any(lo<=printed+14<=hi for _,lo,hi,_ in files):raise RuntimeError('Claim outside supplied ranges')
    records=[];counts={}
    for printed,ch,anchor,slug,title,claim,folder,canonical,limits in ROWS:
        counts[ch]=counts.get(ch,0)+1;n=counts[ch];pid=printed+14
        path,lo,hi,d=next(f for f in files if f[1]<=pid<=f[2]);local=pid-lo+1
        eid=f'EVD-MCG-RNG-CH{ch:02d}-{n:03d}';cid=f'CLM-MCG-RNG-CH{ch:02d}-{n:03d}';stem=f'McGee-Ranges-CH{ch:02d}-{slug}'
        src={'source_id':SOURCE,'book_title':'On Food and Cooking: The Science and Lore of the Kitchen','author':'Harold McGee','edition':'Completely Revised and Updated, 2004','year':2004,'chapter':f'Chapter {ch}','printed_pages':f'p. {printed}','pdf_pages':f'p. {pid}','split_filename':path.name,'split_page':local,'anchor':anchor,'page_text_sha256':sha(norm(d[local-1].get_text()).encode())}
        rels=[{'type':'SUPPORTED_BY','target_id':SOURCE,'target_name':'[[SRC-MCGEE-2004]]','evidence':cid,'confidence':'HIGH_SOURCE_ATTRIBUTION'},{'type':'SUPPORTS','target_id':nodes[canonical],'target_name':f'[[{canonical}]]','evidence':cid,'conditions':limits,'confidence':'CONDITIONAL_INTERPRETIVE_MAPPING'}]
        meta={'id':eid,'type':'EVIDENCE_RECORD','name':title,'domain':folder.split('_',1)[1].upper(),'claim_id':cid,'claim_type':'SOURCE_SUPPORTED_CLAIM','claim':claim,'source_text_checked':True,'scientific_validation':'NOT_INDEPENDENTLY_VALIDATED','verification_status':'PRELIMINARY','canonical_concept_id':nodes[canonical],'conditions':[limits],'sources':[src],'relationships':rels}
        note(ROOT/folder/(stem+'.md'),meta,f'# {title}\n\n{claim}\n\nתנאים ומגבלות: {limits}\n\nמקור: [[SRC-MCGEE-2004]], פרק {ch}, עמוד מודפס {printed}, עמוד PDF מלא {pid}, עמוד {local} בחלק `{path.name}`. סימן איתור: `{anchor}`.\n\nזהו ייחוס לטקסט שנבדק בספר, לא אימות עצמאי של הטענה. הקישור ל־[[{canonical}]] הוא מיפוי פרשני; מושגים סמוכים אינם בהכרח זהים.\n\n[[McGee-Ranges-Report-HE]]')
        records.append({'id':eid,'claim_id':cid,'stem':stem,'chapter':ch,'printed_page':printed,'pdf_page':pid,'split_page':local,'split_filename':path.name,'page_text_sha256':src['page_text_sha256'],'canonical_id':nodes[canonical]})
    rules=[]
    for ch,index,slug,title,if_,then,because,tradeoff in RULES:
        ev=[r for r in records if r['chapter']==ch][index-1];rid=f'RUL-MCG-RNG-CH{ch:02d}-001';stem=f'McGee-Ranges-CH{ch:02d}-Rule-{slug}'
        meta={'id':rid,'type':'CULINARY_RULE','name':title,'domain':'RULES','claim_type':'INTERPRETATION','verification_status':'PRELIMINARY','source_text_checked':True,'if':if_,'then':then,'because':because,'tradeoffs':tradeoff,'exceptions':['זהו כלל פרשני מותנה, לא מתכון מלא ולא נוהל בטיחות.'],'source_claim_ids':[ev['claim_id']],'sources':[{'source_id':SOURCE,'chapter':f'Chapter {ch}','printed_pages':f"p. {ev['printed_page']}",'pdf_pages':f"p. {ev['pdf_page']}",'split_filename':ev['split_filename'],'split_page':ev['split_page']}],'relationships':[{'type':'SUPPORTED_BY','target_id':ev['id'],'target_name':f"[[{ev['stem']}]]",'conditions':if_,'evidence':ev['claim_id'],'confidence':'CONDITIONAL_INTERPRETATION'}]}
        note(ROOT/'12_Rules'/(stem+'.md'),meta,f'# {title}\n\n**IF:** {if_}\n\n**THEN:** {then}\n\n**BECAUSE:** {because}\n\n**EXCEPTIONS / TRADEOFFS:** {tradeoff}\n\nראיה: [[{ev["stem"]}]]. כלל פרשני בלבד; לא הומצאו יחסי המרה או הוראות זמן.\n\n[[McGee-Ranges-Report-HE]]')
        rules.append({'id':rid,'stem':stem,'chapter':ch,'source_claim_id':ev['claim_id']})
    manifest={'source_id':SOURCE,'full_pdf_path':str(full),'full_pdf_sha256':sha(full.read_bytes()),'sources':[{'path':str(p),'sha256':sha(p.read_bytes()),'pdf_start':lo,'pdf_end':hi,'pages':len(d)} for p,lo,hi,d in files],'pages':pages,'records':records,'rules':rules,'existing_knowledge_hashes':originals,'coverage':'SELECTIVE_EVIDENCE_FROM_ALL_THREE_SUPPLIED_RANGES','unprovided_pdf_range':[501,700]}
    dest=OUT/'McGee-Ranges-manifest.json'
    if dest.exists():raise RuntimeError('Manifest exists; review before rerunning')
    dest.write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'pages_mapped':len(pages),'claims':len(records),'rules':len(rules),'chapters':counts}))


if __name__=='__main__':main()
