from database import search_item, borrow_item, return_item, donate_item, find_event, register_event, volunteer, ask_for_help, borrow_history


def main():
    while True:
        print("1. Search item")
        print("2. Borrow item")
        print("3. Return item")
        print("4. Donate item")
        print("5. Find event")
        print("6. Register event")
        print("7. I want to be a volunteer")
        print("8. Ask for help")
        print("9. History")
        print("0. Exit")

        option = input("Select an option: ")

        if option == "1":
            item_title = input("Enter item's title: ")
            search_item(item_title)
        elif option == "2":
            item_title = input("Enter item's title: ")
            cust_id = int(input("Enter your customer ID: "))
            borrow_item(item_title, cust_id)
        elif option == "3":
            item_title = input("Enter item's title: ")
            cust_id = int(input("Enter your customer ID: "))
            return_item(item_title, cust_id)
        elif option == "4":
            item_title = input("Enter item's title: ")
            item_type = input("Enter item's type: ")
            donate_item(item_title, item_type)
        elif option == "5":
            event_type = input("Enter event's type: ")
            find_event(event_type)
        elif option == "6":
            first_name = input("Enter your first name: ")
            last_name = input("Enter your last name: ")
            event_type = input("Which event do you want to register: ")
            register_event(first_name, last_name, event_type)
        elif option == "7":
            first_name = input("Enter your first name: ")
            last_name = input("Enter your last name: ")
            SIN = input("Enter your SIN number (9-digit): ")
            volunteer(first_name, last_name, SIN)
        elif option == "8":
            ask_for_help()
        elif option == "9":
            borrow_history()
        elif option == "0":
            print("Exiting the application.")
            break
        else:
            print("Invalid option. Please select a valid option.")

if __name__ == "__main__":
    main()
