"""Source table transcription, for reference only; never automatic safety rules."""

import json

from build_book_network import DEST, SCRATCH, write_note


def build():
    source = json.loads((SCRATCH / "nosrat-pages.json").read_text(encoding="utf-8"))[0]
    tables = [
        ("TABLE-NOSRAT-SALT", "טבלת כמויות מלח והמרות נפח", [65],
         ["FLV-TASTE-001"], "VISUAL_TABLE_REVIEW",
         {"percentage_basis": {"boneless_meat": "1.25% of food weight", "bone_in_meat": "1.5% of food weight",
                               "vegetables_and_grains": "1% of food weight", "blanching_pasta_water": "2% salinity",
                               "doughs_and_batters": "2.5% of flour weight"},
          "columns": ["salt", "grams_per_tablespoon", "per_pound_boneless_meat", "per_pound_bone_in_meat", "per_pound_vegetables_grains", "per_quart_blanching_pasta_water", "per_cup_flour"],
          "rows": [["Fine sea salt", 14.6, "1 1/8 tsp", "1 1/3 tsp", "1 scant tsp", "1 Tbsp + 1 scant tsp", "3/4 tsp"],
                   ["Maldon", 8.4, "2 tsp", "2 1/2 tsp", "1 2/3 tsp", "2 Tbsp + 3/4 tsp", "1 1/3 tsp"],
                   ["Sel gris", 13, "1 1/4 tsp", "1 1/4 tsp", "1 tsp", "1 Tbsp + 3/8 tsp", "1 scant tsp"],
                   ["Table salt", 18.6, "2/3 tsp", "7/8 tsp", "3/4 tsp", "1 Tbsp", "2/3 tsp"],
                   ["Morton's kosher", 14.75, "1 1/8 tsp", "1 1/3 tsp", "1 scant tsp", "1 Tbsp + 1 scant tsp", "3/4 tsp"],
                   ["Diamond Crystal kosher", 9.75, "1 3/4 tsp", "2 1/8 tsp", "1 1/3 tsp", "2 scant Tbsp", "1 1/8 tsp"]]},
         "אלו נקודות התחלה קולינריות מהספר, לא המלצות תזונתיות. אין לערבב אחוז ממשקל קמח עם אחוז ממשקל המזון או מליחות מים. מידות הנפח תלויות במלח; תמלול המקור אינו מבטיח התאמה בין המרות מקור מעוגלות."),
        ("TABLE-NOSRAT-BRAISE", "נתחים וזמני קדרה לפי הספר", [438, 439, 440],
         ["TEC-COMB-001", "DEC-PLAN-001"], "NATIVE_TEXT_REVIEW",
         {"time_unit": "minutes", "times": [
             {"cut": "Chicken breast, boneless", "range": [5, 8]},
             {"cut": "Chicken breast, bone-in", "range": [15, 18]},
             {"cut": "Chicken legs", "range": [35, 40]},
             {"cut": "Duck legs", "range": [90, 120]},
             {"cut": "Turkey legs", "range": [150, 180]},
             {"cut": "Pork shoulder", "range": [150, 210], "exception": "Longer on the bone"},
             {"cut": "Bony beef: short ribs, osso buco, oxtail", "range": [180, 210]},
             {"cut": "Meaty beef: chuck, brisket, round", "range": [180, 210]},
             {"cut": "Lamb shoulder on the bone", "range": [150, 180]}],
          "braising_cuts": {"pork": ["spare ribs", "shoulder", "shank", "sausages", "belly"],
                            "chicken_duck_rabbit": ["legs", "thighs", "wings (poultry only)"],
                            "beef": ["oxtail", "short ribs", "shank", "chuck", "brisket", "round"],
                            "lamb_goat": ["shoulder", "neck", "shank"]}},
         "המרת שעות לדקות נעשתה לצורך האינדקס בלבד. הטבלה אינה מציינת לכל שורה משקל, עובי וטמפרטורת נוזל, ולכן אין להפעיל את הזמנים כהבטחת רכות או בטיחות. הפרד חלקים שמתבשלים בקצב שונה ובדוק לפי נתח."),
        ("TABLE-NOSRAT-PORTIONS", "אומדן קניית חלבון לפי משקל", [440],
         ["DEC-PLAN-001"], "NATIVE_TEXT_REVIEW",
         {"basis": "people per 1 pound; source average, not grams per person",
          "rows": [{"food": "fish fillet", "people": 3}, {"food": "shell-on shellfish except shrimp", "people": 1},
                   {"food": "shell-on shrimp", "people": 3}, {"food": "bone-in roast", "people": 1.5},
                   {"food": "steak", "people": 3}, {"food": "whole animals and meat on the bone", "people": 1},
                   {"food": "ground meat for burgers or sausages", "people": 3},
                   {"food": "ground meat for ragù or chili", "people": 4}]},
         "זהו אומדן קנייה ממוצע לפי המחברת. תיאבון, גיל הסועדים, עצמות, שאר המנות ופחת בבישול משנים את הכמות הנדרשת; אין להשתמש באומדן כמנת תזונה מחייבת."),
    ]
    for node_id, title, pages, concepts, method, data, limits in tables:
        meta = {"id": node_id, "type": "CULINARY_SOURCE_TABLE", "name": title, "domain": "SOURCES",
                "verification_status": "PRELIMINARY", "source_text_checked": True,
                "runtime_use": "REFERENCE_ONLY", "transcription_method": method,
                "scientific_validation": "NOT_INDEPENDENTLY_VALIDATED", "data": data, "limitations": limits,
                "sources": [{"source_id": "SRC-NOSRAT-2017", "citation": f"Nosrat (2017), PDF {pages}",
                             "pdf_pages": pages, "pdf_sha256": source["source_sha256"]}],
                "relationships": [{"type": "SUPPORTED_BY", "target_id": f"PAGE-NOSRAT-{p:03}"} for p in pages]
                                 + [{"type": "MENTIONS", "target_id": concept} for concept in concepts]}
        body = f"# {title}\n\n{limits}\n\nמקור: " + " · ".join(f"[[nosrat-page-{p:03}]]" for p in pages)
        body += "\n\n```json\n" + json.dumps(data, ensure_ascii=False, indent=2) + "\n```\n"
        write_note(DEST / "Tables" / f"{node_id}.md", meta, body)
    print(f"Transcribed {len(tables)} source tables")


if __name__ == "__main__":
    build()
