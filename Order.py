import json
import os
from datetime import datetime

ITEMS_FILE = "items.json"
ORDERS_FILE = "orders.json"


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


def load_orders():
    if os.path.exists(ORDERS_FILE):
        with open(ORDERS_FILE, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []


def save_orders(orders):
    with open(ORDERS_FILE, "w") as file:
        json.dump(orders, file, indent=4)


def PlaceOrder(logged_in_username, shop_name):
    """Place an order using item code instead of item name."""
    items = load_items()
    if not items:
        print("No items available to order.")
        return []

    orders = load_orders()
    new_orders = []

    while True:
        item_code = input("Enter item code (or 'done' to finish): ").strip()
        if item_code.lower() == "done":
            break

        # 🔍 Match item by item_code instead of item_name
        matched_items = [item for item in items if item['item_code'].lower() == item_code.lower()]
        if not matched_items:
            print("Item not found. Please try again.")
            continue

        item = matched_items[0]

        try:
            quantity = int(input("Enter quantity: "))
            if quantity <= 0:
                print("Quantity must be positive.")
                continue
        except ValueError:
            print("Invalid quantity. Try again.")
            continue

        if quantity > item['quantity']:
            print(f"Insufficient stock! Only {item['quantity']} pcs available.")
            continue

        price = item['price']
        total = quantity * price
        order_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # ✅ Include both item_code and item_name for reference
        order_record = {
            "username": logged_in_username,
            "shop_name": shop_name,
            "item_code": item['item_code'],
            "item_name": item['item_name'],
            "company_name": item.get("company_name", ""),
            "quantity": quantity,
            "price": price,
            "total": total,
            "order_time": order_time
        }

        new_orders.append(order_record)
        item['quantity'] -= quantity  # Deduct from stock

    if not new_orders:
        print("No orders placed.")
        return []

    # 💾 Save updates
    save_items(items)
    orders.extend(new_orders)
    save_orders(orders)

    print("\n✅ Order(s) saved successfully and sent to company.")
    print("\nOrder Summary:")
    grand_total = sum(order["total"] for order in new_orders)
    for order in new_orders:
        print(f"- {order['item_code']} ({order['item_name']}): {order['quantity']} × Rs.{order['price']} = Rs.{order['total']}")
    print(f"Grand Total: Rs.{grand_total}")

    return new_orders
