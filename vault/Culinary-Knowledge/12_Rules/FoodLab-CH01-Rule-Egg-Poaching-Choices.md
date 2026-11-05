---
id: RUL-FLB-CH01-001
canonical_rule_id: NEW_DRAFT_RULE
type: CULINARY_RULE
name: 'שליקת ביצה: חומצה מול עדינות טעם'
domain: RULES
verification_status: PRELIMINARY
claim_type: INTERPRETATION
if: אם רוצים ביצה שלוקה ולבן עדין
then: אפשר לבחור מעט חומצה כשמקבלים את השפעתה על הטעם והמרקם, או להימנע ממנה כשעדינות טעם חשובה יותר
because: לפי התיאור במקור, האצה בהתייצבות אינה בהכרח יתרון מיידי ויכולה להוביל להתייצבות יתר
exceptions:
- התאמה לריכוז, זמן וטריות הביצה; אין ערובה שכל שיטה תייצר אותה צורה
tradeoffs: 'עם חומצה: שינוי בהתייצבות ובטעם; ללא חומצה: שמירת טעם עדין, עם צורך בטיפול אחר בלבן'
source_claim_ids:
- CLM-FLB-CH01-002
sources:
- source_id: SRC-FOODLAB-2015
  edition: First Edition
  chapter: 1 Eggs, Dairy, and the Science of Breakfast
  internal_path: text/part0023.html
  paragraph_index: 23
  paragraph_selector: body descendant p; 1-based; includes empty p; itertext joined with a space then stripped
  paragraph_sha256: 407f6660d2cf6e51b94e7fd0c99bea258fb617860dbfccb2a535e48463d577ec
  anchor_status: UNKNOWN
  pdf_page: UNKNOWN
  printed_page: UNKNOWN
  book_title: 'The Food Lab: Better Home Cooking Through Science'
  author: J. Kenji López-Alt
  year: 2015
  knowledge_type: CONDITIONAL_RULE_INTERPRETATION
relationships:
- type: SUPPORTED_BY
  target_id: EVD-FLB-CH01-002
  target_name: '[[FoodLab-CH01-Poaching-Acid]]'
  confidence: CONDITIONAL
  evidence: CLM-FLB-CH01-002
- type: SUPPORTED_BY
  target_id: TEC-EGG-002
  target_name: '[[Poaching-Scrambling-And-French-Omelet-Control]]'
  conditions: השוואת בחירות בתוך ההקשר בלבד; אינה סתירה גורפת
  confidence: INTERPRETIVE
---

# שליקת ביצה: חומצה מול עדינות טעם

**IF:** אם רוצים ביצה שלוקה ולבן עדין

**THEN:** אפשר לבחור מעט חומצה כשמקבלים את השפעתה על הטעם והמרקם, או להימנע ממנה כשעדינות טעם חשובה יותר

**BECAUSE:** לפי התיאור במקור, האצה בהתייצבות אינה בהכרח יתרון מיידי ויכולה להוביל להתייצבות יתר

**EXCEPTIONS:** התאמה לריכוז, זמן וטריות הביצה; אין ערובה שכל שיטה תייצר אותה צורה

פשרות וחלופות: עם חומצה: שינוי בהתייצבות ובטעם; ללא חומצה: שמירת טעם עדין, עם צורך בטיפול אחר בלבן

כלל פרשני, ולא ציטוט או פרוטוקול מלא מהספר. ביסוס: [[FoodLab-CH01-Poaching-Acid]]. המושג הקיים נשמר: [[Poaching-Scrambling-And-French-Omelet-Control]]. אין הפעלה אוטומטית במנוע השף.
