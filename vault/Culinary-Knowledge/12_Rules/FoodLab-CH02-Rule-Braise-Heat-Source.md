---
id: RUL-FLB-CH02-001
canonical_rule_id: RUL-MEAT-001
type: CULINARY_RULE
name: 'תבשיל סמיך: תנור או כיריים'
domain: RULES
verification_status: PRELIMINARY
claim_type: INTERPRETATION
if: אם תבשיל סמיך נדרש לחימום ממושך
then: אפשר להשתמש בתנור עם סיר מתאים, או בכיריים עם בקרה וערבוב לפי הצורך
because: המקור מבחין בחימום תחתית מקומי לעומת חימום מכמה כיוונים
exceptions:
- יש לוודא התאמת הסיר והמכסה לתנור; אין להסיק זמן בישול זהה
tradeoffs: תנור מפחית צורך בבקרת תחתית אך דורש כלי מתאים; כיריים נגישות לבדיקה אך מחייבות מעקב
source_claim_ids:
- CLM-FLB-CH02-003
sources:
- source_id: SRC-FOODLAB-2015
  edition: First Edition
  chapter: 2 Soups, Stews, and the Science of Stock
  internal_path: text/part0115.html
  paragraph_index: 20
  paragraph_selector: body descendant p; 1-based; includes empty p; itertext joined with a space then stripped
  paragraph_sha256: d27b7baac02c56e0cbaeaa29c0ec153e13503de078fd28dea392d6297263c893
  anchor_status: UNKNOWN
  pdf_page: UNKNOWN
  printed_page: UNKNOWN
  book_title: 'The Food Lab: Better Home Cooking Through Science'
  author: J. Kenji López-Alt
  year: 2015
  knowledge_type: CONDITIONAL_RULE_INTERPRETATION
relationships:
- type: SUPPORTED_BY
  target_id: EVD-FLB-CH02-003
  target_name: '[[FoodLab-CH02-Oven-Stovetop-Braise]]'
  confidence: CONDITIONAL
  evidence: CLM-FLB-CH02-003
- type: SUPPORTED_BY
  target_id: EQP-ENV-001
  target_name: '[[Covered-Vs-Uncovered-Evaporation]]'
  conditions: השוואת בחירות בתוך ההקשר בלבד; אינה סתירה גורפת
  confidence: INTERPRETIVE
---

# תבשיל סמיך: תנור או כיריים

**IF:** אם תבשיל סמיך נדרש לחימום ממושך

**THEN:** אפשר להשתמש בתנור עם סיר מתאים, או בכיריים עם בקרה וערבוב לפי הצורך

**BECAUSE:** המקור מבחין בחימום תחתית מקומי לעומת חימום מכמה כיוונים

**EXCEPTIONS:** יש לוודא התאמת הסיר והמכסה לתנור; אין להסיק זמן בישול זהה

פשרות וחלופות: תנור מפחית צורך בבקרת תחתית אך דורש כלי מתאים; כיריים נגישות לבדיקה אך מחייבות מעקב

כלל פרשני, ולא ציטוט או פרוטוקול מלא מהספר. ביסוס: [[FoodLab-CH02-Oven-Stovetop-Braise]]. המושג הקיים נשמר: [[Covered-Vs-Uncovered-Evaporation]]. אין הפעלה אוטומטית במנוע השף.
