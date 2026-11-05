---
id: RUL-FLB-CH03-001
canonical_rule_id: RUL-MEAT-002
type: CULINARY_RULE
name: נתח רך או עתיר רקמת חיבור
domain: RULES
verification_status: PRELIMINARY
claim_type: INTERPRETATION
if: אם בוחרים שיטת הכנה לנתח מזוהה
then: בחר חימום מהיר מבוקר לנתח רך כשזו מטרת המנה; שקול בישול ממושך מתאים לנתח עתיר רקמת חיבור
because: חימום לטמפרטורת יעד ופירוק רקמת חיבור הן מטרות שונות
exceptions:
- חיתוך, טחינה ויעד קולינרי משנים התאמה; נדרש נוהל בטיחות נפרד
tradeoffs: צריבה מדגישה השחמה; בישול לח ממושך נותן זמן לריכוך קולגן
source_claim_ids:
- CLM-FLB-CH03-003
sources:
- source_id: SRC-FOODLAB-2015
  edition: First Edition
  chapter: 3 Steaks, Chops, Chicken, Fish, and the Science of Fast-Cooking Foods
  internal_path: text/part0121.html
  paragraph_index: 8
  paragraph_selector: body descendant p; 1-based; includes empty p; itertext joined with a space then stripped
  paragraph_sha256: f1cdf41673f9101edc3d05636d84e4d347003cdc5415e44f474156b92655c71c
  anchor_status: UNKNOWN
  pdf_page: UNKNOWN
  printed_page: UNKNOWN
  book_title: 'The Food Lab: Better Home Cooking Through Science'
  author: J. Kenji López-Alt
  year: 2015
  knowledge_type: CONDITIONAL_RULE_INTERPRETATION
relationships:
- type: SUPPORTED_BY
  target_id: EVD-FLB-CH03-003
  target_name: '[[FoodLab-CH03-Tender-Tough-Method]]'
  confidence: CONDITIONAL
  evidence: CLM-FLB-CH03-003
- type: SUPPORTED_BY
  target_id: DEC-PLAN-001
  target_name: '[[Cut-To-Method-Matching]]'
  conditions: השוואת בחירות בתוך ההקשר בלבד; אינה סתירה גורפת
  confidence: INTERPRETIVE
---

# נתח רך או עתיר רקמת חיבור

**IF:** אם בוחרים שיטת הכנה לנתח מזוהה

**THEN:** בחר חימום מהיר מבוקר לנתח רך כשזו מטרת המנה; שקול בישול ממושך מתאים לנתח עתיר רקמת חיבור

**BECAUSE:** חימום לטמפרטורת יעד ופירוק רקמת חיבור הן מטרות שונות

**EXCEPTIONS:** חיתוך, טחינה ויעד קולינרי משנים התאמה; נדרש נוהל בטיחות נפרד

פשרות וחלופות: צריבה מדגישה השחמה; בישול לח ממושך נותן זמן לריכוך קולגן

כלל פרשני, ולא ציטוט או פרוטוקול מלא מהספר. ביסוס: [[FoodLab-CH03-Tender-Tough-Method]]. המושג הקיים נשמר: [[Cut-To-Method-Matching]]. אין הפעלה אוטומטית במנוע השף.
