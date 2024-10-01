document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM fully loaded and parsed');
});

function initializeAutocomplete() {
    const bookSearch = document.getElementById('bookSearch');
    const customerSearch = document.getElementById('customerSearch');
    const bookId = document.getElementById('bookId');
    const customerId = document.getElementById('customerId');

    bookSearch.addEventListener('input', debounce(() => autocomplete(bookSearch, '/books/autocomplete', displayBookDetails), 300));
    customerSearch.addEventListener('input', debounce(() => autocomplete(customerSearch, '/customers/autocomplete', displayCustomerDetails), 300));
    bookId.addEventListener('change', () => fetchDetails(bookId.value, '/books/', displayBookDetails));
    customerId.addEventListener('change', () => fetchDetails(customerId.value, '/customers/', displayCustomerDetails));

    // Add event listeners for radio buttons
    document.getElementById('bookSearchRadio').addEventListener('change', toggleBookInputs);
    document.getElementById('bookIdRadio').addEventListener('change', toggleBookInputs);
    document.getElementById('customerSearchRadio').addEventListener('change', toggleCustomerInputs);
    document.getElementById('customerIdRadio').addEventListener('change', toggleCustomerInputs);
}

function toggleBookInputs() {
    const searchGroup = document.getElementById('bookSearchGroup');
    const idGroup = document.getElementById('bookIdGroup');
    const isSearchSelected = document.getElementById('bookSearchRadio').checked;

    searchGroup.style.display = isSearchSelected ? 'block' : 'none';
    idGroup.style.display = isSearchSelected ? 'none' : 'block';

    // Clear inputs and details when switching
    document.getElementById('bookSearch').value = '';
    document.getElementById('bookId').value = '';
    document.getElementById('bookDetails').innerHTML = '';
}

function toggleCustomerInputs() {
    const searchGroup = document.getElementById('customerSearchGroup');
    const idGroup = document.getElementById('customerIdGroup');
    const isSearchSelected = document.getElementById('customerSearchRadio').checked;

    searchGroup.style.display = isSearchSelected ? 'block' : 'none';
    idGroup.style.display = isSearchSelected ? 'none' : 'block';

    // Clear inputs and details when switching
    document.getElementById('customerSearch').value = '';
    document.getElementById('customerId').value = '';
    document.getElementById('customerDetails').innerHTML = '';
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
    const term = input.value;
    if (term.length < 2) return;

    fetch(`${url}?term=${encodeURIComponent(term)}`)
        .then(response => response.json())
        .then(data => {
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
        });
}

function fetchDetails(id, url, displayFunc) {
    if (!id) return;

    fetch(`${url}${id}`)
        .then(response => response.json())
        .then(data => displayFunc(data));
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
    const bookId = document.getElementById('bookIdRadio').checked ? document.getElementById('bookId').value : document.querySelector(`#bookSearchList option[value="${document.getElementById('bookSearch').value}"]`)?.dataset.id;
    const customerId = document.getElementById('customerIdRadio').checked ? document.getElementById('customerId').value : document.querySelector(`#customerSearchList option[value="${document.getElementById('customerSearch').value}"]`)?.dataset.id;
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

function checkBookAvailability(bookId) {
    return fetch(`/loans`)
        .then(response => response.json())
        .then(loans => {
            const activeLoans = loans.filter(loan => loan.book_id == bookId && !loan.return_date);
            return activeLoans.length === 0;
        });
}

// Existing functions (searchBooks, deactivateBook, searchCustomers, deactivateCustomer, returnBook) remain unchanged
