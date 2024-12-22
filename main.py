import products  # Import the products module
import store  # Import the store module

# Setup initial stock of inventory
product_list = [
    products.Product("MacBook Air M2", price=1450, quantity=100),
    products.Product("Bose QuietComfort Earbuds", price=250, quantity=500),
    products.Product("Google Pixel 7", price=500, quantity=250)
]
best_buy = store.Store(product_list)


def list_all_products(store_obj):
    """
    Lists all active products in the store.
    """
    print("\nAvailable Products:")
    for product in store_obj.get_all_products():
        print(product.show())


def show_total_amount(store_obj):
    """
    Displays the total quantity of items in the store.
    """
    total_quantity = store_obj.get_total_quantity()
    print(f"\nTotal quantity of items in the store: {total_quantity}")


def find_product_by_name(store_obj, product_name):
    """
    Searches for a product by name in the store.
    If an exact match is found, it returns the product.
    If no exact match is found, it searches for partial matches and prints them.

    :param store_obj: The store object containing products.
    :param product_name: The name of the product to search for.
    :return: The exact matching product if found, otherwise None.
    """
    # Find exact match
    product = None
    for product_item in store_obj.products:
        if product_item.name.lower() == product_name.lower():
            product = product_item
            break

    if not product:
        # Search for partial matches
        matching_products = []
        for product_item in store_obj.products:
            if product_name.lower() in product_item.name.lower():
                matching_products.append(product_item)

        if matching_products:
            print(f"\nProducts matching your search '{product_name}':")
            for matched_product in matching_products:
                print(matched_product.show())
        else:
            print(f"No products found for the search query '{product_name}'. Please try again.")

    return product



def make_order(store_obj):
    """
    Allows the user to make an order by specifying product names and quantities.
    """
    shopping_list = []
    while True:
        product_name = input("\nEnter the product name (or 'done' to finish): ").strip()
        if product_name.lower() == 'done':
            break
            
        # Use the find_product_by_name function
        product = find_product_by_name(store_obj, product_name)
        
        if not product:  # If no exact match was returned
            continue

        try:
            quantity = int(input(f"Enter quantity for {product_name}: "))
            shopping_list.append((product, quantity))
        except ValueError:
            print("Invalid quantity. Please enter a valid number.")

    try:
        total_price = store_obj.order(shopping_list)
        print(f"\nOrder placed successfully! Total cost: ${total_price:.2f}")
    except ValueError as e:
        print(f"Error placing order: {e}")


def quit_program():
    """
    Exits the program with a farewell message.
    """
    print("\nThank you for visiting Best Buy! Goodbye!")
    exit()


def start(store_obj):
    """
    Starts the user interface for interacting with the store.
    :param store_obj: Store object to interact with.
    """
    while True:
        print("\nWelcome to Best Buy!")
        print("1. List all products in store")
        print("2. Show total amount in store")
        print("3. Make an order")
        print("4. Quit")

        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 4.")
            continue

        if choice == 1:
            list_all_products(store_obj)
        elif choice == 2:
            show_total_amount(store_obj)
        elif choice == 3:
            make_order(store_obj)
        elif choice == 4:
            quit_program()
        else:
            print("Invalid choice. Please select a number between 1 and 4.")


if __name__ == "__main__":
    start(best_buy)
