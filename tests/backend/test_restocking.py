"""
Tests for restocking API endpoints.
"""


def full_cost(client):
    return client.get("/api/restock/recommendations").json()["max_cost"]


class TestRestockRecommendations:
    """Test suite for budget-based restock recommendations."""

    def test_no_budget_recommends_every_gap(self, client):
        """Without a budget, every item with positive demand gap is recommended in full."""
        response = client.get("/api/restock/recommendations")
        assert response.status_code == 200
        data = response.json()

        forecasts = client.get("/api/demand").json()
        gaps = {f["item_sku"]: f["forecasted_demand"] - f["current_demand"] for f in forecasts}
        expected = {sku for sku, gap in gaps.items() if gap > 0}

        assert {i["item_sku"] for i in data["items"]} == expected
        for item in data["items"]:
            assert item["quantity"] == gaps[item["item_sku"]]
            assert abs(item["line_total"] - item["quantity"] * item["unit_cost"]) < 0.01
        assert abs(data["total_cost"] - data["max_cost"]) < 0.01

    def test_recommendations_ranked_by_gap(self, client):
        """Items are ordered largest demand gap first."""
        items = client.get("/api/restock/recommendations").json()["items"]
        forecasts = {f["item_sku"]: f for f in client.get("/api/demand").json()}
        gaps = [forecasts[i["item_sku"]]["forecasted_demand"] - forecasts[i["item_sku"]]["current_demand"] for i in items]
        assert gaps == sorted(gaps, reverse=True)

    def test_decreasing_items_excluded(self, client):
        """Items whose demand is falling are never recommended."""
        items = client.get("/api/restock/recommendations").json()["items"]
        assert all(i["trend"] != "decreasing" for i in items)

    def test_budget_caps_total_cost(self, client):
        """Total cost never exceeds the budget."""
        for budget in [0, 100, 1000, 2500, full_cost(client) - 1]:
            data = client.get(f"/api/restock/recommendations?budget={budget}").json()
            assert data["total_cost"] <= budget + 0.01
            assert all(i["quantity"] > 0 for i in data["items"])

    def test_partial_fill_of_last_item(self, client):
        """When the budget runs short, the next item gets as many units as fit."""
        first = client.get("/api/restock/recommendations").json()["items"][0]
        budget = first["line_total"] / 2
        items = client.get(f"/api/restock/recommendations?budget={budget}").json()["items"]
        assert len(items) == 1
        assert items[0]["item_sku"] == first["item_sku"]
        assert items[0]["quantity"] == int(budget // first["unit_cost"])

    def test_zero_budget_recommends_nothing(self, client):
        data = client.get("/api/restock/recommendations?budget=0").json()
        assert data["items"] == []
        assert data["total_cost"] == 0

    def test_negative_budget_rejected(self, client):
        response = client.get("/api/restock/recommendations?budget=-5")
        assert response.status_code == 422


class TestRestockOrders:
    """Test suite for submitting and listing restock orders."""

    def test_submit_order_and_list_it(self, client):
        """A submitted order is priced server-side and appears in the list."""
        recs = client.get("/api/restock/recommendations?budget=2000").json()["items"]
        payload = {"items": [{"item_sku": i["item_sku"], "quantity": i["quantity"]} for i in recs]}

        response = client.post("/api/restock-orders", json=payload)
        assert response.status_code == 201
        order = response.json()

        assert order["status"] == "Submitted"
        assert abs(order["total_cost"] - sum(i["line_total"] for i in recs)) < 0.01
        assert order["lead_time_days"] == max(i["lead_time_days"] for i in recs)
        assert "T" in order["submitted_date"] and "T" in order["expected_delivery"]

        listed = client.get("/api/restock-orders").json()
        assert listed[0]["id"] == order["id"]

    def test_unknown_sku_rejected(self, client):
        response = client.post("/api/restock-orders", json={"items": [{"item_sku": "NOPE-999", "quantity": 1}]})
        assert response.status_code == 400
        assert "NOPE-999" in response.json()["detail"]

    def test_empty_order_rejected(self, client):
        response = client.post("/api/restock-orders", json={"items": []})
        assert response.status_code == 422

    def test_non_positive_quantity_rejected(self, client):
        response = client.post("/api/restock-orders", json={"items": [{"item_sku": "WDG-001", "quantity": 0}]})
        assert response.status_code == 422
