---
id: DEC-PLAN-001
type: SCIENTIFIC_PRINCIPLE
name: "התאמת שיטת הבישול למבנה הנתח (Cut-to-Method Decision Matching)"
domain: DECISION_MAKING
category: "PROTEIN"
description: "מודל החלטה הקובע את שיטת הבישול המומלצת והחסומה לפי תכולת הקולגן, השומן והלחות בחומר הגלם"
conditions:
  temperature_range_c:
    min: 50
    max: 230
  water_activity_aw:
    min: 0.30
    max: 1.0
  ph_range:
    min: 4.5
    max: 7.5
  catalysts: ["collagen_density", "intramuscular_fat", "water_content"]
effects:
  molecular_change: "התאמת קצב העברת החום והסביבה (יבשה מול לחה) למבנה הסיבים של חומר הגלם"
  sensory_consequences:
    taste: ["OPTIMAL_FLAVOR_DEVELOPMENT"]
    aroma: []
    color: []
    texture: "מניעת התייבשות בנתחים רזים ומניעת קשיחות בנתחים עתירי קולגן"
exceptions:
  - "קורקבנים מבושלים ורכים יכולים לעבור השחמה קצרה בסיום, אך לא כשיטת ריכוך ראשית"
relationships:
  - type: REQUIRES
    target_id: "ING-MEAT-001"
    target_name: "[[Beef-Chuck-Collagen-Rich]]"
  - type: ENABLES
    target_id: "RUL-MEAT-001"
    target_name: "[[Rule-Collagen-Cut-Moist-Heat]]"
  - type: SUPPORTED_BY
    target_id: "SRC-BCCAMPUS-MEAT-2015"
    target_name: "[[SRC-BCCAMPUS-MEAT-2015]]"
sources:
  - source_id: "SRC-BCCAMPUS-MEAT-2015"
    citation: "BCcampus, Meat Cutting and Processing for Food Service, 2015"
verification_status: VERIFIED
---

# התאמת שיטת הבישול למבנה הנתח (Cut-to-Method Decision Matching)

## מטריצת החלטה (Decision Matrix)
| משפחת חומר גלם | דוגמאות | שיטות מומלצות | שיטות חסומות / שגויות וסיבה מדעית |
| :--- | :--- | :--- | :--- |
| **שריר עשיר בקולגן ודל שומן** | קורקבנים, שוק בקר, כתף | בישול בנוזל (`boil_simmer`), צלי קדרה (`braise`), סיר לחץ | צלייה יבשה בתנור או צריבה קצרה בלבד — מאדה נוזלים לפני הידרוליזת הקולגן (`[[Collagen-Hydrolysis-Gelatin]]`) |
| **חלבון רזה ועדין** | חזה עוף, פילה בקר | צריבה (`pan_sear`), גריל (`grill_direct`), אידוי | בישול ארוך בנוזל — מכווץ סיבי אקטין וגורם ליובש סיבי |
| **דג לבן עדין** | דניס, בקלה, לברק | צריבה עדינה, אידוי, אפייה בתנור | בישול ארוך או הקפצה אגרסיבית — מפרק את הנתח |
