import streamlit as st
import json
import os
from datetime import datetime

# --- File paths ---
USERS_FILE = "users.json"
ITEMS_FILE = "items.json"
ORDERS_FILE = "orders.json"


# --- Helper JSON functions ---
def load_json(filepath, default):
    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return default
    return default


def save_json(filepath, data):
    with open(filepath, "w") as file:
        json.dump(data, file, indent=4)


# --- Streamlit Config ---
st.set_page_config(page_title="ORDEX", layout="centered")
st.title("🏪 ORDEX - Smart Wholesaler & Retailer System")

# --- Session State ---
if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = None
if "user_state" not in st.session_state:
    st.session_state.user_state = None

menu = ["Home", "Register", "Login", "Logout"]
choice = st.sidebar.selectbox("Menu", menu)

# --- HOME PAGE ---
if choice == "Home":
    st.write("Welcome to **ORDEX** — a smart platform that connects wholesalers and retailers.")
    st.image("https://cdn-icons-png.flaticon.com/512/2331/2331970.png", width=120)
    st.info("Please register or log in to continue.")


# --- REGISTRATION PAGE ---
elif choice == "Register":
    st.subheader("📝 Register")

    users = load_json(USERS_FILE, {})

    state = st.radio("Are you registering as:", ["Company", "Customer"])
    state_value = 1 if state == "Company" else 0

    if state_value == 1:
        st.info("Registration fee is Rs.5000.\n\nMonthly fee Rs.2500.\n\nSend payment receipts via WhatsApp within 24 hours. Otherwise your registration/Login will be disabled.")
        st.write("""
        **Bank Details**  
        - People's Bank — A/C: 3602507085 — WMHI Weerasekaera  
        - Sampath Bank — A/C: 6598756412 — DM Jayawickrama  
        **WhatsApp:** 0762075510
        """)
        company_name = st.text_input("Company Name")
        shop_name = ""
    else:
        company_name = ""
        shop_name = st.text_input("Shop Name")

    address = st.text_input("Address")
    phone = st.text_input("Phone Number")
    email = st.text_input("Email")
    username = st.text_input("Create Username")
    password = st.text_input("Create Password (8 chars)", type="password")

    if st.button("Register"):
        if username in users:
            st.error("Username already exists.")
        elif len(password) != 8:
            st.error("Password must be exactly 8 characters.")
        else:
            users[username] = {
                "username": username,
                "company_name": company_name,
                "shop_name": shop_name,
                "address": address,
                "phone_number": phone,
                "email": email,
                "password": password,
                "state": state_value
            }
            save_json(USERS_FILE, users)
            st.success("✅ Registration successful! You can now log in.")


# --- LOGIN PAGE ---
elif choice == "Login":
    st.subheader("🔐 Login")

    users = load_json(USERS_FILE, {})
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in users and users[username]["password"] == password:
            st.session_state.logged_in_user = username
            st.session_state.user_state = users[username]["state"]
            st.success(f"Welcome, {username}!")
        else:
            st.error("Invalid username or password.")

    if st.session_state.logged_in_user:
        logged_in_user = st.session_state.logged_in_user
        user_state = st.session_state.user_state
        users = load_json(USERS_FILE, {})
        st.divider()

        # --- COMPANY DASHBOARD ---
        if user_state == 1:
            st.subheader("🏢 Company Dashboard")
            menu_option = st.radio("Select Action:", ["Enter Items", "View Orders"])

            if menu_option == "Enter Items":
                st.write("### Add New Items")
                item_name = st.text_input("Item Name")
                item_code = st.text_input("Item Code")
                quantity = st.number_input("Quantity", min_value=0, step=1)
                price = st.number_input("Price per Item (Rs.)", min_value=0.0, step=0.01)

                if st.button("Add Item"):
                    items = load_json(ITEMS_FILE, [])
                    company_name = users[logged_in_user].get("company_name", "")
                    new_item = {
                        "item_name": item_name,
                        "item_code": item_code,
                        "quantity": quantity,
                        "price": price,
                        "company_name": company_name
                    }
                    items.append(new_item)
                    save_json(ITEMS_FILE, items)
                    st.success("✅ Item added successfully!")

                st.divider()
                st.subheader("📦 Current Inventory")
                items = load_json(ITEMS_FILE, [])
                if items:
                    company_name = users[logged_in_user].get("company_name", "")
                    company_items = [i for i in items if i.get("company_name") == company_name]
                    st.table(company_items)
                else:
                    st.info("No items yet.")

            elif menu_option == "View Orders":
                st.subheader("📦 Orders Received")

                orders = load_json(ORDERS_FILE, [])
                company_name = users[logged_in_user].get("company_name", "")
                company_orders = [o for o in orders if o.get("company_name") == company_name]

                if company_orders:
                    for order in company_orders:
                        st.markdown(f"""
                        🧾 **Item Code:** {order['item_code']}  
                        🛒 **Item Name:** {order['item_name']}  
                        👤 **Customer:** {order['shop_name']}  
                        📦 **Quantity:** {order['quantity']}  
                        💰 **Total:** Rs.{order['total']}  
                        🕒 **Ordered on:** {order['order_time']}  
                        ---  
                        """)
                else:
                    st.info("No orders received yet.")

        # --- CUSTOMER DASHBOARD ---
        else:
            st.subheader("🛒 Customer Dashboard")
            items = load_json(ITEMS_FILE, [])

            if items:
                st.write("### Available Items")
                st.table(items)

                item_codes = [item["item_code"] for item in items]
                selected_code = st.selectbox("Select Item Code", item_codes)
                selected_item = next((i for i in items if i["item_code"] == selected_code), None)
                selected_qty = st.number_input("Enter Quantity", min_value=1, step=1)
                shop_name_input = st.text_input("Enter Your Shop Name")

                if selected_item and st.button("Place Order"):
                    if not shop_name_input.strip():
                        st.error("Please enter your shop name before placing an order.")
                    elif selected_qty > selected_item["quantity"]:
                        st.warning(f"Only {selected_item['quantity']} available.")
                    else:
                        total = selected_qty * selected_item["price"]
                        st.success(f"✅ Order placed for {selected_qty} × {selected_item['item_name']} (Code: {selected_code}). Total = Rs.{total}")

                        # Deduct from inventory
                        selected_item["quantity"] -= selected_qty
                        save_json(ITEMS_FILE, items)

                        # Save order
                        orders = load_json(ORDERS_FILE, [])
                        order = {
                            "username": logged_in_user,
                            "shop_name": shop_name_input,
                            "item_name": selected_item["item_name"],
                            "item_code": selected_item["item_code"],
                            "company_name": selected_item["company_name"],
                            "quantity": selected_qty,
                            "price": selected_item["price"],
                            "total": total,
                            "order_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                        orders.append(order)
                        save_json(ORDERS_FILE, orders)
            else:
                st.warning("No items available yet.")


# --- LOGOUT PAGE ---
elif choice == "Logout":
    st.session_state.logged_in_user = None
    st.session_state.user_state = None
    st.success("Logged out successfully.")
