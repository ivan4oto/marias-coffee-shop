from app import app, db

def drop_and_create_tables():
    db.drop_all()
    db.create_all()

if __name__ == '__main__':
    with app.app_context():
        drop_and_create_tables()
