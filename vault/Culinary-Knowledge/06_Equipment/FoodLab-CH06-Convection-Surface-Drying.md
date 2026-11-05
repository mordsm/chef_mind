---
id: EVD-FLB-CH06-002
type: EVIDENCE_RECORD
name: מאוורר תנור וייבוש פני שטח
domain: EQUIPMENT
knowledge_type: EQUIPMENT_PROPERTY
claim_id: CLM-FLB-CH06-002
claim_type: SOURCE_SUPPORTED_CLAIM
claim: המחבר מתאר זרימת אוויר מאולצת המספקת חום ומסלקת לחות מפני המזון, ולכן עשויה להאיץ בישול והשחמה.
canonical_concept_id: SCI-HEAT-001
verification_status: PRELIMINARY
source_text_checked: true
scientific_validation: NOT_INDEPENDENTLY_VALIDATED
confidence:
  source_traceability: HIGH
  generalizability: CONDITIONAL
  score_is_probability: false
conditions:
- תנור ביתי אינו בהכרח אחיד; יש לעקוב אחר ההשחמה ולא להניח המרת זמן קבועה.
sources:
- source_id: SRC-FOODLAB-2015
  book_title: 'The Food Lab: Better Home Cooking Through Science'
  author: J. Kenji López-Alt
  edition: First Edition
  year: 2015
  chapter: 6 Chickens, Turkeys, Prime Rib, and the Science of Roasts
  epub_sha256: 9457a6e8f889baf3740e5e82bd136089c5ce255225d77eeb8069f11a12510a54
  internal_path: text/part0285.html
  paragraph_index: 9
  paragraph_selector: body descendant p; 1-based; includes empty p; itertext joined with a space then stripped
  paragraph_sha256: 197e3ccc4542cb7bdad8829e0b17a1d63c3b4672cbecb3203d6322bb1ce45daa
  anchor_status: UNKNOWN
  pdf_page: UNKNOWN
  printed_page: UNKNOWN
relationships:
- type: SUPPORTED_BY
  target_id: SRC-FOODLAB-2015
  target_name: '[[SRC-FOODLAB-2015]]'
  evidence: CLM-FLB-CH06-002
  confidence: HIGH_FOR_SOURCE_ATTRIBUTION
- type: SUPPORTS
  target_id: SCI-HEAT-001
  target_name: '[[Heat-Transfer]]'
  conditions: תנור ביתי אינו בהכרח אחיד; יש לעקוב אחר ההשחמה ולא להניח המרת זמן קבועה.
  confidence: CONDITIONAL_INTERPRETIVE_MAPPING
---

# מאוורר תנור וייבוש פני שטח

המחבר מתאר זרימת אוויר מאולצת המספקת חום ומסלקת לחות מפני המזון, ולכן עשויה להאיץ בישול והשחמה.

תנאים ומגבלות: תנור ביתי אינו בהכרח אחיד; יש לעקוב אחר ההשחמה ולא להניח המרת זמן קבועה.

הטענה נתמכת בפסקה שצוינה בספר; היא אינה אימות מדעי חיצוני. שיוך הטענה למושג הקיים [[Heat-Transfer]] הוא מיפוי פרשני.

מקור: [[SRC-FOODLAB-2015]], 6 Chickens, Turkeys, Prime Rib, and the Science of Roasts, `text/part0285.html`, פסקה 9. אין מספר עמוד PDF או עמוד מודפס זמין בעותק זה.

למפת הפרק: [[FoodLab-2015-Chapter-06]].
