from flask import jsonify, request, render_template
from app import app, db
from models import Book, Customer, Loan
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API Routes

@app.route('/books', methods=['GET', 'POST'])
def books():
    try:
        if request.method == 'POST':
            data = request.json
            new_book = Book(
                name=data['name'],
                author=data['author'],
                year_published=data['year_published'],
                book_type=data['book_type']
            )
            db.session.add(new_book)
            db.session.commit()
            return jsonify({'message': 'Book added successfully'}), 201
        else:
            books = Book.query.filter_by(is_active=True).all()
            return jsonify([{
                'book_id': book.book_id,
                'name': book.name,
                'author': book.author,
                'year_published': book.year_published,
                'book_type': book.book_type
            } for book in books])
    except Exception as e:
        logger.error(f"Error in books route: {str(e)}")
        return jsonify({'error': 'An error occurred'}), 500

@app.route('/books/search', methods=['GET'])
def search_books():
    try:
        name = request.args.get('name')
        books = Book.query.filter(Book.name.ilike(f'%{name}%'), Book.is_active==True).all()
        return jsonify([{
            'book_id': book.book_id,
            'name': book.name,
            'author': book.author,
            'year_published': book.year_published,
            'book_type': book.book_type
        } for book in books])
    except Exception as e:
        logger.error(f"Error in search_books route: {str(e)}")
        return jsonify({'error': 'An error occurred'}), 500

@app.route('/books/<int:book_id>/deactivate', methods=['PUT'])
def deactivate_book(book_id):
    try:
        book = Book.query.get_or_404(book_id)
        book.is_active = False
        db.session.commit()
        return jsonify({'message': 'Book deactivated successfully'})
    except Exception as e:
        logger.error(f"Error in deactivate_book route: {str(e)}")
        return jsonify({'error': 'An error occurred'}), 500

@app.route('/customers', methods=['GET', 'POST'])
def customers():
    try:
        if request.method == 'POST':
            data = request.json
            new_customer = Customer(
                name=data['name'],
                city=data['city'],
                age=data['age']
            )
            db.session.add(new_customer)
            db.session.commit()
            return jsonify({'message': 'Customer added successfully'}), 201
        else:
            customers = Customer.query.filter_by(is_active=True).all()
            return jsonify([{
                'customer_id': customer.customer_id,
                'name': customer.name,
                'city': customer.city,
                'age': customer.age
            } for customer in customers])
    except Exception as e:
        logger.error(f"Error in customers route: {str(e)}")
        return jsonify({'error': 'An error occurred'}), 500

@app.route('/customers/search', methods=['GET'])
def search_customers():
    try:
        name = request.args.get('name')
        customers = Customer.query.filter(Customer.name.ilike(f'%{name}%'), Customer.is_active==True).all()
        return jsonify([{
            'customer_id': customer.customer_id,
            'name': customer.name,
            'city': customer.city,
            'age': customer.age
        } for customer in customers])
    except Exception as e:
        logger.error(f"Error in search_customers route: {str(e)}")
        return jsonify({'error': 'An error occurred'}), 500

@app.route('/customers/<int:customer_id>/deactivate', methods=['PUT'])
def deactivate_customer(customer_id):
    try:
        customer = Customer.query.get_or_404(customer_id)
        customer.is_active = False
        db.session.commit()
        return jsonify({'message': 'Customer deactivated successfully'})
    except Exception as e:
        logger.error(f"Error in deactivate_customer route: {str(e)}")
        return jsonify({'error': 'An error occurred'}), 500

@app.route('/loans', methods=['GET', 'POST'])
def loans():
    try:
        if request.method == 'POST':
            data = request.json
            book = Book.query.get(data['book_id'])
            customer = Customer.query.get(data['customer_id'])
            if not book or not customer or not book.is_active or not customer.is_active:
                return jsonify({'message': 'Invalid book or customer'}), 400
            new_loan = Loan(
                customer_id=data['customer_id'],
                book_id=data['book_id'],
                loan_date=datetime.strptime(data['loan_date'], '%Y-%m-%d').date()
            )
            db.session.add(new_loan)
            db.session.commit()
            return jsonify({'message': 'Loan created successfully'}), 201
        else:
            loans = Loan.query.all()
            return jsonify([{
                'loan_id': loan.loan_id,
                'customer_id': loan.customer_id,
                'book_id': loan.book_id,
                'loan_date': loan.loan_date.isoformat(),
                'return_date': loan.return_date.isoformat() if loan.return_date else None
            } for loan in loans])
    except Exception as e:
        logger.error(f"Error in loans route: {str(e)}")
        return jsonify({'error': 'An error occurred'}), 500

@app.route('/loans/<int:loan_id>/return', methods=['PUT'])
def return_book(loan_id):
    try:
        loan = Loan.query.get_or_404(loan_id)
        loan.return_date = datetime.utcnow().date()
        db.session.commit()
        return jsonify({'message': 'Book returned successfully'})
    except Exception as e:
        logger.error(f"Error in return_book route: {str(e)}")
        return jsonify({'error': 'An error occurred'}), 500

@app.route('/loans/late', methods=['GET'])
def late_loans():
    try:
        today = datetime.utcnow().date()
        loans = Loan.query.filter(Loan.return_date == None).all()
        late_loans = []
        for loan in loans:
            book = Book.query.get(loan.book_id)
            if book:
                max_days = {1: 10, 2: 5, 3: 2}[book.book_type]
                if (today - loan.loan_date).days > max_days:
                    late_loans.append({
                        'loan_id': loan.loan_id,
                        'customer_id': loan.customer_id,
                        'book_id': loan.book_id,
                        'loan_date': loan.loan_date.isoformat(),
                        'days_overdue': (today - loan.loan_date).days - max_days
                    })
        return jsonify(late_loans)
    except Exception as e:
        logger.error(f"Error in late_loans route: {str(e)}")
        return jsonify({'error': 'An error occurred'}), 500

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
