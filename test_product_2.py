import pytest

from products import (
    Product,
    PercentDiscount,
    SecondHalfPrice,
    ThirdOneFree
)


# Test: Product with Percent Discount
def test_product_with_percent_discount():
    """
    Test applying a percent discount to a product.

    Inputs:
        None (test setup includes creating a Product
        and PercentDiscount instance).

    Outputs:
        Asserts that the discounted price and updated quantity are correct.
    """
    product = Product(name = "Laptop", price = 1000, quantity = 10)
    promo = PercentDiscount(name = "10% Off", percent = 10)
    product.set_promotion(promo)

    # Check if promotion is applied correctly
    assert product.buy(2) == 1800  # 1000 * 2 * 0.9
    assert product.quantity == 8


# Test: Product with Second Half Price Promotion
def test_product_with_second_half_price():
    """
    Test applying a "Second Half Price" promotion to a product.

    Inputs:
        None (test setup includes creating a Product
        and SecondHalfPrice instance).

    Outputs:
        Asserts that the promotional pricing and updated quantity are correct.
    """
    product = Product(name = "Headphones", price = 200, quantity = 10)
    promo = SecondHalfPrice(name = "Second Half Price")
    product.set_promotion(promo)

    # Check if promotion is applied correctly
    assert product.buy(3) == 500  # (200 + 100) + 200
    assert product.quantity == 7


# Test: Product with Third One Free Promotion
def test_product_with_third_one_free():
    """
    Test applying a "Buy 2 Get 1 Free" promotion to a product.

    Inputs:
        None (test setup includes creating a Product
        and ThirdOneFree instance).

    Outputs:
        Asserts that the promotional pricing and updated quantity are correct.
    """
    product = Product(name = "Monitor", price = 150, quantity = 10)
    promo = ThirdOneFree(name = "Buy 2 Get 1 Free")
    product.set_promotion(promo)

    # Check if promotion is applied correctly
    assert product.buy(3) == 300  # Only pay for 2 items
    assert product.quantity == 7


# Test: Show Method with Promotion Details
def test_show_method_with_promotion():
    """
    Test that the show method includes promotion details.

    Inputs:
        None (test setup includes creating a Product
        and PercentDiscount instance).

    Outputs:
        Asserts that the promotion details are included
        in the string returned by show().
    """
    product = Product(name = "Smartphone", price = 800, quantity = 5)
    promo = PercentDiscount(name = "20% Off", percent = 20)
    product.set_promotion(promo)

    # Check if show method includes promotion details
    assert "Promotion: 20% Off" in product.show()


# Test: Remove Promotion from Product
def test_remove_promotion():
    """
    Test removing a promotion from a product.

    Inputs:
        None (test setup includes creating a Product
        and PercentDiscount instance).

    Outputs:
        Asserts that the pricing reflects the removal of the promotion.
    """
    product = Product(name = "Tablet", price = 300, quantity = 5)
    promo = PercentDiscount(name = "15% Off", percent = 15)
    product.set_promotion(promo)

    # Apply promotion and verify discounted price
    assert product.buy(2) == 510  # 300 * 2 * 0.85

    # Remove promotion and verify normal price
    product.set_promotion(None)
    assert product.buy(1) == 300


# Test: Invalid Quantity with Promotion
def test_invalid_quantity_with_promotion():
    """
    Test handling of invalid purchase quantities
    (e.g., zero or negative values).

    Inputs:
        None (test setup includes creating a Product
        and ThirdOneFree instance).

    Outputs:
        Asserts that an appropriate ValueError
        is raised for invalid quantities.
    """
    product = Product(name = "Camera", price = 500, quantity = 5)
    promo = ThirdOneFree(name = "Buy 2 Get 1 Free")
    product.set_promotion(promo)

    with pytest.raises(
            ValueError, match = "Quantity to buy must be greater than zero."
    ):
        product.buy(0)


# Test: Buying More Than Stock Allows
def test_buy_more_than_stock_with_promotion():
    """
    Test attempting to purchase more items than are in stock.

    Inputs:
        None (test setup includes creating a Product
        and SecondHalfPrice instance).

    Outputs:
        Asserts that an appropriate ValueError is raised
        when stock is insufficient.
    """
    product = Product(name = "Speaker", price = 100, quantity = 3)
    promo = SecondHalfPrice(name = "Second Half Price")
    product.set_promotion(promo)

    with pytest.raises(
            ValueError, match = "Not enough stock. Only 3 available."
    ):
        product.buy(4)


# Test: Multiple Products with Different Promotions
def test_multiple_products_with_promotions():
    """
    Test applying different promotions to multiple products
    and verifying their behavior.

    Inputs:
        None (test setup includes creating multiple Products
        with different promotions).

    Outputs:
        Asserts that the promotional pricing and updated quantities
        are correct for each product.
    """
    laptop = Product(name = "Laptop", price = 1500, quantity = 5)
    headphones = Product(name = "Headphones", price = 300, quantity = 10)

    laptop_promo = PercentDiscount(name = "10% Off", percent = 10)
    headphones_promo = ThirdOneFree(name = "Buy 2 Get 1 Free")

    laptop.set_promotion(laptop_promo)
    headphones.set_promotion(headphones_promo)

    # Verify prices with promotions applied
    assert laptop.buy(1) == 1350  # 1500 * 0.9
    assert headphones.buy(3) == 600  # Pay for only two items (300 * 2)


# Test: Integration Test for Buying with Promotions
def test_integration_buy_with_promotions():
    """
    Integration test for buying multiple products with promotions applied.

    Inputs:
        None (test setup includes creating multiple Products
        with different promotions).

    Outputs:
        Asserts that the total pricing and updated quantities are correct
        for all purchases.
    """
    macbook = Product("MacBook Air M2", price = 1450, quantity = 100)
    earbuds = Product("Bose QuietComfort Earbuds", price = 250, quantity = 500)

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
