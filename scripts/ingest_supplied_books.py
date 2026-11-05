"""Rebuild curated paraphrases; source PDFs are never copied into the repository.

Run with Python + PyYAML. PDF page references are one-based within each supplied
part; scanned Hebrew pages were read visually, not OCRed. This is a curated slice,
not a claim that the books have been exhaustively processed.
"""

import argparse
import hashlib
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1] / "vault/Culinary-Knowledge"
# title, aliases, method, part, page(s), paraphrase, conditions, checkpoints
NOSRAT = [
    ("המלחת ירקות מימיים לפני צלייה", ["קישואים", "חצילים", "zucchini", "eggplant"], "oven_roast", 0, [55],
     "אפשר להמליח ירקות מימיים כרבע שעה לפני הצלייה. יבש את הנוזל שהצטבר לפני הכנסת הירקות לחום.", {}, ["פני הירק יבשים לפני הצלייה"]),
    ("המלחת פטריות לאחר תחילת ההשחמה", ["פטריות", "mushrooms"], "pan_sear", 0, [55],
     "כדי לשמור על מרקם הפטריות במחבת, הוסף מלח לאחר שהן מתחילות להשחים.", {}, ["נראית תחילת השחמה לפני הוספת המלח"]),
    ("מלח ובישול עדין של קטניות", ["שעועית", "חומוס", "beans", "chickpeas"], "boil_simmer", 0, [55],
     "אפשר להוסיף מלח בתחילת ההשריה או הבישול. אם הקטניות עדיין קשות, בדוק גם את גילן ואת חומציות הנוזל; המשך בישול לפי ההוראות המתאימות לסוג הקטנית.", {}, ["בדוק רכות במרכז; משך הבישול תלוי בסוג ובגיל הקטניות"]),
    ("המלחה מתונה של נוזל תבשיל", ["תבשיל בשר", "בשר בסיר", "braise", "stew"], "boil_simmer", 0, [59],
     "המלח את נוזל התבשיל במתינות: גם המלח מהבשר עובר לרוטב. תקן תיבול בסיום, כשהמנה מוכנה לטעימה.", {}, ["בדוק תיבול לאחר השלמת הבישול"]),
    ("ריכוך חריפות בצל לרוטב סלט", ["בצל", "שאלוט", "shallot", "onion"], "", 0, [150],
     "לרוטב סלט, צפה בצל או שאלוט בחומץ או במיץ הדרים והמתן 15–20 דקות לפני הוספת השמן. אין צורך להטביע את הבצל בנוזל.", {"duration_range": "15–20 minutes, salad dressing preparation"}, ["הוסף שמן אחרי ההשריה בחומצה"]),
    ("עצירת בישול ירקות אחרי חליטה", ["ירקות", "גזר", "כרובית", "שעועית ירוקה", "vegetables"], "boil_simmer", 0, [209],
     "הכן מסננת ותבנית לפני החליטה. בדוק חתיכה במהלך הבישול, וסנן ופרוס את הירקות בשכבה במקום לערום אותם חמים בקערה.", {}, ["בדוק את המרקם הרצוי לפני הסינון"]),
    ("צליית סלק קטן מכוסה", ["סלק", "beets", "beetroot"], "oven_roast", 1, [12, 13],
     "לסלק קטן שלם: צלה מכוסה בשכבה אחת עם כ־6 מ״מ מים. בדוק בסכין קטנה; אם המים התאדו, הוסף מעט כדי למנוע חריכה.",
     {"oven_temperature_c": 220, "duration_minutes": 60, "original_temperature_f": 425},
     ["סכין קטנה נכנסת בקלות למרכז", "בדוק שנותרו מים בתבנית"]),
]
AVIR = [
    ("אחידות גודל ושכבה בירקות לתנור", ["ירקות בתנור", "ירקות צלויים", "אנטיפסטי"], "oven_roast", 1, [10],
     "חתוך את הירקות לחתיכות דומות ופזר בשכבה שאינה צפופה. ערבב ירקות קטנים במהלך הצלייה כדי לשפר אחידות.", {}, ["חתיכות דומות בגודלן", "אין ערימה צפופה בתבנית"]),
    ("ירקות שורש בתנור", ["ירקות שורש", "שורשים בתנור"], "oven_roast", 1, [10],
     "לבצל, צנון, גזר ודלעת חתוכים לרבעים, הטבלה מציעה כשעה ב־180°C. הזמן משוער ותלוי בגודל ובתנור; בדוק רכות והשחמה.", {"oven_temperature_c": 180, "duration_minutes": 60}, ["הדוגמה מתייחסת לירקות חתוכים לרבעים", "בדוק רכות במרכז חתיכה גדולה"]),
    ("גיבץ' ירקות בתנור", ["גיבץ", "גיבץ'", "גיבץ׳", "נזיד ירקות בתנור"], "oven_roast", 1, [10],
     "לגיבץ' של תפוחי אדמה, חציל, בצל ופלפלים צבעוניים, הטבלה מציעה כחצי שעה ב־180°C. בדוק את רכות הירקות ואת ההשחמה.", {"oven_temperature_c": 180, "duration_minutes": 30}, ["בדוק ריכוך והשחמה"]),
    ("רטטוי בתנור", ["רטטוי", "רטטוי בתנור", "ratatouille"], "oven_roast", 1, [10],
     "לרטטוי מזוקיני, חציל, שומר, ראש שום, פלפלים ורסק עגבניות, הטבלה מציעה כחצי שעה ב־160°C לקבלת מרקם נזידי יותר. בדוק רכות והתאם לתנור.", {"oven_temperature_c": 160, "duration_minutes": 30}, ["בדוק את רכות הירקות ואת הנוזלים"]),
    ("דלעת בחום גבוה", ["דלעת", "pumpkin"], "oven_roast", 1, [10],
     "לריבועי דלעת שטוחים בעובי כחצי סנטימטר, הטבלה מציעה תשע דקות ב־240°C. הזמן מותנה בחיתוך הדק; בדוק רכות והשחמה לפני שהקצוות נחרכים.", {"oven_temperature_c": 240, "duration_minutes": 9}, ["הדוגמה מתייחסת לפרוסות בעובי כחצי סנטימטר", "בדוק רכות לפני שהקצוות נחרכים"]),
    ("קירור ביצה בתום הבישול", ["ביצה קשה", "ביצים קשות", "ביצה רכה", "ביצים רכות"], "boil_simmer", 1, [35],
     "בסיום בישול ביצה בקליפתה העבר אותה למים קרים כדי לעצור את המשך החימום. אין להסיק בטיחות רק ממרקם החלמון.", {}, ["הכן קערת מים קרים לפני סיום הבישול"]),
    ("ויניגרט עם חרדל", ["ויניגרט", "vinaigrette"], "", 1, [65],
     "לוויניגרט בסיסי מערבבים תחילה חומץ ותיבול עם חרדל, ואז מוסיפים שמן בהדרגה תוך ערבוב. החרדל מסייע לחבר בין המים לשמן.", {}, ["הוסף שמן בהדרגה תוך ערבוב"]),
    ("רביכה להסמכת רוטב", ["רביכה", "בשמל", "roux", "bechamel"], "", 2, [10],
     "ברביכה מבשלים קמח בחמאה תוך ערבוב לפני הוספת הנוזל. ערבוב הקמח בשומן מסייע לפזר אותו ולהקטין היווצרות גושים ברוטב.", {}, ["ערבב את הקמח בשומן לפני הנוזל"]),
    ("רקמת חיבור ובישול בשר", ["כתף", "אסאדו", "צוואר", "chuck", "shank"], "boil_simmer", 2, [35],
     "נתח עשיר ברקמת חיבור זקוק לבישול שמרכך אותה. בדוק התנגדות במזלג במהלך התבשיל; רכות אינה מחליפה את בדיקת הבטיחות הנפרדת.", {}, ["בדוק רכות של חתיכה מייצגת"]),
]


def build(source_root):
    inventory, records = [], []
    books = [("SRC-NOSRAT-2017", "סאמין נוסראט, Salt, Fat, Acid, Heat (2017)", 9, NOSRAT, [1, 251]),
             ("SRC-AVIR-2019", "אסף אביר, לא ספר בישול (2019)", 12, AVIR, [1, 101, 189])]
    for source_id, title, folder, entries, offsets in books:
        files = sorted((source_root / f"ilovepdf_split-range ({folder})").glob("*.pdf"),
                       key=lambda p: int(p.stem.rsplit("-", 2)[-2]))
        if len(files) != len(offsets):
            raise ValueError(f"Missing source parts for {source_id}")
        hashes = [hashlib.sha256(p.read_bytes()).hexdigest() for p in files]
        for p, digest, offset in zip(files, hashes, offsets):
            inventory.append({"source_id": source_id, "filename": p.name, "sha256": digest,
                              "first_full_pdf_page": offset, "text_layer": folder == 9})
        source = {"id": source_id, "type": "KNOWLEDGE_SOURCE", "name": title,
                  "verification_status": "PRELIMINARY", "source_text_checked": True,
                  "coverage": "CURATED_PARTIAL", "rights": "User-supplied PDF; original paraphrases only"}
        source_path = ROOT / f"09_Sources/{source_id}.md"
        if not source_path.exists():
            source_path.write_text(
                "---\n" + yaml.safe_dump(source, allow_unicode=True, sort_keys=False) + "---\n\n"
                + "מקור שסיפק המשתמש. נבדקו רק העמודים המצוינים בהערות המקושרות.\n",
                encoding="utf-8")
        for index, (name, aliases, method, part, pages, tip, params, checks) in enumerate(entries, 1):
            node_id = f"EVD-{'NOS' if folder == 9 else 'AVR'}-{index:03d}"
            full_pages = [offsets[part] + page - 1 for page in pages]
            citation = f"{title}, PDF {', '.join(map(str, full_pages))}"
            meta = {"id": node_id, "type": "COOKING_TECHNIQUE", "name": name,
                    "project_scope": "chef_mind", "allowed_contexts": ["chef_mind", "related_culinary_projects"],
                    "external_publication": False,
                    "domain": "TECHNIQUES", "verification_status": "PRELIMINARY",
                    "source_text_checked": True, "scientific_validation": "NOT_INDEPENDENTLY_VALIDATED",
                    "claim_type": "INTERPRETATION", "description": tip,
                    "chef_tip": tip, "target_foods": aliases, "tags": aliases,
                    "conditions": {"method_id": method, **params}, "checkpoints": checks,
                    "step_keywords": (["תנור", "צלי", "צלייה", "צלה", "צליית", "חימום", "אפייה"] if method == "oven_roast"
                                      else ["מלח", "המלח", "בישול", "בשל", "תיבול", "רוטב", "ערבוב", "ערבב", "הכנת", "חליטה"]),
                    "recommended_equipment": ["תבנית תנור"] if method == "oven_roast" else [],
                    "sources": [{"source_id": source_id, "citation": citation,
                                 "split_filename": files[part].name, "split_page": pages,
                                 "pdf_pages": full_pages, "pdf_sha256": hashes[part],
                                 "extraction_method": "TEXT_LAYER" if folder == 9 else "VISUAL_PAGE_REVIEW"}],
                    "relationships": [{"type": "SUPPORTED_BY", "target_id": source_id}]}
            path = ROOT / f"03_Techniques/{node_id}.md"
            path.write_text("---\n" + yaml.safe_dump(meta, allow_unicode=True, sort_keys=False)
                            + f"---\n\n# {name}\n\n{tip}\n\nמקור: [[{source_id}]] — {citation}.\n",
                            encoding="utf-8")
            records.append({"id": node_id, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
    dest = ROOT / "09_Sources/Supplied-2026"
    dest.mkdir(exist_ok=True)
    (dest / "manifest.json").write_text(json.dumps({"coverage": "CURATED_PARTIAL", "files": inventory,
                                                  "records": records}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Indexed {len(records)} paraphrased notes from {len(inventory)} source parts")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source_root", type=Path)
    build(parser.parse_args().source_root)
