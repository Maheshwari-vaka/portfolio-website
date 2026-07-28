import mysql.connector

#DATABASE CONNECTION

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="inventory_management"
)

cursor = db.cursor()

#CREATE TABLES 

cursor.execute("""
CREATE TABLE IF NOT EXISTS shopkeeper(
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50),
    password VARCHAR(50)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS items(
    item_id INT PRIMARY KEY AUTO_INCREMENT,
    item_name VARCHAR(50),
    stock INT,
    price INT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS customers(
    customer_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_name VARCHAR(50),
    phone VARCHAR(15),
    total_bill INT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS salesman_sales(
    id INT PRIMARY KEY AUTO_INCREMENT,
    salesman_name VARCHAR(50),
    item_name VARCHAR(50),
    quantity INT,
    amount INT,
    commission DECIMAL(10,2)
)
""")

db.commit()

#INSERT DEFAULT SHOPKEEPER 

cursor.execute("SELECT * FROM shopkeeper")

if len(cursor.fetchall()) == 0:

    cursor.execute("""
    INSERT INTO shopkeeper(username,password)
    VALUES('mahi','216')
    """)

    db.commit()

# INSERT DEFAULT ITEMS

cursor.execute("SELECT * FROM items")

if len(cursor.fetchall()) == 0:

    cursor.execute("""
    INSERT INTO items(item_name,stock,price)
    VALUES
    ('rice',50,60),
    ('oil',30,120),
    ('sugar',40,45),
    ('milk',25,25)
    """)

    db.commit()

#  VARIABLES

total_revenue = 0
total_profit = 0
item_profit = {}

#MAIN PROGRAM 

while True:

    print("\n===== INVENTORY MANAGEMENT =====")
    print("1. Shopkeeper")
    print("2. Customer")
    print("3. Exit")
    print("4. Salesman")

    choice = input("Enter choice: ")

# SHOPKEEPER

    if choice == "1":

        print("\n===== SHOPKEEPER LOGIN =====")

        attempts = 3

        while attempts > 0:

            username = input("Enter Username: ")
            password = input("Enter Password: ")

            query = """
            SELECT * FROM shopkeeper
            WHERE username=%s AND password=%s
            """

            cursor.execute(query, (username, password))

            data = cursor.fetchone()

            if data:
                print("Login Successful!")
                break

            else:
                attempts -= 1
                print("Invalid Credentials!")
                print("Attempts Left:", attempts)

        if attempts == 0:
            continue

        while True:

            print("\n===== SHOPKEEPER MENU =====")
            print("1. View Items")
            print("2. Add Item")
            print("3. Remove Item")
            print("4. Modify Item")
            print("5. Sales Report")
            print("6. Profit Report")
            print("7. Logout")

            ch = input("Enter choice: ")

# VIEW ITEMS

            if ch == "1":

                cursor.execute("SELECT * FROM items")

                records = cursor.fetchall()

                print("\n+------------------------------------------------+")

                print("| {:<5} | {:<10} | {:<10} | {:<10} |".format(
                    "ID", "Item", "Stock", "Price"
                ))

                print("+------------------------------------------------+")

                for row in records:

                    print("| {:<5} | {:<10} | {:<10} | {:<10} |".format(
                        row[0], row[1], row[2], row[3]
                    ))

                print("+------------------------------------------------+")

# ADD ITEM

            elif ch == "2":

                name = input("Enter Item Name: ")
                qty = int(input("Enter Quantity: "))
                pr = int(input("Enter Price: "))

                query = """
                INSERT INTO items(item_name,stock,price)
                VALUES(%s,%s,%s)
                """

                values = (name, qty, pr)

                cursor.execute(query, values)

                db.commit()

                print("Item Added Successfully!")

# REMOVE ITEM

            elif ch == "3":

                name = input("Enter Item Name To Remove: ")

                query = "DELETE FROM items WHERE item_name=%s"

                cursor.execute(query, (name,))

                db.commit()

                print("Item Removed Successfully!")

# MODIFY ITEM

            elif ch == "4":

                name = input("Enter Item Name: ")

                new_stock = int(input("Enter New Stock: "))
                new_price = int(input("Enter New Price: "))

                query = """
                UPDATE items
                SET stock=%s, price=%s
                WHERE item_name=%s
                """

                values = (new_stock, new_price, name)

                cursor.execute(query, values)

                db.commit()

                print("Item Updated Successfully!")

# SALES REPORT

            elif ch == "5":

                print("Total Revenue:", total_revenue)

# PROFIT REPORT

            elif ch == "6":

                print("Total Profit:", total_profit)

# LOGOUT

            elif ch == "7":

                print("Logged Out Successfully!")
                break

            else:
                print("Invalid Choice!")

# CUSTOMER

    elif choice == "2":

        customer_name = input("Enter Customer Name: ")

# PHONE VALIDATION

        while True:

            phone = input("Enter Phone Number: ")

            if phone.isdigit() and len(phone) == 10 and phone[0] in ['6','7','8','9']:
                break

            else:
                print("Invalid Phone Number!")

        cart = []
        total_bill = 0

        while True:

            print("\n===== CUSTOMER MENU =====")
            print("1. View Items")
            print("2. Add To Cart")
            print("3. View Cart")
            print("4. Billing")
            print("5. Exit")

            ch = input("Enter choice: ")

# VIEW ITEMS

            if ch == "1":

                cursor.execute("SELECT * FROM items")

                records = cursor.fetchall()

                print("\n+------------------------------------------------+")

                print("| {:<5} | {:<10} | {:<10} | {:<10} |".format(
                    "ID", "Item", "Stock", "Price"
                ))

                print("+------------------------------------------------+")

                for row in records:

                    print("| {:<5} | {:<10} | {:<10} | {:<10} |".format(
                        row[0], row[1], row[2], row[3]
                    ))

                print("+------------------------------------------------+")

# ADD TO CART

            elif ch == "2":

                item_id = int(input("Enter Item ID: "))
                qty = int(input("Enter Quantity: "))

                query = "SELECT * FROM items WHERE item_id=%s"

                cursor.execute(query, (item_id,))

                item = cursor.fetchone()

                if item:

                    stock = item[2]
                    price = item[3]

                    if qty <= stock:

                        amount = qty * price

                        new_stock = stock - qty

                        update_query = """
                        UPDATE items
                        SET stock=%s
                        WHERE item_id=%s
                        """

                        cursor.execute(update_query, (new_stock, item_id))

                        db.commit()

                        cart.append((item[1], qty, amount))

                        total_bill += amount

                        print("Added To Cart!")

                    else:
                        print("Not Enough Stock!")

                else:
                    print("Item Not Found!")

# VIEW CART

            elif ch == "3":

                if len(cart) == 0:
                    print("Cart Empty!")

                else:

                    print("\n+------------------------------------------+")

                    print("| {:<10} | {:<10} | {:<10} |".format(
                        "Item", "Qty", "Amount"
                    ))

                    print("+------------------------------------------+")

                    for item in cart:

                        print("| {:<10} | {:<10} | {:<10} |".format(
                            item[0], item[1], item[2]
                        ))

                    print("+------------------------------------------+")

                    print("Total Bill:", total_bill)

# BILLING

            elif ch == "4":

                print("\n===== BILL RECEIPT =====")

                print("Customer:", customer_name)
                print("Phone:", phone)

                print("+------------------------------------------+")

                print("| {:<10} | {:<10} | {:<10} |".format(
                    "Item", "Qty", "Amount"
                ))

                print("+------------------------------------------+")

                for item in cart:

                    print("| {:<10} | {:<10} | {:<10} |".format(
                        item[0], item[1], item[2]
                    ))

                    profit = item[2] * 0.20

                    total_profit += profit

                print("+------------------------------------------+")

                print("Final Bill:", total_bill)

                total_revenue += total_bill

                query = """
                INSERT INTO customers(customer_name,phone,total_bill)
                VALUES(%s,%s,%s)
                """

                values = (customer_name, phone, total_bill)

                cursor.execute(query, values)

                db.commit()

                print("Thank You For Shopping!")

                break

# EXIT

            elif ch == "5":

                break

            else:
                print("Invalid Choice!")

# SALESMAN 

    elif choice == "4":

        salesman_name = input("Enter Salesman Name: ")

        while True:

            print("\n===== SALESMAN MENU =====")
            print("1. View Items")
            print("2. Sell Item")
            print("3. Exit")

            ch = input("Enter choice: ")

# VIEW ITEMS

            if ch == "1":

                cursor.execute("SELECT * FROM items")

                records = cursor.fetchall()

                for row in records:
                    print(row)

# SELL ITEM

            elif ch == "2":

                item_id = int(input("Enter Item ID: "))
                qty = int(input("Enter Quantity: "))

                query = "SELECT * FROM items WHERE item_id=%s"

                cursor.execute(query, (item_id,))

                item = cursor.fetchone()

                if item:

                    stock = item[2]
                    price = item[3]

                    if qty <= stock:

                        amount = qty * price

                        commission = amount * 0.05

                        new_stock = stock - qty

                        update_query = """
                        UPDATE items
                        SET stock=%s
                        WHERE item_id=%s
                        """

                        cursor.execute(update_query, (new_stock, item_id))

                        db.commit()

                        query = """
                        INSERT INTO salesman_sales
                        (salesman_name,item_name,quantity,amount,commission)
                        VALUES(%s,%s,%s,%s,%s)
                        """

                        values = (
                            salesman_name,
                            item[1],
                            qty,
                            amount,
                            commission
                        )

                        cursor.execute(query, values)

                        db.commit()

                        total_revenue += amount
                        total_profit += amount * 0.20

                        print("Sale Recorded Successfully!")

                        print("Commission:", commission)

                    else:
                        print("Not Enough Stock!")

                else:
                    print("Item Not Found!")

# EXIT

            elif ch == "3":

                break

            else:
                print("Invalid Choice!")

# EXIT

    elif choice == "3":

        print("Exiting Program...")
        break

    else:
        print("Invalid Choice!")
