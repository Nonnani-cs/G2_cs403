def test_drug_crud(client, auth_header):
    created = client.post(
        "/api/drugs/",
        headers=auth_header,
        json={"drug_code": "D001", "trade_name": "Cisplatin", "stock_qty": 0, "reorder_level": 2},
    )
    assert created.status_code == 200
    drug_id = created.json()["data"]["id"]

    detail = client.get(f"/api/drugs/{drug_id}", headers=auth_header)
    assert detail.status_code == 200
    assert detail.json()["data"]["drug_code"] == "D001"

    updated = client.put(f"/api/drugs/{drug_id}", headers=auth_header, json={"trade_name": "Cisplatin Plus"})
    assert updated.status_code == 200
