// expiry.js - Manages Expiry Tracker interactivity
document.addEventListener('DOMContentLoaded', function () {
    const statusBadges = document.querySelectorAll('.badge');
    
    statusBadges.forEach(badge => {
        if (badge.textContent.trim() === 'EXPIRED') {
            badge.closest('tr').classList.add('table-danger');
        } else if (badge.textContent.trim() === 'EXPIRING SOON') {
            badge.closest('tr').classList.add('table-warning');
        }
    });
    
    console.log("Expiry tracker script initialized.");
});