document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM fully loaded and parsed');
});

function searchBooks() {
    const searchTerm = document.getElementById('bookSearch').value;
    fetch(`/books/search?name=${searchTerm}`)
        .then(response => response.json())
        .then(data => {
            const tableBody = document.querySelector('#booksTable tbody');
            tableBody.innerHTML = '';
            data.forEach(book => {
                const row = `
                    <tr>
                        <td>${book.name}</td>
                        <td>${book.author}</td>
                        <td>${book.year_published}</td>
                        <td>${book.book_type}</td>
                        <td>
                            <button onclick="deactivateBook(${book.book_id})">Deactivate</button>
                        </td>
                    </tr>
                `;
                tableBody.innerHTML += row;
            });
        });
}

function deactivateBook(bookId) {
    if (confirm('Are you sure you want to deactivate this book?')) {
        fetch(`/books/${bookId}/deactivate`, { method: 'PUT' })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
                location.reload();
            });
    }
}

function searchCustomers() {
    const searchTerm = document.getElementById('customerSearch').value;
    fetch(`/customers/search?name=${searchTerm}`)
        .then(response => response.json())
        .then(data => {
            const tableBody = document.querySelector('#customersTable tbody');
            tableBody.innerHTML = '';
            data.forEach(customer => {
                const row = `
                    <tr>
                        <td>${customer.name}</td>
                        <td>${customer.city}</td>
                        <td>${customer.age}</td>
                        <td>
                            <button onclick="deactivateCustomer(${customer.customer_id})">Deactivate</button>
                        </td>
                    </tr>
                `;
                tableBody.innerHTML += row;
            });
        });
}

function deactivateCustomer(customerId) {
    if (confirm('Are you sure you want to deactivate this customer?')) {
        fetch(`/customers/${customerId}/deactivate`, { method: 'PUT' })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
                location.reload();
            });
    }
}

function returnBook(loanId) {
    if (confirm('Are you sure you want to return this book?')) {
        fetch(`/loans/${loanId}/return`, { method: 'PUT' })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
                location.reload();
            });
    }
}

function populateBookDropdown() {
    fetch('/books/active')
        .then(response => response.json())
        .then(data => {
            const bookSelect = document.getElementById('bookSelect');
            bookSelect.innerHTML = '<option value="">Select a book</option>';
            data.forEach(book => {
                const option = document.createElement('option');
                option.value = book.book_id;
                option.textContent = `${book.name} by ${book.author}`;
                bookSelect.appendChild(option);
            });
        });
}

function populateCustomerDropdown() {
    fetch('/customers/active')
        .then(response => response.json())
        .then(data => {
            const customerSelect = document.getElementById('customerSelect');
            customerSelect.innerHTML = '<option value="">Select a customer</option>';
            data.forEach(customer => {
                const option = document.createElement('option');
                option.value = customer.customer_id;
                option.textContent = `${customer.name} (${customer.city})`;
                customerSelect.appendChild(option);
            });
        });
}

function checkBookAvailability(bookId) {
    return fetch(`/loans`)
        .then(response => response.json())
        .then(loans => {
            const activeLoans = loans.filter(loan => loan.book_id == bookId && !loan.return_date);
            return activeLoans.length === 0;
        });
}

function createLoan() {
    const bookId = document.getElementById('bookSelect').value;
    const customerId = document.getElementById('customerSelect').value;
    const loanDate = document.getElementById('loanDate').value;

    if (!bookId || !customerId || !loanDate) {
        alert('Please fill in all fields');
        return;
    }

    checkBookAvailability(bookId)
        .then(isAvailable => {
            if (!isAvailable) {
                alert('This book is currently unavailable');
                return;
            }

            const loanData = {
                book_id: bookId,
                customer_id: customerId,
                loan_date: loanDate
            };

            fetch('/loans', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(loanData),
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
                location.reload();
            })
            .catch((error) => {
                console.error('Error:', error);
                alert('An error occurred while creating the loan');
            });
        });
}

// Initialize dropdowns when the loans page loads
if (document.getElementById('bookSelect')) {
    populateBookDropdown();
    populateCustomerDropdown();
}
