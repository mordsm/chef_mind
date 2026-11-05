---
id: RUL-FLB-CH04-001
canonical_rule_id: NEW_DRAFT_RULE
type: CULINARY_RULE
name: 'חליטה: נפח מים לפי יעד ותנאים'
domain: RULES
verification_status: PRELIMINARY
claim_type: INTERPRETATION
if: אם רוצים שעועית ירוקה רכה־פריכה וירוקה
then: אפשר להשתמש במסת מים שממתנת את ירידת הטמפרטורה, או לבחון חלופה מותאמת לעומס ולציוד
because: בניסוי המתואר מעט מים התקררו יותר לאחר הוספת השעועית
exceptions:
- אין להחיל את ממצאי השעועית על פסטה או על כל ירק
tradeoffs: יותר מים דורשים חימום ראשוני גדול; פחות מים מחייבים התאמת עומס ובדיקת צבע ורכות
source_claim_ids:
- CLM-FLB-CH04-001
sources:
- source_id: SRC-FOODLAB-2015
  edition: First Edition
  chapter: 4 Blanching, Searing, Braising, Glazing, Roasting, and the Science of Vegetables
  internal_path: text/part0193.html
  paragraph_index: 6
  paragraph_selector: body descendant p; 1-based; includes empty p; itertext joined with a space then stripped
  paragraph_sha256: 179097971ece32e8bcafd8d8d51f3af24ed50a1175c07dddc2e3ba2908f850b7
  anchor_status: UNKNOWN
  pdf_page: UNKNOWN
  printed_page: UNKNOWN
  book_title: 'The Food Lab: Better Home Cooking Through Science'
  author: J. Kenji López-Alt
  year: 2015
  knowledge_type: CONDITIONAL_RULE_INTERPRETATION
relationships:
- type: SUPPORTED_BY
  target_id: EVD-FLB-CH04-001
  target_name: '[[FoodLab-CH04-Blanch-Water-Volume]]'
  confidence: CONDITIONAL
  evidence: CLM-FLB-CH04-001
- type: SUPPORTED_BY
  target_id: SCI-HEAT-001
  target_name: '[[Heat-Transfer]]'
  conditions: השוואת בחירות בתוך ההקשר בלבד; אינה סתירה גורפת
  confidence: INTERPRETIVE
---

# חליטה: נפח מים לפי יעד ותנאים

**IF:** אם רוצים שעועית ירוקה רכה־פריכה וירוקה

**THEN:** אפשר להשתמש במסת מים שממתנת את ירידת הטמפרטורה, או לבחון חלופה מותאמת לעומס ולציוד

**BECAUSE:** בניסוי המתואר מעט מים התקררו יותר לאחר הוספת השעועית

**EXCEPTIONS:** אין להחיל את ממצאי השעועית על פסטה או על כל ירק

פשרות וחלופות: יותר מים דורשים חימום ראשוני גדול; פחות מים מחייבים התאמת עומס ובדיקת צבע ורכות

כלל פרשני, ולא ציטוט או פרוטוקול מלא מהספר. ביסוס: [[FoodLab-CH04-Blanch-Water-Volume]]. המושג הקיים נשמר: [[Heat-Transfer]]. אין הפעלה אוטומטית במנוע השף.
