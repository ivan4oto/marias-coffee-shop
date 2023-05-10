from flask import jsonify
from sqlalchemy import text
from app import app, db
from app.queries import get_customers_with_birthday_today, get_top_products_for_year

@app.route('/customers/birthday', methods=['GET'])
def birthday_customers():
    with db.engine.connect() as conn:
        results = conn.execute(text(get_customers_with_birthday_today))
        results = [{'customer_id': row[0], 'customer_first_name': row[1]} for row in results]
    return jsonify(customers=results)


@app.route('/products/top-selling-products/<year>', methods=['GET'])
def top_selling_products(year):
    with db.engine.connect() as conn:
        results = conn.execute(text(get_top_products_for_year), {'year': year})
        top_products = [{'product_name': row[0], 'total_sales': row[1]} for row in results]
    return jsonify(products=top_products)
