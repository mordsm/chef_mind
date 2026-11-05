import hashlib
import json
from pathlib import Path

import pytest
from app.ontology_bridge import (
    DEFAULT_VAULT_ROOT,
    diagnose_prerequisites,
    load_ontology,
    to_knowledge_document,
)
from app.practical_knowledge import cooking_defaults, practical_tips

ROOT = DEFAULT_VAULT_ROOT / "Culinary-Knowledge"
FULL = ROOT / "09_Sources/Full-Books"


@pytest.mark.parametrize("book,pages,images,recipes", [("nosrat", 593, 200, 98), ("avir", 280, 280, 46)])
def test_complete_page_capture_is_distinct_from_semantic_review(book, pages, images, recipes):
    report = json.loads((FULL / f"{book}-coverage.json").read_text(encoding="utf8"))
    assert report["total_pages"] == report["pages_captured"] == pages
    assert {row["pdf_page"] for row in report["pages"]} == set(range(1, pages + 1))
    assert report["image_pages"] == report["ocr_pages_done"] == images
    assert report["ocr_pages_pending"] == []
    assert report["semantic_rule_review"] == "PARTIAL_NOT_COMPLETE"
    assert report["recipe_references"] == recipes


@pytest.mark.parametrize("book", ["nosrat", "avir"])
def test_local_source_pages_preserve_text_and_have_unbroken_graph_links(book):
    if not (FULL / "Pages" / book).is_dir():
        pytest.skip("Private source pages intentionally are not distributed through Git")
    data = load_ontology()
    report = json.loads((FULL / f"{book}-coverage.json").read_text(encoding="utf8"))
    for row in report["pages"]:
        path = ROOT / row["path"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == row["sha256"]
        node = data["by_id"][row["id"]]
        assert node["metadata"]["project_scope"] == "chef_mind"
        assert node["metadata"]["external_publication"] is False
        assert node["metadata"]["source_text_checked"] is False
        for edge in data["edges"]:
            if edge["source_id"] == row["id"]:
                assert edge["resolved"], edge
    assert diagnose_prerequisites(None, "PAGE-NOSRAT-065")["status"] == "reference_only"


def test_full_source_body_is_not_published_by_public_metadata_route(env):
    if not (FULL / "Pages/nosrat").is_dir():
        pytest.skip("Private source pages are local only")
    client = env["client"]
    public = client.get("/v1/ontology/nodes/PAGE-NOSRAT-044")
    assert public.status_code == 200
    assert public.json()["body"] == ""
    private = "/v1/ontology/private/nodes/PAGE-NOSRAT-044"
    assert client.get(private).status_code in (401, 403)
    response = client.get(private, headers=env["headers"])
    assert response.status_code == 200
    assert "Kosher Salt" in response.json()["body"]


def test_only_reviewed_authored_notes_enter_runtime_and_hashes_match():
    manifest = json.loads((FULL / "reviewed-manifest.json").read_text(encoding="utf8"))
    assert sum(row["id"].startswith("EVD-NOS-FULL-") for row in manifest["records"]) == 48
    assert sum(row["id"].startswith("EVD-AVR-FULL-") for row in manifest["records"]) == 31
    for row in manifest["records"]:
        path = ROOT / row["path"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == row["sha256"]
        assert row["id"].startswith(("EVD-NOS-FULL-", "EVD-AVR-FULL-"))
    tips = practical_tips("מיונז נשבר")
    assert tips and "עצור" in tips[0]["text"]
    assert all(not tip["source_ids"][1].startswith("PAGE-") for tip in tips)
    # Historical book times never silently become a time/temperature safety schedule.
    assert cooking_defaults("חזה עוף", "boil_simmer") == {}


def test_user_books_cannot_inherit_the_open_license_of_ontology_export():
    document = to_knowledge_document().model_dump()
    assert document["units"]
    assert all(not unit["knowledge_id"].startswith(("evd-nos", "evd-avr", "page-nosrat", "recipe-nosrat"))
               for unit in document["units"])


def test_every_recipe_reference_has_source_pages_and_is_not_an_executable_recipe():
    for path in (FULL / "Recipes").glob("*.md"):
        from app.ontology_bridge import _parse_markdown_file

        node = _parse_markdown_file(Path(path), ROOT)
        meta = node["metadata"]
        assert meta["claim_type"] == "REFERENCE_NOT_VALIDATED_RECIPE"
        assert meta["source_text_checked"] is False
        assert meta["sources"][0]["pdf_pages"] == meta["pdf_pages"]
        assert meta["pdf_pages"]
