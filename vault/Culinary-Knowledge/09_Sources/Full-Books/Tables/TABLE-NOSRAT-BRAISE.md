---
id: TABLE-NOSRAT-BRAISE
type: CULINARY_SOURCE_TABLE
name: נתחים וזמני קדרה לפי הספר
domain: SOURCES
verification_status: PRELIMINARY
source_text_checked: true
runtime_use: REFERENCE_ONLY
transcription_method: NATIVE_TEXT_REVIEW
scientific_validation: NOT_INDEPENDENTLY_VALIDATED
data:
  time_unit: minutes
  times:
  - cut: Chicken breast, boneless
    range:
    - 5
    - 8
  - cut: Chicken breast, bone-in
    range:
    - 15
    - 18
  - cut: Chicken legs
    range:
    - 35
    - 40
  - cut: Duck legs
    range:
    - 90
    - 120
  - cut: Turkey legs
    range:
    - 150
    - 180
  - cut: Pork shoulder
    range:
    - 150
    - 210
    exception: Longer on the bone
  - cut: 'Bony beef: short ribs, osso buco, oxtail'
    range:
    - 180
    - 210
  - cut: 'Meaty beef: chuck, brisket, round'
    range:
    - 180
    - 210
  - cut: Lamb shoulder on the bone
    range:
    - 150
    - 180
  braising_cuts:
    pork:
    - spare ribs
    - shoulder
    - shank
    - sausages
    - belly
    chicken_duck_rabbit:
    - legs
    - thighs
    - wings (poultry only)
    beef:
    - oxtail
    - short ribs
    - shank
    - chuck
    - brisket
    - round
    lamb_goat:
    - shoulder
    - neck
    - shank
limitations: המרת שעות לדקות נעשתה לצורך האינדקס בלבד. הטבלה אינה מציינת לכל שורה
  משקל, עובי וטמפרטורת נוזל, ולכן אין להפעיל את הזמנים כהבטחת רכות או בטיחות. הפרד
  חלקים שמתבשלים בקצב שונה ובדוק לפי נתח.
sources:
- source_id: SRC-NOSRAT-2017
  citation: Nosrat (2017), PDF [438, 439, 440]
  pdf_pages:
  - 438
  - 439
  - 440
  pdf_sha256: 5e5376bc4b6f1b3f64bd88b660c8efc5740a118b72fd390d61b29cacd437f281
relationships:
- type: SUPPORTED_BY
  target_id: PAGE-NOSRAT-438
- type: SUPPORTED_BY
  target_id: PAGE-NOSRAT-439
- type: SUPPORTED_BY
  target_id: PAGE-NOSRAT-440
- type: MENTIONS
  target_id: TEC-COMB-001
- type: MENTIONS
  target_id: DEC-PLAN-001
project_scope: chef_mind
allowed_contexts:
- chef_mind
- related_culinary_projects
external_publication: false
---

# נתחים וזמני קדרה לפי הספר

המרת שעות לדקות נעשתה לצורך האינדקס בלבד. הטבלה אינה מציינת לכל שורה משקל, עובי וטמפרטורת נוזל, ולכן אין להפעיל את הזמנים כהבטחת רכות או בטיחות. הפרד חלקים שמתבשלים בקצב שונה ובדוק לפי נתח.

מקור: [[nosrat-page-438]] · [[nosrat-page-439]] · [[nosrat-page-440]]

```json
{
  "time_unit": "minutes",
  "times": [
    {
      "cut": "Chicken breast, boneless",
      "range": [
        5,
        8
      ]
    },
    {
      "cut": "Chicken breast, bone-in",
      "range": [
        15,
        18
      ]
    },
    {
      "cut": "Chicken legs",
      "range": [
        35,
        40
      ]
    },
    {
      "cut": "Duck legs",
      "range": [
        90,
        120
      ]
    },
    {
      "cut": "Turkey legs",
      "range": [
        150,
        180
      ]
    },
    {
      "cut": "Pork shoulder",
      "range": [
        150,
        210
      ],
      "exception": "Longer on the bone"
    },
    {
      "cut": "Bony beef: short ribs, osso buco, oxtail",
      "range": [
        180,
        210
      ]
    },
    {
      "cut": "Meaty beef: chuck, brisket, round",
      "range": [
        180,
        210
      ]
    },
    {
      "cut": "Lamb shoulder on the bone",
      "range": [
        150,
        180
      ]
    }
  ],
  "braising_cuts": {
    "pork": [
      "spare ribs",
      "shoulder",
      "shank",
      "sausages",
      "belly"
    ],
    "chicken_duck_rabbit": [
      "legs",
      "thighs",
      "wings (poultry only)"
    ],
    "beef": [
      "oxtail",
      "short ribs",
      "shank",
      "chuck",
      "brisket",
      "round"
    ],
    "lamb_goat": [
      "shoulder",
      "neck",
      "shank"
    ]
  }
}
```
