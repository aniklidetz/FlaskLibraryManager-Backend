# Library Management System

## Project Overview
This project implements a simple library management system using a Flask RESTful API and SQLAlchemy ORM, with an SQLite database. The system manages books, customers, and loans.

## Features
- **Books Management**: Add, search, deactivate, and retrieve active books.
- **Customers Management**: Add, search, deactivate, and retrieve active customers.
- **Loans Management**: Loan books to customers, return books, and view all loans including late loans.

## Database Setup
The application uses an SQLite database with three tables:

### Books Table
- **book_id**: Primary Key, Auto-increment Integer
- **name**: String
- **author**: String
- **year_published**: Integer
- **book_type**: Integer (1, 2, or 3)
- **is_active**: Boolean, default True

### Customers Table
- **customer_id**: Primary Key, Auto-increment Integer
- **name**: String
- **city**: String
- **age**: Integer
- **is_active**: Boolean, default True

### Loans Table
- **loan_id**: Primary Key, Auto-increment Integer
- **customer_id**: Foreign Key to Customers.customer_id
- **book_id**: Foreign Key to Books.book_id
- **loan_date**: Date
- **return_date**: Date or NULL

## API Endpoints
### Books
- **POST /books**: Adds a new book to the database.
- **GET /books**: Retrieves a list of all active books.
- **GET /books/search?name=<name>**: Searches for books by name.
- **PUT /books/<book_id>/deactivate**: Sets the `is_active` field of the book to False.

### Customers
- **POST /customers**: Adds a new customer to the database.
- **GET /customers**: Retrieves a list of all active customers.
- **GET /customers/search?name=<name>**: Searches for customers by name.
- **PUT /customers/<customer_id>/deactivate**: Sets the `is_active` field of the customer to False.

### Loans
- **POST /loans**: Creates a new loan record.
- **PUT /loans/<loan_id>/return**: Sets the return date for a loan.
- **GET /loans**: Retrieves all loan records.
- **GET /loans/late**: Retrieves loans that are overdue.

## Installation
1Clone the repository:
   ```bash
   git clone <https://github.com/aniklidetz/FlaskLibraryManagerBackend.git>