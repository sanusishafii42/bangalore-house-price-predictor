 // Fetch location names from backend
fetch('/get_location_names') // 1. Send a GET request to your Flask API to get the list of locations.
    .then(res => res.json()) // 2. When the response arrives, convert it from JSON text to a JavaScript object.
    .then(data => {          // 3. When the data is ready, run this function:
        const locationSelect = document.getElementById('location'); // 4. Find the <select> element with id="location".
        locationSelect.innerHTML = ''; // 5. Clear any existing options in the dropdown.
        data.location.forEach(loc => { // 6. For each location in the received list:
            const opt = document.createElement('option'); // 7. Create a new <option> element.
            opt.value = loc;                              // 8. Set the value of the option to the location name.
            opt.textContent = loc.charAt(0).toUpperCase() + loc.slice(1); // 9. Capitalize the first letter for display.
            locationSelect.appendChild(opt);              // 10. Add the option to the dropdown.
        });
    });

// Handle form submission
document.getElementById('predictForm').addEventListener('submit', function(e) { // 11. When the form is submitted:
    e.preventDefault(); // 12. Stop the page from reloading.
    const location = document.getElementById('location').value; // 13. Get the selected location.
    const total_sqft = document.getElementById('sqft').value;   // 14. Get the entered square footage.
    const size = document.getElementById('size').value;         // 15. Get the entered number of bedrooms.
    const bath = document.getElementById('bath').value;         // 16. Get the entered number of bathrooms.
    const formData = new URLSearchParams(); // 17. Create a new object to hold form data in URL format.
    formData.append('location', location);      // 18. Add location to the form data.
    formData.append('total_sqft', total_sqft);  // 19. Add total_sqft to the form data.
    formData.append('size', size);              // 20. Add size to the form data.
    formData.append('bath', bath);              // 21. Add bath to the form data.

    fetch('/predict_home_price', {              // 22. Send a POST request to your Flask API to get the prediction.
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, // 23. Tell the server the data format.
        body: formData                         // 24. Attach the form data to the request.
    })
    .then(res => res.json())                   // 25. When the response arrives, convert it to a JavaScript object.
    .then(data => {                            // 26. When the data is ready:
        document.getElementById('result').textContent = 
            "Estimated Price: ₹ " + data.estimated_price.toLocaleString(); // 27. Show the predicted price on the page.
    })
    .catch(() => {                             // 28. If there is an error (e.g., server not working):
        document.getElementById('result').textContent = "Error predicting price."; // 29. Show an error message.
    });
});