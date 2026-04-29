def test_receive_and_stock_levels(client, auth_header):
    drug = client.post(
        "/api/drugs/",
        headers=auth_header,
        json={"drug_code": "DINV01", "trade_name": "Docetaxel", "stock_qty": 0, "reorder_level": 1},
    ).json()["data"]

    rec = client.post("/api/inventory/receive", headers=auth_header, json={"drug_id": drug["id"], "qty": 5})
    assert rec.status_code == 200
    assert rec.json()["data"]["stock_qty"] == 5
