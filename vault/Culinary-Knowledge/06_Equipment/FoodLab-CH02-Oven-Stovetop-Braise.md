---
id: EVD-FLB-CH02-003
type: EVIDENCE_RECORD
name: סיר בתנור לעומת חימום מתחתית
domain: EQUIPMENT
knowledge_type: EQUIPMENT_PROPERTY
claim_id: CLM-FLB-CH02-003
claim_type: SOURCE_SUPPORTED_CLAIM
claim: הספר משווה חימום מקומי מלמטה בכיריים לחימום מכמה כיוונים בתנור מבוקר תרמוסטט, ומעדיף תנור לתבשילים סמיכים
  וארוכים להפחתת חריכת תחתית.
canonical_concept_id: EQP-ENV-001
verification_status: PRELIMINARY
source_text_checked: true
scientific_validation: NOT_INDEPENDENTLY_VALIDATED
confidence:
  source_traceability: HIGH
  generalizability: CONDITIONAL
  score_is_probability: false
conditions:
- אין להסיק שכל תנור אחיד או שכל גודל סיר מתבשל באותו קצב בפועל.
sources:
- source_id: SRC-FOODLAB-2015
  book_title: 'The Food Lab: Better Home Cooking Through Science'
  author: J. Kenji López-Alt
  edition: First Edition
  year: 2015
  chapter: 2 Soups, Stews, and the Science of Stock
  epub_sha256: 9457a6e8f889baf3740e5e82bd136089c5ce255225d77eeb8069f11a12510a54
  internal_path: text/part0115.html
  paragraph_index: 20
  paragraph_selector: body descendant p; 1-based; includes empty p; itertext joined with a space then stripped
  paragraph_sha256: d27b7baac02c56e0cbaeaa29c0ec153e13503de078fd28dea392d6297263c893
  anchor_status: UNKNOWN
  pdf_page: UNKNOWN
  printed_page: UNKNOWN
relationships:
- type: SUPPORTED_BY
  target_id: SRC-FOODLAB-2015
  target_name: '[[SRC-FOODLAB-2015]]'
  evidence: CLM-FLB-CH02-003
  confidence: HIGH_FOR_SOURCE_ATTRIBUTION
- type: SUPPORTS
  target_id: EQP-ENV-001
  target_name: '[[Covered-Vs-Uncovered-Evaporation]]'
  conditions: אין להסיק שכל תנור אחיד או שכל גודל סיר מתבשל באותו קצב בפועל.
  confidence: CONDITIONAL_INTERPRETIVE_MAPPING
---

# סיר בתנור לעומת חימום מתחתית

הספר משווה חימום מקומי מלמטה בכיריים לחימום מכמה כיוונים בתנור מבוקר תרמוסטט, ומעדיף תנור לתבשילים סמיכים וארוכים להפחתת חריכת תחתית.

תנאים ומגבלות: אין להסיק שכל תנור אחיד או שכל גודל סיר מתבשל באותו קצב בפועל.

הטענה נתמכת בפסקה שצוינה בספר; היא אינה אימות מדעי חיצוני. שיוך הטענה למושג הקיים [[Covered-Vs-Uncovered-Evaporation]] הוא מיפוי פרשני.

מקור: [[SRC-FOODLAB-2015]], 2 Soups, Stews, and the Science of Stock, `text/part0115.html`, פסקה 20. אין מספר עמוד PDF או עמוד מודפס זמין בעותק זה.

למפת הפרק: [[FoodLab-2015-Chapter-02]].
