---
id: TEC-MEAT-003
type: COOKING_TECHNIQUE
name: "כללי הזהב לצלי קדרה עסיסי, קירור בנוזל הבישול ופירוק לסיבים (Succulent Braising, Stewing & Liquid Cooling)"
domain: TECHNIQUES
heat_environment: "COMBINATION"
heat_transfer_methods:
  - "CONDUCTION"
  - "CONVECTION"
recommended_equipment:
  - "סיר קדרה כבד עם מכסה אטום (Dutch Oven) ותנור מבוקר"
target_foods:
  - "נתחי כתף, שוק, אוסובוקו, לחי בקר, זנב שור, קורקבנים, לב ולשון"
conditions:
  surface_temperature_min_c: 80
  cooking_medium: "WATER"
  duration_range: "120-240 minutes cooking + cooling in liquid to 50°C"
effects:
  primary_outcome: "המסת קולגן לג'לטין ב-80°C ללא רתיחה מייבשת, וספיגה חוזרת של נוזלי הג'לטין לתוך הנתח בעת קירורו בנוזל ל-50°C"
  texture_change: "SUCCULENT_GELATINOUS_FORK_TENDER"
  moisture_loss_pct_estimate: 15.0
exceptions:
  - "רתיחה חזקה (100°C) מכווצת את הסיבים בחוזקה ומונעת ספיגה יעילה של הג'לטין"
  - "צמצום הרוטב ברתיחה חייב להתבצע רק לאחר הוצאת הבשר מהסיר"
relationships:
  - type: REQUIRES
    target_id: "SCI-PROT-001"
    target_name: "[[Collagen-Hydrolysis-Gelatin]]"
  - type: AFFECTS
    target_id: "TEC-COMB-001"
    target_name: "[[Low-Slow-Braising]]"
  - type: AFFECTS
    target_id: "SCI-MEAT-001"
    target_name: "[[Meat-Thermal-Progression-And-Doneness-Spectrum]]"
  - type: AFFECTS
    target_id: "TEX-MEAT-001"
    target_name: "[[Two-Phase-Juiciness-And-Fiber-Compaction]]"
  - type: ENABLES
    target_id: "RUL-MEAT-001"
    target_name: "[[Rule-Collagen-Cut-Moist-Heat]]"
  - type: SUPPORTED_BY
    target_id: "SRC-MCGEE-2004"
    target_name: "[[SRC-MCGEE-2004]]"
sources:
  - source_id: "SRC-MCGEE-2004"
    citation: "McGee, On Food and Cooking (2nd Ed., 2004), Chapter 3: Meat"
    book_title: "On Food and Cooking: The Science and Lore of the Kitchen"
    author: "Harold McGee"
    edition: "2nd Edition (Completely Revised and Updated)"
    publication_year: 2004
    chapter: "Chapter 3: Meat"
    printed_pages: "pp. 161-163"
    pdf_pages: "pp. 175-177"
    claim_type: "DIRECT_SOURCE_CLAIM"
verification_status: VERIFIED
---

# כללי הזהב לצלי קדרה עסיסי, קירור בנוזל הבישול ופירוק לסיבים (Succulent Braising, Stewing & Liquid Cooling)

## 1. הפרדוקס של צלי קדרה ונזיד: מדוע בשר מבושל בנוזל עלול לצאת יבש? (`DIRECT_SOURCE_CLAIM`, עמ' 161–162 / PDF 175–176)
טבחים רבים מופתעים לגלות שנתח בקר שהתבשל כשהוא שקוע לחלוטין בנוזל יצא יבש וסיבי. מקג'י מסביר את הסיבה המולקולרית (`[[Meat-Thermal-Progression-And-Doneness-Spectrum]]`):
* מעל **60°C–80°C**, חלבוני המיוצין והאקטין בתוך תאי השריר מתכווצים וסוחטים החוצה את המים הפנימיים של התא — **גם כאשר הבשר מוקף במים רותחים**! סיבי השריר המכווצים אינם יכולים לספוג מים כל עוד הם חמים מאוד.
* תחושת העסיסיות והנימוחות בבישול קדרה (`[[Low-Slow-Braising]]`) נובעת מ**ג'לטין מומס וטיפות שומן** הממלאים את החללים ש**בין** סיבי השריר ומצפים את הפה (`[[Two-Phase-Juiciness-And-Fiber-Compaction]]`).

---

## 2. ששת כללי הזהב של מקג'י לצלי קדרה ונזיד עסיסיים (`DIRECT_SOURCE_CLAIM`, עמ' 162–163 / PDF 176–177)

1. **חלופה חכמה להשחמה ראשונית אגרסיבית (עמ' 162 / PDF 176):**
   * צריבה עמוקה של קוביות הבשר לפני הבישול מפתחת טעמי מייאר, אך **מייבשת ומקשה לצמיתות את השכבה החיצונית של הבשר**.
   * **חלופה לגיטימית:** להשחים היטב ירקות ארומטיים, רסק עגבניות או עצמות/קצוות שומן בבסיס הסיר (או לצפות את הבשר במעט קמח שישחים מהר מבלי לייבש את סיבי השריר עצמם).
2. **חימום דו-שלבי לניצול אנזימי היישון (`Two-Stage Braising Temperature`, עמ' 162 / PDF 176):**
   * התחילו את צלי הקדרה בתנור נמוך של **95°C–120°C (200°F–250°F)** למשך שעה–שעתיים כדי שהבשר ישהה בטווח **40°C–50°C** ויזכה לריכוך אנזימטי מואץ של `Calpains` ו-`Cathepsins` (`[[Rigor-Mortis-DFD-Meat-And-Aging-Enzymes]]`).
   * לאחר מכן העלו את חום התנור ל-**150°C–160°C (300°F–325°F)** כך שטמפרטורת הבשר והנוזל תתייצב סביב **80°C–85°C (180°F–185°F)** — טמפרטורה שבה הקולגן מתפרק לג'לטין מבלי שסיבי השריר יתכווצו בעוצמת הרתיחה של 100°C.
3. **עצירת הבישול ברגע השגת רכות מזלג (עמ' 162–163 / PDF 176–177):**
   * המשך בישול לאחר שהקולגן התמוסס גורם לג'לטין המומס לדלוף החוצה מבין הסיבים אל תוך הנוזל ומשאיר את הבשר עצמו יבש ומתפורר.
4. **קירור הבשר בתוך נוזל הבישול ל-50°C (`Cool Meat in the Cooking Liquid`, עמ' 163 / PDF 177):**
   * **כלל קריטי:** בסיום הבישול אסור להוציא את הבשר החם מהנוזל מיד! יש לכבות את האש ולהניח לבשר להתקרר **בתוך נוזל הצלייה** עד שטמפרטורתו יורדת ל-**50°C (120°F)** או לקררו בנוזל למשך לילה במקרר. ככל שהטמפרטורה יורדת והג'לטין מסמיך, החללים בין הסיבים מתרחבים קלות ו**שואבים חזרה פנימה כמות גדולה של נוזל ג'לטיני עשיר**.
5. **הוצאת הבשר לפני צמצום הרוטב ברתיחה (עמ' 163 / PDF 177):**
   * אם רוצים לצמצם ולהסמיך את נוזל הבישול ברתיחה, חובה **להוציא תחילה את הבשר מהסיר**, לצמצם את הרוטב בנפרד, ולהחזיר את הבשר לרוטב רק לחימום עדין.
6. **הצלה ושדרוג באמצעות פירוק לסיבים וערבוב ברוטב סמיך (`Shredding & Coating`, עמ' 163, 165 / PDF 177, 179):**
   * פירוק בשר צלי קדרה מבושל לסיבים או פריסתו וערבובו בנוזלי הבישול שהוסמכו בג'לטין ושומן מכפיל במאות אחוזים את שטח הפנים של הבשר התופס רוטב עשיר בכל ביס (`[[Two-Phase-Juiciness-And-Fiber-Compaction]]`).

