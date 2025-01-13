import unittest
from unittest.mock import patch, MagicMock
import products
import store
import main  # Import main module


class TestMain(unittest.TestCase):
    def setUp(self):
        """Set up a mock store and products for testing."""
        self.product_list = [
            products.Product("MacBook Air M2", price = 1450, quantity = 100),
            products.Product("Bose QuietComfort Earbuds", price = 250, quantity = 500),
            products.Product("Google Pixel 7", price = 500, quantity = 250),
        ]
        self.store = store.Store(self.product_list)

    @patch('builtins.print')
    def test_list_all_products(self, mock_print):
        """Test the list_all_products function."""
        main.list_all_products(self.store)
        self.assertTrue(mock_print.called)

        # Check that each expected product name appears in separate calls
        printed_output = [call[0][0] for call in mock_print.call_args_list]
        self.assertIn("MacBook Air M2", "".join(printed_output))
        self.assertIn("Bose QuietComfort Earbuds", "".join(printed_output))

    @patch('builtins.print')
    def test_show_total_amount(self, mock_print):
        """Test the show_total_amount function."""
        main.show_total_amount(self.store)
        self.assertTrue(mock_print.called)
        self.assertIn("850", mock_print.call_args[0][0])  # Total quantity: 100 + 500 + 250

    @patch('builtins.input', side_effect = ["Google Pixel 7", "2", "done"])
    @patch('builtins.print')
    def test_make_order(self, mock_print, mock_input):
        """Test the make_order function."""
        main.make_order(self.store)
        self.assertTrue(mock_print.called)
        self.assertIn("Order placed successfully!", mock_print.call_args_list[-1][0][0])

    @patch('builtins.input', side_effect = ["Nonexistent Product", "done"])
    @patch('builtins.print')
    def test_make_order_invalid_product(self, mock_print, mock_input):
        """Test make_order with an invalid product name."""
        main.make_order(self.store)
        self.assertTrue(mock_print.called)
        self.assertIn("Product 'Nonexistent Product' not found.",
                      mock_print.call_args_list[-2][0][0])

    @patch('builtins.input', side_effect = ["Google Pixel 7"])
    @patch('builtins.print')
    def test_find_product_by_name_exact_match(self, mock_print, mock_input):
        """Test finding a product by exact name."""
        product = main.find_product_by_name(self.store, "Google Pixel 7")
        self.assertIsNotNone(product)
        self.assertEqual(product.name, "Google Pixel 7")


if __name__ == "__main__":
    unittest.main()
