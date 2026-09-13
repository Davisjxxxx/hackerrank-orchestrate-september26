from datetime import datetime, timezone
from decimal import Decimal

from fastapi.testclient import TestClient

from price_intel.api.app import AppState, create_app
from price_intel.demo import DEMO_NOW
from price_intel.resolver import canonical_product_id


def client():
    return TestClient(create_app(AppState()))


def test_barcode_vertical_slice_captures_price_and_returns_canonical_product():
    response = client().post(
        "/v1/intake/barcode",
        json={"barcode": "036000291452", "observed_price": "899.99", "retailer_hint": "Store A", "currency": "usd"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["state"] == "exact"
    assert body["product"]["gtin"] == "036000291452"
    assert body["normalized_input"]["observed_price"] == "899.99"
    assert body["product_id"] == canonical_product_id(body_to_product(body))


def test_url_and_photo_intake_use_the_same_identity_boundary():
    api = client()
    url_response = api.post("/v1/intake/url", json={"product_url": "https://www.amazon.com/example/dp/B0CHX3TW6K/"})
    photo_response = api.post(
        "/v1/intake/photo",
        json={"image_ref": "upload://fixture-photo-1", "ocr_evidence": {"brand": "Example", "model": "OLED55-X1"}},
    )
    assert url_response.json()["state"] == "exact"
    assert photo_response.json()["state"] == "exact"
    assert url_response.json()["product_id"] == photo_response.json()["product_id"]


def test_evaluation_replay_is_deterministic_and_financial_veto_wins():
    api = client()
    intake = api.post("/v1/intake/barcode", json={"barcode": "036000291452"}).json()
    product_id = intake["product_id"]
    payload = {
        "financial_state": "not_affordable",
        "financial_reason_codes": ["MINIMUM_BALANCE_PROTECTED"],
        "as_of": DEMO_NOW.isoformat(),
    }
    first = api.post(f"/v1/products/{product_id}/evaluate", json=payload).json()
    second = api.post(f"/v1/products/{product_id}/evaluate", json=payload).json()
    assert first["decision_id"] == second["decision_id"]
    assert first["combined_decision"] == "not_recommended"
    assert "FINANCIAL_SAFETY_VETO" in first["reason_codes"]
    assert first["financial_result"]["financial_reason_codes"] == ["MINIMUM_BALANCE_PROTECTED"]


def test_watch_api_is_user_scoped_and_can_be_deleted():
    api = client()
    product_id = api.post("/v1/intake/barcode", json={"barcode": "036000291452"}).json()["product_id"]
    create = api.post(
        "/v1/watches",
        headers={"X-User-Id": "user-a"},
        json={"product_id": product_id, "target_price": "749.00", "max_wait_date": "2026-10-31"},
    )
    assert create.status_code == 200
    watch_id = create.json()["id"]
    assert len(api.get("/v1/watches", headers={"X-User-Id": "user-a"}).json()) == 1
    assert api.get("/v1/watches", headers={"X-User-Id": "user-b"}).json() == []
    assert api.delete(f"/v1/watches/{watch_id}", headers={"X-User-Id": "user-b"}).status_code == 404
    assert api.delete(f"/v1/watches/{watch_id}", headers={"X-User-Id": "user-a"}).json() == {"deleted": True}


def test_invalid_barcode_is_rejected_at_api_boundary():
    response = client().post("/v1/intake/barcode", json={"barcode": "036000291453"})
    assert response.status_code == 422


def test_end_to_end_hold_result_creates_a_decision_aware_watch():
    api = client()
    product_id = api.post("/v1/intake/barcode", json={"barcode": "036000291452"}).json()["product_id"]
    decision = api.post(
        f"/v1/products/{product_id}/evaluate",
        json={"financial_state": "safe_now", "financial_coverage_state": "full", "max_wait_days": 90, "as_of": DEMO_NOW.isoformat()},
    ).json()
    assert decision["combined_decision"] in {"hold_for_price", "set_price_watch"}
    target = decision["price_decision"]["metrics"]["target_buy_price"]
    watch = api.post(
        "/v1/watches",
        headers={"X-User-Id": "vertical-slice-user"},
        json={
            "product_id": product_id,
            "target_price": target,
            "max_wait_date": "2026-12-01",
            "accepted_conditions": ["new"],
            "original_decision": decision["combined_decision"],
        },
    )
    assert watch.status_code == 200
    assert watch.json()["original_decision"] == decision["combined_decision"]


def test_governed_evaluation_exposes_review_certification_and_release():
    api = client()
    product_id = api.post("/v1/intake/barcode", json={"barcode": "036000291452"}).json()["product_id"]
    response = api.post(
        f"/v1/products/{product_id}/governed-evaluate",
        json={"financial_state": "safe_now", "financial_coverage_state": "full", "as_of": DEMO_NOW.isoformat()},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["recommendation"] in {"HOLD_FOR_BETTER_PRICE", "SET_PRICE_WATCH"}
    assert body["governance"]["certification"]["status"] == "CERTIFIED"
    assert body["governance"]["release"]["status"] == "RELEASED"


def body_to_product(body):
    from price_intel.models import ProductIdentity

    value = body["product"]
    return ProductIdentity(**value)
