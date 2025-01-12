import pytest

from products import (
    Product,
    NonStockedProduct,
    LimitedProduct
)


# Test that creating a normal product works
def test_create_normal_product():
    """
    Test the creation of a normal product.

    Input: None
    Output: None (Asserts that product attributes are set correctly)
    """
    product = Product(name = "Laptop", price = 1000, quantity = 10)
    assert product.name == "Laptop"
    assert product.price == 1000
    assert product.quantity == 10  # Use the getter for quantity
    assert product.active is True  # Use the getter for active


# Test that creating a product with invalid details invokes an exception
def test_create_invalid_product():
    """
    Test that creating a product with invalid details
    raises appropriate exceptions.

    Input: None
    Output: None (Asserts exceptions are raised for invalid inputs)
    """
    with pytest.raises(ValueError, match = "Product name cannot be empty."):
        Product(name = "", price = 1450, quantity = 100)

    with pytest.raises(ValueError, match = "Price cannot be negative."):
        Product(name = "MacBook Air M2", price = -10, quantity = 100)

    product = Product(
        name = "MacBook Air M2", price = 1450, quantity = 100
    )  # Create the product first

    with pytest.raises(ValueError, match = "Quantity cannot be negative."):
        product.quantity = -5  # Try setting the quantity to a negative value


# Test that when a product reaches 0 quantity, it becomes inactive
def test_product_becomes_inactive_when_quantity_zero():
    """
    Test that a product becomes inactive when its quantity reaches zero.

    Input: None
    Output: None (Asserts activity status changes when quantity is zero)
    """
    product = Product(name = "Headphones", price = 200, quantity = 1)
    product.buy(1)  # Buying all available stock

    assert product.quantity == 0  # Use the getter for quantity
    assert product.active is False  # Use the getter for active


# Test that product purchase modifies the quantity and returns the right output
def test_product_purchase_modifies_quantity_and_returns_correct_output():
    """
    Test that purchasing a product modifies its quantity and
    returns the correct total price.

    Input: None
    Output: None (Asserts correct total price and
    updated quantity after purchase)
    """
    product = Product(name = "Smartphone", price = 500, quantity = 5)

    total_price = product.buy(2)

    assert total_price == 1000  # 500 * 2
    assert product.quantity == 3  # Use the getter for quantity


# Test that buying a larger quantity than exists invokes an exception
def test_buying_larger_quantity_than_exists_raises_exception():
    """
    Test that attempting to buy more than available stock raises an exception.

    Input: None
    Output: None (Asserts exception is raised when stock is insufficient)
    """
    product = Product(name = "Tablet", price = 300, quantity = 2)

    with pytest.raises(
            ValueError, match = "Not enough stock. Only 2 available."
    ):
        product.buy(3)


# Test that buying a non-positive quantity raises an exception
def test_buying_non_positive_quantity_raises_exception():
    """
    Test that attempting to buy a non-positive quantity raises an exception.

    Input: None
    Output: None (Asserts exception is raised for non-positive quantities)
    """
    product = Product(name = "Monitor", price = 150, quantity = 10)

    with pytest.raises(
            ValueError, match = "Quantity to buy must be greater than zero."
    ):
        product.buy(0)


# Test behavior of NonStockedProduct class
def test_non_stocked_product():
    """
    Test the behavior of NonStockedProduct class.

    Input: None
    Output: None (Asserts non-stocked products have fixed zero quantity
    and cannot be modified)
    """
    product = NonStockedProduct(name = "Windows License", price = 125)

    assert product.quantity == 0  # Use the getter for quantity

    with pytest.raises(ValueError):
        product.quantity = 1  # Use the setter for quantity


# Test behavior of LimitedProduct class
def test_limited_product():
    """
    Test the behavior of LimitedProduct class.

    Input: None
    Output: None
    (Asserts limited products enforce maximum purchase limit correctly)
    """
    product = LimitedProduct(name = "Shipping", price = 10, quantity = 5, maximum = 1)
    with pytest.raises(ValueError):
        product.buy(2)
    assert product.buy(1) == 10


if __name__ == "__main__":
    pytest.main()
