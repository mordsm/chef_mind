---
id: RUL-FLB-CH05-001
canonical_rule_id: NEW_DRAFT_RULE
type: CULINARY_RULE
name: 'בשר טחון: מבנה רך או מלוכד'
domain: RULES
verification_status: PRELIMINARY
claim_type: INTERPRETATION
if: אם מרקם הבשר הטחון הוא יעד ההכנה
then: להמבורגר רך צמצם לישה מיותרת; למוצר שמבנהו המלוכד רצוי אפשר לבחור עיבוד מכוון
because: המקור מתאר התהדקות עם טיפול עודף; ההרחבה למוצר מלוכד היא פרשנות קולינרית
exceptions:
- יש להפריד טחינה קרה ובטיחות מאפקט הלישה; אין כלל אחד לכל מתכון נקניק
tradeoffs: פחות עיבוד שומר פירור רך; עיבוד מכוון משפר אחידות אך עלול ליצור מרקם קפיצי
source_claim_ids:
- CLM-FLB-CH05-003
sources:
- source_id: SRC-FOODLAB-2015
  edition: First Edition
  chapter: 5 Balls, Loaves, Links, Burgers, and the Science of Ground Meat
  internal_path: text/part0271.html
  paragraph_index: 15
  paragraph_selector: body descendant p; 1-based; includes empty p; itertext joined with a space then stripped
  paragraph_sha256: 74fdb20c4c90549da2cf71ba1711c87709ef31423e739c0efcc5f041c42dc95a
  anchor_status: UNKNOWN
  pdf_page: UNKNOWN
  printed_page: UNKNOWN
  book_title: 'The Food Lab: Better Home Cooking Through Science'
  author: J. Kenji López-Alt
  year: 2015
  knowledge_type: CONDITIONAL_RULE_INTERPRETATION
relationships:
- type: SUPPORTED_BY
  target_id: EVD-FLB-CH05-003
  target_name: '[[FoodLab-CH05-Burger-Handling]]'
  confidence: CONDITIONAL
  evidence: CLM-FLB-CH05-003
- type: SUPPORTED_BY
  target_id: SCI-MEAT-004
  target_name: '[[Sausage-Emulsions-Myosin-And-Nitrite-Curing]]'
  conditions: השוואת בחירות בתוך ההקשר בלבד; אינה סתירה גורפת
  confidence: INTERPRETIVE
---

# בשר טחון: מבנה רך או מלוכד

**IF:** אם מרקם הבשר הטחון הוא יעד ההכנה

**THEN:** להמבורגר רך צמצם לישה מיותרת; למוצר שמבנהו המלוכד רצוי אפשר לבחור עיבוד מכוון

**BECAUSE:** המקור מתאר התהדקות עם טיפול עודף; ההרחבה למוצר מלוכד היא פרשנות קולינרית

**EXCEPTIONS:** יש להפריד טחינה קרה ובטיחות מאפקט הלישה; אין כלל אחד לכל מתכון נקניק

פשרות וחלופות: פחות עיבוד שומר פירור רך; עיבוד מכוון משפר אחידות אך עלול ליצור מרקם קפיצי

כלל פרשני, ולא ציטוט או פרוטוקול מלא מהספר. ביסוס: [[FoodLab-CH05-Burger-Handling]]. המושג הקיים נשמר: [[Sausage-Emulsions-Myosin-And-Nitrite-Curing]]. אין הפעלה אוטומטית במנוע השף.
