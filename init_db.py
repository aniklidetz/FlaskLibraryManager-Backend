from app import app, db
from models import Book, Customer, Loan

def init_db():
    with app.app_context():
        try:
            db.create_all()
            print("Database tables created successfully.")
            
            # Test database connection by querying each table
            books = Book.query.all()
            customers = Customer.query.all()
            loans = Loan.query.all()
            
            print(f"Books: {len(books)}")
            print(f"Customers: {len(customers)}")
            print(f"Loans: {len(loans)}")
            
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    init_db()
