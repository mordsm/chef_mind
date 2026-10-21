---
id: TEC-COMB-001
type: COOKING_TECHNIQUE
name: "צלי קדרה ובישול ארוך בנוזל (Low-and-Slow Braising)"
domain: TECHNIQUES
heat_environment: "COMBINATION"
heat_transfer_methods:
  - "CONDUCTION"
  - "CONVECTION"
recommended_equipment:
  - "סיר כבד עם מכסה אטום (Dutch Oven)"
target_foods:
  - "נתחי שריר עתירי קולגן (כתף, שוק, אסאדו, קורקבנים)"
  - "ירקות שורש קשים"
conditions:
  surface_temperature_min_c: 85
  cooking_medium: "WATER"
  duration_range: "90-240 minutes (until collagen hydrolyzes)"
effects:
  primary_outcome: "הידרוליזה מלאה של קולגן לג'לטין וריכוך סיבי שריר עבים"
  texture_change: "FORK_TENDER / GELATINOUS_SUCCULENCE"
  moisture_loss_pct_estimate: 20.0
exceptions:
  - "אסור ליישם על נתחים רזים ודלי קולגן (כגון חזה עוף או פילה בקר) שכן הם יתייבשו לחלוטין"
relationships:
  - type: REQUIRES
    target_id: "SCI-PROT-001"
    target_name: "[[Collagen-Hydrolysis-Gelatin]]"
  - type: ENABLES
    target_id: "TEX-TEND-001"
    target_name: "[[Collagen-Driven-Tenderness]]"
  - type: ALTERNATIVE_TO
    target_id: "TEC-PREC-001"
    target_name: "[[Sous-Vide-Precision-Cooking]]"
sources:
  - source_id: "SRC-BCCAMPUS-MEAT-2015"
    citation: "BCcampus, Meat Cutting and Processing for Food Service, 2015"
  - source_id: "SRC-MCGEE-2004"
    citation: "McGee, On Food and Cooking, 2004, Chapter 3"
verification_status: VERIFIED
---

# צלי קדרה ובישול ארוך בנוזל (Low-and-Slow Braising)

## תיאור הטכניקה (Overview)
טכניקה משולבת הכוללת (אופציונלית) השחמה ראשונית בחום יבש לפיתוח תוצרי `[[Maillard-Reaction]]`, ולאחריה בישול איטי ומכוסה בנוזל מתון (85°C–92°C) לשם פירוק קולגן לג'לטין (`[[Collagen-Hydrolysis-Gelatin]]`).

## פרוטוקול ביצוע שלב-אחר-שלב (Execution Protocol)
1. זיהוי שהנתח אכן עשיר ברקמת חיבור (`[[Rule-Collagen-Cut-Moist-Heat]]`).
2. הוספת נוזל (ציר, מים, יין) וכיסוי הסיר (`[[Covered-Vs-Uncovered-Evaporation]]`).
3. שמירה על בעבוע עדין (Simmer) ולא רתיחה אגרסיבית שדוחקת חלבונים.
4. בדיקת רכות מכנית לצד מדידת טמפרטורת בטיחות (`[[Minimum-Internal-Temperatures]]`).
