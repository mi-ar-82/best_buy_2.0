# Store Class
class Store:
    """
    Represents a store that manages a collection of products.
    """

    # Function: Initialize Store
    def __init__(self, products):
        """
        Initializes the store with a list of products.

        :param products: List of product objects (list[Product]).
        """
        self.products = products

    def add_product(self, product):
        """
        Adds a product to the store inventory.

        :param product: The product to add (Product).
        :return: None
        """
        self.products.append(product)

    def remove_product(self, product):
        """
        Removes a product from the store inventory.

        :param product: The product to remove (Product).
        :return: None
        """
        self.products.remove(product)

    # Function: Get Total Quantity of Products
    def get_total_quantity(self) -> int:
        """
        Calculates the total quantity of all active products in the store.

        :return: Total quantity of items in the store (int).
        """
        total_quantity = 0
        for product in self.products:
            if product.active:  # Use 'active' property instead of 'is_active()'
                total_quantity += product.quantity
        return total_quantity

    # Function: Get All Active Products
    def get_all_products(self):
        """
        Retrieves all active products in the store.

        :return: List of active products (list[Product]).
        """
        active_products = []
        for product in self.products:
            if product.active:
                active_products.append(product)
        return active_products

    # Function: Process an Order
    def order(self, shopping_list) -> float:
        """
        Processes an order based on a shopping list
        and calculates the total price.

        :param shopping_list: A list of tuples where each tuple contains:
                              - A product object (Product).
                              - The quantity to purchase (int).
        :return: Total price of the order (float).
        :raises ValueError: If a product is inactive
        or not available in the store.
                            If the requested quantity exceeds stock.
        """
        total_price = 0.0

        for product, quantity in shopping_list:
            if not product.active:
                raise ValueError(f"The product {product.name} "
                                 f"is inactive and cannot be ordered.")
            if product not in self.products:
                raise ValueError(f"The product {product.name} "
                                 f"is not available in the store.")
            total_price += product.buy(quantity)
        return total_price
