# To run tests type "python3 -m testing -v" in your terminal and press Enter


from app import app
import app as app_module
from unittest.mock import patch, MagicMock
import unittest

with patch('builtins.input', return_value='6'):
    import cli

class TestProductRoutes(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

        self.mock_products = [
            {'id': '3017620422003',
              'product': {'barcode': '3017620422003',
                           'brand': 'Ferrero,Nutella',
                            'ingredients': 'sugar, palm oil, hazelnuts 13%, low-fat cocoa 7.4%, skimmed milk powder 6.6%, whey powder, emulsifiers: lecithins [soya], vanillin, gluten-free,',
                            'name': 'nutella',
                            'price': 8.99,
                            'stock': 90}},
            {'id': '6111242102941',
              'product': {'barcode': '6111242102941',
                            'brand': 'Jaouda',
                            'ingredients': 'Lait Frais Partiellement Écrémé, Poudre De Lait Écrémé, Sucre, Arôme, Ferments Lactiques.',
                            'name': 'Bananas',
                            'price': 2.99,
                            'stock': 10}}
        ]

    @patch('app.products', new_callable=list)
    def test_get_products(self, mock_array):
        mock_array.extend(self.mock_products)
        response = self.client.get('/products')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 2)

    @patch('app.get_product_info')
    @patch('app.products', new_callable=list)
    def test_post_products(self, mock_array, mock_get_product_info):
        mock_get_product_info.return_value = {
            'product_name': 'Peanut Butter',
            'brand': "Menguy's",
            'ingredients': 'Cacahuetes 100%',
            'barcode': '3327272107969'
        }
        response = self.client.post('/products', json={"name": "Peanut Butter", "price": 4.99, "stock": 30})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(mock_array), 1)
        self.assertEqual(mock_array[0]['id'], '3327272107969')

    @patch('app.products', new_callable=list)
    def test_patch_product(self, mock_array):
        mock_array.extend(self.mock_products)
        response = self.client.patch('/products/3017620422003', json={"price": 10.99})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(mock_array[0]["product"]["price"], 10.99)

    @patch('app.products', new_callable=list)
    def test_delete_product(self, mock_array):
        mock_array.extend(self.mock_products)
        response = self.client.delete('/products/3017620422003')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(app_module.products), 1)

class TestCLICommands(unittest.TestCase):
    def setUp(self):
        self.mock_product = {
            'id': '3017620422003',
            'product': {
                'barcode': '3017620422003',
                'brand': 'Ferrero,Nutella',
                'ingredients': 'sugar, palm oil',
                'name': 'nutella',
                'price': 8.99,
                'stock': 90
            }
        }

    def test_format_response(self):
        result = cli.format_response(self.mock_product)
        self.assertIn('nutella', result)
        self.assertIn('Ferrero,Nutella', result)
        self.assertIn('8.99', result)

    @patch('cli.requests.get')
    def test_view_all_products(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = [self.mock_product]
        mock_get.return_value = mock_response
        cli.view_all_products()
        mock_get.assert_called_once_with('http://127.0.0.1:5000/products')

    @patch('cli.requests.post')
    @patch('builtins.input', side_effect=['Nutella', '8.99', '90'])
    def test_add_product(self, mock_input, mock_post):
        mock_post.return_value.json.return_value = self.mock_product
        cli.add_product()
        mock_post.assert_called_once_with(
            'http://127.0.0.1:5000/products',
            json={"name": "Nutella", "price": "8.99", "stock": 90}
        )

    @patch('cli.requests.delete')
    @patch('builtins.input', side_effect=['3017620422003', 'yes'])
    def test_delete_product_confirmed(self, mock_input, mock_delete):
        cli.delete_product()
        mock_delete.assert_called_once_with('http://127.0.0.1:5000/products/3017620422003')


if __name__ == '__main__':
    unittest.main()