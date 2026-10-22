// billing.js - POS Billing calculation and print helper
document.addEventListener('DOMContentLoaded', function () {
    const batchSelect = document.querySelector('select[name="batch_id"]');
    const quantityInput = document.querySelector('input[name="quantity"]');
    
    function updateSubtotal() {
        if (!batchSelect || !quantityInput) return;
        
        const selectedOption = batchSelect.options[batchSelect.selectedIndex];
        if (!selectedOption) return;
        
        // Extract price from option text format: "... | ₹XX.XX"
        const text = selectedOption.text;
        const priceMatch = text.match(/₹([\d.]+)/);
        
        if (priceMatch) {
            const unitPrice = parseFloat(priceMatch[1]);
            const qty = parseInt(quantityInput.value) || 0;
            const subtotal = unitPrice * qty;
            
            // Optional: Display live calculated subtotal in the UI if an element exists
            const subtotalDisplay = document.getElementById('live-subtotal');
            if (subtotalDisplay) {
                subtotalDisplay.textContent = `₹${subtotal.toFixed(2)}`;
            }
        }
    }

    if (batchSelect && quantityInput) {
        batchSelect.addEventListener('change', updateSubtotal);
        quantityInput.addEventListener('input', updateSubtotal);
        updateSubtotal(); // Initial call
    }
});