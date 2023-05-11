from flask import jsonify
from sqlalchemy import text
from app import app, db
from app.queries import get_customers_with_birthday_today, get_top_products_for_year, get_last_order_per_customer


@app.route('/customers/birthday', methods=['GET'])
def birthday_customers():
    app.logger.info('Route birthday_customers was called.')
    """
    Get the customers with birthdays today.

    The result is a JSON object containing a list of customers, where each
    customer is object with the keys "customer_id" and "customer_first_name".

    :returns: A JSON object containing the list of customers with birthdays today.
    :rtype: flask.Response (application/json)
    """
    with db.engine.connect() as conn:
        results = conn.execute(text(get_customers_with_birthday_today))
        results = [{'customer_id': row[0], 'customer_first_name': row[1]} for row in results]
    app.logger.info(f'Returning list of birthday customers. List size: {len(results)}')
    return jsonify(customers=results)

@app.route('/customers/last-order-per-customer', methods=['GET'])
def last_order_per_customer():
    """
    Get the last order date per customer.

    The result is a JSON object containing a list of customers, where
    each customer is object with the keys "customer_id",
    "customer_email", and "last_order_date".

    :returns: A JSON object containing the list of customers and their last order date.
    :rtype: flask.Response (application/json)
    """
    app.logger.info('Route last_order_per_customer was called.')
    with db.engine.connect() as conn:
        results = conn.execute(text(get_last_order_per_customer))
        customers = [
            {
                "customer_id": row[0],
                "customer_email": row[1],
                "last_order_date": row[2].strftime("%Y-%m-%d") if row[2] else None,
            }
            for row in results
        ]
    app.logger.info(f'Returning list of customers. List size: {len(customers)}')
    return jsonify(customers=customers)

@app.route('/products/top-selling-products/<year>', methods=['GET'])
def top_selling_products(year):
    """
    Get the top 10 selling products for a given year.
    
    The result is a JSON object containing a list of products,
    where each product is object with the keys
    "product_name" and "total_sales".

    :param year: The year for which to fetch the top-selling products.
    :type year: str
    :returns: A JSON object containing the top 10 products and their total sales for the given year.
    :rtype: flask.Response (application/json)
    """
    app.logger.info('Route top_selling_products was called.')
    with db.engine.connect() as conn:
        results = conn.execute(text(get_top_products_for_year), {'year': year})
        top_products = [{'product_name': row[0], 'total_sales': row[1]} for row in results]
    app.logger.info(f'Returning list of products. List size: {len(top_products)}')
    return jsonify(products=top_products)
