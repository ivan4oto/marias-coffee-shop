from flask import jsonify
from sqlalchemy import text
from app import app, db
from app.queries import get_customers_with_birthday_today

@app.route('/customers/birthday', methods=['GET'])
def birthday_customers():
    with db.engine.connect() as conn:
        results = conn.execute(text(get_customers_with_birthday_today))
        results = [{'customer_id': row[0], 'customer_first_name': row[1]} for row in results]
    return jsonify(customers=results)