import json
import os

DATA_FILE = "users.json"

def load_users():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {}
    return {}

def save_users(users):
    with open(DATA_FILE, "w") as file:
        json.dump(users, file, indent=4)

def Registration():
    print("\n--- Registration ---")

    users = load_users()

    state_input = input("If you are a company, enter 1; otherwise, enter 0: ")
    if not state_input.isdigit() or int(state_input) not in [0,1]:
        print("Invalid input. Must be 0 or 1.")
        return

    state = int(state_input)

    if state == 1:
        print("\nRegistration fee is Rs.5000")
        print("Send us the payment receipt via WhatsApp during 24 hours. Otherwise your registration will be canceled.")
        print("\nBank Details:",
              "\nPeople's Bank",
              "\nAccount Number: 3602507085",
              "\nName: WMHI Weerasekaera")
        print("\nSampath Bank:",
              "\nAccount Number: 6598756412",
              "\nName: DM Jayawickrama")
        print("\nWhatsApp Number: 0762075510")

        company_name = input("\nEnter company name: ")
        shop_name = ""
    else:
        company_name = ""
        shop_name = input("Enter shop name: ")

    address = input("Enter address: ")
    phone_number = input("Enter phone number: ")
    email = input("Enter email address: ")

    username = input("Create a username: ")
    if username in users:
        print("Username already exists. Please choose another one.")
        return

    password = input("Create a password (exactly 8 characters): ")
    if len(password) != 8:
        print("Password must be exactly 8 characters.")
        return

    users[username] = {
        "username": username,
        "company_name": company_name,
        "shop_name": shop_name,
        "address": address,
        "phone_number": phone_number,
        "email": email,
        "password": password,
        "state": state
    }

    save_users(users)
    print("Successfully registered and saved to datastore!")
