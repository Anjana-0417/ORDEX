from Registration import Registration, load_users
from Login import login
from Item import Item
from Order import PlaceOrder

def main():
    print("=== Welcome to Inventory System ===")

    while True:
        print("\nMain Menu:")
        print("1. Registration")
        print("2. Login")
        print("3. Exit")

        choice = input("Enter your choice (1/2/3): ")

        if choice == '1':
            Registration()

        elif choice == '2':
            logged_in_username = login()
            if logged_in_username:
                users = load_users()
                user_state = users[logged_in_username]["state"]

                while True:
                    print("\nLogged In Menu:")

                    if user_state == 1:  # Company user
                        print("1. Enter Items")
                        print("2. Logout")
                        valid_choices = ['1', '2']
                    else:  # state 0 user
                        print("1. Place Order")
                        print("2. Logout")
                        valid_choices = ['1', '2']

                    sub_choice = input(f"Enter your choice ({'/'.join(valid_choices)}): ")

                    if user_state == 1:
                        if sub_choice == '1':
                            Item(logged_in_username)
                        elif sub_choice == '2':
                            print("Logged out.")
                            break
                        else:
                            print("Invalid choice. Try again.")
                    else:
                        if sub_choice == '1':
                            PlaceOrder()
                        elif sub_choice == '2':
                            print("Logged out.")
                            break
                        else:
                            print("Invalid choice. Try again.")
            else:
                print("Login failed. Returning to main menu.")

        elif choice == '3':
            print("Exiting program. Goodbye!")
            break

        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
