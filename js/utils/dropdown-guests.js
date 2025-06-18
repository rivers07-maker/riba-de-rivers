// Utility function for updating dropdown counters in the Guest section
// Use the global guests object for updateSummary
function getCurrentGuests() {
    return window.guests || { adults: 1, children: 0, pets: 0 };
}

window.updateCount = function(event, type, change) {
    event.preventDefault();
    event.stopPropagation();

    // Always read the latest values from the DOM, do not default to 1 if 0
    const adults = parseInt(document.getElementById('adults').innerText, 10);
    const children = parseInt(document.getElementById('children').innerText, 10);
    const pets = parseInt(document.getElementById('pets').innerText, 10);
    window.guests = { adults, children, pets };

    // Update the value for the type being changed
    window.guests[type] += change;

    // Enforce bounds
    if (window.guests[type] < 0) window.guests[type] = 0;
    if ((type === "adults" || type === "children") && (window.guests.adults + window.guests.children) > 4) {
        window.guests[type] -= change; // revert
        return;
    }
    if (type === "pets" && window.guests.pets > 2) {
        window.guests[type] -= change; // revert
        return;
    }

    // Update DOM
    document.getElementById(type).innerText = window.guests[type];
    document.getElementById(`input-${type}`).value = window.guests[type];

    // Update summary
    if (typeof updateSummary === 'function') {
        updateSummary(window.guests);
    }
}

// Event listener for i18n readiness
document.addEventListener("i18nReady", () => {
    updateSummary(); // When language is ready, show translated summary
});
