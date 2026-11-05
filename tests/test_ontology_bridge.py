from app.evaluation import activation_gate
from app.ontology_bridge import (
    diagnose_prerequisites,
    load_ontology,
    query_ontology,
    to_knowledge_document,
)
from app.retrieval import semantic_concepts


def test_ontology_loads_all_domains_and_resolves_graph():
    data = load_ontology()
    assert data["total_nodes"] >= 50
    assert data["verified_nodes"] >= 45
    assert data["sources_count"] >= 8
    assert {"SRC-NOSRAT-2017", "SRC-AVIR-2019", "SRC-MCGEE-2004", "SRC-FOODLAB-2015"} <= data["by_id"].keys()
    assert data["rules_count"] >= 6
    assert data["conflicts_count"] >= 3
    assert data["open_gaps_count"] >= 2
    assert data["total_edges"] >= 100

    folders = {f["folder"]: f["total"] for f in data["folder_stats"]}
    for required_folder in (
        "00_Ontology",
        "01_Ingredients",
        "02_Food-Science",
        "03_Techniques",
        "04_Flavors",
        "05_Textures",
        "06_Equipment",
        "07_Food-Safety",
        "08_Decision-Making",
        "09_Sources",
        "10_Knowledge-Gaps",
        "11_Conflicts",
        "12_Rules",
    ):
        assert folders.get(required_folder, 0) > 0, f"Folder {required_folder} should not be empty"


def test_hybrid_semantic_concepts_and_ontology_query():
    concepts_he = semantic_concepts("הבצל משחים מהר מדי בסיר והחלבון מתייבש")
    concepts_en = semantic_concepts("onion browning maillard and dry protein")
    assert "concept_allium_aromatic" in concepts_he
    assert "concept_maillard_browning" in concepts_he
    assert concepts_he & concepts_en

    results = query_ontology(None, "בצל משחים מהר מדי לפני ריכוך", limit=5)
    assert results
    top_ids = [item["id"] for item in results]
    assert "RUL-VEG-001" in top_ids or "ING-VEG-001" in top_ids


def test_graph_prerequisite_diagnosis_detects_missing_conditions_and_inhibitors():
    diag = diagnose_prerequisites(
        None,
        "TEX-CRUST-001",
        confirmed_conditions=[],
        active_factors=["אדים לחות כיסוי"],
    )
    assert diag["node_id"] == "TEX-CRUST-001"
    assert len(diag["missing_prerequisites"]) >= 1
    assert len(diag["active_inhibitors"]) >= 1

    alt_diag = diagnose_prerequisites(None, "TEC-PREC-001")
    assert alt_diag["alternatives"]


def test_ontology_exports_valid_knowledge_document_and_passes_activation_gate():
    doc = to_knowledge_document()
    assert doc.source_id == "culinary-ontology-curated"
    assert len(doc.units) >= 12
    gate = activation_gate(doc)
    assert gate["passed"] is True, gate


def test_ontology_api_endpoints_and_draft_export_workflow(env):
    client = env["client"]

    summary = client.get("/v1/ontology/summary")
    assert summary.status_code == 200
    body = summary.json()
    assert body["total_nodes"] >= 50
    assert body["rules_count"] >= 6

    nodes = client.get("/v1/ontology/nodes", params={"q": "קולגן בישול ארוך", "limit": 5})
    assert nodes.status_code == 200
    items = nodes.json()["items"]
    assert any(item["id"] in ("SCI-PROT-001", "RUL-MEAT-001", "ING-MEAT-001") for item in items)

    node_detail = client.get("/v1/ontology/nodes/RUL-MEAT-001")
    assert node_detail.status_code == 200
    assert node_detail.json()["id"] == "RUL-MEAT-001"
    assert node_detail.json()["outgoing_edges"]

    diag = client.post(
        "/v1/ontology/diagnose",
        json={
            "node_id": "TEC-DRY-001",
            "confirmed_conditions": ["dry surface"],
            "active_factors": ["crowded pan moisture"],
        },
    )
    assert diag.status_code == 200
    assert diag.json()["node_id"] == "TEC-DRY-001"

    export_resp = client.post("/v1/ontology/export-draft", headers=env["headers"])
    assert export_resp.status_code == 201, export_resp.text
    exported = export_resp.json()
    assert exported["status"] == "pending_review"
    assert exported["units_count"] >= 12

    approve_resp = client.post(
        f"/v1/knowledge/{exported['revision_id']}/approve",
        headers=env["headers"],
        json={
            "expected_revision": exported["revision"],
            "reason": "Approved curated ontology rules for engine use",
        },
    )
    assert approve_resp.status_code == 200, approve_resp.text
    assert approve_resp.json()["status"] == "active"
