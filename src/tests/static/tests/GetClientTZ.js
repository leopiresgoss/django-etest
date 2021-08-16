// Get between it and UTC in minutes 
const clientTzInput = document.getElementById('id_client_timezone')

// Get client's time zone
const date = new Date()
const TzOffSet = date.getTimezoneOffset()

// Get between it and UTC in minutes 
function load() {
    const submitButton = document.getElementById('submit-button') 
    submitButton.addEventListener("click", function() {
        // To send to the server
        clientTzInput.value = TzOffSet
    })
}

document.addEventListener("DOMContentLoaded", load, false)