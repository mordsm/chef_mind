---
id: TEX-TEND-001
type: texture_transformation
name: "רכות ועסיסיות מבוססת ג'לטין (Collagen-Driven Tenderness & Succulence)"
domain: textures
subdomain: meat_tenderness
status: VERIFIED
title_he: רכות ועסיסיות מבוססת ג'לטין
sensory_attributes:
  - fork_tenderness
  - silky_mouthfeel
  - perceived_juiciness
physical_transformations:
  - collagen_to_gelatin_conversion
  - muscle_bundle_separation
  - viscosity_increase_of_interstitial_liquid
relationships:
  - type: ENABLED_BY
    target: "[[Collagen-Hydrolysis-Gelatin]]"
    note: "המרת סיבי הקולגן הקשים לג'לטין סופח מים"
  - type: REQUIRES
    target: "[[Low-Slow-Braising]]"
    note: "דורש זמן וחום לח לפירוק רקמת החיבור"
  - type: SUPPORTED_BY
    target: "[[SRC-BCCAMPUS-MEAT-2015]]"
    note: "הבחנה בין נתחים עשירים בקולגן לנתחים עדינים"
sources:
  - "[[SRC-BCCAMPUS-MEAT-2015]]"
  - "[[SRC-MCGEE-2004]]"
verification_status: VERIFIED
created_at: 2026-10-21
updated_at: 2026-10-21
---

# רכות ועסיסיות מבוססת ג'לטין (Collagen-Driven Tenderness & Succulence)

## 1. הגדרה מרקמית ופיזיקלית (Physical Transformation)
בנתחים עובדים עתירי קולגן (`[[Beef-Chuck-Collagen-Rich]]`), סיבי השריר עצמם מתכווצים ומאבדים מים חופשיים כשהטמפרטורה חוצה 70°C. עם זאת, המשך הבישול בנוזל (`[[Low-Slow-Braising]]`) מפרק את רשת הקולגן לג'לטין (`[[Collagen-Hydrolysis-Gelatin]]`), המאפשר לסיבים להיפרד בקלות ויוצר נוזל סמיך וחלקלק בין הסיבים המעניק תחושת עסיסיות ורכות בפה.
