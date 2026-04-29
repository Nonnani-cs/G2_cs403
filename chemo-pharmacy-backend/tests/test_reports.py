def test_report_endpoints(client, auth_header):
    stock = client.get("/api/reports/stock-summary", headers=auth_header)
    expiry = client.get("/api/reports/expiry-analysis", headers=auth_header)
    audit = client.get("/api/reports/dispensing-audit", headers=auth_header)
    assert stock.status_code == 200
    assert expiry.status_code == 200
    assert audit.status_code == 200
