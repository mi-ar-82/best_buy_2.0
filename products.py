from abc import ABC, abstractmethod


# Product Class
class Product:
    """
    Represents a general product in the store.
    """
    def __init__(self, name, price, quantity):
        """
        Initializes a product with a name, price, and quantity.

        :param name: Name of the product (str).
        :param price: Price of the product (float).
        :param quantity: Quantity of the product in stock (int).
        :raises ValueError: If name is empty or price/quantity is invalid.
        """
        if not name:
            raise ValueError("Product name cannot be empty.")
        if price < 0:
            raise ValueError("Price cannot be negative.")

        # Initialize instance variables
        self.name = name
        self.price = price
        self._quantity = quantity  # Note the underscore for the protected attribute
        self._active = True  # Product is active by default
        self.promotion = None  # New attribute for promotions

    # Getter and setter for promotion
    def get_promotion(self):
        """
        Gets the promotion applied to the product.

        :return: Promotion object or None.
         """
        return self.promotion

    def set_promotion(self, promotion):
        """
        Sets a promotion for the product.

        :param promotion: Promotion object to apply.
        """
        self.promotion = promotion

    @property
    def quantity(self):
        """
        Gets the current quantity of the product.

        :return: Quantity of the product (int).
        """
        return self._quantity

    @quantity.setter
    def quantity(self, quantity: int):
        """
        Sets the quantity of the product. Deactivates it if quantity is zero.

        :param quantity: New quantity to set (int).
        :raises ValueError: If quantity is negative.
        """
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")
        self._quantity = quantity
        if self._quantity == 0:
            self.deactivate()

    @property
    def active(self) -> bool:
        """
        Checks if the product is active.

        :return: True if active, False otherwise.
        """
        return self._active

    @active.setter
    def active(self, active: bool):
        """
        Sets the active status of the product.

        :param active: Boolean indicating whether the product is active.
        """
        self._active = active

    def deactivate(self):
        """
        Sets the product's active status to False.
        """
        self._active = False

    def show(self) -> str:
        """
        Displays details about the product.

        :return: A string representation of the product.
        """
        promo_info = f" (Promotion: {self.promotion.name})" if self.promotion else ""
        return f"{self.name}, Price: {self.price}, Quantity: {self.quantity}{promo_info}"

    def buy(self, quantity: int) -> float:
        """
        Processes a purchase of the product.

        :param quantity: Quantity to purchase (int).
        :return: Total price after applying promotions (float).
        :raises ValueError: If requested quantity is invalid or exceeds stock.
        """
        if quantity <= 0:
            raise ValueError("Quantity to buy must be greater than zero.")
        if quantity > self.quantity:
            raise ValueError(f"Not enough stock. Only {self.quantity} available.")

        total_price = (
            self.promotion.apply_promotion(self, quantity)
            if self.promotion else self.price * quantity
        )

        self.quantity -= quantity
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

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, quantity: int):
        if quantity != 0:
            raise ValueError("Non-stocked products must always have a quantity of 0.")

    def show(self) -> str:
        return f"{self.name} (Non-Stocked), Price: {self.price}"


class LimitedProduct(Product):
    """
    Represents a product with a maximum purchase limit per order.
    This subclass extends the base Product class to add the functionality of limiting
    the quantity that can be purchased in a single order.
    If an attempt is made to
    buy more than the allowed maximum, an exception is raised.
    """

    def __init__(self, name, price, quantity, maximum):
        super().__init__(name, price, quantity)
        self._maximum = maximum  # Protected attribute for maximum
        if maximum < 0:
            raise ValueError("Maximum purchase limit cannot be negative.")

    @property
    def maximum(self):
        return self._maximum

    @maximum.setter
    def maximum(self, maximum):
        if maximum < 0:
            raise ValueError("Maximum purchase limit cannot be negative.")
        self._maximum = maximum

    def buy(self, quantity: int) -> float:
        if quantity > self.maximum:
            raise ValueError(f"You cannot buy more than {self.maximum} of this product.")
        return super().buy(quantity)

    def show(self) -> str:
        return (f"{self.name} (Limited, Max: {self.maximum}), "
                f"Price: {self.price}, Quantity: {self.quantity}")


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
        self._percent = percent
        if not (0 <= percent <= 100):
            raise ValueError("Percent must be between 0 and 100.")

    @property
    def percent(self):
        return self._percent

    @percent.setter
    def percent(self, percent):
        if not (0 <= percent <= 100):
            raise ValueError("Percent must be between 0 and 100.")
        self._percent = percent

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
