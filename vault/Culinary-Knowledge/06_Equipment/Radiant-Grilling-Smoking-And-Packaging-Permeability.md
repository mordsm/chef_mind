---
id: EQP-MEAT-001
type: EQUIPMENT
name: "גריל קורן (1100°C), כימיית עישון עץ וחדירות חמצן בניילון נצמד (Radiant Grilling, Smoking & Packaging Permeability)"
domain: EQUIPMENT
equipment_type: "HEAT_SOURCE_AND_STORAGE_MATERIALS"
material: "Glowing Charcoal / Wood Smoke / Polyethylene (PE) vs. Polyvinylidene Chloride (PVDC)"
thermal_properties:
  heat_capacity: "HIGH"
  conductivity: "HIGH_RADIANT_FLUX"
  max_safe_temp_c: 1100
best_for:
  - "השחמת מייאר מהירה בקרינת אינפרא-אדום (גריל וגריל עליון / Broiler)"
  - "עישון עץ בטמפרטורה נמוכה ליצירת טבעת עשן (Smoke Ring) ושימור נוגד חמצון"
  - "בחירת חומר אריזה מתאים למקרר (PE חדיר לחמצן) מול הקפאה ארוכה (PVDC / ואקום / אלומיניום אטומים)"
limitations:
  - "טפטוף שומן על גחלים לוהטות ב-1100°C יוצר עשן עשיר ב-PAHs מסרטנים — דורש צלייה עקיפה או מגש טפטוף"
  - "ניילון נצמד רגיל (Polyethylene) חדיר לחמצן ולאדי מים וגורם לכוויות קור (Freezer Burn) ולחמצון שומן בהקפאה"
relationships:
  - type: AFFECTS
    target_id: "ING-MEAT-002"
    target_name: "[[Muscle-Fiber-Types-And-Myoglobin-Chemistry]]"
  - type: AFFECTS
    target_id: "TEC-MEAT-002"
    target_name: "[[Whole-Bird-Roasting-And-Crisp-Poultry-Skin]]"
  - type: AFFECTS
    target_id: "SAF-MEAT-001"
    target_name: "[[Meat-Pathogens-Blanch-Grinding-And-Carcinogens]]"
  - type: ENABLES
    target_id: "RUL-MEAT-005"
    target_name: "[[Rule-Freezing-Ice-Water-Thawing-And-WOF-Prevention]]"
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
    printed_pages: "pp. 145-147, 156-160, 164"
    pdf_pages: "pp. 159-161, 170-174, 178"
    claim_type: "DIRECT_SOURCE_CLAIM"
verification_status: VERIFIED
---

# גריל קורן (1100°C), כימיית עישון עץ וחדירות חמצן בניילון נצמד (Radiant Grilling, Smoking & Packaging Permeability)

## 1. פיזיקת גריל וגריל עליון (`Grilling & Broiling`) וקרינת אינפרא-אדום (`DIRECT_SOURCE_CLAIM`, עמ' 156–157 / PDF 170–171)
בניגוד לתנור אפייה המעביר חום בעיקר באמצעות **הסעת אוויר חם (`Convection`)** איטית יחסית, גריל פחמים או גוף חימום עליון לוהט (*Broiler*) פועלים באמצעות **קרינה תרמית ישירה (`Infrared Radiation`)**:
* **טמפרטורת המקור הקורן (`DIRECT_SOURCE_CLAIM`, עמ' 156 / PDF 170):** גחלים לוחשות, להבות גז וגופי חימום חשמליים מגיעים לטמפרטורות של כ-**1,100°C (2,000°F)** ומשגרים שטף אדיר של קרינת אינפרא-אדום המאדה מים מפני הבשר ומשחימה אותו בתוך שניות עד דקות.
* **חוק המרחק והבקרה הדו-אזורית (`Two-Zone Fire`):** עוצמת הקרינה יורדת בחדות עם הגדלת המרחק מהגחלים. לנתחים עבים נדרשת מערכת דו-אזורית: אזור קרינה ישירה ועזה לצריבת פני השטח, ואזור חום עקיף (*Indirect Heat*) להשלמת בישול הליבה ללא שריפת החוץ וללא טפטוף שומן על הגחלים היוצר `PAHs` (`[[Meat-Pathogens-Blanch-Grinding-And-Carcinogens]]`).
* **מיסוך קרינה באמצעות רדיד אלומיניום מבריק (`Foil Radiation Shielding`, עמ' 160 / PDF 174):**
  * באוויר התנור או הגריל, משטח אלומיניום מבריק **מחזיר קרינת אינפרא-אדום** ומאט ב-30%–50% את קצב החימום של אזורים רגישים (כגון חזה עוף שלם או קצות עצמות; `[[Whole-Bird-Roasting-And-Crisp-Poultry-Skin]]`).

---

## 2. כימיית עישון עץ ויצירת "טבעת העשן" הוורודה (`Wood Smoke & Smoke Ring`, עמ' 149, 164 / PDF 163, 178)
בעת שריפה איטית של עץ קשה (אלון, היקורי, עצי פרי) בטמפרטורות של 300°C–400°C, פולימרי העץ (**תאית/צלולוז, המיצלולוז וליגנין**) מתפרקים לעשן המכיל מאות תרכובות פעילות (`DIRECT_SOURCE_CLAIM`, עמ' 164 / PDF 178):
1. **פנולים ארומטיים (`Phenols` — כגון *Guaiacol* ו-*Syringol* מליגנין):** מעניקים את ארומת העשן הקלאסית, ופועלים כ**נוגדי חמצון חזקים** וכ**קוטלי חיידקים** על פני שטח הבשר.
2. **חומצה אצטית וקרבונילים (`Acetic Acid & Carbonyls` מתאית):** מורידים את ה-pH של פני השטח ומשתתפים בתגובות השחמה ליצירת מעטפת ה-*Bark* הכהה בברביקיו.
3. **גזי תחמוצת החנקן ($\text{NO}$) ופחמן חד-חמצני ($\text{CO}$) — מנגנון "טבעת העשן" (`Smoke Ring`, עמ' 149, 164 / PDF 163, 178):**
   * בעירת עץ ופחמים מייצרת גזי $\text{NO}$ ו-$\text{CO}$ החודרים בדיפוזיה לעומק של **5–10 מ"מ** לתוך הבשר החי (כל עוד פני הבשר לחים וקרים מ-60°C) ונקשרים לאטום הברזל במיוגלובין (`[[Muscle-Fiber-Types-And-Myoglobin-Chemistry]]`). הקומפלקס הנוצר נשאר **ורוד בוהק גם לאחר 12 שעות עישון ב-90°C**!

---

## 3. פיזיקת חומרי עטיפה והפשרה: מדוע ניילון נצמד רגיל כושל בהקפאה? (`Packaging Permeability & Thawing Physics`, עמ' 145–147 / PDF 159–161)
מקג'י חושף הבדל קריטי בין סוגי סרטי הפלסטיק המשמשים לאריזת בשר (`DIRECT_SOURCE_CLAIM`, עמ' 145–147 / PDF 159–161):

| סוג חומר האריזה | חדירות לחמצן ($\text{O}_2$) ולאדי מים | שימוש נכון במטבח (`[[Rule-Freezing-Ice-Water-Thawing-And-WOF-Prevention]]`) |
| :--- | :--- | :--- |
| **ניילון פוליאתילן רגיל (`Polyethylene — PE` / ניילון מגשי סופרמרקט)** | **חדיר מאוד לחמצן** (נבחר בכוונה על ידי קצביות וסופרמרקטים כדי שחמצן יחדור וישמור על צבע `Oxymyoglobin` אדום בוהק בדלפק!) | מתאים לכיסוי קצר של **1–2 ימים במקרר בלבד**. **אסור להקפאה ארוכה** — החמצן והיובש חודרים דרכו וגורמים ל**כוויות קור (`Freezer Burn`)** ולעיפוש השומן |
| **ס (PVDC / `Saran`), שקיות ואקום ורדיד אלומיניום עבה** | **אטומים כמעט לחלוטין לחמצן ולאדי מים** | **חובה להקפאת בשר** ולאחסון ממושך; מונעים המראה (Sublimation) של גבישי קרח מפני הבשר ומונעים חמצון שומנים |

* **פיזיקת ההפשרה באמבט מי קרח: מהירה פי 20 מאוויר (`Ice-Water Thawing`, עמ' 147 / PDF 161):**
  * **מים מוליכים חום ביעילות גבוהה פי 20 מאוויר** (`[[Heat-Transfer]]`). לכן טבילת בשר קפוא (ארוז בשקית אטומה למים) בתוך **קערת מים קרים או מי קרח** מפשירה את הבשר בשבריר מהזמן שלוקחת הפשרה באוויר המקרר, ובו-זמנית מונעת מפני השטח להתחמם לטווח הסכנה החיידקי (כפי שקורה בהפשרה על השיש או במיקרוגל; עמ' 147 / PDF 161).
  * **בישול בשר קפוא ללא הפשרה (עמ' 147 / PDF 161):** בנתחים בעובי בינוני (או צלי) ניתן לבשל ישירות ממצב קפוא בחום מתון יותר תוך **הארכת זמן הבישול ב-30% עד 50%**.

