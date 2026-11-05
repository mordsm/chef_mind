---
id: EVD-FLB-CH01-001
type: EVIDENCE_RECORD
name: חלמון כמקור לחומר מתחלב
domain: INGREDIENTS
knowledge_type: INGREDIENT_PROPERTY
claim_id: CLM-FLB-CH01-001
claim_type: SOURCE_SUPPORTED_CLAIM
claim: המחבר מתאר חלמון כמערכת המכילה מים, חלבונים ושומן, ובה לציטין המסייע לשילוב השומן במים.
canonical_concept_id: ING-EGG-003
verification_status: PRELIMINARY
source_text_checked: true
scientific_validation: NOT_INDEPENDENTLY_VALIDATED
confidence:
  source_traceability: HIGH
  generalizability: CONDITIONAL
  score_is_probability: false
conditions:
- אין להסיק מכאן יחס שמן קבוע לכל רוטב.
sources:
- source_id: SRC-FOODLAB-2015
  book_title: 'The Food Lab: Better Home Cooking Through Science'
  author: J. Kenji López-Alt
  edition: First Edition
  year: 2015
  chapter: 1 Eggs, Dairy, and the Science of Breakfast
  epub_sha256: 9457a6e8f889baf3740e5e82bd136089c5ce255225d77eeb8069f11a12510a54
  internal_path: text/part0018.html
  paragraph_index: 11
  paragraph_selector: body descendant p; 1-based; includes empty p; itertext joined with a space then stripped
  paragraph_sha256: 3743488fe0e42cb19acd8e2802cf2f412f34c2941c6546e64604a57f121425cf
  anchor_status: UNKNOWN
  pdf_page: UNKNOWN
  printed_page: UNKNOWN
relationships:
- type: SUPPORTED_BY
  target_id: SRC-FOODLAB-2015
  target_name: '[[SRC-FOODLAB-2015]]'
  evidence: CLM-FLB-CH01-001
  confidence: HIGH_FOR_SOURCE_ATTRIBUTION
- type: SUPPORTS
  target_id: ING-EGG-003
  target_name: '[[Egg-Yolk-Lipoproteins-And-Amylase]]'
  conditions: אין להסיק מכאן יחס שמן קבוע לכל רוטב.
  confidence: CONDITIONAL_INTERPRETIVE_MAPPING
---

# חלמון כמקור לחומר מתחלב

המחבר מתאר חלמון כמערכת המכילה מים, חלבונים ושומן, ובה לציטין המסייע לשילוב השומן במים.

תנאים ומגבלות: אין להסיק מכאן יחס שמן קבוע לכל רוטב.

הטענה נתמכת בפסקה שצוינה בספר; היא אינה אימות מדעי חיצוני. שיוך הטענה למושג הקיים [[Egg-Yolk-Lipoproteins-And-Amylase]] הוא מיפוי פרשני.

מקור: [[SRC-FOODLAB-2015]], 1 Eggs, Dairy, and the Science of Breakfast, `text/part0018.html`, פסקה 11. אין מספר עמוד PDF או עמוד מודפס זמין בעותק זה.

למפת הפרק: [[FoodLab-2015-Chapter-01]].
