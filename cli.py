import requests


BASE_URL = "http://127.0.0.1:5000"


def show_menu():
    print("\n=== Inventory Management System ===")
    print("1. View all inventory")
    print("2. View one item")
    print("3. Add inventory item")
    print("4. Update inventory item")
    print("5. Delete inventory item")
    print("6. View low-stock items")
    print("7. View products from external API")
    print("8. Add product from external API")
    print("9. Exit")


def view_inventory():
    response = requests.get(f"{BASE_URL}/inventory")

    if response.status_code == 200:
        items = response.json()

        print("\n=== Inventory ===")

        for item in items:
            print(
                f"ID: {item['id']} | "
                f"Name: {item['name']} | "
                f"Quantity: {item['quantity']} | "
                f"Price: ${item['price']}"
            )
    else:
        print("Could not retrieve inventory.")


def view_item():
    item_id = input("Enter item ID: ")

    response = requests.get(
        f"{BASE_URL}/inventory/{item_id}"
    )

    if response.status_code == 200:
        print(response.json())
    else:
        print("Item not found.")


def add_item():
    name = input("Enter item name: ")
    quantity = int(input("Enter quantity: "))
    price = float(input("Enter price: "))

    data = {
        "name": name,
        "quantity": quantity,
        "price": price
    }

    response = requests.post(
        f"{BASE_URL}/inventory",
        json=data
    )

    if response.status_code == 201:
        print("Item added successfully:")
        print(response.json())
    else:
        print("Could not add item.")


def update_item():
    item_id = input("Enter item ID: ")

    name = input("Enter new name: ")
    quantity = int(input("Enter new quantity: "))
    price = float(input("Enter new price: "))

    data = {
        "name": name,
        "quantity": quantity,
        "price": price
    }

    response = requests.patch(
        f"{BASE_URL}/inventory/{item_id}",
        json=data
    )

    if response.status_code == 200:
        print("Item updated successfully:")
        print(response.json())
    else:
        print("Item not found.")


def delete_item():
    item_id = input("Enter item ID: ")

    response = requests.delete(
        f"{BASE_URL}/inventory/{item_id}"
    )

    if response.status_code == 200:
        print("Item deleted successfully.")
    else:
        print("Item not found.")


def low_stock():
    response = requests.get(
        f"{BASE_URL}/inventory/low-stock"
    )

    if response.status_code == 200:
        items = response.json()

        print("\n=== Low Stock Items ===")

        if not items:
            print("No low-stock items.")

        for item in items:
            print(
                f"ID: {item['id']} | "
                f"Name: {item['name']} | "
                f"Quantity: {item['quantity']}"
            )


def external_products():
    response = requests.get(
        f"{BASE_URL}/external-products"
    )

    if response.status_code == 200:
        products = response.json()

        print("\n=== External Products ===")

        for product in products[:10]:
            print(
                f"ID: {product['id']} | "
                f"Name: {product['title']} | "
                f"Price: ${product['price']}"
            )
    else:
        print("Could not retrieve external products.")


def add_external_product():
    product_id = input(
        "Enter external product ID to import: "
    )

    response = requests.post(
        f"{BASE_URL}/inventory/from-api/{product_id}"
    )

    if response.status_code == 201:
        print("External product added successfully:")
        print(response.json())
    else:
        print("Could not add external product.")


def main():
    while True:
        show_menu()

        choice = input("\nChoose an option: ")

        if choice == "1":
            view_inventory()

        elif choice == "2":
            view_item()

        elif choice == "3":
            add_item()

        elif choice == "4":
            update_item()

        elif choice == "5":
            delete_item()

        elif choice == "6":
            low_stock()

        elif choice == "7":
            external_products()

        elif choice == "8":
            add_external_product()

        elif choice == "9":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()