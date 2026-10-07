
from unittest.mock import patch, Mock

from app import app


def test_home():
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200


def test_get_inventory():
    client = app.test_client()

    response = client.get("/inventory")

    assert response.status_code == 200


def test_get_single_item():
    client = app.test_client()

    response = client.get("/inventory/1")

    assert response.status_code == 200

    data = response.get_json()

    assert data["name"] == "Laptop"


def test_get_missing_item():
    client = app.test_client()

    response = client.get("/inventory/999")

    assert response.status_code == 404


def test_create_item():
    client = app.test_client()

    response = client.post(
        "/inventory",
        json={
            "name": "Monitor",
            "quantity": 5,
            "price": 100
        }
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["name"] == "Monitor"
    assert data["quantity"] == 5
    assert data["price"] == 100


def test_create_item_missing_data():
    client = app.test_client()

    response = client.post(
        "/inventory",
        json={
            "name": "Monitor"
        }
    )

    assert response.status_code == 400


def test_update_item():
    client = app.test_client()

    response = client.patch(
        "/inventory/1",
        json={
            "name": "Updated Laptop",
            "quantity": 5,
            "price": 800
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["name"] == "Updated Laptop"
    assert data["quantity"] == 5
    assert data["price"] == 800


def test_update_missing_item():
    client = app.test_client()

    response = client.patch(
        "/inventory/999",
        json={
            "name": "Does Not Exist"
        }
    )

    assert response.status_code == 404


def test_delete_item():
    client = app.test_client()

    response = client.delete("/inventory/2")

    assert response.status_code == 200


def test_delete_missing_item():
    client = app.test_client()

    response = client.delete("/inventory/999")

    assert response.status_code == 404


def test_low_stock():
    client = app.test_client()

    response = client.get("/inventory/low-stock")

    assert response.status_code == 200


@patch("app.requests.get")
def test_external_products(mock_get):
    client = app.test_client()

    mock_response = Mock()
    mock_response.status_code = 200

    mock_response.json.return_value = [
        {
            "id": 1,
            "title": "Test Product",
            "price": 50
        }
    ]

    mock_get.return_value = mock_response

    response = client.get("/external-products")

    assert response.status_code == 200


@patch("app.requests.get")
def test_external_products_failure(mock_get):
    client = app.test_client()

    mock_response = Mock()
    mock_response.status_code = 500

    mock_get.return_value = mock_response

    response = client.get("/external-products")

    assert response.status_code == 502


@patch("app.requests.get")
def test_add_external_product(mock_get):
    client = app.test_client()

    mock_response = Mock()
    mock_response.status_code = 200

    mock_response.json.return_value = {
        "id": 1,
        "title": "External Laptop",
        "price": 500
    }

    mock_get.return_value = mock_response

    response = client.post("/inventory/from-api/1")

    assert response.status_code == 201

    data = response.get_json()

    assert data["name"] == "External Laptop"
    assert data["price"] == 500
    assert data["quantity"] == 10


@patch("app.requests.get")
def test_external_product_not_found(mock_get):
    client = app.test_client()

    mock_response = Mock()
    mock_response.status_code = 404

    mock_get.return_value = mock_response

    response = client.post("/inventory/from-api/999")

    assert response.status_code == 404

