"""Hybrid local semantic-concept + character n-gram retrieval."""

import hashlib
import math
import re

from sqlalchemy import func, literal_column

from app.knowledge import active_rows
from app.schemas import KnowledgeDocument

EMBEDDING_VERSION = "local-char-hash-384-v1"

CONCEPT_CLUSTERS = {
    "concept_maillard_browning": {
        "maillard",
        "browning",
        "sear",
        "searing",
        "crust",
        "melanoidins",
        "מייאר",
        "השחמה",
        "משחים",
        "צריבה",
        "קראסט",
        "שחום",
        "זהוב",
    },
    "concept_collagen_gelatin": {
        "collagen",
        "gelatin",
        "connective",
        "braise",
        "braising",
        "gizzard",
        "gizzards",
        "shank",
        "chuck",
        "קולגן",
        "גלטין",
        "חיבור",
        "ריכוך",
        "קורקבנים",
        "קורקבן",
        "כתף",
        "שוק",
        "קדרה",
    },
    "concept_starch_thickening": {
        "starch",
        "slurry",
        "cornstarch",
        "gelatinization",
        "amylose",
        "thickening",
        "lumps",
        "עמילן",
        "קורנפלור",
        "הסמכה",
        "גושים",
        "מסמיכים",
        "סמיכות",
    },
    "concept_protein_coagulation": {
        "coagulation",
        "denaturation",
        "custard",
        "curdling",
        "curdle",
        "albumen",
        "yolk",
        "קרישה",
        "דנטורציה",
        "התגבנות",
        "מתגבן",
        "להתגבן",
        "קרם",
        "ביצים",
        "חלמון",
    },
    "concept_sugar_crystallization": {
        "sugar",
        "syrup",
        "crystals",
        "crystallization",
        "caramel",
        "caramelization",
        "סוכר",
        "סירופ",
        "גבישים",
        "התגבשות",
        "קרמל",
        "קרמליזציה",
    },
    "concept_thermometry_safety": {
        "thermometer",
        "probe",
        "internal",
        "temperature",
        "pasteurization",
        "salmonella",
        "מדחום",
        "טמפרטורה",
        "מדידה",
        "ליבה",
        "בטיחות",
        "פסטור",
    },
    "concept_heat_moisture": {
        "conduction",
        "convection",
        "radiation",
        "evaporation",
        "steam",
        "simmer",
        "הולכה",
        "הסעה",
        "קרינה",
        "אידוי",
        "אדים",
        "בעבוע",
    },
    "concept_osmosis_salting": {
        "osmosis",
        "brine",
        "brining",
        "salting",
        "salinity",
        "אוסמוזה",
        "המלחה",
        "מלח",
        "מליחות",
    },
    "concept_allium_aromatic": {
        "onion",
        "onions",
        "garlic",
        "shallot",
        "allium",
        "sweat",
        "sweating",
        "בצל",
        "בצלים",
        "שום",
        "אליום",
        "אידוי",
    },
}


def tokens(text):
    return set(re.findall(r"[^\W_]+", text.lower()))


def semantic_concepts(text):
    words = tokens(text)
    expanded = set()
    for word in list(words):
        if len(word) >= 4 and word[0] in "בהוכלמש":
            words.add(word[1:])
    for concept, vocabulary in CONCEPT_CLUSTERS.items():
        if words & vocabulary:
            expanded.add(concept)
    return expanded


def embed(text):
    vector = [0.0] * 384
    for token in sorted(tokens(text)):
        padded = f" {token} "
        for i in range(max(1, len(padded) - 2)):
            gram = padded[i : i + 3]
            digest = hashlib.sha256(gram.encode()).digest()
            vector[int.from_bytes(digest[:4], "big") % 384] += 1 if digest[4] % 2 else -1
    for concept in sorted(semantic_concepts(text)):
        for slot in range(4):
            digest = hashlib.sha256(f"{concept}:{slot}".encode()).digest()
            vector[int.from_bytes(digest[:4], "big") % 384] += 2.5 if digest[4] % 2 else -2.5
    norm = math.sqrt(sum(value * value for value in vector))
    return [value / norm for value in vector] if norm else vector


def retrieve(session, owner, query, limit=4):
    query_vector = embed(query)
    statement = active_rows(session, owner)
    if session.bind.dialect.name == "postgresql":
        from app.db import IndexedUnit

        lexical = func.ts_rank_cd(
            func.to_tsvector(literal_column("'simple'"), IndexedUnit.text),
            func.plainto_tsquery(literal_column("'simple'"), query),
        )
        statement = statement.order_by(
            (lexical + 1 - IndexedUnit.embedding.cosine_distance(query_vector)).desc()
        ).limit(50)
    ranked = []
    query_tokens = tokens(query)
    query_concepts = semantic_concepts(query)
    for index, revision, source in session.execute(statement):
        document = KnowledgeDocument.model_validate(revision.document)
        if document.license_status == "unknown":
            continue
        unit = next((unit for unit in document.units if unit.knowledge_id == index.knowledge_id), None)
        if unit is None:
            continue
        unit_tokens = tokens(index.text)
        matching = query_tokens & unit_tokens
        concept_matches = query_concepts & semantic_concepts(index.text)
        # Hash similarity alone never qualifies an unrelated source.
        if not matching and not concept_matches:
            continue
        lexical_score = len(matching) / max(1, len(query_tokens))
        concept_score = 0.6 * (len(concept_matches) / max(1, len(query_concepts))) if concept_matches else 0.0
        cosine_score = sum(a * b for a, b in zip(query_vector, index.embedding))
        score = lexical_score + concept_score + cosine_score
        ranked.append((score, unit, revision, source))
    return sorted(ranked, key=lambda item: item[0], reverse=True)[:limit]
