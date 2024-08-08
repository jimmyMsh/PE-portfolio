document.addEventListener('DOMContentLoaded', function() {
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

    // Welcome message animation
    const welcomeMessage = document.querySelector('.welcome-message');
    welcomeMessage.classList.add('animate');
});