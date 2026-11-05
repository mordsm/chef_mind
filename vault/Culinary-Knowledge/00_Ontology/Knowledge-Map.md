---
id: ONT-MAP-001
type: ONTOLOGY_MAP
name: Universal Culinary Knowledge Map
domain: CULINARY_ONTOLOGY
version: 1.2.0
last_updated: 2026-10-21
verification_status: FOUNDATIONAL
---

# מפת הידע הקולינרי האוניברסלי (Universal Culinary Knowledge Map)

מפה זו מגדירה את הארכיטקטורה והאונטולוגיה של הידע הקולינרי עבור מערכת השף והסו-שף. המערכת מבוססת על 8 תחומי ידע ראשיים המקושרים ביניהם כרשת ידע (Knowledge Graph) גמישה ולא כעץ ספריות קשיח.

---

## 1. תחום חומרי גלם (Ingredients)
ספרייה: `[[01_Ingredients/]]`

* **1.1 סיווג חומרי גלם (Ingredient Classification)**
  * חלבונים מן החי (בשר בקר, עוף, דגים, פירות ים, ביצים)
  * מוצרי חלב ושומן חלבי (חלב, שמנת, חמאה, גבינות קשות/רכות, יוגורט)
  * דגנים וקמחים (חיטה, אורז, שיבולת שועל, תירס, קמחי קטניות/שקדים)
  * ירקות ועלים (שורשים, פקעות, בצל וסולניים, מצליבים, עשבי תיבול)
  * פירות וחומציים (הדרים, פירות יער, תפוחים, פירות גלעין)
  * שומנים ושמנים (שמן זית, שמנים צמחיים מזוככים, שומן מן החי, חמאת קקאו)
  * קטניות ואגוזים (עדשים, חומוס, שעועית, שקדים, אגוזי מלך)
* **1.2 הרכב מולקולרי ותזונתי (Composition)**
  * יחסי מים-חלבון-שומן-פחמימה
  * תכולת סוכרים חופשיים וחומצות אמינו
  * pH פנימי של חומר הגלם
* **1.3 תכונות פיזיקליות (Physical Properties)**
  * צפיפות, נקבוביות, הולכת חום סגולית
  * מבנה תאי, דפנות תא, רקמות חיבור (קולגן ואלסטין)
* **1.4 תכונות כימיות (Chemical Properties)**
  * נטייה לחמצון, תגובה עם חומצות/בסיסים, אנזימים פעילים פנימיים
* **1.5 טריות, איכות ובשלות (Freshness & Quality)**
  * מדדי קלקול ובשלות, רמת הידרציה, פעילות אנזימטית לאחר קטיף/שחיטה
* **1.6 התנהגות בתנאי בישול שונים (Behavior Under Cooking)**
  * התכווצות חלבונים ואיבוד נוזלים, פירוק עמילנים, ריכוך פקטין בדפנות תא

---

## 2. תחום מדע המזון (Food Science)
ספרייה: `[[02_Food-Science/]]`

* **2.1 מעבר חום ותרמודינמיקה (Heat Transfer & Thermodynamics)**
  * [[Heat-Transfer|הולכת חום (Conduction)]]
  * הסעת חום (Convection)
  * קרינת חום (Radiation)
  * שטף חום ומפל טמפרטורה (Temperature Gradient & Heat Flux)
* **2.2 מים, לחות ופעילות מים (Water & Moisture)**
  * פעילות מים ($a_w$)
  * אידוי, ספיחת מים, לחות יחסית בסביבת הבישול
* **2.3 חלבונים ודנטורציה (Proteins & Coagulation)**
  * טמפרטורות דנטורציה של חלבונים שונים (מיוצין, אקטין, אובלבומין)
  * קרישה (Coagulation), הצטמקות רשת החלבון וכליאת נוזלים
* **2.4 פחמימות ועמילנים (Carbohydrates & Starches)**
  * ג'לטיניזציה (Gelatinization) של עמילנים
  * רטרוגרדציה (Retrogradation) של עמילן
  * פירוק רב-סוכרים לסוכרים פשוטים
* **2.5 שומנים וליפידים (Fats & Lipids)**
  * נקודת עשן (Smoke Point)
  * חמצון שומנים (Rancidity)
  * התגבשות שומנים ופולימורפיזם
* **2.6 תגובות כימיות והשחמה (Chemical Reactions & Browning)**
  * [[Maillard-Reaction|תגובת מייאר (Maillard Reaction)]]
  * קרמליזציה (Caramelization)
  * השחמה אנזימטית מול לא-אנזימטית
* **2.7 תחליבים ומערכות קולואידיות (Emulsions & Colloids)**
  * תחליב שמן-במים ומים-בשמן
  * חומרים מתחלבים (לציטין, פוספוליפידים, חרדל)
  * שבירת תחליב ויציבות תרמית

---

## 3. תחום טכניקות בישול (Cooking Techniques)
ספרייה: `[[03_Techniques/]]`

* **3.1 בישול בסביבה יבשה (Dry-Heat Cooking)**
  * צריבה (Searing / Pan-Frying)
  * צלייה בתנור (Roasting / Baking)
  * גריל ישיר ועקיף (Grilling / Broiling)
  * טיגון עמוק (Deep Frying)
* **3.2 בישול בסביבה לחה (Moist-Heat Cooking)**
  * רתיחה (Boiling)
  * בישול עדין (Simmering / Poaching)
  * אידוי (Steaming)
* **3.3 בישול משולב וארוך (Combination Cooking)**
  * צלי קדרה (Braising / Stewing)
  * בישול בסיר לחץ (Pressure Cooking)
* **3.4 בישול מבוקר מדויק (Precision Cooking)**
  * סו-וויד (Sous-Vide)
  * תנורים משולבי אדים (Combi-Ovens)
* **3.5 טכניקות קרות ושימור (Cold & Preservation Techniques)**
  * התססה לקטית (Lacto-Fermentation)
  * החמצה וכבישה (Pickling / Curing)
  * המלחה יבשה ורטובה (Brining)

---

## 4. תחום טעמים וארומות (Flavors & Aromas)
ספרייה: `[[04_Flavors/]]`

* **4.1 טעמי יסוד (Basic Tastes)**
  * מליחות (Salinity / Sodium perception)
  * מתיקות (Sweetness)
  * חמיצות (Acidity / pH perception)
  * מרירות (Bitterness)
  * אומאמי (Umami / Glutamates & Nucleotides)
  * שומניות (Kokumi / Fat mouthfeel)
* **4.2 תרכובות ארומה ונדיפות (Volatile Aromas)**
  * תרכובות מסיסות בשומן מול מסיסות במים
  * השפעת חום על שחרור ארומות
* **4.3 שידוכי טעמים (Flavor Pairing)**
  * מולקולות ארומה משותפות
  * ניגודים מאזנים (חמיצות מאזנת שומן, מליחות מדגישה מתיקות)
* **4.4 תיבול והתפתחות טעמים (Seasoning Dynamics)**
  * תיבול מוקדם מול תיבול מאוחר
  * מיצוי תבלינים בשומן חם (Blooming Spices)
  * רדוקציה וריכוז טעמים

---

## 5. תחום מרקמים (Textures)
ספרייה: `[[05_Textures/]]`

* **5.1 פריכות וקראנץ' (Crispness & Crunch)**
  * [[Surface-Browning|השחמת משטח וקראסט (Surface Browning)]]
  * איבוד לחות בשכבה החיצונית
* **5.2 רכות ועסיסיות (Tenderness & Juiciness)**
  * פירוק קולגן לג'לטין
  * כליאת מים ברשת שריר
* **5.3 צמיגות והסמכה (Viscosity & Thickening)**
  * הסמכה עמילנית (Starch slurries, Roux)
  * צמצום נוזלים והסמכת קולגן
* **5.4 ג'לטיניזציה וקרישה (Gelation & Setting)**
  * ג'לים חמים וקרים (פקטין, ג'לטין, אגר)
* **5.5 טרנספורמציות מרקם (Texture Transitions)**
  * מעבר מנוזל למוצק וממוצק לצמיגי

---

## 6. תחום ציוד וסביבה (Equipment & Environment)
ספרייה: `[[06_Equipment/]]`

* **6.1 תנורים ומקורות חום (Ovens & Heat Sources)**
  * תנורי קונבקציה (טורבו) מול תנורים סטטיים
  * גז, אינדוקציה, גוף חימום חשמלי
* **6.2 כלי בישול ומחבתות (Pans, Pots & Materials)**
  * ברזל יצוק (Cast Iron) - קיבול חום גבוה, הולכה איטית
  * נירוסטה (Stainless Steel) - הולכה אחידה (במיוחד בציפוי אלומיניום/נחושת)
  * טפלון/קרמי (Non-Stick) - מגבלת טמפרטורה
  * נחושת (Copper) - תגובה תרמית מיידית
* **6.3 בקרת טמפרטורה ולחות (Temperature & Humidity Control)**
  * מדי חום ליבה (Probe thermometers)
  * מאזן לחות בסיר סגור מול פתוח
* **6.4 מגבלות ציוד (Equipment Constraints)**
  * איבוד חום בעת הכנסת מזון קר למחבת דקה
  * נקודות חמות (Hot spots)

---

## 7. תחום בטיחות מזון ושימור (Food Safety & Preservation)
ספרייה: `[[07_Food-Safety/]]`

* **7.1 גורמי סיכון ביולוגיים וכימיים (Biological & Chemical Hazards)**
  * סלמונלה, ליסטריה, E. coli, בוטולינום, קמפילובקטר
  * טווח טמפרטורות הסכנה (Danger Zone: 4°C – 60°C)
* **7.2 פרקטיקות בישול בטוח (Safe Cooking Practices)**
  * טמפרטורות ליבה מינימליות (עוף: 74°C, בקר טחון: 71°C)
  * זמן מול טמפרטורה בפסטור (Pasteurization curves)
* **7.3 קירור, הקפאה ואחסון (Chilling, Freezing & Storage)**
  * קירור מהיר (פחות משעתיים מ-60°C ל-20°C, ו-4 שעות ל-4°C)
  * מניעת כוויות קור (Freezer burn)
* **7.4 מניעת זיהום צולב (Cross-Contamination)**
  * הפרדת משטחי חיתוך, כלי עבודה ומרינדות לא מבושלות

---

## 8. תחום תכנון וקבלת החלטות (Planning & Decision-Making)
ספרייה: `[[08_Decision-Making/]]`

* **8.1 הגדרת תוצאת המטרה (Goal Specification)**
  * מרקם רצוי (עסיסי / פריך / נימוח)
  * פרופיל טעם (מודגש / מאוזן / חמצמץ)
* **8.2 בחירת טכניקה מותאמת (Technique Selection)**
  * התאמת סוג החלבון ורמת השומן/קולגן לטכניקה
* **8.3 אלטרנטיבות ואילוצים (Constraints & Alternatives)**
  * תחליפי ציוד (מחבת במקום גריל)
  * תחליפי חומרי גלם עקב כשרות, אלרגיה או זמינות
* **8.4 אבחון ופתרון כשלים בזמן אמת (Failure Diagnosis)**
  * "הבצל משחים לפני שהתרכך" -> הפחתת חום, הוספת מעט מים, כיסוי
  * "הרוטב נשבר" -> הורדת חום, טריפה עם מעט מים קרים/שמנת
  * "הבשר יבש" -> חיתוך דק נגד הסיבים, הגשה עם רוטב עשיר
* **8.5 אופטימיזציה (Optimization)**
  * קיצור זמנים ללא פגיעה באיכות (שימוש בסיר לחץ, המלחה מוקדמת Dry Brining)

---

## 9. אינדקס רשומות פיילוט חילוץ ספרות: *On Food and Cooking* (McGee 2004) — Chapter 2: Eggs
מקור מאומת: `[[SRC-MCGEE-2004]]` (עמודים מודפסים 68–117 | עמודי PDF 82–131):

* **01. חומרי גלם (`01_Ingredients/`):**
  * `[[Egg-Proteins-Yolk-Albumen]]` (`ING-EGG-001`) — הרכב ביצת תרנגולת שלמה, חלבון וחלמון
  * `[[Egg-Albumen-Key-Proteins]]` (`ING-EGG-002`) — שבעת חלבוני האלבומין (`Ovalbumin`, `Ovotransferrin`, `Ovomucin`, `Lysozyme`, `Globulins`)
  * `[[Egg-Yolk-Lipoproteins-And-Amylase]]` (`ING-EGG-003`) — כדורי חלמון, גרנולות, `LDL`, לציטין ואנזים ה-`Amylase` העמיד לחום
  * `[[Egg-Aging-Alkalinization-And-Grades]]` (`ING-EGG-004`) — איבוד $\text{CO}_2$, עליית pH מ-7.7 ל-9.2, אוסמוזה ודירוג איכות
* **02. מדע המזון (`02_Food-Science/`):**
  * `[[Protein-Denaturation-Coagulation]]` (`SCI-PROT-002`) — מנגנון דנטורציה וקרישה וסיפי טמפרטורה
  * `[[Custard-Dilution-Ion-Shielding-And-Starch-Protection]]` (`SCI-PROT-003`) — דילול פי 6, מיסוך סוכרוז, חובת יונים ליצירת ג'ל והגנת עמילן ב-77°C
  * `[[Egg-Foam-Stability-Disulfide-And-Acid-Copper-Chemistry]]` (`SCI-FOAM-001`) — ייצוב קצף, קשרי גופרית ($\text{S}-\text{S}$), נחושת, חומצה, מלח וסוכר
  * `[[Souffle-Thermodynamics-Gas-Expansion-And-Vaporization]]` (`SCI-THERM-001`) — חוק שארל (25%) מול אידוי מים לקיטור (75%) בתפיחת סופלה
  * `[[Alkali-And-Salt-Egg-Curing-Chemistry]]` (`SCI-CHEM-003`) — ביצים מומלחות (35% מלח) וכבישה בסיסית ב-pH 12 (*Pidan / Songhuadan*)
  * `[[Conflict-Acid-And-Salt-Tenderize-Vs-Toughen-Eggs]]` (`CNF-EGG-001`) — יישוב סתירה: חומצה ומלח מרככים ביצה מבושלת אך מלח מחליש קצף חי
* **03. טכניקות בישול (`03_Techniques/`):**
  * `[[In-Shell-Egg-Simmering-And-Steaming]]` (`TEC-EGG-001`) — בישול בקליפה בבעבוע שקט (80–85°C), אידוי ובישול ארוך (*Hamindas* ב-71–74°C)
  * `[[Poaching-Scrambling-And-French-Omelet-Control]]` (`TEC-EGG-002`) — שליקה (ניקוז חלבון דליל ושיטת הריחוף), טיגון ב-120°C, מקושקשת איטית ואומלט צרפתי
  * `[[Custard-Water-Bath-Baking-And-Cream-Stirring]]` (`TEC-EGG-003`) — קסטרדים אפויים, קרמים בחושים ומניעת סדקים בעוגת גבינה
  * `[[Meringue-Souffle-And-Sabayon-Whipping]]` (`TEC-EGG-004`) — 4 שלבי קצף, מרנג צרפתי/איטלקי/שווייצרי, קיפול איטי של סופלה וזביונה ב-50°C
  * `[[Conflict-Souffle-Dish-Buttering-And-Oven-Door-Myths]]` (`CNF-EGG-003`) — הפרכת מיתוסי שימון סופלה, דלת התנור, חור סיכה בביצה ושלב ה"סרט"
* **04. טעמים וארומות (`04_Flavors/`):**
  * `[[Egg-Sulfur-Volatiles-And-Ferrous-Sulfide-Greening]]` (`FLV-EGG-001`) — מימן גופרי ($\text{H}_2\text{S}$), הירקרקות ברזל גופרי ($\text{FeS}$) וטרימתילאמין
* **05. מרקמים (`05_Textures/`):**
  * `[[Egg-Gels-Custard-Networks-And-Foam-Stages]]` (`TEX-EGG-001`) — ג'ל אלבומין מול חלמון ואבחון הזעה/חרוזים/גרגיריות במרנג
* **06. ציוד וסביבה (`06_Equipment/`):**
  * `[[Water-Bath-Materials-And-Copper-Whisking-Bowls]]` (`EQP-EGG-001`) — פיזיקת חומרי אמבט מים (ברזל יצוק 87°C, זכוכית 83°C, נירוסטה 80°C) וקערות נחושת
  * `[[Conflict-Copper-Bowl-Ovotransferrin-Vs-Sulfur-Theory]]` (`CNF-EGG-002`) — ניסוי קערת הכסף והפרכת תיאוריית האובטרנספרין מ-1984
* **07. בטיחות מזון (`07_Food-Safety/`):**
  * `[[Egg-Salmonella-Pasteurization-And-Lead-Pidan-Hazards]]` (`SAF-EGG-001`) — משטרי פסטור *Salmonella*, מרנג שווייצרי מול איטלקי ורעילות עופרת ב-*Pidan*
  * `[[Conflict-Dietary-Egg-Cholesterol-Vs-Saturated-Fat]]` (`CNF-EGG-004`) — כולסטרול תזונתי בביצה מול שומן רווי ופוספוליפידים
* **08. קבלת החלטות וכללים מותנים (`08_Decision-Making/` & `12_Rules/`):**
  * `[[Rule-Custard-Curdling-Rescue]]` (`RUL-EGG-001`) — עצירה ומניעת התגבנות בקסטרד וקרם ביצים
  * `[[Rule-Egg-Age-And-Grade-Selection-Matrix]]` (`RUL-EGG-002`) — בחירת גיל ודירוג ביצים לפי משימה ופתרון קילוף
  * `[[Rule-Starch-Stabilized-Pastry-Cream-Boiling]]` (`RUL-EGG-003`) — חובת הרתחת קרם פטיסייר להשבתת עמילאז החלמון מול איסור הרתחה בקרם אנגלז
  * `[[Rule-Meringue-And-Egg-Foam-Stabilization-Methods]]` (`RUL-EGG-004`) — בחירת שיטת ייצוב קצף וסוג מרנג
  * `[[Rule-Custard-Water-Bath-And-Tempering-Control]]` (`RUL-EGG-005`) — בקרת אמבט מים והשוואת טמפרטורות (Tempering)
* **10. פערי ידע ואי-ודאויות (`10_Knowledge-Gaps/`):**
  * `[[Egg-Albumen-Biological-And-Adhesion-Unknowns]]` (`GAP-EGG-001`) — 5 אי-ודאויות מדעיות המתועדות בפרק 2

---

## 10. אינדקס רשומות חילוץ ספרות: *On Food and Cooking* (McGee 2004) — Chapter 3: Meat
מקור מאומת: `[[SRC-MCGEE-2004]]` (עמודים מודפסים 118–178 | עמודי PDF 132–192):

* **01. חומרי גלם (`01_Ingredients/`):**
  * `[[Beef-Chuck-Collagen-Rich]]` (`ING-MEAT-001`) — הרכב שריר עובד (75% מים, 20% חלבון, 3% שומן), קולגן מול אלסטין בלתי-מסיס
  * `[[Poultry-Breast-Lean]]` (`ING-POUL-001`) — חזה עוף והודו רזה (90% סיבים לבנים, צפידת מוות מהירה תוך פחות משעה ורגישות לייבוש)
  * `[[Muscle-Fiber-Types-And-Myoglobin-Chemistry]]` (`ING-MEAT-002`) — סיבים לבנים מהירים מול סיבים אדומים איטיים (חזה ברווז 80% אדומים, יונה 85% אדומים) ו-4 מצבי הצבע של המיוגלובין ($\text{Fe}^{2+}/\text{Fe}^{3+}/\text{O}_2/\text{NO}/\text{CO}$)
  * `[[Offal-Organs-And-Animal-Fat-Saturation]]` (`ING-MEAT-003`) — שרירים לא-שלדיים עתירי קולגן (קורקבן, לב, לשון, קיבה) מול איברים בלוטיים דלי קולגן (כבד, כבד אווז 50–65% שומן, שקדים, מוח) ומדרג רוויית שומן מן החי
* **02. מדע המזון (`02_Food-Science/`):**
  * `[[Collagen-Hydrolysis-Gelatin]]` (`SCI-PROT-001`) — התכווצות קולגן ב-60°C, המסה לג'לטין ב-70–90°C והשפעת גיל בעל החיים על קשרי הצילוב
  * `[[Meat-Thermal-Progression-And-Doneness-Spectrum]]` (`SCI-MEAT-001`) — ספקטרום השינויים המולקולריים בבשר מ-40°C עד 90°C וטבלת דרגות העשייה (עמ' 152)
  * `[[Rigor-Mortis-DFD-Meat-And-Aging-Enzymes]]` (`SCI-MEAT-002`) — ירידת ה-pH לחומצה לקטית, פגמי DFD ו-PSE, צפידת מוות, צינון מים מול אוויר ואנזימי יישון `Calpains` (עד 40°C) ו-`Cathepsins` (עד 50°C)
  * `[[Brining-Marinades-And-Protease-Tenderizers]]` (`SCI-MEAT-003`) — כימיית תמלחת (3%–6% מלח הממיס מיוצין ומפחית איבוד נוזלים ב-50%), מרינדות חומציות ואנזימי פרוטאז צמחיים (`Papain`, `Bromelain`, `Ficin`)
  * `[[Sausage-Emulsions-Myosin-And-Nitrite-Curing]]` (`SCI-MEAT-004`) — מיצוי מיוצין כדבק חלבוני, ספי טמפרטורה בנקניקיות מתחלבות ($\le 16^\circ\text{C}$ לחזיר, $\le 21^\circ\text{C}$ לבקר) וכימיית כבישה בניטריט ($\text{NO}$)
* **03. טכניקות בישול (`03_Techniques/` & `11_Conflicts/`):**
  * `[[Low-Slow-Braising]]` (`TEC-COMB-001`) — צלי קדרה מבוקר ב-80–90°C
  * `[[Two-Stage-Roasting-Flipping-And-Heat-Scaling]]` (`TEC-MEAT-001`) — היפוך תכוף מדי דקה, צלייה דו-שלבית וחוקי קנה-מידה ($t \propto L^2$ ו-$t \propto W^{2/3}$)
  * `[[Whole-Bird-Roasting-And-Crisp-Poultry-Skin]]` (`TEC-MEAT-002`) — דילמת העוף השלם (חזה מול כרעיים) ופרוטוקול 5 הצעדים לעור פריך
  * `[[Succulent-Braising-Stewing-And-Liquid-Cooling]]` (`TEC-MEAT-003`) — ששת כללי הזהב לצלי קדרה עסיסי וקירור בתוך נוזל הבישול ל-50°C
  * `[[Resting-Carryover-Cooking-And-Carving]]` (`TEC-MEAT-004`) — בישול שאריתי (`Carryover` עד 10°C), מנוחה ל-50°C ופריסה נגד הסיבים
  * `[[Searing-Locks-In-Juices-Myth]]` (`CON-MEAT-001`) — הפרכת מיתוס נעילת המיצים של פון ליביג (1850)
  * `[[Conflict-Octopus-Corks-Marinades-And-Breading-Myths]]` (`CNF-MEAT-002`) — הפרכת מיתוס פקקי השעם בתמנון, חדירת מרינדות וציפוי שניצל כמבודד תרמי
* **04. טעמים וארומות (`04_Flavors/` & `11_Conflicts/`):**
  * `[[Meat-Flavor-Precursors-Feed-And-Warmed-Over-Flavor]]` (`FLV-MEAT-001`) — ליבת מייאר מול חמצון שומן ספציפי למין, מרעה מול דגנים (`Skatole` & `Terpenes`) ומניעת `Warmed-Over Flavor` ברוזמרין/מרווה
  * `[[Pre-Salting-Steak-Timing]]` (`CON-SALT-001`) — יישוב סתירת תזמון המלחת סטייק
* **05. מרקמים (`05_Textures/`):**
  * `[[Two-Phase-Juiciness-And-Fiber-Compaction]]` (`TEX-MEAT-001`) — תפיסת העסיסיות הדו-שלבית וטכניקות מכניות לשבירת סיבים וציפויים ברוטב
* **06. ציוד וסביבה (`06_Equipment/`):**
  * `[[Radiant-Grilling-Smoking-And-Packaging-Permeability]]` (`EQP-MEAT-001`) — קרינת גריל ב-1100°C, כימיית עישון עץ וטבעת עשן, חדירות חמצן בניילון `PE` מול `PVDC`, והפשרה באמבט מים (מהירה פי 20 מאוויר)
* **07. בטיחות מזון (`07_Food-Safety/`):**
  * `[[Meat-Pathogens-Blanch-Grinding-And-Carcinogens]]` (`SAF-MEAT-001`) — פתוגנים (*E. coli* O157:H7, *Trichina* ב-58°C, פריונים), פרוטוקול חליטה-וטחינה (30–60 שניות במים רותחים) ומניעת `HCAs`, `PAHs` וניטרוזאמינים
* **08. קבלת החלטות וכללים מותנים (`08_Decision-Making/` & `12_Rules/`):**
  * `[[Rule-Collagen-Cut-Moist-Heat]]` (`RUL-MEAT-001`) — התאמת חום לח לנתחים ושרירים לא-שלדיים עתירי קולגן
  * `[[Rule-Poultry-Safe-Core-Temperature]]` (`RUL-SAF-001`) — אימות טמפרטורת ליבה במדחום וחריג חליטה-וטחינה
  * `[[Rule-Tender-Vs-Tough-Cut-Thermal-Strategy]]` (`RUL-MEAT-002`) — מטריצת בחירת אסטרטגיה תרמית לנתחים רכים מול קשים
  * `[[Rule-Whole-Bird-Breast-Vs-Leg-Thermal-Solutions]]` (`RUL-MEAT-003`) — פתרון דילמת העוף השלם והשגת עור פריך
  * `[[Rule-Pre-Cooking-Tenderization-Brine-Marinade-Enzymes]]` (`RUL-MEAT-004`) — בחירה בין תמלחת, מרינדה ואנזימי פירות
  * `[[Rule-Freezing-Ice-Water-Thawing-And-WOF-Prevention]]` (`RUL-MEAT-005`) — פרוטוקול הקפאה ב-PVDC, הפשרה במים ומניעת Warmed-Over Flavor
* **10. פערי ידע ואי-ודאויות (`10_Knowledge-Gaps/`):**
  * `[[Collagen-Time-Curve-By-Animal-Age]]` (`GAP-PROT-001`) — שונות זמן פירוק הקולגן לפי גיל בעל החיים
  * `[[Meat-Science-And-Cooking-Documented-Unknowns]]` (`GAP-MEAT-002`) — פיגמנט האבץ בפרושוטו די פארמה ללא ניטריט, קולגן במיקרוגל ומנגנון "אפקט הבשר" בספיגת ברזל

---

## 11. אינדקס רשומות חילוץ ספרות: *On Food and Cooking* (McGee 2004) — Chapter 4: Fish and Shellfish
מקור מאומת: `[[SRC-MCGEE-2004]]` (עמודים מודפסים 179–242 | עמודי PDF 193–256):

* **01. חומרי גלם (`01_Ingredients/`):**
  * `[[Finfish-Muscle-Myotomes-Fat-And-Pigments]]` (`ING-FISH-001`) — יריעות מיוטומים (`Myotomes`), קולגן `Myocommata` הנמס ב-50–55°C, תכולת שומן, אסטרי שעווה באסקולר ופיגמנט אסטקסנטין בסלמון
  * `[[Crustaceans-Hepatopancreas-Molting-And-Astaxanthin]]` (`ING-FISH-002`) — סרטנאים (שרימפס, לובסטר, סרטן), פרוטאזות בלוטת הכבד-לבלב (`Hepatopancreas / Tomalley`), מחזור הנשל ופיגמנט האסטקסנטין
  * `[[Molluscs-Bivalves-Cephalopods-And-Roe-Caviar]]` (`ING-FISH-003`) — רכיכות דו-קשוותיות (שריר `Quick` מול `Catch`), ראשי-רגליים ואבאלון (סיבי 0.004 מ"מ ופי 3–5 קולגן מצולב), קיפודי ים (`Uni`) וביצי דגים/קוויאר (`Transglutaminase`)
* **02. מדע המזון (`02_Food-Science/`):**
  * `[[Fish-Thermal-Progression-Proteases-And-Sarcoplasmic-Glue]]` (`SCI-FISH-001`) — טבלת המעברים התרמיים בדגים (20–90°C), שיא פעילות הפרוטאזות ב-55–60°C במינים מועדים להתפוררות, ודבק חלבוני הסרקופלזמה ב-55°C+ בטונה ודג חרב
  * `[[Osmoregulation-TMAO-TMA-Spoilage-And-Acid-Neutralization]]` (`SCI-FISH-002`) — אוסמורגולציה בים (חומצות אמינו חופשיות, `TMAO` ואוריאה), הפיכת `TMAO` ל-`TMA` ריחני, ונטרול כימי בחומצה (פרוטונציה, הידרציה של אלדהידים ופירוק גאוסמין)
  * `[[Fish-Rigor-Mortis-Icing-And-Freeze-Denaturation]]` (`SCI-FISH-003`) — צפידת מוות בדגים, איסור פילוט לפני צפידה ללא בישול מיידי, הכפלת חיי מדף בקרח ב-0°C מול מקרר ב-5°C, ויצירת `DMA` ופורמלדהיד בדגי קוד קפואים
  * `[[Seafood-Curing-Fermentation-Surimi-And-Katsuobushi]]` (`SCI-FISH-004`) — מוסלין, קנלים וסורימי (`Surimi`), לוטפיסק בסיסי ב-pH 12 (`Lutefisk`), קוד מלוח, הרינג מאטיאס (`Pyloric caecum`), רוטב דגים אוטוליטי, עישון דגים וייצור קצואובושי (`Katsuobushi` ודאשי)
* **03. טכניקות בישול (`03_Techniques/`):**
  * `[[Gentle-Simmering-Poaching]]` (`TEC-MOIST-001`) — שליקה עדינה (מועשר בדגים, קור-בויון, ציר דגים ובויאבז)
  * `[[High-Heat-Pan-Searing]]` (`TEC-DRY-001`) — צריבה בחום גבוה (מועשר בעור דג פריך, טמפורה וחריצה)
  * `[[Sous-Vide-Precision-Cooking]]` (`TEC-PREC-001`) — בישול מדויק (מועשר בסו-וויד דגים ב-47–55°C ומגבלת הפרוטאזות)
  * `[[Fish-Dry-Heat-Baking-Tempura-And-En-Papillote]]` (`TEC-FISH-001`) — המלחה מוקדמת (3–5%), אפייה איטית (95–110°C) מול מהירה (260°C), מעטפת `En Papillote`, עור פריך ונוסחת טמפורה יפנית במי קרח
  * `[[Fish-Poaching-Fumet-Bouillabaisse-And-Steaming]]` (`TEC-FISH-002`) — שליקה במים ושמן, קור-בויון, ציר דגים (`Fumet` $\le 60$ דק'), אמולסיית הרתיחה העזה בבויאבז ואידוי ב-80°C/65–70°C
  * `[[Raw-Fish-Ceviche-Sushi-Poke-And-Live-Shellfish]]` (`TEC-FISH-003`) — סושי/סשימי, דנטורציה חומצית בסביצ'ה, פוקה, הרדמת סרטנים במי קרח מלוחים, ניקוי חול מצדפות ב-20 g/L מלח ואחסון אויסטרים קעורים כלפי מטה
  * `[[Conflict-Fish-Slow-Cooking-Cephalopod-Dual-Window-And-Shells]]` (`CNF-FISH-001`) — יישוב 3 מחלוקות: בישול איטי מול פרוטאזות ב-55–60°C, חלון הרכות הדו-קוטבי של דיונון/תמנון/אבאלון, ומיתוס המולים/צדפות הסגורים לאחר הבישול
* **04. טעמים וארומות (`04_Flavors/`):**
  * `[[Seafood-Flavor-Chemistry-Amino-Acids-DMS-And-Bromophenols]]` (`FLV-FISH-001`) — גליצין מתוק, גלוטמט, `IMP`, חומצה סוקצינית, ליפאוקסיגנאז, ברומופנולים ימיים, גאוסמין בוצי ודימתיל סולפיד (`DMS` המשותף לצדפות, חלב מחומם ותירס)
* **05. מרקמים (`05_Textures/`):**
  * `[[Fish-Flaking-Gelatin-Melting-Point-And-Bivalve-Muscles]]` (`TEX-FISH-001`) — התפרקות לעלעלים ב-50–55°C, נקודת ההתכה הנמוכה של ג'לטין דגים (25°C מול 30°C בבקר), דלדול רבייה (`Sloppy cod`), `Gaping` ופוליפוספטים בסקאלופ
* **06. ציוד וסביבה (`06_Equipment/`):**
  * `[[Fish-Slush-Icing-Enclosures-And-Cookware-Control]]` (`EQP-FISH-001`) — מערכת קרח כתוש מתנקז ב-0°C, מרית דגים ורשתות גריל, מגש מתכת לוהט וקרש ארז, מעטפות אדים ומיגון קרינה ברדיד אלומיניום
* **07. בטיחות מזון (`07_Food-Safety/`):**
  * `[[Seafood-Toxins-Scombroid-Parasites-And-Freezing-Rules]]` (`SAF-FISH-001`) — הרעלת היסטמין (`Scombroid`), 5 רעלני האצות העמידים לחום (`Ciguatera, PSP, DSP, ASP, NSP`), כספית מול `PCBs`, חיידקי *Vibrio* ובוטוליזם זן E, ופרוטוקול הקפאת ה-FDA להשמדת טפילים (*Anisakis* ותולעי סרט)
* **08. קבלת החלטות וכללים מותנים (`08_Decision-Making/`):**
  * `[[Rule-Fish-Target-Temperature-And-Protease-Management]]` (`RUL-FISH-001`) — התאמת טמפרטורת היעד וקצב החימום לסוג הדג, לדבק הסרקופלזמה ולפרוטאזות השריר
  * `[[Rule-Cephalopod-Abalone-And-Bivalve-Thermal-Windows]]` (`RUL-FISH-002`) — חלונות החום הדו-קוטביים של דיונון/תמנון/אבאלון וכללי הטיפול והבישול של צדפות, מולים, אויסטרים וסקאלופ
  * `[[Rule-Fish-Odor-Control-Storage-And-Stock-Extraction]]` (`RUL-FISH-003`) — אחסון ב-0°C, איסור פילוט לפני צפידה, נטרול ריחות `TMA`/גאוסמין בחומצה, ומיצוי ציר דגים ($\le 60$ דק') מול בויאבז (רתיחה של 10 דק')
  * `[[Rule-Raw-Seafood-Parasite-Freezing-And-Toxin-Screening]]` (`RUL-FISH-004`) — השמדת טפילים בהקפאה לדגים נאים (`-35°C` ל-15 ש' או `-20°C` ל-7 ימים), מניעת היסטמין וסינון רעלנים לאוכלוסיות בסיכון
* **10. פערי ידע ואי-ודאויות (`10_Knowledge-Gaps/`):**
  * `[[Fish-And-Shellfish-Documented-Unknowns]]` (`GAP-FISH-001`) — שונות בלתי-צפויה ברמת הפרוטאזות בפילה בודד, היעדר בדיקת מטבח לסיגואטרה/רעלני אצות, ושחזור טעם דגי פרא בחקלאות ימית
