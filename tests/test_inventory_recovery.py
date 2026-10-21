from conftest import chef_body


def test_inventory_recovers_from_old_cooking_and_is_owner_scoped(env):
    client = env["client"]
    assert client.get("/v1/inventory").status_code == 401
    body = chef_body("older-inventory")
    body["inventory"] = [{"name": "onion", "quantity": 2, "unit": "pieces"}]
    assert client.post("/v1/chef/respond", headers=env["headers"], json=body).status_code == 200
    assert (
        client.post("/v1/chef/respond", headers=env["headers"], json=chef_body("new-empty")).status_code
        == 200
    )
    recovered = client.get("/v1/inventory", headers=env["headers"]).json()
    assert recovered["origin"] == "recovered"
    assert recovered["items"][0]["name"] == "onion"
    assert client.get("/v1/inventory", headers=env["other"]).json()["items"] == []


def test_saved_empty_inventory_does_not_resurrect_removed_items(env):
    client = env["client"]
    body = chef_body()
    body["inventory"] = [{"name": "onion", "quantity": 2}]
    client.post("/v1/chef/respond", headers=env["headers"], json=body)
    result = client.put("/v1/inventory", headers=env["headers"], json={"items": []})
    assert result.status_code == 200
    saved = client.get("/v1/inventory", headers=env["headers"]).json()
    assert saved['items'] == [] and saved['origin'] == 'saved' and saved['updated_at']
    assert (
        client.put("/v1/inventory", headers=env["other"], json={"items": [{"name": "milk"}]}).status_code
        == 200
    )
    assert client.get("/v1/inventory", headers=env["headers"]).json()["items"] == []


def test_inventory_input_validation(env):
    result = env["client"].put(
        "/v1/inventory", headers=env["headers"], json={"items": [{"name": "rice", "quantity": -1}]}
    )
    assert result.status_code == 422
