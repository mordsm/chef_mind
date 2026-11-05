---
id: TEC-MEAT-002
type: COOKING_TECHNIQUE
name: "צליית עוף שלם (דילמת החזה מול השוק) ופרוטוקול עור פריך (Whole-Bird Roasting & Crisp Poultry Skin)"
domain: TECHNIQUES
heat_environment: "DRY"
heat_transfer_methods:
  - "CONVECTION"
  - "RADIATION"
  - "CONDUCTION"
recommended_equipment:
  - "תבנית צלייה שטוחה עם רשת (Roasting Rack) ומדחום ליבה"
target_foods:
  - "תרנגולת שלמה, הודו שלם, ברווז ואווז"
conditions:
  surface_temperature_min_c: 190
  cooking_medium: "AIR"
  duration_range: "45-180 minutes (until breast reaches 68-74°C and thigh reaches 75-77°C)"
effects:
  primary_outcome: "השוואת קצב החימום בין החזה הרזה לבין הכרעיים עתירות הקולגן תוך המסת קולגן העור ואיוד המים ליצירת עור פריך"
  texture_change: "CRISP_GLASSY_SKIN / JUICY_BREAST_AND_TENDER_THIGH"
  moisture_loss_pct_estimate: 15.0
exceptions:
  - "משיחת העור בנוזלים מימיים (Basting במרק/יין) בדקות הסיום מרככת את העור ופוגעת בפריכות"
  - "עופות שצוננו במים (Water-chilled) סופגים 5%-12% מים ומתקשים להגיע לעור פריך ללא ייבוש מוקדם במקרר"
relationships:
  - type: AFFECTS
    target_id: "ING-POUL-001"
    target_name: "[[Poultry-Breast-Lean]]"
  - type: AFFECTS
    target_id: "SCI-MEAT-002"
    target_name: "[[Rigor-Mortis-DFD-Meat-And-Aging-Enzymes]]"
  - type: AFFECTS
    target_id: "SCI-MEAT-003"
    target_name: "[[Brining-Marinades-And-Protease-Tenderizers]]"
  - type: ENABLES
    target_id: "RUL-MEAT-003"
    target_name: "[[Rule-Whole-Bird-Breast-Vs-Leg-Thermal-Solutions]]"
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
    printed_pages: "pp. 143, 159-160 (Box on p. 160)"
    pdf_pages: "pp. 157, 173-174 (Box on p. 174)"
    claim_type: "DIRECT_SOURCE_CLAIM"
verification_status: VERIFIED
---

# צליית עוף שלם (דילמת החזה מול השוק) ופרוטוקול עור פריך (Whole-Bird Roasting & Crisp Poultry Skin)

## 1. דילמת העוף השלם: פער של 10°C בין החזה לבין הכרעיים (`DIRECT_SOURCE_CLAIM`, עמ' 159–160 / PDF 173–174)
בעופות קרקע (תרנגולת והודו), צליית העוף בשלמותו מציבה בעיה תרמית מובנית משום שהחזה והרגליים בנויים משני סוגי שריר מנוגדים (`[[Poultry-Breast-Lean]]`, `[[Muscle-Fiber-Types-And-Myoglobin-Chemistry]]`):
* **החזה (`Breast` — 90% סיבים לבנים, דל שומן וקולגן):** מגיע לשיא העסיסיות והרכות סביב **65°C–68°C (150°F–155°F)**; מעבר לכך סיבי האקטין מתכווצים והחזה הופך יבש, חולי וסיבי.
* **השוק והירך (`Leg & Thigh` — סיבים אדומים עובדים, עשירים בשומן, מיוגלובין ורקמת חיבור):** בטמפרטורה של 68°C הם עדיין צמיגיים, ורודים סביב המפרקים ובעלי מרקם גומי; הם דורשים חימום ל-**73°C–77°C (165°F–170°F)** כדי להמיס את הקולגן לג'לטין ולהקריש את המיוגלובין.

### 5 פתרונות הנדסיים וקולינריים לדילמת העוף השלם (`DIRECT_SOURCE_CLAIM`, עמ' 159–160 / PDF 173–174; `[[Rule-Whole-Bird-Breast-Vs-Leg-Thermal-Solutions]]`):
1. **קירור מוקדם של החזה בקרח (`Ice-Packing the Breast`):** הנחת שקית קרח כתוש על חזה העוף/ההודו למשך **שעה אחת לפני הכניסה לתנור** (בזמן שהכרעיים מתחממות לטמפרטורת החדר). החזה מתחיל את הצלייה בטמפרטורה נמוכה ב-10°C–15°C מהכרעיים, ולכן שני החלקים מגיעים לטמפרטורת היעד שלהם בו-זמנית!
2. **מיסוך קרינת החום מהחזה (`Foil Shielding / Breast-Down Start`):** כיסוי החזה ברדיד אלומיניום בחצי הראשון של הצלייה (המחזיר קרינת אינפרא-אדום; `[[Radiant-Grilling-Smoking-And-Packaging-Permeability]]`) או התחלת הצלייה כשהחזה פונה כלפי מטה והפיכתו רק להשחמת הסיום.
3. **השריה בתמלחת (`Brining` של 3%–6% מלח, עמ' 155, 160 / PDF 169, 174):** תמלחת חותכת בחצי את איבוד הנוזלים בחזה (`[[Brining-Marinades-And-Protease-Tenderizers]]`) ומעניקה מרווח ביטחון גם אם החזה מגיע ל-74°C.
4. **הגנה בשומן תת-עורי (`Barding / Butter Under Skin`):** החדרת חמאה או שומן מתחת לעור החזה להאטת חדירת החום ושימון הסיבים הרזים.
5. **הפרדת חלקים או פריסת פרפר (`Separate Cooking / Spatchcocking`):** פירוק החזה והכרעיים לצלייה בזמנים שונים, או הוצאת עמוד השדרה ושיטוח העוף כך שהירכיים חשופות לחום מלא מכל הכיוונים.

---

## 2. המדע של עור עוף וברווז פריך (`Box: Keys to Crisp Poultry Skin`, עמ' 160 / PDF 174)
עור עוף חי מורכב מכ-**50% מים**, רשת צפופה של **סיבי קולגן** ושכבת **שומן תת-עורי**. אם אופים עוף בחום מתון בלבד, המים מתאדים לאט והקולגן מתייבש ליריעה דמוית קלף או גומי קשה (*Parchment / Leathery*). כדי להפוך את העור לפריך ושביר ("זכוכיתי") נדרשים שני תהליכים במקביל (`DIRECT_SOURCE_CLAIM`, עמ' 160 / PDF 174):
1. **המסת חלק מהקולגן בעור לג'לטין** (כדי להחליש את היריעה הסיבית).
2. **הרתחה ואיוד מהיר של המים בעור בחום גבוה (200°C–230°C / 400°F–450°F)** תוך טיגון העור בשומן המותך של עצמו, מה שיוצר בועות מיקרוסקופיות פריכות ומשחים אותן בתגובת מייאר.

### פרוטוקול 5 הצעדים לעור פריך מושלם (עמ' 143, 160 / PDF 157, 174):
* **צעד 1 — בחירת עוף שצונן באוויר או עוף כשר (`Air-Chilled or Kosher Poultry`):** עופות שצוננו במים (*Water-chilled*) ספגו **5%–12% מים** עודפים הפוגעים בפריכות (`[[Rigor-Mortis-DFD-Meat-And-Aging-Enzymes]]`). עוף שצונן באוויר או עבר המלחה כשרה מתחיל עם עור יבש בהרבה.
* **צעד 2 — ייבוש מוקדם באוויר המקרר (`Uncovered Air-Drying`):** השארת העוף **ללא כיסוי במקרר למשך 24 עד 48 שעות** לפני הצלייה כדי לאדות לחות חיצונית מהעור.
* **צעד 3 — הפרדת העור וניקוב שומן בעופות שמנים (ברווז/אווז):** בברווז ואווז, חליטת העוף במים רותחים ל-60 שניות מכווצת ומהדקת את העור, ודקירת העור במחט בזווית שטוחה (ללא פציעת הבשר) מאפשרת לשומן התת-עורי העודף להינתך ולהתנקז החוצה.
* **צעד 4 — שימון פני העור (`Oiling the Skin`):** מריחת העור בשכבה דקה של שמן או חמאה מומסת משפרת את הולכת החום אל העור כבר מדקות הצלייה הראשונות.
* **צעד 5 — הימנעות מהרטבת העור בסיום (`No Watery Basting at the End`):** אין לצקת נוזלי תבנית מימיים על העור בחלק האחרון של הצלייה, ואין לכסות את העוף בנייר אלומיניום לאחר היציאה מהתנור (האדים ירככו מיד את העור הפריך).

