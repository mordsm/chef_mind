---
id: RUL-FLB-CH06-001
canonical_rule_id: RUL-MEAT-003
type: CULINARY_RULE
name: 'עוף שלם: פרישה מול צלייה שלמה'
domain: RULES
verification_status: PRELIMINARY
claim_type: INTERPRETATION
if: אם רוצים לתאם בישול חזה וירכיים
then: אפשר לפרוש את העוף לשינוי חשיפת החלקים, או לשמור צורה שלמה ולבקר את החלקים בנפרד
because: הספר מסביר שהפרישה חושפת יותר את הבשר הכהה
exceptions:
- אין לאמץ טמפרטורות בטיחות מקוצרות בלי נוהל מאומת; בדיקה בכמה נקודות נדרשת
tradeoffs: פרישה משנה הצגה ומקום בתבנית; צורה שלמה שומרת הצגה אך מקשה על אחידות
source_claim_ids:
- CLM-FLB-CH06-001
sources:
- source_id: SRC-FOODLAB-2015
  edition: First Edition
  chapter: 6 Chickens, Turkeys, Prime Rib, and the Science of Roasts
  internal_path: text/part0283.html
  paragraph_index: 11
  paragraph_selector: body descendant p; 1-based; includes empty p; itertext joined with a space then stripped
  paragraph_sha256: a46a91e6c2ca7df79704108f9d27206a295873f8120eaf45570da6d180abf39f
  anchor_status: UNKNOWN
  pdf_page: UNKNOWN
  printed_page: UNKNOWN
  book_title: 'The Food Lab: Better Home Cooking Through Science'
  author: J. Kenji López-Alt
  year: 2015
  knowledge_type: CONDITIONAL_RULE_INTERPRETATION
relationships:
- type: SUPPORTED_BY
  target_id: EVD-FLB-CH06-001
  target_name: '[[FoodLab-CH06-Spatchcock-Geometry]]'
  confidence: CONDITIONAL
  evidence: CLM-FLB-CH06-001
- type: SUPPORTED_BY
  target_id: TEC-MEAT-002
  target_name: '[[Whole-Bird-Roasting-And-Crisp-Poultry-Skin]]'
  conditions: השוואת בחירות בתוך ההקשר בלבד; אינה סתירה גורפת
  confidence: INTERPRETIVE
---

# עוף שלם: פרישה מול צלייה שלמה

**IF:** אם רוצים לתאם בישול חזה וירכיים

**THEN:** אפשר לפרוש את העוף לשינוי חשיפת החלקים, או לשמור צורה שלמה ולבקר את החלקים בנפרד

**BECAUSE:** הספר מסביר שהפרישה חושפת יותר את הבשר הכהה

**EXCEPTIONS:** אין לאמץ טמפרטורות בטיחות מקוצרות בלי נוהל מאומת; בדיקה בכמה נקודות נדרשת

פשרות וחלופות: פרישה משנה הצגה ומקום בתבנית; צורה שלמה שומרת הצגה אך מקשה על אחידות

כלל פרשני, ולא ציטוט או פרוטוקול מלא מהספר. ביסוס: [[FoodLab-CH06-Spatchcock-Geometry]]. המושג הקיים נשמר: [[Whole-Bird-Roasting-And-Crisp-Poultry-Skin]]. אין הפעלה אוטומטית במנוע השף.
