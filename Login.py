import json
import os

DATA_FILE = "users.json"
ITEMS_FILE = "items.json"

def load_users():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {}
    return {}

def load_items():
    if os.path.exists(ITEMS_FILE):
        with open(ITEMS_FILE, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []

def login():
    print("\n--- Login ---")

    users = load_users()

    username = input("Enter your username: ")
    password = input("Enter your password: ")

    if username in users and users[username]["password"] == password:
        print("Login successful!\n")

        # Show all available items after login, including company name
        items = load_items()
        if items:
            print("Available items:")
            for item in items:
                company = item.get('company_name', 'N/A')
                print(f"- {item['item_name']} (Company: {company}): {item['quantity']} pcs @ Rs.{item['price']} each")
        else:
            print("No items available yet.")

        return username  # Return username instead of True
    else:
        print("Login failed. Invalid username or password.")
        return None
