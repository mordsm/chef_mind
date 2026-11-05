---
id: EVD-FLB-CH04-001
type: EVIDENCE_RECORD
name: נפח מים ותוצאת חליטת ירקות
domain: TECHNIQUES
knowledge_type: EMPIRICAL_OBSERVATION
claim_id: CLM-FLB-CH04-001
claim_type: SOURCE_SUPPORTED_CLAIM
claim: בניסוי המתואר בשעועית ירוקה, מעט מים איבדו יותר טמפרטורה לאחר הוספת הירק, ונצפו ריכוך איטי יותר וגוון פחות
  ירוק מאשר במנות מים גדולות.
canonical_concept_id: SCI-HEAT-001
verification_status: PRELIMINARY
source_text_checked: true
scientific_validation: NOT_INDEPENDENTLY_VALIDATED
confidence:
  source_traceability: HIGH
  generalizability: CONDITIONAL
  score_is_probability: false
conditions:
- זהו ניסוי מטבח במזון ובעומס מוגדרים; אין להעתיק את מסקנת נפח המים לפסטה.
sources:
- source_id: SRC-FOODLAB-2015
  book_title: 'The Food Lab: Better Home Cooking Through Science'
  author: J. Kenji López-Alt
  edition: First Edition
  year: 2015
  chapter: 4 Blanching, Searing, Braising, Glazing, Roasting, and the Science of Vegetables
  epub_sha256: 9457a6e8f889baf3740e5e82bd136089c5ce255225d77eeb8069f11a12510a54
  internal_path: text/part0193.html
  paragraph_index: 6
  paragraph_selector: body descendant p; 1-based; includes empty p; itertext joined with a space then stripped
  paragraph_sha256: 179097971ece32e8bcafd8d8d51f3af24ed50a1175c07dddc2e3ba2908f850b7
  anchor_status: UNKNOWN
  pdf_page: UNKNOWN
  printed_page: UNKNOWN
relationships:
- type: SUPPORTED_BY
  target_id: SRC-FOODLAB-2015
  target_name: '[[SRC-FOODLAB-2015]]'
  evidence: CLM-FLB-CH04-001
  confidence: HIGH_FOR_SOURCE_ATTRIBUTION
- type: SUPPORTS
  target_id: SCI-HEAT-001
  target_name: '[[Heat-Transfer]]'
  conditions: זהו ניסוי מטבח במזון ובעומס מוגדרים; אין להעתיק את מסקנת נפח המים לפסטה.
  confidence: CONDITIONAL_INTERPRETIVE_MAPPING
---

# נפח מים ותוצאת חליטת ירקות

בניסוי המתואר בשעועית ירוקה, מעט מים איבדו יותר טמפרטורה לאחר הוספת הירק, ונצפו ריכוך איטי יותר וגוון פחות ירוק מאשר במנות מים גדולות.

תנאים ומגבלות: זהו ניסוי מטבח במזון ובעומס מוגדרים; אין להעתיק את מסקנת נפח המים לפסטה.

הטענה נתמכת בפסקה שצוינה בספר; היא אינה אימות מדעי חיצוני. שיוך הטענה למושג הקיים [[Heat-Transfer]] הוא מיפוי פרשני.

מקור: [[SRC-FOODLAB-2015]], 4 Blanching, Searing, Braising, Glazing, Roasting, and the Science of Vegetables, `text/part0193.html`, פסקה 6. אין מספר עמוד PDF או עמוד מודפס זמין בעותק זה.

למפת הפרק: [[FoodLab-2015-Chapter-04]].
