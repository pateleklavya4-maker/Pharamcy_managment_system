// inventory.js - Handles dynamic search and UI feedback on the Inventory page
document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.querySelector('input[name="search"]');
    
    if (searchInput) {
        searchInput.addEventListener('input', function (e) {
            const term = e.target.value.trim();
            // You can add live search AJAX logic here if required, 
            // otherwise the form submit handles it smoothly.
        });
    }
    console.log("Inventory script loaded successfully.");
});