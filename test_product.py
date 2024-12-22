import pytest
from products import Product, NonStockedProduct, LimitedProduct, PercentDiscount, SecondHalfPrice, ThirdOneFree

# Test that creating a normal product works
def test_create_normal_product():
    product = Product(name="Laptop", price=1000, quantity=10)
    assert product.name == "Laptop"
    assert product.price == 1000
    assert product.quantity == 10
    assert product.is_active() is True

# Test that creating a product with invalid details invokes an exception
def test_create_invalid_product():
    with pytest.raises(ValueError, match="Product name cannot be empty."):
        Product(name="", price=1450, quantity=100)
    with pytest.raises(ValueError, match="Price cannot be negative."):
        Product(name="MacBook Air M2", price=-10, quantity=100)
    with pytest.raises(ValueError, match="Quantity cannot be negative."):
        Product(name="MacBook Air M2", price=1450, quantity=-5)

# Test that when a product reaches 0 quantity, it becomes inactive
def test_product_becomes_inactive_when_quantity_zero():
    product = Product(name="Headphones", price=200, quantity=1)
    product.buy(1)  # Buying all available stock
    assert product.get_quantity() == 0
    assert product.is_active() is False

# Test that product purchase modifies the quantity and returns the right output
def test_product_purchase_modifies_quantity_and_returns_correct_output():
    product = Product(name="Smartphone", price=500, quantity=5)
    total_price = product.buy(2)
    assert total_price == 1000  # 500 * 2
    assert product.get_quantity() == 3

# Test that buying a larger quantity than exists invokes an exception
def test_buying_larger_quantity_than_exists_raises_exception():
    product = Product(name="Tablet", price=300, quantity=2)
    with pytest.raises(ValueError, match="Not enough on stock. Only 2 available."):
        product.buy(3)

# Test that buying a non-positive quantity raises an exception
def test_buying_non_positive_quantity_raises_exception():
    product = Product(name="Monitor", price=150, quantity=10)
    with pytest.raises(ValueError, match="Quantity to buy must be greater than zero."):
        product.buy(0)

def test_non_stocked_product():
    product = NonStockedProduct(name="Windows License", price=125)
    assert product.get_quantity() == 0
    with pytest.raises(ValueError):
        product.set_quantity(1)

def test_limited_product():
    product = LimitedProduct(name="Shipping", price=10, quantity=5, maximum=1)
    with pytest.raises(ValueError):
        product.buy(2)
    assert product.buy(1) == 10



def test_percent_discount():
    promo = PercentDiscount(name="10% Off", percent=10)
    assert promo.apply_promotion(product=Product("Laptop", 1000, 10), quantity=2) == 1800

def test_second_half_price():
    promo = SecondHalfPrice(name="Second Half Price")
    assert promo.apply_promotion(product=Product("Headphones", 200, 10), quantity=3) == 500

def test_third_one_free():
    promo = ThirdOneFree(name="Buy 2 Get 1 Free")
    assert promo.apply_promotion(product=Product("Monitor", 150, 10), quantity=3) == 300


if __name__ == "__main__":
    pytest.main()
