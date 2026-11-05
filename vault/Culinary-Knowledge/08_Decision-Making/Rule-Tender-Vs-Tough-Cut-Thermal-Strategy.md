---
id: RUL-MEAT-002
type: CULINARY_RULE
name: "מטריצת בחירת אסטרטגיה תרמית: נתחים רכים דלי-קולגן מול נתחים עובדים עתירי-קולגן (Tender vs. Tough Cut Thermal Strategy)"
domain: DECISION_MAKING
rule_scope: "TECHNIQUE_AND_TEMPERATURE_SELECTION"
trigger_conditions:
  food_class: "MEAT"
  observed_problem: "בחירת שיטת בישול, טמפרטורת יעד ומשך בישול לפי אנטומיית הנתח ותכולת הקולגן"
  cooking_phase: "PLANNING_AND_EXECUTION"
recommended_action:
  action_code: "MATCH_CUT_COLLAGEN_TO_THERMAL_REGIME"
  parameters:
    tender_cut_target_temp_c: "52_TO_60C_BEEF_LAMB_OR_65_68C_POULTRY_BREAST"
    tough_cut_target_temp_c: "80_TO_90C_HOLD_UNTIL_COLLAGEN_HYDROLYZED"
    braise_cooling_target_c: 50
  explanation: "בנתחים רכים (מותן/פילה/חזה) עצור ב-52-60°C (או 65-68°C בעוף) לפני התכווצות הקולגן והאקטין; בנתחים עתירי קולגן (כתף/שוק/קורקבן) בשל בלחות ב-80-90°C לאורך שעות וקרר בנוזל ל-50°C."
legitimate_methods_and_tradeoffs:
  - method: "צריבה והיפוך תכוף כל 60 שניות (Frequent-Flip Pan Searing — לסטייקים והמבורגרים)"
    advantages: "בישול מהיר בעד 30%, שכבה אפורה מינימלית מתחת לקרום והשחמת מייאר אחידה (עמ' 156)"
    tradeoffs: "דורש תשומת לב רציפה ליד המחבת"
  - method: "צלייה דו-שלבית הפוכה (Low-to-High / Reverse Sear — לנתחי צלי וסטייקים עבים)"
    advantages: "פנים הנתח מתחמם באחידות (40-50°C מזרז אנזימי יישון), פני השטח מתייבשים מראש ולכן משחימים מהר מאוד בסיום עם מינימום Carryover (עמ' 156, 158)"
    tradeoffs: "משך הכנה כולל ארוך יותר מצריבה ישירה"
  - method: "צלי קדרה דו-שלבי וקירור בנוזל ל-50°C (Two-Stage Braise + Liquid Cooling — לנתחים עתירי קולגן)"
    advantages: "מנצל ריכוך אנזימטי ב-40-50°C, ממיס קולגן ב-80°C ללא רתיחה מייבשת, ומחזיר עסיסיות ג'לטינית בקירור ל-50°C (עמ' 162-163)"
    tradeoffs: "דורש 2.5 עד 4 שעות כולל שלב הקירור בנוזל"
expected_effects:
  moisture_retention: "MAXIMIZED_PHASE_1_OR_PHASE_2_JUICINESS"
  reaction_rate: "CONTROLLED_PROTEIN_DENATURATION"
scientific_rationale: "מיוצין נקרש ב-50-55°C (שיא עסיסיות שלב 1), קולגן מתכווץ וסוחט מיצים ב-60°C ואקטין נדחס ב-66-80°C; רק מעל 70-80°C לאורך זמן הקולגן מתמוסס לג'לטין המעניק עסיסיות שלב 2 (McGee 2004, pp. 147-163)."
confidence: 98
verified_on: "2026-10-21"
exceptions:
  - "נתח עשיר בקולגן שנפרס דק מאוד נגד הסיבים (למוקפץ) או נטחן לבשר טחון מתנהג כנתח רך ודורש בישול קצר"
  - "כבד (Liver) הוא איבר פנימי דל קולגן ולכן חלים עליו כללי נתח רך (בישול קצר בלבד, עמ' 166)"
relationships:
  - type: SUPPORTED_BY
    target_id: "SCI-MEAT-001"
    target_name: "[[Meat-Thermal-Progression-And-Doneness-Spectrum]]"
  - type: SUPPORTED_BY
    target_id: "TEC-MEAT-001"
    target_name: "[[Two-Stage-Roasting-Flipping-And-Heat-Scaling]]"
  - type: SUPPORTED_BY
    target_id: "TEC-MEAT-003"
    target_name: "[[Succulent-Braising-Stewing-And-Liquid-Cooling]]"
  - type: SUPPORTED_BY
    target_id: "TEX-MEAT-001"
    target_name: "[[Two-Phase-Juiciness-And-Fiber-Compaction]]"
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
    printed_pages: "pp. 147-163"
    pdf_pages: "pp. 161-177"
    claim_type: "DIRECT_SOURCE_CLAIM"
verification_status: VERIFIED
---

# כלל החלטה: מטריצת בחירת אסטרטגיה תרמית — נתחים רכים מול נתחים עתירי קולגן (`RUL-MEAT-002`)

## 1. הצהרת הכלל המותנה (`IF / THEN / BECAUSE / EXCEPTIONS`)
* **אם (`IF`):** מתכננים בישול של נתח בשר או עוף ונדרשת התאמה בין מבנה הנתח לבין משטר הטמפרטורה והזמן:
  * **מקרה א' (נתח רך דל קולגן — פילה, סינטה, אנטרקוט, צלעות טלה/חזיר, חזה עוף/ברווז, כבד):**
    * **אז (`THEN`):** יש לבשל לתוצאת ליבה של **52°C–60°C (125°F–140°F)** בבקר/טלה/ברווז (או **65°C–68°C** בחזה עוף/חזיר, בכפוף לסף הבטיחות), תוך שימוש בהיפוך תכוף או בצלייה דו-שלבית (`[[Two-Stage-Roasting-Flipping-And-Heat-Scaling]]`) והוצאה מהחום **3°C–10°C לפני טמפרטורת היעד** לטובת בישול שאריתי במנוחה (`[[Resting-Carryover-Cooking-And-Carving]]`).
  * **מקרה ב' (נתח עובד עשיר בקולגן — כתף, שוק, חזה בקר/בריסקט, צוואר, זנב, קורקבנים, לב, לשון, קיבה):**
    * **אז (`THEN`):** יש לבשל בסביבה לחה ומכוסה (`[[Succulent-Braising-Stewing-And-Liquid-Cooling]]`) בטמפרטורת בשר פנימית מבוקרת של **80°C–90°C (180°F–195°F)** לאורך שעות עד להמסת הקולגן לג'לטין, ולצנן את הבשר **בתוך נוזל הבישול עד 50°C (120°F)** לפני הגשה.
* **משום ש (`BECAUSE`):** בנתחים דלי קולגן העסיסיות נשענת על המים התוך-תאיים (שלב 1 של עסיסיות; `[[Two-Phase-Juiciness-And-Fiber-Compaction]]`) הנסחטים החוצה כאשר הקולגן מתכווץ ב-**60°C** והאקטין נקרש ב-**66°C–80°C**; לעומת זאת בנתחים עתירי קולגן חובה לעבור את שלב ההתכווצות ולהמיס את הקולגן לג'לטין (שלב 2 של עסיסיות) ב-**80°C–90°C** (`[[Meat-Thermal-Progression-And-Doneness-Spectrum]]`, `[[SRC-MCGEE-2004]]`, עמ' 148–163 / PDF 162–177).
* **חריגים (`EXCEPTIONS`):**
  1. **פריסה דקיקה נגד הסיבים או טחינה:** נתח קשה שנפרס דק מאוד בניצב לסיבים (למוקפץ) או נטחן להמבורגר עבר קיצור מכני של הסיבים ולכן מתבשל כנתח רך ומהיר (עמ' 154 / PDF 168).
  2. **חוק קנה-המידה התרמי (`Thickness Squared`):** אין לחשב זמן צלייה לפי "דקות לקילוגרם" — הכפלת עובי הנתח מאריכה את זמן הבישול **פי 4 ($L^2$)**, והכפלת משקל של נתח בעל צורה דומה מאריכה את הזמן ב-**~60% בלבד ($W^{2/3}$)** (עמ' 159 / PDF 173).

