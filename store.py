class Store:
    def __init__(self, products):
        # Initialize the store with a list of products
        self.products = products
        
    def add_product(self, product):
        # Add a product to the store inventory
        self.products.append(product)
        
    def remove_product(self, product):
        # Remove a product from the store inventory
        self.products.remove(product)
    
    def get_total_quantity(self) -> int:
        # Returns how many items are in the store in total.
        total_quantity = 0
        for product in self.products:
            if product.is_active():
                total_quantity += product.get_quantity()
        return total_quantity
    
    def get_all_products(self) :
        # Returns all products in the store that are active.
        active_products = []
        for product in self.products:
            if product.is_active():
                active_products.append(product)
        return active_products
        
    def order(self, shopping_list) -> float:
        # Gets a list of tuples, where each tuple has 2 items:
        # Product (Product class)
        # and
        # quantity (int).
        # Buys the products and returns the total price of the order.
        # Process an order and return the total price of the order
        total_price = 0.0
        for item in shopping_list:
            product, quantity = item
            if product not in self.products:
                raise ValueError(f"The product {product.name} is not available in the store.")
            total_price += product.buy(quantity)
        return total_price