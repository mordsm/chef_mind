---
id: GAP-EGG-001
type: KNOWLEDGE_GAP
name: "פערי ידע ואי-ודאויות מדעיות בפרק הביצים של מקג'י (Documented Scientific Unknowns in Egg Chemistry)"
title_he: "פערי ידע ואי-ודאויות מדעיות המתועדים בפרק הביצים של מקג'י"
domain: KNOWLEDGE_GAPS
priority: "P2_SCIENTIFIC_UNCERTAINTY"
book_title: "On Food and Cooking: The Science and Lore of the Kitchen"
author: "Harold McGee"
edition: "2nd Edition, Completely Revised and Updated"
publication_year: 2004
chapter: "Chapter 2: Eggs (Benefits and Costs; The White; The Chemistry of Egg Flavor; Hard-Cooked Eggs)"
pdf_page: "87, 91-92, 101-102"
printed_page: "73, 77-78, 87-88"
knowledge_type: "UNVERIFIED_CLAIM_OR_SCIENTIFIC_UNKNOWN"
claim_type: "HYPOTHESIS"
description: "ריכוז מפורש של הטענות הבלתי-מאומתות, ההשערות ופערי הידע המדעיים שהרולד מקג'י עצמו מסמן בפרק 2 כבלתי פתורים או חסרי הוכחה ניסויית"
effects:
  molecular_change: "הבחנה קפדנית בין עובדות מוכחות לבין מנגנונים שמקג'י מסמן בסימן שאלה (?) או במילים 'somehow' / 'remains unclear' / 'proven hard to document'"
  texture_change: "אי-ודאות לגבי התרומה הקולינרית של Ovomucoid ו-Avidin והמנגנון המולקולרי המדויק של הידבקות אלבומין טרי לממברנת הקליפה"
relationships:
  - type: AFFECTS
    target_id: "ING-EGG-002"
    target_name: "[[Egg-Albumen-Key-Proteins]]"
    condition: "אי-ודאות לגבי התפקיד הטבעי של Ovalbumin והתכונות הקולינריות של Ovomucoid ו-Avidin"
    evidence: "McGee 2004, Ch. 2, pp. 77-78 (PDF pp. 91-92)"
    confidence: 95
  - type: AFFECTS
    target_id: "RUL-EGG-002"
    target_name: "[[Rule-Egg-Age-And-Grade-Selection-Matrix]]"
    condition: "המנגנון המדויק שבו pH נמוך גורם לאלבומין להידבק לממברנת הקליפה טרם פוענח במלואו ('somehow causes')"
    evidence: "McGee 2004, Ch. 2, p. 88 (PDF p. 102)"
    confidence: 95
  - type: SUPPORTED_BY
    target_id: "SRC-MCGEE-2004"
    target_name: "[[SRC-MCGEE-2004]]"
    note: "Chapter 2, Printed pp. 73, 77-78, 87-88 (PDF pp. 87, 91-92, 101-102)"
sources:
  - source_id: "SRC-MCGEE-2004"
    citation: "Harold McGee, On Food and Cooking (2nd Ed., 2004), Chapter 2: Eggs, Printed pp. 73, 77-78, 87-88 (PDF pp. 87, 91-92, 101-102)"
verification_status: DOCUMENTED_UNKNOWN
created_at: 2026-10-21
updated_at: 2026-10-21
---

# פערי ידע ואי-ודאויות מדעיות המתועדים בפרק הביצים של מקג'י (`GAP-EGG-001`)

> [!IMPORTANT] שקיפות מדעית והפרדת עובדות מהשערות (STEP 5 & STEP 12)
> בהתאם לעקרון אי-המצאת סימוכין והבחנה קפדנית בין עובדה מבוססת-מקור (`DIRECT_SOURCE_CLAIM`), פרשנות (`INTERPRETATION`) והשערה/פער ידע (`HYPOTHESIS` / `UNKNOWN`), רשומה זו מתעדת את 5 הנקודות שבהן הרולד מקג'י עצמו מציין במפורש כי המדע טרם מצא תשובה מלאה או הוכחה ניסויית.

---

## טבלת אי-ודאויות, השערות וטענות בלתי מאומתות בפרק 2

| מזהה פער | הנושא בפרק 2 | הציטוט והניסוח המדויק במקור (McGee 2004) | סיווג אפיסטמולוגי | עמוד מודפס (ועמוד PDF) |
| :--- | :--- | :--- | :--- | :--- |
| **`UNK-EGG-01`** | **התפקיד הביולוגי הטבעי של `Ovalbumin` (54% מחלבון הביצה)** | *"Ovalbumin, the most plentiful egg protein, was the first protein ever crystallized in the laboratory (in 1890), **yet its natural function remains unclear**. It seems related to a family of proteins that inhibit protein-digesting enzymes, and **may be** a mainly nutritional relic of ancient battles against a now-extinct microbe."* | `HYPOTHESIS` / `UNKNOWN` | עמ' מודפס 77–78 (PDF עמ' 91–92) |
| **`UNK-EGG-02`** | **התכונות הקולינריות של `Ovomucoid` (11%), `Avidin` (0.06%) ו-10% חלבוני אלבומין נוספים** | בטבלת *"The Proteins in Egg White"*, תחת עמודת *"Culinary Properties"* מסמן מקג'י **`?`** עבור `Ovomucoid`, `Avidin` ו-`Others`, ומוסיף סימן שאלה (`?`) גם על תפקיד ה-`Globulins` באיטום פגמים בקליפה. | `UNKNOWN` | עמ' מודפס 77 (PDF עמ' 91) |
| **`UNK-EGG-03`** | **המנגנון המולקולרי שבו `Ovomucin` בונה את מבנה השכבות של החלבון הסמיך** | *"Ovomucin **somehow** pulls together the otherwise soupy protein solution into an organized structure... This structure is **thought to** help cushion the yolk."* | `INTERPRETATION` / `PARTIAL_UNKNOWN` | עמ' מודפס 78 (PDF עמ' 92) |
| **`UNK-EGG-04`** | **המנגנון המולקולרי המדויק של הידבקות חלבון טרי (pH נמוך) לממברנת הקליפה בביצה קשה** | *"Difficult peeling is characteristic of fresh eggs with a relatively low albumen pH, which **somehow** causes the albumen to adhere to the inner shell membrane more strongly than it coheres to itself."* | `DIRECT_OBSERVATION_WITH_UNKNOWN_MECHANISM` | עמ' מודפס 88 (PDF עמ' 102) |
| **`UNK-EGG-05`** | **הטענה שביצי חופש מתרנגולות הניזונות מעשבים וחרקים טעימות יותר מביצים תעשייתיות** | *"people who pay close attention to eggs say that flavor has suffered: that the chicken's natural, varied diet of grains, leaves, and bugs provides a richness that the commercial soy and fish meals don't. **(This difference has proven hard to document in taste tests; see p. 87.)**"* | `UNVERIFIED_CLAIM_IN_BLIND_TASTE_TESTS` | עמ' מודפס 73, 87 (PDF עמ' 87, 101) |

