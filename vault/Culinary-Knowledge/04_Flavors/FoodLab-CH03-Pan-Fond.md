---
id: EVD-FLB-CH03-002
type: EVIDENCE_RECORD
name: משקעי השחמה כבסיס לרוטב
domain: FLAVORS
knowledge_type: CULINARY_PRINCIPLE
claim_id: CLM-FLB-CH03-002
claim_type: SOURCE_SUPPORTED_CLAIM
claim: הספר מזהה משקעי מיצי בשר שהתייבשו והשחימו במחבת כבסיס טעם לרוטב מחבת.
canonical_concept_id: SCI-CHEM-001
verification_status: PRELIMINARY
source_text_checked: true
scientific_validation: NOT_INDEPENDENTLY_VALIDATED
confidence:
  source_traceability: HIGH
  generalizability: CONDITIONAL
  score_is_probability: false
conditions:
- משקע שחום אינו שקול למשקע חרוך; לא כל מחבת מייצרת אותה כמות משקע.
sources:
- source_id: SRC-FOODLAB-2015
  book_title: 'The Food Lab: Better Home Cooking Through Science'
  author: J. Kenji López-Alt
  edition: First Edition
  year: 2015
  chapter: 3 Steaks, Chops, Chicken, Fish, and the Science of Fast-Cooking Foods
  epub_sha256: 9457a6e8f889baf3740e5e82bd136089c5ce255225d77eeb8069f11a12510a54
  internal_path: text/part0142.html
  paragraph_index: 5
  paragraph_selector: body descendant p; 1-based; includes empty p; itertext joined with a space then stripped
  paragraph_sha256: 1fa2d0c4820d72c58698a9c7cc7a70f565fc699dbf458db2b96abb12a00a9d28
  anchor_status: UNKNOWN
  pdf_page: UNKNOWN
  printed_page: UNKNOWN
relationships:
- type: SUPPORTED_BY
  target_id: SRC-FOODLAB-2015
  target_name: '[[SRC-FOODLAB-2015]]'
  evidence: CLM-FLB-CH03-002
  confidence: HIGH_FOR_SOURCE_ATTRIBUTION
- type: SUPPORTS
  target_id: SCI-CHEM-001
  target_name: '[[Maillard-Reaction]]'
  conditions: משקע שחום אינו שקול למשקע חרוך; לא כל מחבת מייצרת אותה כמות משקע.
  confidence: CONDITIONAL_INTERPRETIVE_MAPPING
---

# משקעי השחמה כבסיס לרוטב

הספר מזהה משקעי מיצי בשר שהתייבשו והשחימו במחבת כבסיס טעם לרוטב מחבת.

תנאים ומגבלות: משקע שחום אינו שקול למשקע חרוך; לא כל מחבת מייצרת אותה כמות משקע.

הטענה נתמכת בפסקה שצוינה בספר; היא אינה אימות מדעי חיצוני. שיוך הטענה למושג הקיים [[Maillard-Reaction]] הוא מיפוי פרשני.

מקור: [[SRC-FOODLAB-2015]], 3 Steaks, Chops, Chicken, Fish, and the Science of Fast-Cooking Foods, `text/part0142.html`, פסקה 5. אין מספר עמוד PDF או עמוד מודפס זמין בעותק זה.

למפת הפרק: [[FoodLab-2015-Chapter-03]].
