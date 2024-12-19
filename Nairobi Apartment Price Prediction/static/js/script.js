function predictPrice() {

    

    // Collect form data
    const location = document.getElementById('location').value;
    const distance = document.getElementById('distance').value;
    const floorSize = document.getElementById('floor-size').value;
    const bedrooms = document.getElementById('bedrooms').value;
    const bathrooms = document.getElementById('bathrooms').value;

    // Collect selected amenities
    const amenities = [];
    if (document.getElementById('amenity1').checked) amenities.push(1);
    else amenities.push(0);
    if (document.getElementById('amenity2').checked) amenities.push(1);
    else amenities.push(0);
    if (document.getElementById('amenity3').checked) amenities.push(1);
    else amenities.push(0);
    if (document.getElementById('amenity4').checked) amenities.push(1);
    else amenities.push(0);
    if (document.getElementById('amenity5').checked) amenities.push(1);
    else amenities.push(0);

    // Prepare the data to send to the backend
    const data = {
        location: location,
        distance: distance,
        floor_size: floorSize,
        bedrooms: bedrooms,
        bathrooms: bathrooms,
        amenities: amenities
    };

    // Send a POST request to the Flask backend
    fetch('http://127.0.0.1:5000/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
       
        // Display the predicted price and location name in an alert
        const locationName = data.location_name || "Unknown Location";
        const predictedPrice = data.predicted_price;
        alert(`The predicted apartment price for  ${locationName} is Ksh  ${predictedPrice.toLocaleString()}`);
    })
    .catch(error => {
        
        console.error('Error:', error);
    });
}
