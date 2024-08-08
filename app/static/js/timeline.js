// scripts.js
document.getElementById('timeline-form').addEventListener('submit', function(event) {
    alert('Form submitted successfully! Redirecting...');
});

// Function to format dates
function formatDates() {
    const dateElements = document.querySelectorAll('.post-date');
    dateElements.forEach(el => {
        const date = new Date(el.getAttribute('data-date'));
        const options = { 
            year: 'numeric', 
            month: 'short', 
            day: 'numeric', 
            hour: '2-digit', 
            minute: '2-digit', 
            timeZone: 'GMT',
            timeZoneName: 'short'
        };
        el.textContent = date.toLocaleString('en-US', options);
    });
}

// Initial call to format existing dates
formatDates();
