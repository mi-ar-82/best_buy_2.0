import pytest
from products import (Product, NonStockedProduct,
                      LimitedProduct, PercentDiscount,
                      SecondHalfPrice, ThirdOneFree)


# Test that creating a normal product works
def test_create_normal_product():
    product = Product(name="Laptop", price=1000, quantity=10)
    assert product.name == "Laptop"
    assert product.price == 1000
    assert product.quantity == 10  # Use the getter for quantity
    assert product.active is True  # Use the getter for active


# Test that creating a product with invalid details invokes an exception
def test_create_invalid_product():
    with pytest.raises(ValueError, match = "Product name cannot be empty."):
        Product(name = "", price = 1450, quantity = 100)
    with pytest.raises(ValueError, match = "Price cannot be negative."):
        Product(name = "MacBook Air M2", price = -10, quantity = 100)

    product = Product(name = "MacBook Air M2", price = 1450, quantity = 100)  # Create the product first
    with pytest.raises(ValueError, match = "Quantity cannot be negative."):
        product.quantity = -5  # Try setting the quantity to a negative value


# Test that when a product reaches 0 quantity, it becomes inactive
def test_product_becomes_inactive_when_quantity_zero():
    product = Product(name="Headphones", price=200, quantity=1)
    product.buy(1)  # Buying all available stock
    assert product.quantity == 0  # Use the getter for quantity
    assert product.active is False  # Use the getter for active


# Test that product purchase modifies the quantity and returns the right output
def test_product_purchase_modifies_quantity_and_returns_correct_output():
    product = Product(name="Smartphone", price=500, quantity=5)
    total_price = product.buy(2)
    assert total_price == 1000  # 500 * 2
    assert product.quantity == 3  # Use the getter for quantity


# Test that buying a larger quantity than exists invokes an exception
def test_buying_larger_quantity_than_exists_raises_exception():
    product = Product(name="Tablet", price=300, quantity=2)
    with pytest.raises(ValueError, match="Not enough stock. Only 2 available."):
        product.buy(3)



# Test that buying a non-positive quantity raises an exception
def test_buying_non_positive_quantity_raises_exception():
    product = Product(name="Monitor", price=150, quantity=10)
    with pytest.raises(ValueError, match="Quantity to buy must be greater than zero."):
        product.buy(0)



def test_non_stocked_product():
    product = NonStockedProduct(name="Windows License", price=125)
    assert product.quantity == 0  # Use the getter for quantity
    with pytest.raises(ValueError):
        product.quantity = 1  # Use the setter for quantity



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


#########################################################


def test_product_with_percent_discount():
    product = Product(name="Laptop", price=1000, quantity=10)
    promo = PercentDiscount(name="10% Off", percent=10)
    product.set_promotion(promo)

    # Check if promotion is applied correctly
    assert product.buy(2) == 1800  # 1000 * 2 * 0.9
    assert product.quantity == 8

def test_product_with_second_half_price():
    product = Product(name="Headphones", price=200, quantity=10)
    promo = SecondHalfPrice(name="Second Half Price")
    product.set_promotion(promo)

    # Check if promotion is applied correctly
    assert product.buy(3) == 500  # (200 + 100) + 200
    assert product.quantity == 7

def test_product_with_third_one_free():
    product = Product(name="Monitor", price=150, quantity=10)
    promo = ThirdOneFree(name="Buy 2 Get 1 Free")
    product.set_promotion(promo)

    # Check if promotion is applied correctly
    assert product.buy(3) == 300  # Only pay for 2 items
    assert product.quantity == 7

def test_show_method_with_promotion():
    product = Product(name="Smartphone", price=800, quantity=5)
    promo = PercentDiscount(name="20% Off", percent=20)
    product.set_promotion(promo)

    # Check if show method includes promotion details
    assert "Promotion: 20% Off" in product.show()



def test_remove_promotion():
    product = Product(name="Tablet", price=300, quantity=5)
    promo = PercentDiscount(name="15% Off", percent=15)
    product.set_promotion(promo)

    # Apply promotion and verify discounted price
    assert product.buy(2) == 510  # 300 * 2 * 0.85

    # Remove promotion and verify normal price
    product.set_promotion(None)
    assert product.buy(1) == 300


def test_invalid_quantity_with_promotion():
    product = Product(name="Camera", price=500, quantity=5)
    promo = ThirdOneFree(name="Buy 2 Get 1 Free")
    product.set_promotion(promo)

    with pytest.raises(ValueError, match="Quantity to buy must be greater than zero."):
        product.buy(0)

def test_buy_more_than_stock_with_promotion():
    product = Product(name="Speaker", price=100, quantity=3)
    promo = SecondHalfPrice(name="Second Half Price")
    product.set_promotion(promo)

    with pytest.raises(ValueError, match="Not enough stock. Only 3 available."):
        product.buy(4)


def test_multiple_products_with_promotions():
    laptop = Product(name="Laptop", price=1500, quantity=5)
    headphones = Product(name="Headphones", price=300, quantity=10)

    laptop_promo = PercentDiscount(name="10% Off", percent=10)
    headphones_promo = ThirdOneFree(name="Buy 2 Get 1 Free")

    laptop.set_promotion(laptop_promo)
    headphones.set_promotion(headphones_promo)

    # Verify prices with promotions applied
    assert laptop.buy(1) == 1350  # 1500 * 0.9
    assert headphones.buy(3) == 600  # Pay for only two items (300 * 2)




def test_integration_buy_with_promotions():
    macbook = Product("MacBook Air M2", price=1450, quantity=100)
    earbuds = Product("Bose QuietComfort Earbuds", price=250, quantity=500)

    macbook_promo = SecondHalfPrice("Second Half Price!")
    earbuds_promo = ThirdOneFree("Third One Free!")

    macbook.set_promotion(macbook_promo)
    earbuds.set_promotion(earbuds_promo)

    # Customer buys products with promotions applied
    total_macbook_price = macbook.buy(4)  # (1450 + (1450 / 2)) * 2
    total_earbuds_price = earbuds.buy(6)  # Pay for only four items

    assert total_macbook_price == (1450 + 725) * 2
    assert total_earbuds_price == (250 * 4)








if __name__ == "__main__":
    pytest.main()
