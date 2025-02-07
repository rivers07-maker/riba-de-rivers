document.getElementById("reservation-form").addEventListener("submit", async function(event) {
    event.preventDefault(); // Prevent default form submission

    const apiKey = HOSTHUB_KEY; // Replace with your actual API key
    const apiUrl = "https://www.hosthub.com/api/v1/reservations"; // Replace with correct endpoint

    // Get form values
    const arrival = document.getElementById("arrival").value;
    const departure = document.getElementById("departure").value;
    const guests = document.getElementById("guests").value;

    // Construct API request body
    const requestData = {
        check_in: arrival,
        check_out: departure,
        guests: parseInt(guests),
        status: "pending" // or "pending" if you want to manually confirm
    };

    try {
        const response = await fetch(apiUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${apiKey}`
            },
            body: JSON.stringify(requestData)
        });

        const data = await response.json();

        if (response.ok) {
            alert("Reservation successfully created!");
        } else {
            alert(`Error: ${data.message}`);
        }
    } catch (error) {
        console.error("API request failed:", error);
        alert("An error occurred while processing your reservation.");
    }
});
