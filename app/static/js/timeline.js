function formatDates() {
    const dateElements = document.querySelectorAll('.post-date');
    dateElements.forEach(el => {
        const dateStr = el.getAttribute('data-date');
        if (!dateStr) return;
        
        
        // Create date object - it will be in UTC
        const date = new Date(dateStr);
        
        // Debug UTC time
        console.log('UTC time:', date.toISOString());
        
        const options = { 
            year: 'numeric', 
            month: 'short', 
            day: 'numeric', 
            hour: 'numeric',
            minute: '2-digit',
            timeZone: 'America/New_York',
            timeZoneName: 'short',
            hour12: true
        };
        
        // Convert to EST and format
        const formattedDate = date.toLocaleString('en-US', options);
        console.log('Formatted in EST:', formattedDate);
        
        el.textContent = formattedDate;
    });
}

document.addEventListener('DOMContentLoaded', formatDates);