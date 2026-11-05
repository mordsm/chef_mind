"""Build a lossless local source layer, page graph, recipe references and coverage.

Source pages are evidence, not verified culinary rules. Generated topic edges mean
literal mentions only. OCR and numeric/table layout review remain explicit.
"""

import hashlib
import json
import re
import sys
from pathlib import Path

import yaml

PROJECT = Path(__file__).resolve().parents[1]
VAULT = PROJECT / "vault/Culinary-Knowledge"
DEST = VAULT / "09_Sources/Full-Books"
SCRATCH = PROJECT / "tmp-book-processing"

CHAPTERS = [
    (1, 34, "פתיחה ותוכן עניינים"), (35, 79, "מלח"), (80, 128, "שומן"),
    (129, 163, "חומצה"), (164, 237, "חום ושיטות בישול"), (238, 243, "איזון ושימוש במתכונים"),
    (244, 258, "כלי מטבח וחומרי גלם"), (259, 289, "סלטים"), (290, 310, "רטבים לסלט"),
    (311, 330, "ירקות"), (331, 344, "צירים ומרקים"), (345, 374, "קטניות דגנים ופסטה"),
    (375, 383, "ביצים"), (384, 391, "דגים"), (392, 429, "עוף"), (430, 447, "בשר"),
    (448, 486, "רטבים וממרחים"), (487, 504, "בצקים ומאפים"), (505, 539, "קינוחים"),
    (540, 547, "תרגול והרכבת תפריטים"), (548, 559, "מקורות ותודות"), (560, 593, "מפתח ופרטי מהדורה"),
]
AVIR_CHAPTERS = [
    (1, 6, "פתיחה ותוכן עניינים"), (7, 10, "הקדמה"), (11, 54, "טעם וחושים"),
    (55, 72, "מלח"), (73, 97, "מים"), (98, 126, "השחמה וצלייה"),
    (127, 162, "ביצים"), (163, 204, "רטבים ותחליבים"), (205, 268, "בשר"),
    (269, 280, "תודות מתכונים ומפתח"),
]
# References transcribed from the book's own recipe list, PDF 272.
AVIR_RECIPES = [
    ("איולי קטלוני מקורי", 189), ("ארנצ'י אה פינוקי", 23), ("ארנצ'יני", 38),
    ("מקושקשת בחומץ לפי קלודיה רודן", 145), ("ביצה קשה כבושה בחומץ", 143),
    ("גזרים א־לה וישי", 87), ("ויניגרט אורן", 166), ("חמאה אגוזית", 100),
    ("טפנד", 191), ("ירקות צלויים לפי מאריו בטאלי", 109),
    ("לובסטונה תרמידור לפי רון מיסטרי", 75), ("מיונז בסיסי", 186), ("מלבי בסיסי", 197),
    ("מלח שמפניה", 72), ("מלח עם צ'ילי יבש", 72), ("מקושקשת של אסקופייה", 132),
    ("מקושקשת של תוכניות בישול", 133), ("מרק כרובית ממרכיב אחד", 61),
    ("מרק שלושה סוגי פטריות", 196), ("סופלה משני מרכיבים", 161),
    ("סטייק כיפת הצלע", 212), ("סטייק בגריל", 112), ("עוף סיני מאודה עם בוק צ'וי", 94),
    ("פסטה ירוקה ביתית", 149), ("פסטו", 191), ("פריטאטת תרד", 148), ("פשטידת תרד", 148),
    ("צ'יפס ביתי בטיגון יחיד לפי ז'ואל רובושון", 116), ("ציר עוף", 78),
    ("קארנה אסאצ'י", 144), ("קונפי אווז", 245), ("קציצות גבינה בהשראת גיל חובב", 151),
    ("הקרם ברולה הראשון", 155), ("קרפצ'יו טואלט של ארז קומרובסקי — הדגמה", 16),
    ("רוטב בשמל בסיסי", 194), ("רוטב חמאה ומרווה", 173),
    ("רוטב יין אדום לפי המזללה", 199), ("רוטב כוסברה מולקולרי", 202),
    ("רוטב פומודורו", 181), ("רוסטביף מהיר", 226), ("רוסטביף מושלם", 227),
    ("ריבת חלב", 121), ("שוק כבש בתנור", 197), ("שמן שום ובזיליקום", 171),
    ("תבשיל קדירה בסיסי", 240), ("התפודים הטובים בעולם", 91),
]
# Existing canonical graph nodes; these edges assert a mention, not agreement.
CONCEPTS = [
    ("FLV-TASTE-001", "Salt-Osmosis-And-Perception", "מלח", r"\b(salt|salting|brine|osmosis|diffusion)\b|מלח|המלחה|תמלחת"),
    ("FLV-BAL-001", "Acid-Fat-Balance", "חומצה ואיזון", r"\b(acid|acidity|sour|vinegar|lemon)\b|חומצ|חומץ|לימון"),
    ("FLV-AROMA-001", "Fat-Soluble-Volatile-Aromas", "שומן וארומה", r"\b(fat|oil|aroma|fragrant)\b|שומן|ארומ|שמן"),
    ("SCI-HEAT-001", "Heat-Transfer", "העברת חום", r"\b(heat|conduction|convection|radiation)\b|חום|הולכ|הסע"),
    ("SCI-CHEM-001", "Maillard-Reaction", "מייאר", r"maillard|מייאר|מאייר"),
    ("SCI-CHEM-002", "Caramelization-And-Emulsification", "קרמל ותחליבים", r"carameli|emuls|קרמל|תחליב|אמולסי"),
    ("SCI-CARB-001", "Starch-Gelatinization-Retrogradation", "עמילן", r"\b(starch|starches|gelatiniz)\b|עמילן|ג.לטיניז"),
    ("SCI-PROT-002", "Protein-Denaturation-Coagulation", "חלבונים", r"\b(protein|proteins|coagulat|denatur)\b|חלבו|דנטור|קריש"),
    ("SCI-PROT-001", "Collagen-Hydrolysis-Gelatin", "קולגן", r"\b(collagen|gelatin)\b|קולגן|ג.לטין"),
    ("ING-DAI-001", "Dairy-Butter-Emulsion", "חמאה ושמנת", r"\b(butter|cream|buttermilk)\b|חמאה|שמנת|רוויון"),
    ("ING-EGG-001", "Egg-Proteins-Yolk-Albumen", "ביצים", r"\b(egg|eggs|yolk|albumen|meringue)\b|ביצה|ביצים|חלמון|חלבון ביצה"),
    ("ING-POUL-001", "Poultry-Breast-Lean", "עוף", r"\b(chicken|poultry|turkey)\b|עוף|הודו"),
    ("ING-FISH-001", "Finfish-Muscle-Myotomes-Fat-And-Pigments", "דגים", r"\b(fish|salmon|tuna|cod)\b|דגים|סלמון|טונה"),
    ("ING-MEAT-001", "Beef-Chuck-Collagen-Rich", "בשר", r"\b(beef|steak|pork|lamb|braise)\b|בשר|סטייק|כתף|אסאדו"),
    ("ING-VEG-001", "Allium-Onion-Sulfur-Sugars", "בצל ושום", r"\b(onion|onions|shallot|garlic)\b|בצל|שום|שאלוט"),
    ("TEC-MOIST-001", "Gentle-Simmering-Poaching", "בעבוע ושליקה", r"\b(simmer|poach|coddle)\w*\b|בעבוע|שליקה|שליקת"),
    ("TEC-DRY-001", "High-Heat-Pan-Searing", "צריבה", r"\b(sear|searing|seared)\b|צריבה|צריבת"),
    ("TEC-COMB-001", "Low-Slow-Braising", "קדרה", r"\b(braise|braising|stew|stewing)\b|קדרה|קדירה|תבשיל"),
    ("TEC-EGG-004", "Meringue-Souffle-And-Sabayon-Whipping", "הקצפה", r"\b(whip|whipping|meringue|souffl)\w*\b|הקצפ|מרנג|סופלה"),
    ("TEC-EGG-003", "Custard-Water-Bath-Baking-And-Cream-Stirring", "קסטרד ואמבט מים", r"custard|bain.marie|water bath|קסטרד|קוסטרד|אמבט מים"),
    ("TEC-MEAT-004", "Resting-Carryover-Cooking-And-Carving", "מנוחה ופריסה", r"carryover|resting|against the grain|מנוחה|נגד הסיבים"),
    ("EQP-ENV-001", "Covered-Vs-Uncovered-Evaporation", "אידוי וכיסוי", r"\b(evaporat|steam|cover|uncovered)\w*\b|אידוי|אידו|מכסה|מכוסה"),
    ("EQP-PAN-001", "Cast-Iron-Vs-Stainless-Thermal-Mass", "כלי בישול", r"cast.iron|stainless|skillet|saucepan|מחבת|יציק|נירוסטה"),
    ("EQP-SENS-001", "Core-Probe-Thermometry", "מדידה", r"thermometer|מדחום"),
    ("TEX-CRUST-001", "Surface-Browning", "השחמה", r"\b(brown|browning|crust|crisp)\w*\b|השחמ|קראסט|פריך|פריכ"),
    ("TEX-VISC-001", "Starch-And-Emulsion-Viscosity", "הסמכה", r"\b(thicken|thickening|viscosity|roux)\w*\b|הסמכ|רביכה|צמיג"),
    ("DEC-PLAN-001", "Cut-To-Method-Matching", "בחירת שיטה", r"tough cut|tender cut|connective tissue|נתח|רקמת חיבור"),
]


def write_note(path, meta, body):
    path.parent.mkdir(parents=True, exist_ok=True)
    meta.update(project_scope="chef_mind", allowed_contexts=["chef_mind", "related_culinary_projects"],
                external_publication=False)
    path.write_text("---\n" + yaml.safe_dump(meta, allow_unicode=True, sort_keys=False) + "---\n\n" + body,
                    encoding="utf-8")


def normalize(text):
    return " ".join(text.split())


def curated_section(book):
    prefix = "EVD-NOS-" if book == "nosrat" else "EVD-AVR-"
    links = []
    for manifest in (VAULT / "09_Sources/Supplied-2026/manifest.json", DEST / "reviewed-manifest.json"):
        if not manifest.exists():
            continue
        for row in json.loads(manifest.read_text(encoding="utf-8"))["records"]:
            if row["id"].startswith(prefix):
                path = VAULT / row.get("path", f"03_Techniques/{row['id']}.md")
                meta = yaml.safe_load(path.read_text(encoding="utf-8").split("---", 2)[1])
                links.append(f"- [[{path.stem}|{meta['name']}]]")
    return "\n\n## הערות מעובדות בעברית\n\n" + "\n".join(links) + "\n"


def build(book):
    records = json.loads((SCRATCH / f"{book}-pages.json").read_text(encoding="utf-8"))
    source_id = "SRC-NOSRAT-2017" if book == "nosrat" else "SRC-AVIR-2019"
    title = "Salt, Fat, Acid, Heat" if book == "nosrat" else "לא ספר בישול"
    topics, chapter_pages, recipes, pages = {}, {}, [], []
    for record in records:
        n = record["pdf_page"]
        native = Path(record["text_path"]).read_text(encoding="utf-8")
        ocr_path = Path(record.get("ocr_path", "missing"))
        ocr = json.loads(ocr_path.read_text(encoding="utf-8")) if ocr_path.is_file() else None
        combined = native + "\n" + (ocr["text"] if ocr else "")
        matches = [c for c in CONCEPTS if re.search(c[3], combined, re.IGNORECASE)]
        book_chapters = CHAPTERS if book == "nosrat" else AVIR_CHAPTERS
        chapter = next((c for c in book_chapters if c[0] <= n <= c[1]), None)
        label = chapter[2] if chapter else "מקור סרוק"
        chapter_id = f"BOOK-{book.upper()}-CH-{chapter[0]:03}" if chapter else f"BOOK-{book.upper()}-SOURCE"
        page_id = f"PAGE-{book.upper()}-{n:03}"
        stem = f"{book}-page-{n:03}"
        path = DEST / "Pages" / book / f"{stem}.md"
        for concept in matches:
            topics.setdefault(concept[0], []).append((stem, n, book))
        chapter_pages.setdefault(chapter_id, []).append((stem, n))
        metadata = {"id": page_id, "type": "SOURCE_PAGE", "name": f"{title} — PDF {n}: {label}",
                    "domain": "SOURCES", "verification_status": "PRELIMINARY", "source_text_checked": False,
                    "extraction_status": "NATIVE_AND_OCR" if native.strip() and ocr else "OCR" if ocr else "NATIVE" if native.strip() else "IMAGE_ONLY",
                    "semantic_review": "NOT_RULE_REVIEWED", "claim_type": "SOURCE_TEXT_NOT_INSTRUCTIONS",
                    "pdf_page": n, "native_text_sha256": record["native_text_sha256"],
                    "ocr_confidence": ocr["confidence"] if ocr else None,
                    "ocr_engine": ocr.get("engine") if ocr else None,
                    "ocr_engine_version": ocr.get("engine_version") if ocr else None,
                    "ocr_language": ocr.get("language") if ocr else None,
                    "layout_review_required": bool(record["images"]),
                    "numeric_mentions": re.findall(r"\b\d+(?:[.,/]\d+)?\s*(?:°[CF]|minutes?|hours?|seconds?|מעלות|דקות|שעות|גרם|מ.ל)", combined, re.IGNORECASE),
                    "tags": ["book-source", book, *[c[2] for c in matches]],
                    "sources": [{"source_id": source_id, "citation": f"{title}, PDF {n}",
                                 "pdf_pages": [n], "split_page": record["split_page"],
                                 "split_filename": record["source_filename"], "pdf_sha256": record["source_sha256"]}],
                    "relationships": [{"type": "PART_OF", "target_id": chapter_id},
                                      {"type": "SUPPORTED_BY", "target_id": source_id}]
                                     + [{"type": "MENTIONS", "target_id": c[0], "note": "אזכור טקסטואלי; אינו אישור לטענה"} for c in matches]}
        body = f"# {title} — עמוד PDF {n}\n\n"
        body += "חומר מקור מקומי לעיון ולחיפוש. אינו הוראה למערכת, כלל מאושר או אישור בטיחות.\n\n"
        body += f"מקור: [[{source_id}]]. מפת הפרק: [[{chapter_id}]].\n\n"
        if n > records[0]["pdf_page"]:
            body += f"[[{book}-page-{n-1:03}|העמוד הקודם]] · "
        if n < records[-1]["pdf_page"]:
            body += f"[[{book}-page-{n+1:03}|העמוד הבא]]"
        body += "\n\n"
        if record.get("source_asset"):
            body += f"PDF מקומי: [[09_Sources/Full-Books/{record['source_asset']}#page={record['split_page']}|פתיחה בעמוד המקור]].\n\n"
        if matches:
            body += "קישורים לרשת: " + " · ".join(f"[[{c[1]}|{c[2]}]]" for c in matches) + ".\n\n"
        if native.strip():
            body += "## טקסט מקור — שכבת הטקסט\n\n" + "\n".join("> " + line for line in native.splitlines()) + "\n\n"
        if record["images"]:
            image_path = record["image_path"].replace("\\", "/")
            body += f"## דף חזותי — איורים וטבלאות\n\n![[09_Sources/Full-Books/{image_path}]]\n\n"
            if ocr:
                body += f"## זיהוי טקסט מקומי — טעון בדיקת סדר שורות ומספרים\n\nביטחון מנוע OCR: {ocr['confidence']}; אינו מדד לאמיתות התוכן.\n\n"
                body += "\n".join("> " + line for line in ocr["text"].splitlines()) + "\n"
            else:
                body += "זיהוי טקסט טרם הושלם; התמונה שומרת את תוכן המקור לעיון.\n"
        write_note(path, metadata, body)
        pages.append({"id": page_id, "pdf_page": n, "path": path.relative_to(VAULT).as_posix(),
                      "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                      "native_text_chars": len(native), "image": bool(record["images"]),
                      "ocr_done": bool(ocr), "ocr_confidence": ocr["confidence"] if ocr else None,
                      "concept_ids": [c[0] for c in matches]})
        if book == "nosrat" and 259 <= n <= 539:
            lines = [line.strip() for line in native.splitlines() if line.strip()]
            for index, line in enumerate(lines):
                if re.match(r"^(Serves|Makes|serves)\s+", line) and index:
                    name = lines[index - 1]
                    if len(name) < 110 and name not in ("Variations",):
                        recipes.append({"name": name, "yield": line, "page": n, "concepts": matches})
                    break
    if book == "avir":
        recipes = [{"name": name, "yield": "הפניה לפי רשימת המתכונים בעמוד 272", "page": page,
                    "concepts": [c for c in CONCEPTS if re.search(c[3], name, re.IGNORECASE)]}
                   for name, page in sorted(AVIR_RECIPES, key=lambda item: (item[1], item[0]))]
    for i, recipe in enumerate(recipes):
        start = recipe["page"]
        end = ((recipes[i + 1]["page"] - 1) if i + 1 < len(recipes) else 539) if book == "nosrat" else start
        end = max(start, end)
        name = recipe["name"]
        recipe_id = f"RECIPE-{book.upper()}-{start:03}" + (f"-{i+1:02}" if book == "avir" else "")
        recipe["id"] = recipe_id
        body = f"# {name}\n\n{recipe['yield']}\n\n"
        body += "רשומת הפניה למתכון המקורי ולווריאציות שלו. הכמויות, הסדר, הזמנים והחריגים נשמרים בדפי המקור המקושרים. זו אינה תוכנית בישול שאושרה לביצוע.\n\n"
        body += "\n".join(f"- [[{book}-page-{n:03}|עמוד PDF {n}]]" for n in range(start, end + 1))
        if book == "avir":
            body += "\n\nמקור רשימת ההפניות: [[avir-page-272]]. להמשך המתכון השתמש בקישור לעמוד הבא.\n"
            if start == 16:
                body += "\nזו הדגמה על חומר שאינו מזון, ולא מנה המיועדת למאכל.\n"
        meta = {"id": recipe_id, "type": "RECIPE_REFERENCE", "name": name, "domain": "TECHNIQUES",
                "verification_status": "PRELIMINARY", "source_text_checked": False,
                "claim_type": "REFERENCE_NOT_VALIDATED_RECIPE", "boundary_detection": "AUTOMATIC_REVIEW_REQUIRED" if book == "nosrat" else "APPENDIX_START_PAGE_ONLY",
                "pdf_pages": list(range(start, end + 1)), "yield_as_printed": recipe["yield"],
                "sources": [{"source_id": source_id, "citation": f"{title}, PDF {start}–{end}",
                             "pdf_pages": list(range(start, end + 1)), "pdf_sha256": records[0]["source_sha256"]}],
                "tags": ["recipe-reference", book, *[c[2] for c in recipe["concepts"]]],
                "relationships": [{"type": "SUPPORTED_BY", "target_id": source_id}]
                                 + [{"type": "PART_OF", "target_id": f"PAGE-{book.upper()}-{start:03}"}]
                                 + [{"type": "MENTIONS", "target_id": c[0]} for c in recipe["concepts"]]}
        write_note(DEST / "Recipes" / f"{recipe_id}.md", meta, body)
    for chapter_id, chapter_list in chapter_pages.items():
        first = chapter_list[0][1]
        book_chapters = CHAPTERS if book == "nosrat" else AVIR_CHAPTERS
        label = next((c[2] for c in book_chapters if c[0] <= first <= c[1]), "מקור סרוק")
        links = "\n".join(f"- [[{stem}|PDF {n}]]" for stem, n in chapter_list)
        meta = {"id": chapter_id, "type": "SOURCE_CHAPTER", "name": f"{title} — {label}",
                "domain": "SOURCES", "verification_status": "PRELIMINARY", "source_text_checked": False,
                "relationships": [{"type": "PART_OF", "target_id": source_id}]}
        write_note(DEST / "Chapters" / f"{chapter_id}.md", meta, f"# {title} — {label}\n\nמפת כיסוי של דפי המקור; המפה אינה מציינת אישור של כל הטענות.\n\n{links}\n")
    for concept_id, stem, label, _ in CONCEPTS:
        refs = topics.get(concept_id, [])
        meta = {"id": f"MAP-{book.upper()}-{concept_id}", "type": "TOPIC_SOURCE_MAP",
                "name": f"{title} — {label}", "domain": "SOURCES", "verification_status": "PRELIMINARY",
                "relationships": [{"type": "MENTIONS", "target_id": concept_id},
                                  {"type": "SUPPORTED_BY", "target_id": source_id}]}
        body = f"# {label} — {title}\n\nמושג קיים: [[{stem}]]. המיפוי אוטומטי לפי אזכור ואינו מוכיח התאמה או הסכמה.\n\n"
        body += "\n".join(f"- [[{page_stem}|PDF {n}]]" for page_stem, n, _ in refs)
        write_note(DEST / "Topics" / f"{meta['id']}.md", meta, body + "\n")
    report = {"book": book, "source_id": source_id, "total_pages": len(pages),
              "pages_captured": len(pages), "image_pages": sum(p["image"] for p in pages),
              "ocr_pages_done": sum(p["ocr_done"] for p in pages),
              "ocr_pages_pending": [p["pdf_page"] for p in pages if p["image"] and not p["ocr_done"]],
              "low_confidence_ocr_pages": [p["pdf_page"] for p in pages if p["ocr_done"] and p["ocr_confidence"] < 70],
              "recipe_references": len(recipes), "chapter_maps": len(chapter_pages),
              "topic_maps": len(CONCEPTS), "semantic_rule_review": "PARTIAL_NOT_COMPLETE", "pages": pages}
    (DEST / f"{book}-coverage.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    index = f"# {title} — מפת הספר המלאה\n\nכל {len(pages)} העמודים נשמרו בשכבת מקור מקומית, עם עמודי PDF וגיבובי תוכן.\n\n"
    index += f"נבנו {len(recipes)} הפניות למתכונים, {len(chapter_pages)} מפות פרקים ו־{len(CONCEPTS)} מפות נושא.\n\n"
    index += "**קליטה אינה אימות:** תוכן OCR, טבלאות, מספרים, גבולות מתכונים וטענות מדעיות טעונים עיון. אין להפעיל אותם אוטומטית ככללי בישול.\n\n"
    index += "\n".join(f"- [[{chapter_id}]]" for chapter_id in chapter_pages)
    index += "\n\n## הפניות למתכונים ולהדגמות\n\n" + "\n".join(f"- [[{r['id']}|{r['name']}]]" for r in recipes)
    index += curated_section(book)
    write_note(DEST / f"{book}-Full-Book-Map.md", {"id": f"BOOK-{book.upper()}-FULL-MAP", "type": "SOURCE_INDEX",
               "name": f"{title} — מפת הספר המלאה", "domain": "SOURCES", "verification_status": "PRELIMINARY",
               "relationships": [{"type": "PART_OF", "target_id": source_id}]}, index + "\n")
    print(json.dumps({key: value for key, value in report.items() if key != "pages"}, ensure_ascii=True))


if __name__ == "__main__":
    build(sys.argv[1])
