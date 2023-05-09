from app import app, db

def create_tables():
    db.create_all()

if __name__ == '__main__':
    with app.app_context():
        create_tables()