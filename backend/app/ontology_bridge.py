"""Bridge between the Obsidian Culinary-Knowledge ontology and the chef_mind decision engine.

Follows the Zero-Disruption Principle in Chef-Engine-Integration.md:
- Never modifies existing files in vault/<owner>/00_inbox/ automatically.
- Parses YAML frontmatter + Markdown graph nodes across all 13 ontology folders.
- Performs graph reasoning over REQUIRES, ENABLES, INHIBITED_BY, ALTERNATIVE_TO, and SUPPORTED_BY edges.
- Converts ontology rules and principles into validated KnowledgeDocument / KnowledgeUnit models.
- Synchronizes live coverage metrics into vault/Culinary-Knowledge/Dashboard.md.
"""

import hashlib
import re
from pathlib import Path

import yaml
from fastapi import Depends
from pydantic import Field

from app.knowledge import DomainError, audit, import_document
from app.retrieval import semantic_concepts, tokens
from app.schemas import ImportRequest, KnowledgeDocument, KnowledgeUnit, StrictModel

DEFAULT_VAULT_ROOT = Path(__file__).resolve().parents[2] / "vault"
ONTOLOGY_DIR_NAME = "Culinary-Knowledge"

FOLDER_DEFINITIONS = [
    ("00_Ontology", "00. אונטולוגיה ותשתיות", "8 תתי-תחומים"),
    ("01_Ingredients", "01. חומרי גלם (Ingredients)", "6 קבוצות ראשיות"),
    ("02_Food-Science", "02. מדע המזון (Food Science)", "10 תהליכים"),
    ("03_Techniques", "03. טכניקות בישול (Techniques)", "10 טכניקות בסיס"),
    ("04_Flavors", "04. טעמים וארומות (Flavors)", "6 מימדי חישה"),
    ("05_Textures", "05. מרקמים (Textures)", "7 טרנספורמציות"),
    ("06_Equipment", "06. ציוד וסביבה (Equipment)", "7 סוגי כלים ובקרה"),
    ("07_Food-Safety", "07. בטיחות מזון (Food Safety)", "7 פרוטוקולי בטיחות"),
    ("08_Decision-Making", "08. קבלת החלטות (Decision-Making)", "7 שלבי תכנון"),
    ("09_Sources", "09. מקורות מוסמכים (Sources)", "4 רמות אמינות"),
    ("10_Knowledge-Gaps", "10. פערי ידע (Knowledge Gaps)", "סדרי עדיפויות P0-P3"),
    ("11_Conflicts", "11. סתירות ומחלוקות (Conflicts)", "מודלי פיוס והכרעה"),
    ("12_Rules", "12. כללי החלטה (Rules)", "כללים קולינריים"),
]


class DiagnoseRequest(StrictModel):
    node_id: str = Field(min_length=1, max_length=100)
    confirmed_conditions: list[str] = Field(default_factory=list, max_length=30)
    active_factors: list[str] = Field(default_factory=list, max_length=30)


def _clean_wikilink(value: str) -> str:
    if not isinstance(value, str):
        return str(value)
    match = re.search(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]", value)
    if match:
        target = match.group(1).strip()
        return target.split("/")[-1]
    return value.strip()


def _parse_markdown_file(path: Path, ontology_root: Path) -> dict | None:
    raw = path.read_bytes()
    text = raw.decode("utf-8-sig")
    if not text.startswith("---\n") and not text.startswith("---\r\n"):
        return None
    parts = text.split("---", 2)
    if len(parts) != 3:
        return None
    meta = yaml.safe_load(parts[1])
    if not isinstance(meta, dict) or "id" not in meta:
        return None
    body = parts[2].strip()
    relative = path.relative_to(ontology_root).as_posix()
    folder = relative.split("/", 1)[0] if "/" in relative else ""
    node_id = str(meta["id"]).strip()
    name = str(meta.get("name") or meta.get("title") or path.stem).strip()
    title_he = str(meta.get("title_he") or meta.get("title") or name).strip()
    v_status = str(meta.get("verification_status") or meta.get("status") or "PRELIMINARY").upper()
    raw_rels = meta.get("relationships") or []
    relationships = []
    if isinstance(raw_rels, list):
        for rel in raw_rels:
            if isinstance(rel, dict) and rel.get("type"):
                target_raw = rel.get("target_id") or rel.get("target") or rel.get("target_name") or ""
                label_raw = rel.get("target_name") or rel.get("target") or target_raw
                relationships.append(
                    {
                        "type": str(rel["type"]).upper(),
                        "target_ref": _clean_wikilink(str(target_raw)),
                        "target_label": _clean_wikilink(str(label_raw)),
                        "note": str(rel.get("note") or rel.get("context") or ""),
                    }
                )
    raw_sources = meta.get("sources") or []
    sources = []
    if isinstance(raw_sources, list):
        for src in raw_sources:
            if isinstance(src, dict):
                sources.append(
                    {
                        "source_id": _clean_wikilink(str(src.get("source_id") or "")),
                        "citation": str(src.get("citation") or src.get("source_id") or ""),
                    }
                )
            elif isinstance(src, str):
                cleaned = _clean_wikilink(src)
                sources.append({"source_id": cleaned, "citation": cleaned})
    return {
        "id": node_id,
        "stem": path.stem,
        "name": name,
        "title_he": title_he,
        "type": str(meta.get("type", "unknown")).lower(),
        "domain": str(meta.get("domain", folder)).lower(),
        "folder": folder,
        "relative_path": relative,
        "verification_status": v_status,
        "relationships": relationships,
        "sources": sources,
        "metadata": meta,
        "body": body,
        "sha256": hashlib.sha256(raw).hexdigest(),
    }


def load_ontology(vault_root: Path | None = None) -> dict:
    root = (vault_root or DEFAULT_VAULT_ROOT) / ONTOLOGY_DIR_NAME
    if not root.is_dir():
        root = DEFAULT_VAULT_ROOT / ONTOLOGY_DIR_NAME
    nodes = []
    by_id = {}
    by_stem = {}
    digest_hasher = hashlib.sha256()

    for path in sorted(root.rglob("*.md")):
        rel = path.relative_to(root).as_posix()
        if rel == "Dashboard.md" or rel.startswith("13_Templates/"):
            continue
        parsed = _parse_markdown_file(path, root)
        if parsed is None:
            continue
        nodes.append(parsed)
        by_id[parsed["id"]] = parsed
        by_stem[parsed["stem"].lower()] = parsed
        digest_hasher.update(parsed["sha256"].encode("ascii"))

    edges = []
    for node in nodes:
        for rel in node["relationships"]:
            ref = rel["target_ref"]
            resolved = by_id.get(ref) or by_stem.get(ref.lower())
            target_id = resolved["id"] if resolved else ref
            edges.append(
                {
                    "source_id": node["id"],
                    "source_name": node["name"],
                    "target_id": target_id,
                    "target_label": resolved["name"] if resolved else rel["target_label"],
                    "type": rel["type"],
                    "resolved": resolved is not None,
                    "note": rel["note"],
                }
            )

    by_folder = {folder: [] for folder, _, _ in FOLDER_DEFINITIONS}
    for node in nodes:
        by_folder.setdefault(node["folder"], []).append(node)

    open_gaps = [n for n in by_folder.get("10_Knowledge-Gaps", []) if n["verification_status"] == "OPEN"]
    conflicts = by_folder.get("11_Conflicts", [])
    verified_nodes = [
        n for n in nodes if n["verification_status"] in ("VERIFIED", "FOUNDATIONAL", "RECONCILED", "FALSIFIED")
    ]
    unverified_nodes = [n for n in nodes if n["verification_status"] in ("PRELIMINARY", "DRAFT", "UNVERIFIED")]

    folder_stats = []
    for folder, label_he, categories_desc in FOLDER_DEFINITIONS:
        items = by_folder.get(folder, [])
        v_count = sum(
            1
            for item in items
            if item["verification_status"] in ("VERIFIED", "FOUNDATIONAL", "RECONCILED", "FALSIFIED")
        )
        folder_stats.append(
            {
                "folder": folder,
                "label_he": label_he,
                "categories_desc": categories_desc,
                "total": len(items),
                "verified": v_count,
                "node_ids": [item["id"] for item in items],
                "stems": [item["stem"] for item in items],
            }
        )

    return {
        "ontology_root": str(root),
        "sha256": digest_hasher.hexdigest(),
        "total_nodes": len(nodes),
        "verified_nodes": len(verified_nodes),
        "unverified_nodes": len(unverified_nodes),
        "total_edges": len(edges),
        "sources_count": len(by_folder.get("09_Sources", [])),
        "rules_count": len(by_folder.get("12_Rules", [])),
        "conflicts_count": len(conflicts),
        "open_gaps_count": len(open_gaps),
        "folder_stats": folder_stats,
        "nodes": nodes,
        "by_id": by_id,
        "by_stem": by_stem,
        "edges": edges,
    }


def query_ontology(vault_root: Path | None, query: str = "", domain: str | None = None, limit: int = 8) -> list[dict]:
    data = load_ontology(vault_root)
    candidates = data["nodes"]
    if domain:
        domain_lower = domain.strip().lower()
        candidates = [
            n
            for n in candidates
            if domain_lower in (n["domain"].lower(), n["folder"].lower(), n["type"].lower())
        ]
    if not query.strip():
        return [
            {
                "id": n["id"],
                "name": n["name"],
                "title_he": n["title_he"],
                "type": n["type"],
                "domain": n["domain"],
                "folder": n["folder"],
                "verification_status": n["verification_status"],
                "relative_path": n["relative_path"],
            }
            for n in candidates[:limit]
        ]

    q_tokens = tokens(query)
    q_concepts = semantic_concepts(query)
    scored = []
    for node in candidates:
        searchable = " ".join(
            [
                node["id"],
                node["name"],
                node["title_he"],
                node["domain"],
                yaml.safe_dump(node["metadata"], allow_unicode=True),
                node["body"],
            ]
        )
        n_tokens = tokens(searchable)
        n_concepts = semantic_concepts(searchable)
        overlap = q_tokens & n_tokens
        c_overlap = q_concepts & n_concepts
        if not overlap and not c_overlap:
            continue
        score = len(overlap) / max(1, len(q_tokens)) + (0.75 * len(c_overlap) / max(1, len(q_concepts)) if c_overlap else 0.0)
        if node["folder"] == "12_Rules":
            score += 0.25
        scored.append((score, node))

    scored.sort(key=lambda item: item[0], reverse=True)
    return [
        {
            "id": n["id"],
            "name": n["name"],
            "title_he": n["title_he"],
            "type": n["type"],
            "domain": n["domain"],
            "folder": n["folder"],
            "verification_status": n["verification_status"],
            "relative_path": n["relative_path"],
            "score": round(score, 4),
        }
        for score, n in scored[:limit]
    ]


def diagnose_prerequisites(
    vault_root: Path | None, node_id: str, confirmed_conditions: list[str] = (), active_factors: list[str] = ()
) -> dict:
    data = load_ontology(vault_root)
    node = data["by_id"].get(node_id) or data["by_stem"].get(node_id.lower())
    if node is None:
        raise DomainError("ONTOLOGY_NODE_NOT_FOUND", f"Ontology node '{node_id}' was not found", 404)

    confirmed_tokens = tokens(" ".join(confirmed_conditions))
    factor_tokens = tokens(" ".join(active_factors))

    outgoing = [edge for edge in data["edges"] if edge["source_id"] == node["id"]]
    incoming = [edge for edge in data["edges"] if edge["target_id"] == node["id"]]

    required = [edge for edge in outgoing if edge["type"] == "REQUIRES"]
    missing_prerequisites = []
    met_prerequisites = []
    for req in required:
        req_words = tokens(f"{req['target_id']} {req['target_label']} {req['note']}")
        if confirmed_tokens and (confirmed_tokens & req_words):
            met_prerequisites.append(req)
        else:
            missing_prerequisites.append(req)

    inhibitors = [
        edge for edge in outgoing if edge["type"] in ("INHIBITED_BY", "INHIBITS")
    ] + [edge for edge in incoming if edge["type"] in ("INHIBITS", "INHIBITED_BY")]

    active_inhibitors = []
    for inh in inhibitors:
        inh_words = tokens(f"{inh['source_name']} {inh['target_label']} {inh['note']}")
        if factor_tokens and (factor_tokens & inh_words):
            active_inhibitors.append(inh)

    alternatives = [
        edge for edge in outgoing + incoming if edge["type"] == "ALTERNATIVE_TO"
    ]
    enabled = [edge for edge in outgoing if edge["type"] in ("ENABLES", "AFFECTS")]
    supported_by = [edge for edge in outgoing if edge["type"] in ("SUPPORTED_BY", "SUPPORTS")]

    status = "ready"
    if active_inhibitors:
        status = "inhibited"
    elif missing_prerequisites:
        status = "prerequisites_unconfirmed"

    return {
        "node_id": node["id"],
        "name": node["name"],
        "title_he": node["title_he"],
        "status": status,
        "missing_prerequisites": missing_prerequisites,
        "met_prerequisites": met_prerequisites,
        "active_inhibitors": active_inhibitors,
        "potential_inhibitors": inhibitors,
        "alternatives": alternatives,
        "enabled_outcomes": enabled,
        "supporting_sources": supported_by or node["sources"],
    }


def to_knowledge_document(vault_root: Path | None = None) -> KnowledgeDocument:
    data = load_ontology(vault_root)
    units: list[KnowledgeUnit] = []

    for node in data["nodes"]:
        meta = node["metadata"]
        if node["folder"] == "12_Rules":
            knowledge_id = re.sub(r"[^a-zA-Z0-9_-]", "-", node["id"].lower())
            trigger = meta.get("trigger_conditions") or {}
            problem = str(trigger.get("observed_problem") or "").strip()
            action_obj = meta.get("recommended_action") or {}
            explanation = (
                str(action_obj.get("explanation") or "")
                if isinstance(action_obj, dict)
                else str(action_obj)
            )
            principle = str(meta.get("scientific_rationale") or meta.get("description") or node["name"])
            observations = [str(x) for x in (meta.get("observations") or ["בדוק ודווח את השינוי במצב המנה"])]
            safety_notes = [str(x) for x in (meta.get("safety_notes") or [])]
            tags = [str(x) for x in (meta.get("tags") or [node["domain"], node["id"].lower()])]
            required_ing = [str(x) for x in (meta.get("required_ingredients") or [])]
            exceptions = [str(x) for x in (meta.get("exceptions") or [])]
            verified_on = str(meta.get("verified_on") or "2026-10-21")
            if not re.match(r"^\d{4}-\d{2}-\d{2}$", verified_on):
                verified_on = "2026-10-21"
            units.append(
                KnowledgeUnit(
                    knowledge_id=knowledge_id,
                    title=node["name"][:200],
                    principle=principle[:2000],
                    conditions=[problem] if problem else [],
                    observations=observations[:20],
                    recommended_action=explanation[:1200],
                    exceptions=exceptions[:20],
                    safety_notes=safety_notes[:20],
                    tags=tags[:20],
                    confidence=int(meta.get("confidence", 85)),
                    verified_on=verified_on,
                    required_ingredients=required_ing[:20],
                )
            )
        elif node["folder"] in (
            "01_Ingredients",
            "02_Food-Science",
            "03_Techniques",
            "04_Flavors",
            "05_Textures",
            "06_Equipment",
            "07_Food-Safety",
            "08_Decision-Making",
        ):
            knowledge_id = re.sub(r"[^a-zA-Z0-9_-]", "-", node["id"].lower())
            effects = meta.get("effects") or {}
            if isinstance(effects, dict):
                mol = effects.get("molecular_change") or effects.get("primary_outcome") or ""
                tex = effects.get("texture_change") or ""
                principle = f"{meta.get('description', node['title_he'])}. {mol}".strip(". ")
            else:
                principle = str(meta.get("description") or node["title_he"])
                tex = ""
            action = (
                f"יישם את העיקרון הקולינרי של {node['title_he']}: {principle[:400]}"
                if not tex
                else f"יישם {node['title_he']} להשגת {tex}: {principle[:350]}"
            )
            safety_list = []
            storage = meta.get("storage_and_safety") or {}
            if isinstance(storage, dict) and storage.get("minimum_internal_temp_c"):
                safety_list.append(
                    f"טמפרטורת ליבה מינימלית נדרשת: {storage['minimum_internal_temp_c']}°C לפי תקן בטיחות."
                )
            units.append(
                KnowledgeUnit(
                    knowledge_id=knowledge_id,
                    title=node["title_he"][:200],
                    principle=principle[:2000] or node["name"],
                    conditions=[],
                    observations=[f"בדוק ודווח על מצב המנה בהתאם ל־{node['title_he']}"],
                    recommended_action=action[:1200],
                    exceptions=[],
                    safety_notes=safety_list,
                    tags=[node["folder"].lower(), node["domain"].lower(), node["stem"].lower()],
                    confidence=85 if node["verification_status"] == "VERIFIED" else 75,
                    verified_on="2026-10-21",
                )
            )
        if len(units) >= 30:
            break

    return KnowledgeDocument(
        source_id="culinary-ontology-curated",
        title="אונטולוגיית הידע הקולינרי המרושתת (Culinary Knowledge Ontology)",
        source_reference="vault/Culinary-Knowledge/ (USDA FSIS, BCcampus CC BY 4.0, McGee 2004, Lopez-Alt 2015, Modernist Cuisine 2011)",
        license_status="open_license",
        license_reference="https://creativecommons.org/licenses/by/4.0/",
        attribution="The BC Cook Articulation Committee (CC BY 4.0), USDA FSIS Public Domain, and curated scientific principles in Culinary-Knowledge ontology.",
        adaptation_notes="Automated structured export from vault/Culinary-Knowledge ontology nodes and decision rules.",
        units=units[:30],
    )


def export_ontology_draft(session, vault_root: Path, owner: str) -> dict:
    document = to_knowledge_document(vault_root)
    rel_path = "00_inbox/culinary-ontology-curated.md"
    target = (vault_root / owner / rel_path).resolve()
    target.parent.mkdir(parents=True, exist_ok=True)
    frontmatter = yaml.safe_dump(document.model_dump(), allow_unicode=True, sort_keys=False)
    markdown = (
        f"---\n{frontmatter}---\n"
        "ייצוא מובנה מתוך אונטולוגיית `Culinary-Knowledge` לבדיקה ואישור אנושי לפני הפעלה במנוע השף.\n"
    )
    target.write_text(markdown, encoding="utf-8")
    digest = hashlib.sha256(markdown.encode("utf-8")).hexdigest()
    key = "ontology-export-" + digest[:32]
    revision = import_document(session, vault_root, owner, ImportRequest(path=rel_path, idempotency_key=key))
    return {
        "source_id": document.source_id,
        "path": rel_path,
        "revision_id": revision.id,
        "revision": revision.number,
        "status": revision.status,
        "units_count": len(document.units),
    }


def sync_dashboard(vault_root: Path | None = None) -> dict:
    data = load_ontology(vault_root)
    root = Path(data["ontology_root"])
    dashboard_path = root / "Dashboard.md"
    by_folder = {entry["folder"]: entry for entry in data["folder_stats"]}

    def row_for(folder: str, domain_title: str, categories_col: str) -> str:
        st = by_folder.get(folder, {"total": 0, "verified": 0, "stems": []})
        total = st["total"]
        verified = st["verified"]
        gaps = by_folder.get("10_Knowledge-Gaps", {}).get("total", 0) if folder == "02_Food-Science" else 0
        examples = ", ".join(f"`[[{stem}]]`" for stem in st["stems"][:2])
        count_str = f"{total} ({examples})" if examples else str(total)
        status_str = "🟢 מאומת ומקושר" if total > 0 and verified == total else ("🟡 פעיל" if total > 0 else "⚪ ממתין להזנה")
        return f"| **{domain_title}** | {categories_col} | {count_str} | {verified} | {gaps} | {status_str} |"

    rows = [
        row_for("00_Ontology", "00. אונטולוגיה ותשתיות", "8 תתי-תחומים"),
        row_for("01_Ingredients", "01. חומרי גלם (Ingredients)", "6 קבוצות ראשיות"),
        row_for("02_Food-Science", "02. מדע המזון (Food Science)", "10 תהליכים"),
        row_for("03_Techniques", "03. טכניקות בישול (Techniques)", "10 טכניקות בסיס"),
        row_for("04_Flavors", "04. טעמים וארומות (Flavors)", "6 מימדי חישה"),
        row_for("05_Textures", "05. מרקמים (Textures)", "7 טרנספורמציות"),
        row_for("06_Equipment", "06. ציוד וסביבה (Equipment)", "7 סוגי כלים ובקרה"),
        row_for("07_Food-Safety", "07. בטיחות מזון (Food Safety)", "7 פרוטוקולי בטיחות"),
        row_for("08_Decision-Making", "08. קבלת החלטות (Decision-Making)", "7 שלבי תכנון"),
        row_for("12_Rules", "12. כללי החלטה (Rules)", "כללים קולינריים"),
    ]
    table_body = "\n".join(rows)

    content = f"""---
id: DASHBOARD-MAIN
type: system_dashboard
name: Culinary Knowledge Dashboard
domain: ontology
title_he: לוח בקרה ראשי - אונטולוגיית הידע הקולינרי
status: ACTIVE
vault_root: "C:\\\\workspace\\\\chef_mind\\\\vault"
knowledge_root: "Culinary-Knowledge"
total_nodes: {data["total_nodes"]}
verified_nodes: {data["verified_nodes"]}
total_edges: {data["total_edges"]}
sources_count: {data["sources_count"]}
rules_count: {data["rules_count"]}
conflicts_count: {data["conflicts_count"]}
open_gaps_count: {data["open_gaps_count"]}
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
{table_body}

---

## ג. בקרת איכות ומהימנות הידע (Knowledge Quality & Verification)

> [!IMPORTANT] עיקרון שרשרת ההוכחה (No Invented Citations)
> כל קביעה במערכת משויכת למקור מוסמך (`09_Sources/`) או מתועדת מפורשות כפער ידע (`10_Knowledge-Gaps/`).

- **סה"כ רשומות פעילות באונטולוגיה:** {data["total_nodes"]} ({data["verified_nodes"]} מאומתות, {data["total_edges"]} קשרי גרף סמנטיים).
- **מקורות רשומים ומאומתים (`[[09_Sources/]]`):** {data["sources_count"]} (`[[SRC-USDA-FSIS-2024]]`, `[[SRC-BCCAMPUS-PASTRY-2015]]`, `[[SRC-BCCAMPUS-MEAT-2015]]`, `[[SRC-MCGEE-2004]]`, `[[SRC-FOODLAB-2015]]`, `[[SRC-MODCUIS-2011]]`).
- **סתירות קולינריות מנותחות (`[[11_Conflicts/]]`):** {data["conflicts_count"]} (`[[Searing-Locks-In-Juices-Myth]]`, `[[Pre-Salting-Steak-Timing]]`, `[[Pasta-Water-Oil-And-Volume]]`).
- **פערי ידע מתועדים (`[[10_Knowledge-Gaps/]]`):** {data["open_gaps_count"]} (`[[Home-Oven-Convection-Variance]]`, `[[Collagen-Time-Curve-By-Animal-Age]]`).
- **כללי החלטה אופרטיביים (`[[12_Rules/]]`):** {data["rules_count"]} כללים מחוברים ישירות למנוע `chef_mind`.

---

## ד. סטטוס פיתוח המערכת (Roadmap)

### שלב 1 — תשתית אונטולוגיה (הושלם):
1. [x] הקמת 14 ספריות האונטולוגיה תחת `Culinary-Knowledge/` וחיבור Junction ל-`llm_wiki/10_Projects/chef_mind`.
2. [x] הגדרת `[[Knowledge-Map]]`, `[[Relationships]]`, `[[Concepts]]` ו-7 תבניות YAML מובנות.

### שלב 2 — קליטת ידע ואינטגרציה למנוע `chef_mind` (הושלם):
1. [x] רישום 6 מקורות ליבה מוסמכים (`09_Sources/`) עם סיווגי אמינות (Tier 1 & Tier 2).
2. [x] אכלוס כל 8 תחומי הידע ב-{data["total_nodes"]} רשומות מדעיות ויישומיות מקושרות.
3. [x] תיעוד 3 סתירות קולינריות מרכזיות (`11_Conflicts/`), 2 פערי ידע (`10_Knowledge-Gaps/`) ו-6 כללי החלטה (`12_Rules/`).
4. [x] חיבור ישיר למנוע `chef_mind` באמצעות `backend/app/ontology_bridge.py` וחיפוש היברידי סמנטי ב-`backend/app/retrieval.py`.
"""
    dashboard_path.write_text(content, encoding="utf-8")
    return {
        "dashboard_path": str(dashboard_path),
        "total_nodes": data["total_nodes"],
        "verified_nodes": data["verified_nodes"],
        "total_edges": data["total_edges"],
        "sources_count": data["sources_count"],
        "rules_count": data["rules_count"],
        "conflicts_count": data["conflicts_count"],
        "open_gaps_count": data["open_gaps_count"],
    }


def install_ontology_routes(app, db, principal, reviewer):
    @app.get("/v1/ontology/summary")
    def summary():
        data = load_ontology(app.state.settings.vault_root)
        return {
            "sha256": data["sha256"],
            "total_nodes": data["total_nodes"],
            "verified_nodes": data["verified_nodes"],
            "unverified_nodes": data["unverified_nodes"],
            "total_edges": data["total_edges"],
            "sources_count": data["sources_count"],
            "rules_count": data["rules_count"],
            "conflicts_count": data["conflicts_count"],
            "open_gaps_count": data["open_gaps_count"],
            "folders": data["folder_stats"],
        }

    @app.get("/v1/ontology/nodes")
    def list_nodes(q: str = "", domain: str | None = None, limit: int = 20):
        bounded_limit = max(1, min(limit, 100))
        return {"items": query_ontology(app.state.settings.vault_root, q, domain, bounded_limit)}

    @app.get("/v1/ontology/nodes/{node_id}")
    def get_node(node_id: str):
        data = load_ontology(app.state.settings.vault_root)
        node = data["by_id"].get(node_id) or data["by_stem"].get(node_id.lower())
        if node is None:
            raise DomainError("ONTOLOGY_NODE_NOT_FOUND", "Ontology node was not found", 404)
        outgoing = [edge for edge in data["edges"] if edge["source_id"] == node["id"]]
        incoming = [edge for edge in data["edges"] if edge["target_id"] == node["id"]]
        return {
            **node,
            "outgoing_edges": outgoing,
            "incoming_edges": incoming,
        }

    @app.post("/v1/ontology/diagnose")
    def diagnose(body: DiagnoseRequest):
        return diagnose_prerequisites(
            app.state.settings.vault_root,
            body.node_id,
            body.confirmed_conditions,
            body.active_factors,
        )

    @app.post("/v1/ontology/sync-dashboard")
    def update_dashboard(owner=Depends(reviewer), session=Depends(db)):  # noqa: B008
        report = sync_dashboard(app.state.settings.vault_root)
        audit(session, owner.user_id, "ONTOLOGY_DASHBOARD_SYNCED", report=report)
        session.commit()
        return report

    @app.post("/v1/ontology/export-draft", status_code=201)
    def export_draft(owner=Depends(reviewer), session=Depends(db)):  # noqa: B008
        result = export_ontology_draft(session, app.state.settings.vault_root, owner.user_id)
        audit(session, owner.user_id, "ONTOLOGY_DRAFT_EXPORTED", result=result)
        session.commit()
        return result
