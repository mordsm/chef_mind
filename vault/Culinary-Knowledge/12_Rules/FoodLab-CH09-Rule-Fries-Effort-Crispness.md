---
id: RUL-FLB-CH09-001
canonical_rule_id: NEW_DRAFT_RULE
type: CULINARY_RULE
name: 'צ׳יפס: פשטות מול פריכות מרבית'
domain: RULES
verification_status: PRELIMINARY
claim_type: INTERPRETATION
if: אם בוחרים שיטת צ׳יפס בהתאם לזמן ולמרקם המבוקש
then: אפשר לבחור שיטה פשוטה או שיטה רב־שלבית עם חליטה וטיגון חוזר לפי מתכון מלא
because: המחבר מציג תוצאת פריכות שונה ופשרה במאמץ
exceptions:
- אין כאן פרוטוקול טיגון עצמאי; נדרשים מתכון מלא וציוד בטוח
tradeoffs: פחות שלבים חוסכים מאמץ; יותר שלבים מאפשרים שליטה במבנה ובפריכות
source_claim_ids:
- CLM-FLB-CH09-004
sources:
- source_id: SRC-FOODLAB-2015
  edition: First Edition
  chapter: 9 Batter, Breadings, and the Science of Frying
  internal_path: text/part0453.html
  paragraph_index: 23
  paragraph_selector: body descendant p; 1-based; includes empty p; itertext joined with a space then stripped
  paragraph_sha256: 3e281175b23160af1a4660773eead328d70c008b6b312b2370b94ed0a0ec3c32
  anchor_status: UNKNOWN
  pdf_page: UNKNOWN
  printed_page: UNKNOWN
  book_title: 'The Food Lab: Better Home Cooking Through Science'
  author: J. Kenji López-Alt
  year: 2015
  knowledge_type: CONDITIONAL_RULE_INTERPRETATION
relationships:
- type: SUPPORTED_BY
  target_id: EVD-FLB-CH09-004
  target_name: '[[FoodLab-CH09-Fries-Crispness-Tradeoff]]'
  confidence: CONDITIONAL
  evidence: CLM-FLB-CH09-004
- type: SUPPORTED_BY
  target_id: SCI-CARB-001
  target_name: '[[Starch-Gelatinization-Retrogradation]]'
  conditions: השוואת בחירות בתוך ההקשר בלבד; אינה סתירה גורפת
  confidence: INTERPRETIVE
---

# צ׳יפס: פשטות מול פריכות מרבית

**IF:** אם בוחרים שיטת צ׳יפס בהתאם לזמן ולמרקם המבוקש

**THEN:** אפשר לבחור שיטה פשוטה או שיטה רב־שלבית עם חליטה וטיגון חוזר לפי מתכון מלא

**BECAUSE:** המחבר מציג תוצאת פריכות שונה ופשרה במאמץ

**EXCEPTIONS:** אין כאן פרוטוקול טיגון עצמאי; נדרשים מתכון מלא וציוד בטוח

פשרות וחלופות: פחות שלבים חוסכים מאמץ; יותר שלבים מאפשרים שליטה במבנה ובפריכות

כלל פרשני, ולא ציטוט או פרוטוקול מלא מהספר. ביסוס: [[FoodLab-CH09-Fries-Crispness-Tradeoff]]. המושג הקיים נשמר: [[Starch-Gelatinization-Retrogradation]]. אין הפעלה אוטומטית במנוע השף.
