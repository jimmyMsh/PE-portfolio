document.addEventListener('DOMContentLoaded', function() {
    // Welcome message animation
    const welcomeMessage = document.querySelector('.welcome-message');
    welcomeMessage.classList.add('animate');
    
    // Map initialization
    const locationsStr = document.querySelector("#locations_id").value;
    const locations = eval(locationsStr);

    var map = L.map("map").setView([locations[0][0], locations[0][1]], 3);

    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);

    for (const [lat, lng, desc] of locations) {
        L.marker([lat, lng]).addTo(map).bindPopup(desc);
    }

    // PDF viewer responsiveness
    function handlePDFViewer() {
        const pdfViewer = document.getElementById('pdf-viewer');
        const pdfLink = document.getElementById('pdf-link');
        
        if (window.innerWidth <= 480) {
            pdfViewer.style.display = 'none';
            pdfLink.style.display = 'block';
        } else {
            pdfViewer.style.display = 'block';
            pdfLink.style.display = 'none';
        }
    }

    // Initial call
    handlePDFViewer();

    // Listen for window resize events
    window.addEventListener('resize', handlePDFViewer);
});