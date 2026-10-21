---
id: DASHBOARD-MAIN
type: system_dashboard
name: Culinary Knowledge Dashboard
domain: ontology
title_he: לוח בקרה ראשי - אונטולוגיית הידע הקולינרי
status: ACTIVE
vault_root: "C:\\workspace\\chef_mind\\vault"
knowledge_root: "Culinary-Knowledge"
total_nodes: 53
verified_nodes: 49
total_edges: 118
sources_count: 6
rules_count: 6
conflicts_count: 3
open_gaps_count: 2
created_at: 2026-10-21
updated_at: 2026-10-21
---

# לוח בקרה ראשי: אונטולוגיית הידע הקולינרי (Culinary Knowledge Dashboard)

> [!NOTE] סביבת עבודה מקומית באובסידיאן (Obsidian Native)
> לוח בקרה זה נבנה בתחביר Markdown תקני הנתמך במלואו על ידי מנוע Obsidian ומסונכרן אוטומטית מול מנוע ההחלטות של `chef_mind` (`app/ontology_bridge.py`).

---

## א. ניווט מהיר ברשת הידע (Knowledge Navigation)

```mermaid
graph LR
    subgraph Core ["תשתית האונטולוגיה"]
        Map["[[Knowledge-Map|מפת הידע הראשית]]"]
        Rel["[[Relationships|מודל הקשרים]]"]
        Con["[[Concepts|טקסונומיית מושגים]]"]
    end

    subgraph Domains ["8 תחומי הידע המרכזיים"]
        D1["[[01_Ingredients/|01. חומרי גלם]]"]
        D2["[[02_Food-Science/|02. מדע המזון]]"]
        D3["[[03_Techniques/|03. טכניקות בישול]]"]
        D4["[[04_Flavors/|04. טעמים וארומות]]"]
        D5["[[05_Textures/|05. מרקמים]]"]
        D6["[[06_Equipment/|06. ציוד וסביבה]]"]
        D7["[[07_Food-Safety/|07. בטיחות ושימור]]"]
        D8["[[08_Decision-Making/|08. קבלת החלטות]]"]
    end

    subgraph Operations ["ניהול, אימות ואיכות"]
        Sources["[[09_Sources/|09. מקורות]]"]
        Gaps["[[10_Knowledge-Gaps/|10. פערי ידע]]"]
        Conflicts["[[11_Conflicts/|11. סתירות ומחלוקות]]"]
        Rules["[[12_Rules/|12. כללי החלטה]]"]
        Templates["[[13_Templates/|13. תבניות]]"]
    end

    Core --> Domains
    Domains --> Operations
```

### קישורים ישירים למדורי המערכת
| מדור | נתיב | תיאור ותפקיד במערכת |
| :--- | :--- | :--- |
| **מפת הידע הראשית** | `[[00_Ontology/Knowledge-Map]]` | פריסה היררכית ואינטגרטיבית של כל תחומי הידע |
| **מודל הקשרים הסמנטי** | `[[00_Ontology/Relationships]]` | הגדרת סוגי הקשרים, כיווניות וכללי הכרעה מרובת-פתרונות |
| **טקסונומיית מושגים** | `[[00_Ontology/Concepts]]` | מילון מונחים, ספי טמפרטורה, פרמטרי בקרה ומצבי צבירה |
| **ארכיטקטורת קליטת ספרות** | `[[00_Ontology/Book-Ingestion-Architecture]]` | צינור 7 השלבים לחילוץ עובדות וכללים עם עקיבות מקורות |
| **חיבור למנוע השף** | `[[00_Ontology/Chef-Engine-Integration]]` | מיפוי רשומות ה-YAML וקשרי הגרף למנוע `chef_mind` |

---

## ב. כיסוי הידע (Knowledge Coverage Overview)

| תחום ידע | קטגוריות מוגדרות | רשומות קיימות | רשומות מאומתות | פערי ידע פתוחים | סטטוס כיסוי |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **00. אונטולוגיה ותשתיות** | 8 תתי-תחומים | 5 (`[[Book-Ingestion-Architecture]]`, `[[Chef-Engine-Integration]]`) | 3 | 0 | 🟡 פעיל |
| **01. חומרי גלם (Ingredients)** | 6 קבוצות ראשיות | 6 (`[[Allium-Onion-Sulfur-Sugars]]`, `[[Beef-Chuck-Collagen-Rich]]`) | 6 | 0 | 🟢 מאומת ומקושר |
| **02. מדע המזון (Food Science)** | 10 תהליכים | 6 (`[[Caramelization-And-Emulsification]]`, `[[Collagen-Hydrolysis-Gelatin]]`) | 6 | 2 | 🟢 מאומת ומקושר |
| **03. טכניקות בישול (Techniques)** | 10 טכניקות בסיס | 4 (`[[Gentle-Simmering-Poaching]]`, `[[High-Heat-Pan-Searing]]`) | 4 | 0 | 🟢 מאומת ומקושר |
| **04. טעמים וארומות (Flavors)** | 6 מימדי חישה | 3 (`[[Acid-Fat-Balance]]`, `[[Fat-Soluble-Volatile-Aromas]]`) | 3 | 0 | 🟢 מאומת ומקושר |
| **05. מרקמים (Textures)** | 7 טרנספורמציות | 3 (`[[Collagen-Driven-Tenderness]]`, `[[Starch-And-Emulsion-Viscosity]]`) | 3 | 0 | 🟢 מאומת ומקושר |
| **06. ציוד וסביבה (Equipment)** | 7 סוגי כלים ובקרה | 3 (`[[Cast-Iron-Vs-Stainless-Thermal-Mass]]`, `[[Core-Probe-Thermometry]]`) | 3 | 0 | 🟢 מאומת ומקושר |
| **07. בטיחות מזון (Food Safety)** | 7 פרוטוקולי בטיחות | 3 (`[[Cross-Contamination-Prevention]]`, `[[Microbial-Danger-Zone-Cooling]]`) | 3 | 0 | 🟢 מאומת ומקושר |
| **08. קבלת החלטות (Decision-Making)** | 7 שלבי תכנון | 3 (`[[Cut-To-Method-Matching]]`, `[[Real-Time-Thermal-Rescue]]`) | 3 | 0 | 🟢 מאומת ומקושר |
| **12. כללי החלטה (Rules)** | כללים קולינריים | 6 (`[[Rule-Collagen-Cut-Moist-Heat]]`, `[[Rule-Custard-Curdling-Rescue]]`) | 6 | 0 | 🟢 מאומת ומקושר |

---

## ג. בקרת איכות ומהימנות הידע (Knowledge Quality & Verification)

> [!IMPORTANT] עיקרון שרשרת ההוכחה (No Invented Citations)
> כל קביעה במערכת משויכת למקור מוסמך (`09_Sources/`) או מתועדת מפורשות כפער ידע (`10_Knowledge-Gaps/`).

- **סה"כ רשומות פעילות באונטולוגיה:** 53 (49 מאומתות, 118 קשרי גרף סמנטיים).
- **מקורות רשומים ומאומתים (`[[09_Sources/]]`):** 6 (`[[SRC-USDA-FSIS-2024]]`, `[[SRC-BCCAMPUS-PASTRY-2015]]`, `[[SRC-BCCAMPUS-MEAT-2015]]`, `[[SRC-MCGEE-2004]]`, `[[SRC-FOODLAB-2015]]`, `[[SRC-MODCUIS-2011]]`).
- **סתירות קולינריות מנותחות (`[[11_Conflicts/]]`):** 3 (`[[Searing-Locks-In-Juices-Myth]]`, `[[Pre-Salting-Steak-Timing]]`, `[[Pasta-Water-Oil-And-Volume]]`).
- **פערי ידע מתועדים (`[[10_Knowledge-Gaps/]]`):** 2 (`[[Home-Oven-Convection-Variance]]`, `[[Collagen-Time-Curve-By-Animal-Age]]`).
- **כללי החלטה אופרטיביים (`[[12_Rules/]]`):** 6 כללים מחוברים ישירות למנוע `chef_mind`.

---

## ד. סטטוס פיתוח המערכת (Roadmap)

### שלב 1 — תשתית אונטולוגיה (הושלם):
1. [x] הקמת 14 ספריות האונטולוגיה תחת `Culinary-Knowledge/` וחיבור Junction ל-`llm_wiki/10_Projects/chef_mind`.
2. [x] הגדרת `[[Knowledge-Map]]`, `[[Relationships]]`, `[[Concepts]]` ו-7 תבניות YAML מובנות.

### שלב 2 — קליטת ידע ואינטגרציה למנוע `chef_mind` (הושלם):
1. [x] רישום 6 מקורות ליבה מוסמכים (`09_Sources/`) עם סיווגי אמינות (Tier 1 & Tier 2).
2. [x] אכלוס כל 8 תחומי הידע ב-53 רשומות מדעיות ויישומיות מקושרות.
3. [x] תיעוד 3 סתירות קולינריות מרכזיות (`11_Conflicts/`), 2 פערי ידע (`10_Knowledge-Gaps/`) ו-6 כללי החלטה (`12_Rules/`).
4. [x] חיבור ישיר למנוע `chef_mind` באמצעות `backend/app/ontology_bridge.py` וחיפוש היברידי סמנטי ב-`backend/app/retrieval.py`.
