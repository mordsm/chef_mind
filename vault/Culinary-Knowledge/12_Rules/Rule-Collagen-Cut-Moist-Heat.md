---
id: RUL-MEAT-001
type: CULINARY_RULE
name: "התאמת חום לח לנתחים עתירי קולגן (Collagen-Rich Cut Moist Heat Rule)"
domain: RULES
rule_scope: "TECHNIQUE_CHOICE"
trigger_conditions:
  food_class: "MEAT"
  observed_problem: "הנתח זוהה כעשיר ברקמת חיבור ומתאים לבישול לח"
  cooking_phase: "PREPARATION"
recommended_action:
  action_code: "SELECT_MOIST_SLOW_COOKING"
  parameters:
    heat_adjustment: "SIMMER_80_90C"
    liquid_addition_ml: 250
    cover_vessel: true
  explanation: "אמת את שם הנתח ובחר בישול ממושך בנוזל (צלי קדרה בטמפרטורת ליבה ~80°C/180°F, בישול בסיר מכוסה או סיר לחץ) לפירוק הקולגן לג'לטין, וקירור בתוך הנוזל עד 50°C לספיגה חוזרת."
expected_effects:
  moisture_retention: "INCREASED"
  reaction_rate: "COLLAGEN_HYDROLYSIS_ENABLED"
scientific_rationale: "שרירים עובדים כמו כתף, שוק וקורקבנים עשירים בקולגן הדורש חום לח וזמן להידרוליזה לג'לטין רך (McGee 2004, pp. 130-131, 162-163)."
observations:
  - "בדוק ודווח על שינוי ברכות הנתח; רכות לבדה אינה בדיקת בטיחות"
safety_notes:
  - "יש לאמת טמפרטורת ליבה בטוחה במדחום לפי סוג הבשר (74°C בעוף/קורקבנים, 63°C עם מנוחה בנתח בקר שלם)"
tags:
  - "קולגן"
  - "רקמת חיבור"
  - "ריכוך"
  - "קורקבנים"
  - "כתף"
  - "collagen"
  - "braise"
confidence: 95
verified_on: "2026-10-21"
exceptions:
  - "אלסטין (רצועות לבנות/צהובות כגון Silverskin) אינו מתפרק בבישול לח ויש להסירו בסכין או לטחון מכנית (McGee p. 131)"
  - "כבד (Liver) הוא איבר פנימי דל מאוד בקולגן ולכן בישול ארוך מייבש ומקשה אותו במקום לרככו (McGee p. 166)"
relationships:
  - type: SUPPORTED_BY
    target_id: "SCI-PROT-001"
    target_name: "[[Collagen-Hydrolysis-Gelatin]]"
  - type: SUPPORTED_BY
    target_id: "TEC-MEAT-003"
    target_name: "[[Succulent-Braising-Stewing-And-Liquid-Cooling]]"
  - type: SUPPORTED_BY
    target_id: "SRC-BCCAMPUS-MEAT-2015"
    target_name: "[[SRC-BCCAMPUS-MEAT-2015]]"
  - type: SUPPORTED_BY
    target_id: "SRC-MCGEE-2004"
    target_name: "[[SRC-MCGEE-2004]]"
sources:
  - source_id: "SRC-BCCAMPUS-MEAT-2015"
    citation: "BCcampus, Meat Cutting and Processing for Food Service, 2015"
  - source_id: "SRC-MCGEE-2004"
    citation: "McGee, On Food and Cooking (2nd Ed., 2004), Chapter 3: Meat"
    book_title: "On Food and Cooking: The Science and Lore of the Kitchen"
    author: "Harold McGee"
    edition: "2nd Edition (Completely Revised and Updated)"
    publication_year: 2004
    chapter: "Chapter 3: Meat"
    printed_pages: "pp. 130-131, 150-154, 162-163"
    pdf_pages: "pp. 144-145, 164-168, 176-177"
    claim_type: "DIRECT_SOURCE_CLAIM"
verification_status: VERIFIED
---

# כלל החלטה: התאמת חום לח לנתחים עתירי קולגן (`RUL-MEAT-001`)

## הצהרת הכלל המותנה (Conditional Rule Statement — `IF / THEN / BECAUSE / EXCEPTIONS`)
* **אם (`IF`):** חומר הגלם הוא שריר עובד עשיר בקולגן (`[[Beef-Chuck-Collagen-Rich]]`, כתף, שוק, צוואר, חזה/בריסקט, זנב, או שרירים לא-שלדיים כגון קורקבנים, לב ולשון; `[[Offal-Organs-And-Animal-Fat-Saturation]]`),
* **אז (`THEN`):** יש לבחור בישול ממושך ומבוקר בנוזל או באדים (`[[Low-Slow-Braising]]`, `[[Succulent-Braising-Stewing-And-Liquid-Cooling]]`) תוך שמירה על טמפרטורת בשר פנימית סביב **80°C (180°F)** (בעבוע תת-רתיחתי שקט, לעולם לא רתיחה סוערת), ולקרר את הבשר בתוך נוזל הבישול ל-**50°C (120°F)** לפני הגשה או צמצום הרוטב,
* **משום ש (`BECAUSE`):** מעטפות הקולגן מתכווצות ב-60°C ודורשות חימום ממושך בנוכחות מים מעל **60°C–70°C** (ובקצב מיטבי ב-**80°C–90°C**) כדי לעבור הידרוליזה לג'לטין מסיס המפצה על התייבשות סיבי השריר (`[[Collagen-Hydrolysis-Gelatin]]`, `[[SRC-MCGEE-2004]]`, עמ' 150–152, 162–163 / PDF 164–166, 176–177),
* **חריגים (`EXCEPTIONS`):**
  1. **אלסטין (`Elastin`):** רצועות גידים ואלסטין (כגון *Silverskin*) אינן מתפרקות בחום לח וחובה להסירן בסכין או לטחון אותן מכנית (עמ' 131 / PDF 145).
  2. **חיתוך דק או טחינה מכנית:** אם נתח עשיר בקולגן נפרס לפרוסות דקיקות מאוד נגד הסיבים (למשל למוקפץ אסייתי) או נטחן לבשר טחון, הסיבים ורקמת החיבור קוצרו מכנית ולכן ניתן לבשלו בחום יבש ומהיר (עמ' 154 / PDF 168).
  3. **כבד (`Liver`):** בניגוד לקורקבנים, לב וקיבה, הכבד דל מאוד בקולגן ולכן חום ממושך מקשה ומייבש אותו (עמ' 166 / PDF 180).
