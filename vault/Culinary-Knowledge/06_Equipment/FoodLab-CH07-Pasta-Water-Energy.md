---
id: EVD-FLB-CH07-001
type: EVIDENCE_RECORD
name: רתיחה, הספק ונפח מים לפסטה
domain: EQUIPMENT
knowledge_type: SCIENTIFIC_PRINCIPLE
claim_id: CLM-FLB-CH07-001
claim_type: SOURCE_SUPPORTED_CLAIM
claim: המחבר מנתח מאזן אנרגיה בשני נפחי מים רותחים על מבערים זהים, ומפריד בין חימום, איבוד חום ואנרגיית אידוי.
canonical_concept_id: SCI-HEAT-001
verification_status: PRELIMINARY
source_text_checked: true
scientific_validation: NOT_INDEPENDENTLY_VALIDATED
confidence:
  source_traceability: HIGH
  generalizability: CONDITIONAL
  score_is_probability: false
conditions:
- המודל מניח תנאים מסוימים; מים רותחים אינם מבטיחים טמפרטורה זהה בכל גובה.
sources:
- source_id: SRC-FOODLAB-2015
  book_title: 'The Food Lab: Better Home Cooking Through Science'
  author: J. Kenji López-Alt
  edition: First Edition
  year: 2015
  chapter: 7 Tomato Sauce, Macaroni, and the Science of Pasta
  epub_sha256: 9457a6e8f889baf3740e5e82bd136089c5ce255225d77eeb8069f11a12510a54
  internal_path: text/part0334.html
  paragraph_index: 13
  paragraph_selector: body descendant p; 1-based; includes empty p; itertext joined with a space then stripped
  paragraph_sha256: c9d9d5176b95dde5dae57431b675eb2ba5e4b4985b26eb025d8d91183c4ed130
  anchor_status: UNKNOWN
  pdf_page: UNKNOWN
  printed_page: UNKNOWN
relationships:
- type: SUPPORTED_BY
  target_id: SRC-FOODLAB-2015
  target_name: '[[SRC-FOODLAB-2015]]'
  evidence: CLM-FLB-CH07-001
  confidence: HIGH_FOR_SOURCE_ATTRIBUTION
- type: SUPPORTS
  target_id: SCI-HEAT-001
  target_name: '[[Heat-Transfer]]'
  conditions: המודל מניח תנאים מסוימים; מים רותחים אינם מבטיחים טמפרטורה זהה בכל גובה.
  confidence: CONDITIONAL_INTERPRETIVE_MAPPING
---

# רתיחה, הספק ונפח מים לפסטה

המחבר מנתח מאזן אנרגיה בשני נפחי מים רותחים על מבערים זהים, ומפריד בין חימום, איבוד חום ואנרגיית אידוי.

תנאים ומגבלות: המודל מניח תנאים מסוימים; מים רותחים אינם מבטיחים טמפרטורה זהה בכל גובה.

הטענה נתמכת בפסקה שצוינה בספר; היא אינה אימות מדעי חיצוני. שיוך הטענה למושג הקיים [[Heat-Transfer]] הוא מיפוי פרשני.

מקור: [[SRC-FOODLAB-2015]], 7 Tomato Sauce, Macaroni, and the Science of Pasta, `text/part0334.html`, פסקה 13. אין מספר עמוד PDF או עמוד מודפס זמין בעותק זה.

למפת הפרק: [[FoodLab-2015-Chapter-07]].
