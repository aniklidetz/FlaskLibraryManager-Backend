document.addEventListener('DOMContentLoaded', function() {
    // Add event listeners or other JavaScript functionality here
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
