---
id: RUL-FLB-CH07-001
canonical_rule_id: NEW_DRAFT_RULE
type: CULINARY_RULE
name: 'פסטה אפויה: השריה או בישול מקדים'
domain: RULES
verification_status: PRELIMINARY
claim_type: INTERPRETATION
if: אם מכינים פסטה הממשיכה להתבשל ברוטב בתנור
then: אפשר להשתמש בהשריה מותאמת או בבישול מקדים מותאם, ולכוון נוזל ברוטב בהתאם
because: המקור מפריד ספיחת מים משלב הבישול בחום
exceptions:
- השריה אינה בישול מלא; תנאי זמן ושמירה חייבים להגיע מהמתכון המתאים
tradeoffs: השריה משנה תזמון וספיחת רוטב; בישול מקדים מוסיף שלב ועלול להביא לבישול יתר
source_claim_ids:
- CLM-FLB-CH07-003
sources:
- source_id: SRC-FOODLAB-2015
  edition: First Edition
  chapter: 7 Tomato Sauce, Macaroni, and the Science of Pasta
  internal_path: text/part0378.html
  paragraph_index: 6
  paragraph_selector: body descendant p; 1-based; includes empty p; itertext joined with a space then stripped
  paragraph_sha256: 81fe35c7480beda2fd79ef140cbf3d2fba8e48f99a6665d389332edcbdfad969
  anchor_status: UNKNOWN
  pdf_page: UNKNOWN
  printed_page: UNKNOWN
  book_title: 'The Food Lab: Better Home Cooking Through Science'
  author: J. Kenji López-Alt
  year: 2015
  knowledge_type: CONDITIONAL_RULE_INTERPRETATION
relationships:
- type: SUPPORTED_BY
  target_id: EVD-FLB-CH07-003
  target_name: '[[FoodLab-CH07-Pasta-Hydration-Separate]]'
  confidence: CONDITIONAL
  evidence: CLM-FLB-CH07-003
- type: SUPPORTED_BY
  target_id: SCI-CARB-001
  target_name: '[[Starch-Gelatinization-Retrogradation]]'
  conditions: השוואת בחירות בתוך ההקשר בלבד; אינה סתירה גורפת
  confidence: INTERPRETIVE
---

# פסטה אפויה: השריה או בישול מקדים

**IF:** אם מכינים פסטה הממשיכה להתבשל ברוטב בתנור

**THEN:** אפשר להשתמש בהשריה מותאמת או בבישול מקדים מותאם, ולכוון נוזל ברוטב בהתאם

**BECAUSE:** המקור מפריד ספיחת מים משלב הבישול בחום

**EXCEPTIONS:** השריה אינה בישול מלא; תנאי זמן ושמירה חייבים להגיע מהמתכון המתאים

פשרות וחלופות: השריה משנה תזמון וספיחת רוטב; בישול מקדים מוסיף שלב ועלול להביא לבישול יתר

כלל פרשני, ולא ציטוט או פרוטוקול מלא מהספר. ביסוס: [[FoodLab-CH07-Pasta-Hydration-Separate]]. המושג הקיים נשמר: [[Starch-Gelatinization-Retrogradation]]. אין הפעלה אוטומטית במנוע השף.
