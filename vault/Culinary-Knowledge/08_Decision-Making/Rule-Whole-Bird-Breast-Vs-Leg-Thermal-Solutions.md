---
id: RUL-MEAT-003
type: CULINARY_RULE
name: "פתרון דילמת העוף השלם (חזה ב-65-68°C מול כרעיים ב-75-77°C) והשגת עור פריך (Whole-Bird Breast vs. Leg Solutions)"
domain: DECISION_MAKING
rule_scope: "THERMAL_GRADIENT_AND_TEXTURE_CONTROL"
trigger_conditions:
  food_class: "POULTRY"
  observed_problem: "צליית עוף או הודו שלם שבה החזה הרזה מתייבש לפני שהכרעיים מתרככות, או עור שנותר רך וגומי"
  cooking_phase: "PREPARATION_AND_ROASTING"
recommended_action:
  action_code: "APPLY_DIFFERENTIAL_HEAT_AND_SKIN_DRYING"
  parameters:
    breast_target_temp_c: "68_TO_74C"
    leg_thigh_target_temp_c: "75_TO_77C"
    pre_roast_breast_ice_pack_min: 60
    fridge_air_dry_hours: "24_TO_48"
  explanation: "האט את חימום החזה ביחס לכרעיים (באמצעות קירור החזה בקרח לשעה לפני הצלייה, מיסוך אלומיניום או השריה בתמלחת 3%-6%), וייבש את העור ללא כיסוי במקרר 24-48 שעות לפני צלייה בחום גבוה."
legitimate_methods_and_tradeoffs:
  - method: "קירור מוקדם של החזה בשקית קרח לשעה לפני הצלייה (Ice-Packing the Breast — עמ' 160)"
    advantages: "מוריד את טמפרטורת הפתיחה של החזה ב-10-15°C לעומת הכרעיים כך ששניהם מגיעים לטמפרטורת היעד יחד ללא פירוק העוף"
    tradeoffs: "דורש הכנה של שעה מראש לפני הכניסה לתנור"
  - method: "השריה בתמלחת 3%-6% מלח וייבוש באוויר המקרר (Brining + Uncovered Air-Drying — עמ' 155, 160)"
    advantages: "חותך ב-50% את איבוד הנוזלים בחזה ומעניק מרווח ביטחון תרמי רחב"
    tradeoffs: "תמלחת מרטיבה את העור ולכן מחייבת ייבוש חוזר של 24 שעות במקרר להשגת עור פריך"
  - method: "מיסוך החזה ברדיד אלומיניום או פירוק ובישול נפרד (Foil Shielding / Separate Cooking — עמ' 159-160)"
    advantages: "שליטה מוחלטת ומדויקת בטמפרטורת החזה והכרעיים בנפרד"
    tradeoffs: "מוותר על הגשת עוף שלם לשולחן (בפירוק) או מעכב מעט את השחמת העור (במיסוך)"
expected_effects:
  moisture_retention: "JUICY_BREAST_AND_COLLAGEN_MELTED_LEGS"
  reaction_rate: "SKIN_COLLAGEN_HYDROLYSIS_AND_WATER_VAPORIZATION"
scientific_rationale: "חזה עוף מורכב מ-90% סיבים לבנים דלי שומן וקולגן המתייבשים מעל 68°C, בעוד הכרעיים עשירות בקולגן ומיוגלובין הדורשים 75-77°C; עור עוף מכיל 50% מים וקולגן הדורשים ייבוש וחום גבוה (200-230°C) לפריכות (McGee 2004, pp. 134, 143, 159-160)."
confidence: 96
verified_on: "2026-10-21"
exceptions:
  - "בברווז ואווז החזה מורכב מ-80% סיבים אדומים (עמ' 134) ונאכל במיטבו במדיום-רייר (55-60°C), ולכן בהם פירוק החזה והכרעיים לצלייה נפרדת עדיף עוד יותר"
relationships:
  - type: SUPPORTED_BY
    target_id: "TEC-MEAT-002"
    target_name: "[[Whole-Bird-Roasting-And-Crisp-Poultry-Skin]]"
  - type: SUPPORTED_BY
    target_id: "ING-POUL-001"
    target_name: "[[Poultry-Breast-Lean]]"
  - type: SUPPORTED_BY
    target_id: "ING-MEAT-002"
    target_name: "[[Muscle-Fiber-Types-And-Myoglobin-Chemistry]]"
  - type: SUPPORTED_BY
    target_id: "EQP-MEAT-001"
    target_name: "[[Radiant-Grilling-Smoking-And-Packaging-Permeability]]"
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
    printed_pages: "pp. 134, 143, 159-160"
    pdf_pages: "pp. 148, 157, 173-174"
    claim_type: "DIRECT_SOURCE_CLAIM"
verification_status: VERIFIED
---

# כלל החלטה: פתרון דילמת העוף השלם והשגת עור פריך (`RUL-MEAT-003`)

## 1. הצהרת הכלל המותנה (`IF / THEN / BECAUSE / EXCEPTIONS`)
* **אם (`IF`):** צולים עוף או הודו שלם ורוצים למנוע את התייבשות החזה בזמן שהכרעיים והירכיים מתבשלות, ובו-זמנית להשיג עור פריך ושחום,
* **אז (`THEN`):**
  1. **ניהול תרמי דיפרנציאלי:** יש להאט את קצב החימום של החזה ביחס לכרעיים באמצעות **קירור החזה בשקית קרח למשך שעה לפני הצלייה**, מיסוך החזה ברדיד אלומיניום בחלק מהזמן, או הגנה על החזה באמצעות **תמלחת (3%–6% מלח)**, כך שהחזה יסיים סביב **68°C–74°C** בזמן שהירכיים מגיעות ל-**75°C–77°C**.
  2. **פרוטוקול עור פריך:** יש לבחור עוף שצונן באוויר (`Air-chilled`) או הומלח בהכשרה (לא `Water-chilled` שספג 5%–12% מים), לייבש אותו **ללא כיסוי במקרר למשך 24–48 שעות**, למשוח את העור בשמן/שומן, לצלות בחום גבוה (**200°C–230°C**) בשלב הסיום ולהימנע מהרטבת העור בנוזלים מימיים בדקות האחרונות (`[[Whole-Bird-Roasting-And-Crisp-Poultry-Skin]]`).
* **משום ש (`BECAUSE`):** חזה עוף והודו בנוי מ-**90% סיבים לבנים** דלי שומן וקולגן המתייבשים מעל 68°C (`[[Poultry-Breast-Lean]]`), בעוד שרירי הרגליים עשירים בקולגן הדורש 75°C–77°C כדי להתמוסס לג'לטין; ועור עוף מכיל **50% מים** וקולגן ההופכים ליריעת גומי אם המים אינם מתאדים במהירות בחום גבוה (`[[SRC-MCGEE-2004]]`, עמ' 134, 143, 159–160 / PDF 148, 157, 173–174).
* **חריגים (`EXCEPTIONS`):**
  * **ברווז ויונה (`Duck & Squab`, עמ' 134 / PDF 148):** שריר החזה שלהם בנוי מ-**80%–85% סיבים אדומים** עתירי מיוגלובין ושומן, ולכן חזה ברווז ניצלה לדרגת **מדיום-רייר (55°C–58°C)** בעוד רגלי הברווז דורשות בישול ארוך ל-85°C — בברווז הפרדת החזה מהרגליים (או צליית החזה והוצאתו מוקדם) היא הפתרון המיטבי.

