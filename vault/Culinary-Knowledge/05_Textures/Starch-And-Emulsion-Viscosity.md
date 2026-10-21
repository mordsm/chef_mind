---
id: TEX-VISC-001
type: texture_transformation
name: "סמיכות, צמיגות ויציבות רטבים (Sauce Viscosity & Emulsion Stability)"
domain: textures
subdomain: viscosity_and_thickening
status: VERIFIED
title_he: סמיכות, צמיגות ויציבות רטבים
sensory_attributes:
  -glossy_coating
  - velvety_viscosity
  - homogenous_body
physical_transformations:
  - starch_granule_swelling
  - amylose_network_entanglement
  - droplet_dispersion_emulsification
relationships:
  - type: ENABLED_BY
    target: "[[Starch-Gelatinization-Retrogradation]]"
    note: "ג'לטיניזציה של עמילן מעלה את צמיגות הפאזה המימית"
  - type: ENABLED_BY
    target: "[[Caramelization-And-Emulsification]]"
    note: "ייצוב טיפות שומן מונע היפרדות שכבת שמן ברוטב"
  - type: SUPPORTED_BY
    target: "[[SRC-BCCAMPUS-PASTRY-2015]]"
    note: "פרוטוקול פיזור עמילן ומניעת גושים"
sources:
  - "[[SRC-BCCAMPUS-PASTRY-2015]]"
  - "[[SRC-FOODLAB-2015]]"
verification_status: VERIFIED
created_at: 2026-10-21
updated_at: 2026-10-21
---

# סמיכות, צמיגות ויציבות רטבים (Sauce Viscosity & Emulsion Stability)

## 1. הגדרה מרקמית ופיזיקלית (Physical Transformation)
סמיכות של רוטב ויכולתו לצפות מזון (Nappé) נשלטות על ידי שלושה מנגנונים פיזיקליים:
1. **ג'לטיניזציה של עמילן (`[[Rule-Starch-Slurry-Dispersion]]`)**: התנפחות גרנולות עמילן שהופردו מראש בנוזל קר או ברביכה (Roux).
2. **רדוקציה (אידוי מים)**: ריכוז מוצקים מומסים, ג'לטין ופוליסכרידים טבעיים (כגון פקטין בעגבניות) בבעבוע עדין ללא מכסה (`[[Covered-Vs-Uncovered-Evaporation]]`).
3. **אמולסיה**: טריפת שומן (שמן זית או חמאה) עם מים עמילניים (כגון מי בישול פסטה `[[Pasta-Water-Oil-And-Volume]]`) ליצירת רוטב קרמי אחיד.
