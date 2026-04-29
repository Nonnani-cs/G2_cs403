def test_prescription_create_and_status_update(client, auth_header):
    patient = client.post("/api/patients/", headers=auth_header, json={"hn": "66001", "full_name": "P1"}).json()["data"]
    drug = client.post(
        "/api/drugs/",
        headers=auth_header,
        json={"drug_code": "DPRE01", "trade_name": "Cyclophosphamide", "stock_qty": 10, "reorder_level": 2},
    ).json()["data"]

    rx = client.post(
        "/api/prescriptions/",
        headers=auth_header,
        json={"order_no": "TEST-001", "patient_id": patient["id"], "notes": "", "items": [{"drug_id": drug["id"], "qty": 2}]},
    )
    assert rx.status_code == 200
    rx_id = rx.json()["data"]["id"]

    st = client.patch(f"/api/prescriptions/{rx_id}/status", headers=auth_header, json={"status": "กำลังจัดยา"})
    assert st.status_code == 200
