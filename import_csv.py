import os
import pandas as pd
from app import db, app, models

def import_customer_data(csv_file):
    data = pd.read_csv(csv_file)
    with app.app_context():
        for _, row in data.iterrows():
            customer = models.Customer(
                customer_id=row['customer_id'],
                customer_email=row['customer_email'],
                customer_first_name=row['customer_first-name'],
                birth_date=row['birthdate']
            )
            db.session.add(customer)
        db.session.commit()

def import_product_data(csv_file):
    data = pd.read_csv(csv_file)
    with app.app_context():
        for _, row in data.iterrows():
            product = models.Product(
                product_id=row['product_id'],
                product_name=row['product'],
            )
            db.session.add(product)
        db.session.commit()

def import_transactions_data(csv_file):
    data = pd.read_csv(csv_file)
    with app.app_context():
        for _, row in data.iterrows():
            customer_id = row['customer_id']
            if customer_id == 0:
                customer_id = None
        
            transaction = models.Transaction(
                transaction_id=row['transaction_id'],
                transaction_date=row['transaction_date'],
                transaction_time=row['transaction_time'],
                customer_id=customer_id,
                quantity=row['quantity'],
                product_id=row['product_id']
            )
            db.session.add(transaction)
        db.session.commit()



if __name__ == '__main__':
    customer_data = os.path.join(os.path.dirname(__file__), 'datasets/customer.csv')
    import_customer_data(customer_data)

    product_data = os.path.join(os.path.dirname(__file__), 'datasets/product.csv')
    import_product_data(product_data)

    transaction_data = os.path.join(os.path.dirname(__file__), 'datasets/sales_reciepts.csv')
    import_transactions_data(transaction_data)