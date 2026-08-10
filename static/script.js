// pharmacies data coming from Flask
console.log(pharmacies);

// Initialize map
var map = L.map('map').setView([28.6139, 77.2090], 13);

// OpenStreetMap tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{
 attribution:'© OpenStreetMap'
}).addTo(map);

var userLat;
var userLng;
var routingControl;

// Get user location
navigator.geolocation.getCurrentPosition(function(position){

    userLat = position.coords.latitude;
    userLng = position.coords.longitude;

    // Add user marker
    L.marker([userLat,userLng])
    .addTo(map)
    .bindPopup("You are here")
    .openPopup();

    // Center map on user
    map.setView([userLat,userLng],14);

    console.log("User Location:", userLat, userLng);

    // Add pharmacy markers
    pharmacies.forEach(function(p){

        var marker = L.marker([p.latitude,p.longitude])
        .addTo(map)
        .bindPopup(
            "<b>"+p.name+"</b><br>" +
            "Medicine: "+p.medicine+"<br>" +
            "Stock: "+p.stock
        );

        marker.on("click",function(){

            // Remove old route
            if(routingControl){
                map.removeControl(routingControl);
            }

            // Create new route
            routingControl = L.Routing.control({
                waypoints:[
                    L.latLng(userLat,userLng),
                    L.latLng(p.latitude,p.longitude)
                ],
                routeWhileDragging:false,
                show:false
            }).addTo(map);

        });

    });

}, function(error){

    alert("Location permission denied. Map may not work properly.");

    console.log(error);

});


// ===============================
// Voice Search
// ===============================

function startVoice(){

    if(!('webkitSpeechRecognition' in window)){
        alert("Voice recognition not supported in this browser.");
        return;
    }

    const recognition = new webkitSpeechRecognition();

    recognition.lang = "en-IN";

    recognition.continuous = false;

    recognition.interimResults = false;

    recognition.start();

    recognition.onstart = function(){
        console.log("Voice recognition started...");
    };

    recognition.onresult = function(event){

        let text = event.results[0][0].transcript;

        console.log("Detected voice:", text);

        // Fill input box
        document.querySelector("input[name='medicine']").value = text;

    };

    recognition.onerror = function(event){

        console.log("Voice error:", event.error);

        alert("Voice recognition failed. Try again.");

    };

    recognition.onend = function(){
        console.log("Voice recognition stopped.");
    };

}
