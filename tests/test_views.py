import unittest
from datetime import date, datetime
from app import db, app, models

class TestViews(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()


    ###########################################
    # Testing the birthday_customers() endpoint.
    ###########################################

    def test_birthday_customers__no_birthday_boyz(self):
        """
        Test case: Today there are no customers who have birthday.
        Expected result: Empty json.
        """
        response = self.client.get('/customers/birthday')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'customers': []})

    def test_birthday_customers__one_birthday_boy(self):
        """
        Test case: One customer has birthday today.
        Expected result: A JSON object containing the customer's details should be returned.
                         Length of the response should be 1.
        """
        customer1 = models.Customer(customer_id=1, customer_first_name='Pesho', customer_email='baipesho@abv.bg', birth_date=date.today())
        customer2 = models.Customer(customer_id=2, customer_first_name='Joreto', customer_email='jorkata777@abv.bg', birth_date=date(1990, 1, 1))
        with app.app_context():
            db.session.add_all([customer1, customer2])
            db.session.commit()

        response = self.client.get('/customers/birthday')
        self.assertEqual(response.status_code, 200)

        json_data = response.get_json()
        self.assertIn('customers', json_data)
        customers = json_data['customers']
        self.assertEqual(len(customers), 1)

        customer = customers[0]
        self.assertEqual(customer['customer_id'], 1)
        self.assertEqual(customer['customer_first_name'], 'Pesho')

    def test_birthday_customers__lotta_birthday_boyz(self):
        """
        Test case: Multiple customers have their birthday today.
        Expected result: A JSON object containing the details of all customers with their birthday today should be returned.
        """
        customer1 = models.Customer(customer_id=1, customer_first_name='Ahil', customer_email='simong@abv.bg', birth_date=date.today())
        customer2 = models.Customer(customer_id=2, customer_first_name='Kolev', customer_email='skolev@gmail.com', birth_date=date.today())
        with app.app_context():
            db.session.add_all([customer1, customer2])
            db.session.commit()

        response = self.client.get('/customers/birthday')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json['customers']), 2)

        customer_ids = [customer['customer_id'] for customer in response.json['customers']]
        customer_names = [customer['customer_first_name'] for customer in response.json['customers']]

        self.assertIn(1, customer_ids)
        self.assertIn(2, customer_ids)
        self.assertIn('Ahil', customer_names)
        self.assertIn('Kolev', customer_names)


    ###########################################
    # Testing the last_order_per_customer() endpoint.
    ###########################################

    def test_last_order_per_customer__empty_db(self):
        """
        Test the case when there are no customers in the database.
        Expected behavior: The endpoint should return an empty list.
        """
        response = self.client.get('/customers/last-order-per-customer')
        data = response.get_json()
        self.assertEqual(data["customers"], [])

    def test_last_order_per_customer__single_customer_single_order(self):
        """
        Test the case when there is only one customer with a single order.
        Expected behavior: The endpoint should return the correct last order date for that customer.
        """
        product = models.Product(product_id=7, product_name="VaflaBorovec")
        customer = models.Customer(customer_id=2, customer_first_name='Kolev', customer_email='skolev@gmail.com', birth_date=date(1990, 1, 1))
        transaction = models.Transaction(
            transaction_id=1001,
            transaction_date=datetime(2023, 1, 10).date(),
            transaction_time=datetime.strptime('14:30:00', '%H:%M:%S').time(),
            quantity=5,
            customer_id=2,
            product_id=7
        )

        with app.app_context():
            db.session.add(product)
            db.session.commit()
            db.session.add_all([customer, transaction])
            db.session.commit()

        
        response = self.client.get('/customers/last-order-per-customer')
        data = response.get_json()
        self.assertEqual(len(data["customers"]), 1)
        self.assertEqual(data["customers"][0]["customer_id"], 2)
        self.assertEqual(data["customers"][0]["customer_email"], "skolev@gmail.com")
        self.assertEqual(data["customers"][0]["last_order_date"], '2023-01-10')

    def test_last_order_per_customer__multiple_orders(self):
        """
        Test the case when there are multiple customers with multiple orders.
        Expected behavior: The endpoint should return the correct last order date for each customer.
        """
        product1 = models.Product(product_id=7, product_name="VaflaBorovec")
        customer1 = models.Customer(customer_id=2, customer_first_name='Kolev', customer_email='skolev@gmail.com', birth_date=date(1990, 1, 1))
        transaction1 = models.Transaction(
            transaction_id=1,
            transaction_date=datetime(1999, 1, 10).date(),
            transaction_time=datetime.strptime('14:30:00', '%H:%M:%S').time(),
            quantity=3,
            customer_id=2,
            product_id=7
        )
        transaction2 = models.Transaction(
            transaction_id=2,
            transaction_date=datetime(2015, 1, 10).date(),
            transaction_time=datetime.strptime('14:30:00', '%H:%M:%S').time(),
            quantity=5,
            customer_id=2,
            product_id=7
        )

        product2 = models.Product(product_id=12, product_name="Ayrqnche")
        customer2 = models.Customer(customer_id=42, customer_first_name='Joni', customer_email='jonkata@gmail.com', birth_date=date(1988, 2, 2))
        transaction3 = models.Transaction(
            transaction_id=1,
            transaction_date=datetime(2020, 1, 9).date(),
            transaction_time=datetime.strptime('14:30:00', '%H:%M:%S').time(),
            quantity=1,
            customer_id=42,
            product_id=12
        )
        transaction4 = models.Transaction(
            transaction_id=2,
            transaction_date=datetime(2020, 1, 11).date(),
            transaction_time=datetime.strptime('15:30:00', '%H:%M:%S').time(),
            quantity=2,
            customer_id=42,
            product_id=7
        )
        with app.app_context():
            db.session.add_all([product1, product2])
            db.session.commit()
            db.session.add_all([customer1, customer2, transaction1, transaction2, transaction3, transaction4])
            db.session.commit()

        response = self.client.get('/customers/last-order-per-customer')
        data = response.get_json()
        self.assertEqual(len(data["customers"]), 2)

        # There's absolutely a better way to do this...
        counter = 0
        for customer in data["customers"]:
            customer_id = customer["customer_id"]
            if customer_id == 2:
                counter += 1
                self.assertEqual(customer["customer_email"], 'skolev@gmail.com')
                self.assertEqual(customer["last_order_date"], "2015-01-10")
            if customer_id == 42:
                counter += 1
                self.assertEqual(customer["customer_email"], 'jonkata@gmail.com')
                self.assertEqual(customer["last_order_date"], "2020-01-11")
        if counter != 2:
            raise ValueError("Counter should be 2")


    ###########################################
    # Testing the top_selling_products() endpoint.
    ###########################################

    def test_top_selling_products__response_status_code(self):
        """
        Test the status code returned from hitting the endpoint.
        Expected behavior: The endpoint should return 200 SUCCESS.
        """
        response = self.client.get('/products/top-selling-products/2021')
        self.assertEqual(response.status_code, 200)


    def test_top_selling_products__response_data_format(self):
        """
        Test correct total_sales are returned for each product
        Expected behavior: The endpoint should return the correct total_sales for the selected year for each product.
        """
        product1 = models.Product(product_id=1, product_name="CocaCola")
        product2 = models.Product(product_id=2, product_name="Pepsi")
        transaction1 = models.Transaction(
            transaction_id=1,
            transaction_date=datetime(2010, 1, 9).date(),
            transaction_time=datetime.strptime('14:30:00', '%H:%M:%S').time(),
            quantity=10,
            customer_id=42,
            product_id=2
        )
        transaction2 = models.Transaction(
            transaction_id=1,
            transaction_date=datetime(2020, 1, 9).date(),
            transaction_time=datetime.strptime('14:30:00', '%H:%M:%S').time(),
            quantity=4,
            customer_id=42,
            product_id=2
        )
        transaction3 = models.Transaction(
            transaction_id=2,
            transaction_date=datetime(2020, 12, 11).date(),
            transaction_time=datetime.strptime('15:30:00', '%H:%M:%S').time(),
            quantity=5,
            customer_id=42,
            product_id=1
        )
        with app.app_context():
            db.session.add_all([product1, product2])
            db.session.commit()
            db.session.add_all([transaction1, transaction2, transaction3])
            db.session.commit()

        response = self.client.get('/products/top-selling-products/2020')
        data = response.get_json()

        self.assertIn("products", data)
        products = data["products"]
        self.assertIsInstance(products, list)

        product_names = ['CocaCola', "Pepsi"]
        for product in products:
            if product["product_name"] == "CocaCola":
                self.assertIn(product["product_name"], product_names)
                self.assertEqual(product["total_sales"], 5)
            if product["product_name"] == "Pepsi":
                self.assertIn(product["product_name"], product_names)
                self.assertEqual(product["total_sales"], 4)


if __name__ == '__main__':
    unittest.main()
