from flask import jsonify, request, render_template
from app import app, db
from models import Book, Customer, Loan
from datetime import datetime, timedelta
import logging
from sqlalchemy import or_

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API Routes

@app.route('/books/autocomplete', methods=['GET'])
def books_autocomplete():
    try:
        term = request.args.get('term', '')
        books = Book.query.filter(
            or_(
                Book.name.ilike(f'%{term}%'),
                Book.author.ilike(f'%{term}%')
            )
        ).filter_by(is_active=True).limit(10).all()
        return jsonify([{'id': book.book_id, 'name': f"{book.name} by {book.author}"} for book in books])
    except Exception as e:
        logger.error(f"Error in books_autocomplete route: {str(e)}")
        return jsonify({'error': 'An error occurred'}), 500

@app.route('/customers/autocomplete', methods=['GET'])
def customers_autocomplete():
    try:
        term = request.args.get('term', '')
        customers = Customer.query.filter(
            or_(
                Customer.name.ilike(f'%{term}%'),
                Customer.city.ilike(f'%{term}%')
            )
        ).filter_by(is_active=True).limit(10).all()
        return jsonify([{'id': customer.customer_id, 'name': f"{customer.name} ({customer.city})"} for customer in customers])
    except Exception as e:
        logger.error(f"Error in customers_autocomplete route: {str(e)}")
        return jsonify({'error': 'An error occurred'}), 500

@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    try:
        book = Book.query.get_or_404(book_id)
        return jsonify({
            'book_id': book.book_id,
            'name': book.name,
            'author': book.author,
            'year_published': book.year_published,
            'book_type': book.book_type
        })
    except Exception as e:
        logger.error(f"Error in get_book route: {str(e)}")
        return jsonify({'error': 'An error occurred'}), 500

@app.route('/customers/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    try:
        customer = Customer.query.get_or_404(customer_id)
        return jsonify({
            'customer_id': customer.customer_id,
            'name': customer.name,
            'city': customer.city,
            'age': customer.age
        })
    except Exception as e:
        logger.error(f"Error in get_customer route: {str(e)}")
        return jsonify({'error': 'An error occurred'}), 500

# Existing routes (books, active_books, search_books, deactivate_book, customers, active_customers, search_customers, deactivate_customer, loans, return_book, late_loans) remain unchanged

# Web Routes

@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Error in index route: {str(e)}")
        return "An error occurred", 500

@app.route('/web/books')
def web_books():
    try:
        books = Book.query.filter_by(is_active=True).all()
        return render_template('books.html', books=books)
    except Exception as e:
        logger.error(f"Error in web_books route: {str(e)}")
        return "An error occurred", 500

@app.route('/web/customers')
def web_customers():
    try:
        customers = Customer.query.filter_by(is_active=True).all()
        return render_template('customers.html', customers=customers)
    except Exception as e:
        logger.error(f"Error in web_customers route: {str(e)}")
        return "An error occurred", 500

@app.route('/web/loans')
def web_loans():
    try:
        loans = Loan.query.all()
        return render_template('loans.html', loans=loans)
    except Exception as e:
        logger.error(f"Error in web_loans route: {str(e)}")
        return "An error occurred", 500

@app.route('/web/about')
def about():
    try:
        return render_template('about.html')
    except Exception as e:
        logger.error(f"Error in about route: {str(e)}")
        return "An error occurred", 500
