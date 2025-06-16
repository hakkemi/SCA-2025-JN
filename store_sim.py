alerts = [] # for inventory
toppings_data = {
    "Boba": 0.5,
    "Fruit Jelly": 0.75,
    "Cheese Foam": 0.85,
}
menu_data = [
    {"name": "Signature Milk Tea", "type": "Tea Based", "price": 5.00, "size": "Medium", "toppings": None},
    {"name": "Thai Milk Tea", "type": "Tea Based","price": 5.00, "size": "Medium", "toppings": None},
    {"name": "Oolong Milk Tea", "type": "Tea Based", "price": 5.00, "size": "Medium", "toppings": None},
    {"name": "Oreo Milk Tornado", "type": "Milk Based","price": 7.00, "size": "Medium", "toppings": None},
    {"name": "Strawberry Milk Tornado", "type": "Milk Based", "price": 7.00, "size": "Medium", "toppings": None},
    {"name": "Taronado", "type": "Milk Based", "price": 7.00, "size": "Medium", "toppings": None},
]
# i am nawt handling any exceptions or errors rn
class Drink:

    def __init__(self, drink_id, name, type, price, size="Medium", toppings=None):
        if size.lower() == "Large".lower():
            price += 1
        if toppings == "Boba".lower():
            price += 0.5
        elif toppings == "Fruit Jelly".lower():
            price += 0.75
        elif toppings == "Cheesefoam".lower():
            price += 0.85
        self.drink_id = drink_id
        self.name = name
        self.type = type
        self.price = price
        self.size = size
        self.toppings = toppings
class Current_Drink (Drink):
    pass
class Order():
    total_order_count = 0
    def __init__(self, drink_list):
        self.drink_list = drink_list
        Order.total_order_count += 1
def display_dashboard():
    print("--- Dashboard ---")
    print("1. Add Order")
    print("2. View Orders")
    print("3. View Inventory")
    print("4. Adjust Inventory")
    print("5. Quit program")
    print(f"Alerts: {alerts}")
    try:
        choice = int(input("Choice: "))
        validate_option_menu(choice)
    except ValueError:
        print("Invalid input. Please enter an integer number between 1 and 5.")
        display_dashboard()  # Call dashboard again if input is invalid

def add_drink_to_order(drink_list):
    print("--- Menu ---")
    print("0. View Total Drinks in Order")
    for i, drink in enumerate(menu):
        print(f"{i + 1}. {drink.name} (${drink.price:.2f})")
    try:
        drink_choice = int(input("Choice: "))
    except ValueError:
        print("Invalid input. Enter an int #")
        return add_drink_to_order(drink_list)

    if 0 <= drink_choice <= len(menu):
        for index, drink in enumerate(menu):
            if drink_choice == 0:
                view_orders()
            if drink_choice == drink.drink_id:
                print("--- Size ---")
                size_choice = input("Size (M/L): ")
                if size_choice.lower() == "L".lower():
                    current_size = "Large"
                    current_price = (drink.price + 1)
                elif size_choice.lower() == "M".lower():
                    current_size = "Medium"
                    current_price = drink.price
                else:
                    return add_drink_to_order(drink_list)
                print("--- Toppings ---")
                for i, topping in enumerate(toppings_data):
                    print(f"{i + 1}. {topping}")
                toppings_choice = int(input("Choice: "))
                for i, topping in enumerate(toppings_data):
                    if toppings_choice == (i + 1):
                        current_topping = topping
                        current_price += toppings_data[topping]
                    elif (toppings_choice > len(toppings_data)) or toppings_choice == 0:
                        print("Invalid option")
                        return add_drink_to_order(drink_list)
                current_drink = Current_Drink(drink.name, drink.type, current_price, current_size, current_topping)
                print("--- Final ---")
                print("1. Complete order")
                print("2. Add another drink")
                re_choice = int(input("Choice: "))
                if re_choice == 1:
                    drink_list.append(current_drink)
                    return drink_list
                elif re_choice == 2:
                    drink_list.append(current_drink)
                    add_drink_to_order(drink_list)
    else:
        print("Invalid option, please try again")
        return add_drink_to_order(drink_list)

def add_new_order():
    order = []
    new_order_drink_list = add_drink_to_order(order)
    new_order = Order(new_order_drink_list)
    print(new_order.total_order_count)
    every_order.append(new_order)
    return new_order

def view_orders():
    if not every_order:
        print("You have no completed orders!")
        display_dashboard()
    for i, order in enumerate(every_order):
        print(f"--- Order {i+1} ---")
        for j, drink in enumerate(order.drink_list):
            print(f"{drink.drink_id}, {drink.size}, {drink.price}, ${drink.type}")

#def view_inventory () :
#def adjust_inventory () :
def validate_option_menu (choice):
    if choice == 1:
        add_new_order()
        display_dashboard()
    elif choice == 2:
        view_orders()
    elif choice == 3:
        view_inventory()
    elif choice == 4:
        adjust_inventory()
    elif choice == 5:
        print("Program terminated")
    else:
        print("Invalid option! Please choose a number between 1 and 5.")
        display_dashboard()

def main ():
    display_dashboard()

menu = [Drink(drink_id = i + 1, **item_data) for i, item_data in enumerate(menu_data)]
# literally the same thing menu = []
# for i, item_data in enumerate(menu_data):
#     drink = Drink(drink_id = i + 1, **item_data)
#     menu.append(drink)
every_order = []
main()
