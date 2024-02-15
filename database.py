import sqlite3
import random
from datetime import date, timedelta

def generate_random_number(max_number):
    return random.randint(1, max_number)

def return_item(item_title, cust_id):
    conn = create_connection()
    cursor = conn.cursor()

    # Check if the item is borrowed by the given customer and has not been returned
    with conn:
        cur = conn.cursor()
        my_query = "SELECT itemID FROM Items WHERE title=:Item"
        cur.execute(my_query, {"Item": item_title})
        row = cur.fetchone()

        if row:
            item_id = row[0]
            print(item_id)

            # Check if the item is borrowed by the given customer and has not been returned
            my_query = "SELECT * FROM BorrowedItems WHERE itemID=:ItemID AND custID=:CustID AND retDate IS NULL"
            cur.execute(my_query, {"ItemID": item_id, "CustID": cust_id})
            row = cur.fetchone()

            if row:
                # Get the current date as return date
                return_date = date.today()

                # Update the BorrowedItems table to mark the item as returned
                update_query = "UPDATE BorrowedItems SET retDate=? WHERE itemID=? AND custID=? AND retDate IS NULL"
                cursor.execute(update_query, (return_date, item_id, cust_id))

                # Update the Items table to mark the item as returned
                update_query = "UPDATE Items SET availability=1 WHERE itemID=:Item"
                cursor.execute(update_query, {"Item": item_id})

                conn.commit()

                print("You have successfully returned the item.")
                print(f"Returned Item ID: {item_id}")
                print(f"Return Date: {return_date}")
            else:
                print("Sorry, the item is not borrowed by the given customer or has already been returned.")
        else:
            print("The item does not exist in the library.")

    conn.close()




def create_connection():
    return sqlite3.connect('library.db')

def boolean_to_yes_no(value):
    return "Yes" if value == 1 else "No"

def search_item(item_title):
    conn = create_connection()

    with conn:
        conn.row_factory = sqlite3.Row  # Set the row_factory to return rows as dictionaries
        cur = conn.cursor()
        my_query = "SELECT * FROM Items WHERE title=:Item"
        cur.execute(my_query, {"Item": item_title})

        rows = cur.fetchall()
        if rows:
            print("Here is the search result: ")

            for row in rows:
                # Convert the availability value (0 or 1) to a more readable format
                availability = "Available" if row["availability"] else "Not Available"

                # Print the item information
                print(f"Item ID: {row['itemID']}")
                print(f"Title: {row['title']}")
                print(f"Type: {row['type']}")
                print(f"Availability: {availability}\n")
        else:
            print("Unfortunately, we don't have the item you want!\n")

    conn.close()




def borrow_item(item_title, cust_id):
    conn = create_connection()
    cursor = conn.cursor()

    # Check if the item is available for borrowing in the Items table
    with conn:
        cur = conn.cursor()
        my_query = "SELECT b.borID, b.itemID FROM BorrowedItems b JOIN Items i ON b.itemID = i.itemID WHERE i.title=:Item AND i.availability = 1"
        cur.execute(my_query, {"Item": item_title})
        rows = cur.fetchone()
        emp_id = generate_random_number(10)

        if rows:
            item_id = rows[1]
            borrow_date = date.today()
            due_date = borrow_date + timedelta(days=7)

            # Update the existing row in BorrowedItems table to record this borrowing
            insert_query = "INSERT INTO BorrowedItems (itemID, custID, empID, borDate, dueDate, retDate, isReturned) VALUES (?, ?, ?, ?, ?, ?, ?)"
            cursor.execute(insert_query, (item_id, cust_id, emp_id, borrow_date, due_date, None, False))

            # Update the existing row in Items table to mark it as borrowed
            update_query = "UPDATE Items SET availability = FALSE WHERE title=:item"
            cursor.execute(update_query, {"item": item_title})

            print("Borrowed Item: " + item_title)

        else:
            print("Sorry! This item is currently not available!")
    conn.close()

def donate_item(item_title, item_type):
    conn = create_connection()
    cursor = conn.cursor()

    with conn:
        # Insert the item
        insert_query = "INSERT INTO Items (type, title, availability) VALUES (?, ?, ?)"
        cursor.execute(insert_query, (item_type, item_title, True))

        print("Successfully Donated!")

    conn.close()

def find_event(event_type):
    conn = create_connection()
    cursor = conn.cursor()

    with conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        find_query = "SELECT type, eventDate, roomNum FROM Events WHERE type=:Event"
        cursor.execute(find_query, {"Event": event_type})

        rows = cursor.fetchall()

        # Convert the rows to a list of dictionaries
        rows_as_dicts = [dict(row) for row in rows]

        if rows_as_dicts:
            print("Here is the search result: ")

            for row in rows_as_dicts:
                # Print the event information
                print(f"Type: {row['type']}")
                print(f"Date: {row['eventDate']}")
                print(f"Room Number: {row['roomNum']}")
        else:
            print("Unfortunately, we don't have the event you want!\n")

    conn.close()


def register_event(firstname, lastname, event_type):
    conn = create_connection()

    with conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        find_query = "SELECT eventID, type, eventDate, roomNum FROM Events WHERE type=:Event"
        cursor.execute(find_query, {"Event": event_type})

        row = cursor.fetchone()

        if row:
            event_id = row["eventID"]
            cur = conn.cursor()
            insert_query = "INSERT INTO EventParticipants (eventID, firstName, lastName) VALUES (?, ?, ?)"
            cur.execute(insert_query, (event_id, firstname, lastname))

            print("Successfully Registered!")
            print(f"Date: {row['eventDate']}")
            print(f"Room Number: {row['roomNum']}")

        else:
            print("Sorry! We don't have this event!")

    conn.close()

def count_digits(number):
    number_str = str(number)
    return len(number_str)

def volunteer(firstname, lastname, SIN):
    if count_digits(SIN) != 9:
        print("Please input valid SIN!")
    else:
        conn = create_connection()

        with conn:
            cursor = conn.cursor()

            insert_query = "INSERT INTO Employees (firstName, lastName, SIN, salary) VALUES (?, ?, ?, ?)"
            cursor.execute(insert_query, (firstname, lastname, SIN, 45000))

        conn.close()

def ask_for_help():
    conn = create_connection()

    with conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        find_query = "SELECT firstName, lastName FROM Employees ORDER BY RANDOM() LIMIT 1"
        cursor.execute(find_query)

        row = cursor.fetchone()

        if row:
            # Convert the row to a dictionary
            row_dict = dict(row)

            # Access the columns using dictionary-like access
            print(f"Name: {row_dict['firstName']} {row_dict['lastName']}")
        else:
            print("Sorry! We don't have any librarians yet!")

    conn.close()

def borrow_history():
    conn = create_connection()

    with conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        print_query = "SELECT * FROM BorrowedItems ORDER BY borDate DESC LIMIT 10"
        cursor.execute(print_query)

        rows = cursor.fetchall()

        print("itemID  custID  Borrowed Date  Due Date  Return Date  isReturned")
        
        if rows:
            for row in rows:
                row_dict = dict(row)

                print(f"{row_dict['itemID']}         {row_dict['custID']}     {row_dict['borDate']}   {row_dict['dueDate']}                {row_dict['isReturned']}")

    conn.close()