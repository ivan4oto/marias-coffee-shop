from app import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer)
    customer_first_name = db.Column(db.String(80))
    customer_email = db.Column(db.String(120), unique=True, nullable=False)
    birth_date = db.Column(db.Date)

    def __repr__(self):
        return f'<User: {self.customer_email}>'


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer)
    product_name = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f'<Product: {self.product_name}>'
    

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.Integer)
    transaction_date = db.Column(db.Date)
    transaction_time = db.Column(db.Time)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

    customer = db.relationship('Customer', backref=db.backref('transactions', lazy=True))
    product = db.relationship('Product', backref=db.backref('transactions', lazy=True))

    def __repr__(self):
        return f'<Transaction: {self.transaction_id}>'