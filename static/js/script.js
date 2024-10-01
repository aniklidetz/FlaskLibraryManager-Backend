document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM fully loaded and parsed');
    initializeAutocomplete();
});

function initializeAutocomplete() {
    console.log('Initializing autocomplete');
    const bookSearch = document.getElementById('bookSearch');
    const customerSearch = document.getElementById('customerSearch');

    if (bookSearch) {
        console.log('Setting up book search listener');
        bookSearch.addEventListener('input', debounce(() => autocomplete(bookSearch, '/books/autocomplete', displayBookDetails), 300));
    }
    if (customerSearch) {
        console.log('Setting up customer search listener');
        customerSearch.addEventListener('input', debounce(() => autocomplete(customerSearch, '/customers/autocomplete', displayCustomerDetails), 300));
    }
}

function debounce(func, delay) {
    let debounceTimer;
    return function() {
        const context = this;
        const args = arguments;
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => func.apply(context, args), delay);
    }
}

function autocomplete(input, url, displayFunc) {
    console.log('Autocomplete function called');
    const term = input.value;
    if (term.length < 2) return;

    console.log(`Fetching autocomplete data for: ${term}`);
    fetch(`${url}?term=${encodeURIComponent(term)}`)
        .then(response => response.json())
        .then(data => {
            console.log('Autocomplete data received:', data);
            const datalist = document.createElement('datalist');
            datalist.id = `${input.id}List`;
            data.forEach(item => {
                const option = document.createElement('option');
                option.value = item.name;
                option.dataset.id = item.id;
                datalist.appendChild(option);
            });
            
            const existingDatalist = document.getElementById(datalist.id);
            if (existingDatalist) {
                existingDatalist.replaceWith(datalist);
            } else {
                document.body.appendChild(datalist);
            }
            
            input.setAttribute('list', datalist.id);
        })
        .catch(error => console.error('Error in autocomplete:', error));
}

function displayBookDetails(book) {
    const detailsDiv = document.getElementById('bookDetails');
    detailsDiv.innerHTML = `
        <p><strong>Title:</strong> ${book.name}</p>
        <p><strong>Author:</strong> ${book.author}</p>
        <p><strong>Year:</strong> ${book.year_published}</p>
        <p><strong>Type:</strong> ${book.book_type}</p>
    `;
}

function displayCustomerDetails(customer) {
    const detailsDiv = document.getElementById('customerDetails');
    detailsDiv.innerHTML = `
        <p><strong>Name:</strong> ${customer.name}</p>
        <p><strong>City:</strong> ${customer.city}</p>
        <p><strong>Age:</strong> ${customer.age}</p>
    `;
}

function createLoan() {
    console.log('Creating loan');
    const bookId = document.querySelector(`#bookSearchList option[value="${document.getElementById('bookSearch').value}"]`)?.dataset.id;
    const customerId = document.querySelector(`#customerSearchList option[value="${document.getElementById('customerSearch').value}"]`)?.dataset.id;
    const loanDate = document.getElementById('loanDate').value;

    console.log('Book ID:', bookId);
    console.log('Customer ID:', customerId);
    console.log('Loan Date:', loanDate);

    if (!bookId || !customerId || !loanDate) {
        console.log('Missing fields');
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

function checkBookAvailability(bookId) {
    return fetch(`/loans`)
        .then(response => response.json())
        .then(loans => {
            const activeLoans = loans.filter(loan => loan.book_id == bookId && !loan.return_date);
            return activeLoans.length === 0;
        });
}

// Existing functions (searchBooks, deactivateBook, searchCustomers, deactivateCustomer, returnBook) remain unchanged
