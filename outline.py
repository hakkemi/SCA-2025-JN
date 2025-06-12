'''
Core Features to Implement:
Menu Management:
Define your boba menu: drinks, toppings, sizes, prices. Store this in a Python dictionary or list of dictionaries.
Example: {"Classic Milk Tea": {"small": 4.00, "medium": 4.50, "large": 5.00, "toppings": ["boba", "pudding"]}, ...}
Take New Order:
Display the menu.
Prompt the user (the "barista") to select drinks and toppings.
Validate choices (e.g., ensure the drink exists, topping is valid for that drink).
Calculate the price for each item and the total order.
Store the order (e.g., in a list of dictionaries representing active orders).
View Active Orders:
List all pending orders with their details and total price.
Mark Order as Completed:
Allow the user to select an order by ID and mark it as "completed" or "picked up."
Move completed orders to a "history" or "completed" list/file.
Basic Inventory (Challenge):
Keep track of ingredient quantities (e.g., "boba pearls remaining: 100 servings," "milk tea base remaining: 50 cups").
Decrement inventory when an order is placed.
Display low stock warnings.


Development Steps:
Define Data Structures: Create dictionaries for menu, current_orders, inventory.
main() function / Menu Loop: Display options to the user (take order, view orders, etc.) and call appropriate functions based on input.
display_menu() function: Prints the menu in a readable format.
take_order() function: Handles user input, calculates price, adds to current_orders.
view_orders() function: Iterates and prints current_orders.
complete_order() function: Updates order status and moves it.
save_data() and load_data() functions: Use json (built-in module, very easy to use for structured data) or simple text file writing to save current_orders and inventory so they persist when the program is closed and reopened.
'''