import logging
from app import app, db
from models import Book, Customer, Loan
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def insert_sample_books():
    books = [
        {"name": "To Kill a Mockingbird", "author": "Harper Lee", "year_published": 1960, "book_type": 1},
        {"name": "1984", "author": "George Orwell", "year_published": 1949, "book_type": 2},
        {"name": "The Great Gatsby", "author": "F. Scott Fitzgerald", "year_published": 1925, "book_type": 3},
        {"name": "The Catcher in the Rye", "author": "J.D. Salinger", "year_published": 1951, "book_type": 1},
        {"name": "Pride and Prejudice", "author": "Jane Austen", "year_published": 1813, "book_type": 2},
        {"name": "The Hobbit", "author": "J.R.R. Tolkien", "year_published": 1937, "book_type": 3},
        {"name": "Moby Dick", "author": "Herman Melville", "year_published": 1851, "book_type": 1},
        {"name": "War and Peace", "author": "Leo Tolstoy", "year_published": 1869, "book_type": 2},
        {"name": "Crime and Punishment", "author": "Fyodor Dostoevsky", "year_published": 1866, "book_type": 3},
        {"name": "Brave New World", "author": "Aldous Huxley", "year_published": 1932, "book_type": 1}
    ]
    for book_data in books:
        existing_book = Book.query.filter_by(name=book_data['name'], author=book_data['author']).first()
        if not existing_book:
            new_book = Book(**book_data)
            db.session.add(new_book)
            logger.info(f"Added book: {book_data['name']}")
        else:
            logger.info(f"Book already exists: {book_data['name']}")

def insert_sample_customers():
    customers = [
        {"name": "John Doe", "city": "New York", "age": 30},
        {"name": "Emily Clark", "city": "Los Angeles", "age": 25},
        {"name": "Michael Johnson", "city": "Chicago", "age": 40},
        {"name": "Sophia Brown", "city": "Houston", "age": 35},
        {"name": "James Wilson", "city": "Phoenix", "age": 28},
        {"name": "Olivia Martin", "city": "Philadelphia", "age": 22},
        {"name": "William Garcia", "city": "San Antonio", "age": 45},
        {"name": "Isabella Anderson", "city": "San Diego", "age": 31},
        {"name": "Henry Davis", "city": "Dallas", "age": 26},
        {"name": "Amelia Rodriguez", "city": "San Jose", "age": 50}
    ]
    for customer_data in customers:
        existing_customer = Customer.query.filter_by(name=customer_data['name'], city=customer_data['city']).first()
        if not existing_customer:
            new_customer = Customer(**customer_data)
            db.session.add(new_customer)
            logger.info(f"Added customer: {customer_data['name']}")
        else:
            logger.info(f"Customer already exists: {customer_data['name']}")

def insert_sample_loans():
    loans = [
        {"book_id": 1, "customer_id": 5, "loan_date": "2023-09-01", "return_date": "2023-09-08"},
        {"book_id": 3, "customer_id": 1, "loan_date": "2023-09-05", "return_date": "2023-09-10"},
        {"book_id": 2, "customer_id": 7, "loan_date": "2023-09-07", "return_date": "2023-09-09"},
        {"book_id": 4, "customer_id": 6, "loan_date": "2023-09-10", "return_date": "2023-09-15"},
        {"book_id": 5, "customer_id": 8, "loan_date": "2023-09-12", "return_date": None},
        {"book_id": 6, "customer_id": 9, "loan_date": "2023-09-14", "return_date": None},
        {"book_id": 7, "customer_id": 2, "loan_date": "2023-09-15", "return_date": "2023-09-18"},
        {"book_id": 8, "customer_id": 10, "loan_date": "2023-09-17", "return_date": None},
        {"book_id": 9, "customer_id": 3, "loan_date": "2023-09-19", "return_date": None},
        {"book_id": 10, "customer_id": 4, "loan_date": "2023-09-20", "return_date": None}
    ]
    for loan_data in loans:
        existing_loan = Loan.query.filter_by(
            book_id=loan_data['book_id'],
            customer_id=loan_data['customer_id'],
            loan_date=datetime.strptime(loan_data['loan_date'], '%Y-%m-%d').date()
        ).first()
        if not existing_loan:
            new_loan = Loan(
                book_id=loan_data['book_id'],
                customer_id=loan_data['customer_id'],
                loan_date=datetime.strptime(loan_data['loan_date'], '%Y-%m-%d').date(),
                return_date=datetime.strptime(loan_data['return_date'], '%Y-%m-%d').date() if loan_data['return_date'] else None
            )
            db.session.add(new_loan)
            logger.info(f"Added loan: Book ID {loan_data['book_id']}, Customer ID {loan_data['customer_id']}")
        else:
            logger.info(f"Loan already exists: Book ID {loan_data['book_id']}, Customer ID {loan_data['customer_id']}")

if __name__ == '__main__':
    with app.app_context():
        try:
            insert_sample_books()
            insert_sample_customers()
            insert_sample_loans()
            db.session.commit()
            logger.info("Sample data inserted successfully.")
        except Exception as e:
            db.session.rollback()
            logger.error(f"An error occurred while inserting sample data: {str(e)}")
