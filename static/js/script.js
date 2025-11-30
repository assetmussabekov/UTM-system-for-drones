$(document).ready(function() {
    var map = L.map('map').setView([51.1801, 71.4451], 10);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© <a href="http://openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    var route = [];
    var markers = [];

    map.on('click', function(e) {
        var coord = e.latlng;
        route.push({ lat: coord.lat, lng: coord.lng });
        var marker = L.marker([coord.lat, coord.lng]).addTo(map);
        markers.push(marker);
        $('#routeInput').val(JSON.stringify(route));
    });

    $('#clearRoute').click(function() {
        route = [];
        markers.forEach(function(marker) {
            map.removeLayer(marker);
        });
        markers = [];
        $('#routeInput').val('');
    });

    $('#droneForm').submit(function(e) {
        e.preventDefault();
        $.post('/register_drone', $(this).serialize(), function(data) {
            alert(data.message);
        });
    });

    $('#pilotForm').submit(function(e) {
        e.preventDefault();
        $.post('/register_pilot', $(this).serialize(), function(data) {
            alert(data.message);
        });
    });

    $('#flightForm').submit(function(e) {
        e.preventDefault();
        if (!route.length) {
            alert('Пожалуйста, выберите хотя бы одну точку маршрута на карте');
            return;
        }
        $.post('/submit_flight_request', $(this).serialize(), function(data) {
            alert(data.message);
            if (data.status === 'approved') {
                $('#clearRoute').click();
            }
        });
    });
});