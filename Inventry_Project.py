# SHOPKEEPER LOGIN
shopkeeper_username = "mahi"
shopkeeper_password = "216"

# INVENTORY DATA
items = ["rice", "oil", "sugar", "milk"]
stock = [50, 30, 40, 25]
price = [60, 120, 45, 25]

total_revenue = 0
total_profit = 0
item_profit = {}

customer_records = []

while True:

    print("\n----- INVENTORY MANAGEMENT -----")
    print("1. Shopkeeper")
    print("2. Customer")
    print("3. Exit")

    choice = input("Enter choice: ")

# SHOPKEEPER SECTION
    if choice == "1":

        print("\n------ SHOPKEEPER LOGIN ------")
        attempts = 3

        while attempts > 0:
            username = input("Enter Username: ")
            password = input("Enter Password: ")

            if username == shopkeeper_username and password == shopkeeper_password:
                print("Login Successful!\n")
                break
            else:
                attempts -= 1
                print("Invalid Credentials!")
                print("Attempts left:", attempts)

        if attempts == 0:
            print("Too many failed attempts!")
            continue

        while True:

            print("\n--- SHOPKEEPER MENU ---")
            print("1. View Items")
            print("2. Add Item")
            print("3. Remove Item")
            print("4. Modify Items")
            print("5. Sales Report")
            print("6. Profit Report")
            print("7. Itemized Profit")
            print("8. Customer List")
            print("9. Logout")

            ch = input("Enter choice: ")

            if ch == "1":

                print("\n+-------------------------------------------+")
                print("| {:<10} | {:<10} | {:<10} |".format("Item", "Stock", "Price"))
                print("+-------------------------------------------+")

                for i in range(len(items)):
                    print("| {:<10} | {:<10} | {:<10} |".format(items[i], stock[i], price[i]))

                print("+-------------------------------------------+")

            elif ch == "2":

                name = input("Enter new item name: ")
                qty = int(input("Enter quantity: "))
                pr = int(input("Enter price: "))

                items.append(name)
                stock.append(qty)
                price.append(pr)

                print("Item added successfully!")

            elif ch == "3":

                name = input("Enter item name to remove: ")

                if name in items:
                    index = items.index(name)

                    items.pop(index)
                    stock.pop(index)
                    price.pop(index)

                    print("Item removed successfully!")
                else:
                    print("Item not found!")

            elif ch == "4":

                name = input("Enter item name to modify: ")

                if name in items:
                    index = items.index(name)

                    new_stock = int(input("Enter new stock: "))
                    new_price = int(input("Enter new price: "))

                    stock[index] = new_stock
                    price[index] = new_price

                    print("Item modified successfully!")

                else:
                    print("Item not found!")

            elif ch == "5":
                print("Total Sales:", total_revenue)

            elif ch == "6":
                print("Total Profit:", total_profit)

            elif ch == "7":

                print("\n------ ITEMIZED PROFIT REPORT ------")
                print("+--------------------------------------+")
                print("| {:<15} | {:<10} |".format("Item", "Profit"))
                print("+--------------------------------------+")

                if not item_profit:
                    print("| {:<15} | {:<10} |".format("No Sales", "0"))
                else:
                    combined_profit = 0

                    for key, value in item_profit.items():
                        print("| {:<15} | {:<10} |".format(key, value))
                        combined_profit += value

                    print("+--------------------------------------+")
                    print("| {:<15} | {:<10} |".format("TOTAL", combined_profit))

                print("+--------------------------------------+")

            elif ch == "8":

                print("\n------ CUSTOMER LIST ------")

                if len(customer_records) == 0:
                    print("No customers yet.")
                else:

                    print("+--------------------------------------------------+")
                    print("| {:<15} | {:<15} | {:<10} |".format("Name", "Phone", "Bill"))
                    print("+--------------------------------------------------+")

                    for customer in customer_records:
                        print("| {:<15} | {:<15} | {:<10} |".format(
                            customer["name"],
                            customer["phone"],
                            customer["bill"]
                        ))

                    print("+--------------------------------------------------+")

            elif ch == "9":
                print("Logged out successfully!")
                break

            else:
                print("Invalid choice!")

# CUSTOMER SECTION
    elif choice == "2":

        while True:

            print("\n------ CUSTOMER DETAILS ------")

            customer_name = input("Enter Customer Name: ")

# PHONE VALIDATION (0,1 start kakudadu)
            while True:
                phone_number = input("Enter Phone Number: ")

                if phone_number.isdigit() and len(phone_number) == 10 and phone_number[0] not in ["0","1"]:
                    break
                else:
                    print("Invalid phone number! Enter 10 digit number starting with 6,7,8,9.")

            cart = []
            cart_qty = []
            total_bill = 0

            while True:

                print("\n--- CUSTOMER MENU ---")
                print("1. View Items")
                print("2. Add to Cart")
                print("3. Remove from Cart")
                print("4. Modify Cart Item")
                print("5. View Cart")
                print("6. Billing")
                print("7. Exit")

                ch = input("Enter choice: ")

                if ch == "1":

                    print("\n+-------------------------------------------+")
                    print("| {:<10} | {:<10} | {:<10} |".format("Item", "Stock", "Price"))
                    print("+-------------------------------------------+")

                    for i in range(len(items)):
                        print("| {:<10} | {:<10} | {:<10} |".format(items[i], stock[i], price[i]))

                    print("+-------------------------------------------+")

                elif ch == "2":

                    name = input("Enter item name to add: ")

                    if name in items:
                        index = items.index(name)
                        qty = int(input("Enter quantity: "))

                        if qty <= stock[index]:
                            cart.append(name)
                            cart_qty.append(qty)

                            stock[index] -= qty
                            total_bill += qty * price[index]

                            print("Added to cart!")
                        else:
                            print("Not enough stock")
                    else:
                        print("Item not found!")

                elif ch == "3":

                    if len(cart) == 0:
                        print("Cart is empty!")
                        continue

                    name = input("Enter item to remove: ")

                    if name in cart:

                        index = cart.index(name)
                        stock_index = items.index(name)

                        stock[stock_index] += cart_qty[index]
                        total_bill -= cart_qty[index] * price[stock_index]

                        cart.pop(index)
                        cart_qty.pop(index)

                        print("Removed from cart!")

                    else:
                        print("Item not in cart!")

                elif ch == "4":

                    if len(cart) == 0:
                        print("Cart is empty!")
                        continue

                    item = input("Enter item to modify: ")

                    if item in cart:

                        idx = cart.index(item)
                        stock_index = items.index(item)

                        old_qty = cart_qty[idx]

                        new_qty = int(input("Enter new quantity: "))

                        stock[stock_index] += old_qty

                        if new_qty <= stock[stock_index]:

                            cart_qty[idx] = new_qty
                            stock[stock_index] -= new_qty

                            total_bill -= old_qty * price[stock_index]
                            total_bill += new_qty * price[stock_index]

                            print("Cart modified successfully!")

                        else:
                            stock[stock_index] -= old_qty
                            print("Not enough stock!")

                    else:
                        print("Item not in cart!")

                elif ch == "5":

                    if len(cart) == 0:
                        print("Cart is empty!")
                    else:
                        print("\nCart Items:")
                        print("+----------------------------------+")
                        print("| {:<10} | {:<10} |".format("Item", "Quantity"))
                        print("+----------------------------------+")

                        for i in range(len(cart)):
                            print("| {:<10} | {:<10} |".format(cart[i], cart_qty[i]))

                        print("+----------------------------------+")
                        print("Total Bill:", total_bill)

                elif ch == "6":

                    print("\n------ BILL RECEIPT ------")
                    print("Customer Name:", customer_name)
                    print("Phone Number:", phone_number)

                    print("+----------------------------------+")
                    print("| {:<10} | {:<10} |".format("Item", "Quantity"))
                    print("+----------------------------------+")

                    for i in range(len(cart)):

                        print("| {:<10} | {:<10} |".format(cart[i], cart_qty[i]))

                        index = items.index(cart[i])
                        profit = cart_qty[i] * price[index] * 0.20

                        total_profit += profit

                        if cart[i] in item_profit:
                            item_profit[cart[i]] += profit
                        else:
                            item_profit[cart[i]] = profit

                    print("+----------------------------------+")
                    print("Final Bill:", total_bill)

                    total_revenue += total_bill

                    customer_records.append({
                        "name": customer_name,
                        "phone": phone_number,
                        "bill": total_bill
                    })

                    print("Thank you for shopping!")
                    break

                elif ch == "7":
                    print("Exited Successfully!")
                    break

                else:
                    print("Invalid choice!")

            next_customer = input("\nNext Customer? (yes/no): ")

            if next_customer.lower() != "yes":
                break

# EXIT
    elif choice == "3":
        print("Exiting program...")
        break

    else:
        print("Invalid choice!")
