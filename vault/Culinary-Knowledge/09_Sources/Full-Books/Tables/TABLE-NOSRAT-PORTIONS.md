---
id: TABLE-NOSRAT-PORTIONS
type: CULINARY_SOURCE_TABLE
name: אומדן קניית חלבון לפי משקל
domain: SOURCES
verification_status: PRELIMINARY
source_text_checked: true
runtime_use: REFERENCE_ONLY
transcription_method: NATIVE_TEXT_REVIEW
scientific_validation: NOT_INDEPENDENTLY_VALIDATED
data:
  basis: people per 1 pound; source average, not grams per person
  rows:
  - food: fish fillet
    people: 3
  - food: shell-on shellfish except shrimp
    people: 1
  - food: shell-on shrimp
    people: 3
  - food: bone-in roast
    people: 1.5
  - food: steak
    people: 3
  - food: whole animals and meat on the bone
    people: 1
  - food: ground meat for burgers or sausages
    people: 3
  - food: ground meat for ragù or chili
    people: 4
limitations: זהו אומדן קנייה ממוצע לפי המחברת. תיאבון, גיל הסועדים, עצמות, שאר המנות
  ופחת בבישול משנים את הכמות הנדרשת; אין להשתמש באומדן כמנת תזונה מחייבת.
sources:
- source_id: SRC-NOSRAT-2017
  citation: Nosrat (2017), PDF [440]
  pdf_pages:
  - 440
  pdf_sha256: 5e5376bc4b6f1b3f64bd88b660c8efc5740a118b72fd390d61b29cacd437f281
relationships:
- type: SUPPORTED_BY
  target_id: PAGE-NOSRAT-440
- type: MENTIONS
  target_id: DEC-PLAN-001
project_scope: chef_mind
allowed_contexts:
- chef_mind
- related_culinary_projects
external_publication: false
---

# אומדן קניית חלבון לפי משקל

זהו אומדן קנייה ממוצע לפי המחברת. תיאבון, גיל הסועדים, עצמות, שאר המנות ופחת בבישול משנים את הכמות הנדרשת; אין להשתמש באומדן כמנת תזונה מחייבת.

מקור: [[nosrat-page-440]]

```json
{
  "basis": "people per 1 pound; source average, not grams per person",
  "rows": [
    {
      "food": "fish fillet",
      "people": 3
    },
    {
      "food": "shell-on shellfish except shrimp",
      "people": 1
    },
    {
      "food": "shell-on shrimp",
      "people": 3
    },
    {
      "food": "bone-in roast",
      "people": 1.5
    },
    {
      "food": "steak",
      "people": 3
    },
    {
      "food": "whole animals and meat on the bone",
      "people": 1
    },
    {
      "food": "ground meat for burgers or sausages",
      "people": 3
    },
    {
      "food": "ground meat for ragù or chili",
      "people": 4
    }
  ]
}
```
