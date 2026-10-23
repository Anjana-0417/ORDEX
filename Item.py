import json
import os

ITEMS_FILE = "items.json"
DATA_FILE = "users.json"

def load_items():
    if os.path.exists(ITEMS_FILE):
        with open(ITEMS_FILE, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []

def save_items(items):
    with open(ITEMS_FILE, "w") as file:
        json.dump(items, file, indent=4)

def load_users():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {}
    return {}

def Item(logged_in_username):
    users = load_users()
    if logged_in_username not in users:
        print("Error: user not found.")
        return []

    user_data = users[logged_in_username]
    user_state = user_data["state"]
    company_name = user_data.get("company_name", "")  # Get company name, empty if not company

    print("\n--- Enter Item Details ---")

    items = load_items()

    while True:
        item_name = input("Enter item name (or type 'done' to finish): ")
        if item_name.lower() == "done":
            break

        if user_state == 1:  # Company user
            item_code = input("Enter item code: ")
        else:
            item_code = None

        try:
            quantity = int(input("Enter quantity: "))
            price = float(input("Enter price per item: "))
            item_record = {
                "item_name": item_name,
                "quantity": quantity,
                "price": price,
                "company_name": company_name  # Save company name with item
            }
            if item_code:
                item_record["item_code"] = item_code

            items.append(item_record)
        except ValueError:
            print("Invalid input. Please enter numeric values for quantity and price.")

    save_items(items)

    print("\nItems entered successfully:")
    for item in items:
        code_display = f" (Code: {item['item_code']})" if "item_code" in item else ""
        comp_display = f" (Company: {item['company_name']})" if item.get("company_name") else ""
        print(f"- {item['item_name']}{code_display}{comp_display}: {item['quantity']} pcs @ Rs.{item['price']} each")

    return items
