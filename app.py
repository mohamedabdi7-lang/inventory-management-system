from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

inventory = [
    {
        "id": 1,
        "name": "Laptop",
        "quantity": 10,
        "price": 750.00
    },
    {
        "id": 2,
        "name": "Keyboard",
        "quantity": 25,
        "price": 35.00
    }
]


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Inventory Management API is running"
    })


@app.route("/inventory", methods=["GET"])
def get_inventory():
    return jsonify(inventory)


@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_item(item_id):
    for item in inventory:
        if item["id"] == item_id:
            return jsonify(item)

    return jsonify({
        "error": "Inventory item not found"
    }), 404


@app.route("/inventory", methods=["POST"])
def add_item():
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    if "name" not in data or "quantity" not in data or "price" not in data:
        return jsonify({
            "error": "name, quantity, and price are required"
        }), 400

    new_id = max(
        [item["id"] for item in inventory],
        default=0
    ) + 1

    new_item = {
        "id": new_id,
        "name": data["name"],
        "quantity": data["quantity"],
        "price": data["price"]
    }

    inventory.append(new_item)

    return jsonify(new_item), 201


@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def update_item(item_id):
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    for item in inventory:
        if item["id"] == item_id:
            if "name" in data:
                item["name"] = data["name"]

            if "quantity" in data:
                item["quantity"] = data["quantity"]

            if "price" in data:
                item["price"] = data["price"]

            return jsonify(item)

    return jsonify({
        "error": "Inventory item not found"
    }), 404


@app.route("/inventory/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    for item in inventory:
        if item["id"] == item_id:
            inventory.remove(item)

            return jsonify({
                "message": "Inventory item deleted successfully"
            })

    return jsonify({
        "error": "Inventory item not found"
    }), 404


@app.route("/inventory/low-stock", methods=["GET"])
def low_stock():
    low_stock_items = [
        item for item in inventory
        if item["quantity"] < 10
    ]

    return jsonify(low_stock_items)


@app.route("/external-products", methods=["GET"])
def get_external_products():
    try:
        response = requests.get(
            "https://fakestoreapi.com/products",
            timeout=10
        )

        if response.status_code != 200:
            return jsonify({
                "error": "External API request failed"
            }), 502

        return jsonify(response.json())

    except requests.RequestException:
        return jsonify({
            "error": "Could not connect to external API"
        }), 502


@app.route("/inventory/from-api/<int:product_id>", methods=["POST"])
def add_external_product(product_id):
    try:
        response = requests.get(
            f"https://fakestoreapi.com/products/{product_id}",
            timeout=10
        )

        if response.status_code != 200:
            return jsonify({
                "error": "Product not found in external API"
            }), 404

        product = response.json()

        new_id = max(
            [item["id"] for item in inventory],
            default=0
        ) + 1

        new_item = {
            "id": new_id,
            "name": product["title"],
            "quantity": 10,
            "price": product["price"]
        }

        inventory.append(new_item)

        return jsonify(new_item), 201

    except requests.RequestException:
        return jsonify({
            "error": "Could not connect to external API"
        }), 502


if __name__ == "__main__":
    app.run(debug=True)
