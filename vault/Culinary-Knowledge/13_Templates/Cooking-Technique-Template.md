---
id: TEC-TEMPLATE
type: COOKING_TECHNIQUE
name: "שם טכניקת הבישול (Cooking Technique)"
domain: TECHNIQUES
heat_environment: "DRY / MOIST / COMBINATION / PRECISION / COLD"
heat_transfer_methods:
  - "CONDUCTION" # CONDUCTION / CONVECTION / RADIATION
recommended_equipment:
  - "מחבת ברזל יצוק / סיר לחץ / תנור קונבקציה"
target_foods:
  - "בשר אדום"
  - "ירקות שורש"
conditions:
  surface_temperature_min_c: 150
  cooking_medium: "OIL / WATER / STEAM / AIR"
  duration_range: "2-5 minutes"
effects:
  primary_outcome: "השחמה וקראסט פריך / ריכוך עמוק"
  texture_change: "CRISP_EXTERIOR / TENDER_INTERIOR"
  moisture_loss_pct_estimate: 15.0
exceptions:
  - "מתי אסור להשתמש בטכניקה זו"
relationships:
  - type: REQUIRES
    target_id: "SCI-PRINCIPLE-ID"
    target_name: "עיקרון מדעי דרוש"
  - type: ALTERNATIVE_TO
    target_id: "TEC-OTHER-ID"
    target_name: "טכניקה חלופית"
sources:
  - source_id: "SRC-MODERNIST-CUISINE"
    citation: "Modernist Cuisine, Vol 2"
verification_status: PRELIMINARY
---

# {{name}}

## תיאור הטכניקה (Overview)
הגדרה מדויקת של הטכניקה, אופן העברת החום אל המזון והמטרה הקולינרית המרכזית שלה.

## פרוטוקול ביצוע שלב-אחר-שלב (Execution Protocol)
1. הכנת חומר הגלם (ייבוש, המלחה, חיתוך).
2. הכנת הכלי ובקרת החום.
3. מהלך הבישול וזיהוי סימני מוכנות (חזותיים, קוליים, מדידת חום).
4. מנוחה או סיום.

## שגיאות נפוצות ואבחון כשלים (Troubleshooting)
* **בעיה**: "חומר הגלם נדבק למחבת" $\rightarrow$ **סיבה**: הטמפרטורה לא הגיעה לאפקט ליידנפרוסט / לא מספיק שומן.
* **בעיה**: "השחמה איטית ואידוי נוזלים" $\rightarrow$ **סיבה**: צפיפות יתר במחבת (Crowding).

## קשרים וטכניקות אלטרנטיביות (Alternatives)
* [[טכניקה חלופית לאותה מטרה]]

