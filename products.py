from abc import ABC, abstractmethod

class Product:
# Instance variables:
# Name (str)
# Price (float)
# Quantity (int)
# Active (bool)
    
    def __init__(self, name, price, quantity):
        # Validate inputs and raise exceptions if invalid
        if not name:
            raise ValueError("Product name cannot be empty.")
        if price < 0:
            raise ValueError("Price cannot be negative.")
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")

        # Initialize instance variables
        self.name = name
        self.price = price
        self.quantity = quantity
        self.active = True  # Product is active by default
    
    def get_quantity(self):
        # get method for quantity
        return self.quantity


    def set_quantity(self, quantity: int):
        #Set method for quantity. Deactivates the product if quantity reaches 0.
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")
        self.quantity = quantity
        if self.quantity == 0:
            self.deactivate()

    def is_active(self) -> bool:
        #checks if the product is active (boolean value)
        return self.active

    def activate(self):
        #activates product
        self.active = True

    def deactivate(self):
        # deactivates product
        self.active = False

    def show(self) -> str:
        #returns a string representation of the product
        return f"{self.name}, Price: {self.price}, Quantity: {self.quantity}"

    def buy(self, quantity: int) -> float:
        #buys a given quantity of the product.
        #returns the total price of the purchase.
        #raises an exception if there is insufficient stock or invalid input.
        if quantity <= 0:
            raise ValueError("Quantity to buy must be greater than zero.")
        
        if quantity > self.quantity:
            raise ValueError(f"You can not buy {quantity} items.Not enough on stock. Only {self.quantity} available.")
        
        # calculates total price and update stock
        total_price = self.price * quantity
        #sets new available stock by removing the stock that was just sold
        self.set_quantity(self.quantity - quantity)
        
        return total_price

class NonStockedProduct(Product):
    """
    Represents a product that is not physically stocked.
    This subclass overrides the behavior of quantity to ensure it is always zero,
    as these products are intangible and do not require stock tracking.
    """
    def __init__(self, name, price):
        # Initialize a non-stocked product with quantity always set to 0
        super().__init__(name, price, quantity=0)

    def set_quantity(self, quantity: int):
        # Prevent any change to quantity for non-stocked products
        if quantity != 0:
            raise ValueError("Non-stocked products must always have a quantity of 0.")

    def show(self) -> str:
        # Return a string representation indicating the product is non-stocked
        return f"{self.name} (Non-Stocked), Price: {self.price}"


class LimitedProduct(Product):
    """
    Represents a product with a maximum purchase limit per order.
    This subclass extends the base Product class to add the functionality of limiting
    the quantity that can be purchased in a single order. If an attempt is made to
    buy more than the allowed maximum, an exception is raised.
    """
    def __init__(self, name, price, quantity, maximum):
        super().__init__(name, price, quantity)
        self.maximum = maximum
        if maximum < 0:
            raise ValueError("Maximum purchase limit cannot be negative.")

    def buy(self, quantity: int) -> float:
        if quantity > self.maximum:
            raise ValueError(f"You cannot buy more than {self.maximum} of this product.")
        return super().buy(quantity)

    def show(self) -> str:
        return f"{self.name} (Limited, Max: {self.maximum}), Price: {self.price}, Quantity: {self.quantity}"
    

class Promotion(ABC):
    """
    Abstract base class for promotions.
    """
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def apply_promotion(self, product, quantity) -> float:
        pass

class PercentDiscount(Promotion):
    """
    Applies a percentage discount to the product.
    """
    def __init__(self, name, percent):
        super().__init__(name)
        self.percent = percent
        if not (0 <= percent <= 100):
            raise ValueError("Percent must be between 0 and 100.")
    
    def apply_promotion(self, product, quantity) -> float:
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")
        if product.price < 0:
            raise ValueError("Product price cannot be negative.")
        return product.price * quantity * (1 - self.percent / 100)

class SecondHalfPrice(Promotion):
    """
    Applies a promotion where the second item is half price.
    """
    def apply_promotion(self, product, quantity) -> float:
        full_price_items = quantity // 2 + quantity % 2
        half_price_items = quantity // 2
        return full_price_items * product.price + half_price_items * product.price * 0.5

class ThirdOneFree(Promotion):
    """
    Applies a promotion where every third item is free.
    """
    def apply_promotion(self, product, quantity) -> float:
        paid_items = quantity - (quantity // 3)
        return paid_items * product.price


