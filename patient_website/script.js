// Existing login functionality
const users = {
    "admin": "password123",
    "doctor": "securepass",
    "nurse": "nursepassword"
};

// Handle login form submission
const loginForm = document.getElementById('login-form');
if (loginForm) {
    loginForm.addEventListener('submit', function(event) {
        event.preventDefault();  // Prevent the form from submitting normally

        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        // Check if the username and password are correct
        if (users[username] && users[username] === password) {
            // Show the loading screen
            document.getElementById('loading-screen').style.display = 'flex';

            // Simulate the login process
            setTimeout(function() {
                // After login process, redirect to medical records
                window.location.href = "medical-record.html";
            }, 3000);  // Simulate a 3-second login delay
        } else {
            alert("Invalid username or password. Please try again.");
        }
    });
}

// Back button functionality
function handleBackButtonClick() {
    // Show the loading screen
    document.getElementById('loading-screen').style.display = 'flex';

    // Simulate a brief delay before navigating back
    setTimeout(function() {
        window.history.back();
    }, 1000); // 1-second delay
}

// Check if back button exists on the page before adding the event listener
const backButton = document.getElementById('back-button');
if (backButton) {
    backButton.addEventListener('click', function(event) {
        event.preventDefault();
        handleBackButtonClick();
    });
}

// Hide loading screen on page show (including back navigation)
window.addEventListener('pageshow', function(event) {
    var loadingScreen = document.getElementById('loading-screen');
    if (loadingScreen) {
        loadingScreen.style.display = 'none';
    }
});
