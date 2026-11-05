---
id: QA-FLB-2015-001
type: HUMAN_REASONING_CHECK
name: חמש שאלות בדיקה לרשת הידע של The Food Lab
verification_status: PRELIMINARY
automated_reasoning_engine_claimed: false
---

# חמש שאלות בדיקה

אלה מסלולי ראיות לבחינה ידנית. לא הופעל או הוקם כאן מנוע הסקה אוטומטי.

1. **למה בשר עשוי להיות יבש אף שהתבשל בנוזל?**
   [[FoodLab-CH02-Braising-Moisture]] → [[Two-Phase-Juiciness-And-Fiber-Compaction]] ו־[[Collagen-Hydrolysis-Gelatin]]. התשובה הנתמכת: רכות רקמת החיבור ואחזקת מים בסיבי השריר הן תוצאות שונות. אין להסיק משך בישול מדויק בלי זיהוי נתח ותהליך. בדיקה משלימה: [[FoodLab-CH02-Rule-Braise-Heat-Source]].

2. **למה המבורגר נעשה צפוף, בעוד מבנה מלוכד עשוי להיות רצוי בנקניק?**
   [[FoodLab-CH05-Burger-Handling]] → [[Sausage-Emulsions-Myosin-And-Nitrite-Curing]] → [[FoodLab-CH05-Rule-Ground-Meat-Texture]]. המקור תומך בהשפעת טיפול עודף בהמבורגר; ההשוואה למוצר מלוכד מסומנת כפרשנות. אין כאן היתר לאמץ יעד טמפרטורה של מוצר אחד לאחר.

3. **האם כלל נפח המים לפסטה מתאים גם לשעועית ירוקה?**
   [[FoodLab-CH04-Blanch-Water-Volume]] לעומת [[FoodLab-CH07-Pasta-Water-Energy]] → [[Heat-Transfer]] → [[FoodLab-2015-Conflicts-And-Gaps]]. התשובה: הראיות עוסקות במזונות וביעדים שונים; אין להעביר כלל ללא בדיקת ירידת טמפרטורה, צבע, ריכוך ועמילן. טענת מינימום מים לפסטה דורשת את ההקשר המלא, ולא רק את משוואת האנרגיה שנבחרה.

4. **איך לבחור בין ויניגרט יציב יותר לבין טעם ללא חרדל?**
   [[FoodLab-CH08-Mustard-Vinaigrette]] → [[FoodLab-CH08-Rule-Vinaigrette-Stability]] ו־[[Caramelization-And-Emulsification]]. ההשוואה במקור מראה האטת הפרדה בתנאים שנבדקו; חלופת ערבוב סמוך להגשה היא כלל פרשני. יש להביא בחשבון רגישות לחרדל וטעם, ולא להניח חיי מדף בלתי מוגבלים.

5. **מדוע פרישת עוף ומאוורר תנור משנים את תוצאת הצלייה?**
   [[FoodLab-CH06-Spatchcock-Geometry]] + [[FoodLab-CH06-Convection-Surface-Drying]] → [[Heat-Transfer]] → [[FoodLab-CH06-Rule-Bird-Geometry]]. פרישה משנה חשיפה גאומטרית; המאוורר משנה העברת חום וסילוק לחות. אלה מנגנונים שונים. [[Core-Probe-Thermometry]] ו־[[Minimum-Internal-Temperatures]] נדרשים בנפרד; צבע העור אינו הוכחת מוכנות.
