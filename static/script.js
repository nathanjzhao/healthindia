// script.js

// Translation data
var translations = {
    en: {
        // index
        selectLanguage: "Select Your Language",
        // login
        accessMedicalRecords: "Access Medical Records",
        login: "Login",
        username: "Phone Number:",
        password: "Password:",
        loginButton: "Log In",
        callTelemedicineHub: "Call Telemedicine Hub",
        phoneNumber: "Phone Number:",
        callButton: "Call",
        loggingIn: "Logging in...",
        back: "Back",
        // medical-record
        medicalRecordSummary: "Medical Record Summary",
        patientInformation: "Patient Information",
        firstName: "First Name",
        lastName: "Last Name",
        dateOfBirth: "Date of Birth",
        gender: "Gender",
        height: "Height (cm)",
        weight: "Weight (kg)",
        chronologicalSummary: "Chronological Medical Records Summary",
        dateTime: "Date/Time",
        encounterSummary: "Encounter Summary",
        loading: "Loading..."
    },
    hi: {
        // index
        selectLanguage: "अपनी भाषा चुनें",
        // login
        accessMedicalRecords: "मेडिकल रिकॉर्ड तक पहुंचें",
        login: "लॉगिन",
        username: "फोन नंबर:",
        password: "पासवर्ड:",
        loginButton: "लॉग इन करें",
        callTelemedicineHub: "टेलीमेडिसिन हब को कॉल करें",
        phoneNumber: "फोन नंबर:",
        callButton: "कॉल करें",
        loggingIn: "लॉग इन हो रहा है...",
        back: "वापस",
        // medical-record
        medicalRecordSummary: "मेडिकल रिकॉर्ड सारांश",
        patientInformation: "रोगी की जानकारी",
        firstName: "पहला नाम",
        lastName: "अंतिम नाम",
        dateOfBirth: "जन्म तिथि",
        gender: "लिंग",
        height: "ऊंचाई (सेमी)",
        weight: "वजन (किग्रा)",
        chronologicalSummary: "कालानुक्रमिक मेडिकल रिकॉर्ड सारांश",
        dateTime: "दिनांक/समय",
        encounterSummary: "मुठभेड़ सारांश",
        loading: "लोड हो रहा है..."
    },
    mr: {
    // index
    selectLanguage: "உங்கள் மொழியைத் தேர்ந்தெடுக்கவும்",
    // login
    accessMedicalRecords: "மருத்துவ பதிவுகளை அணுகவும்",
    login: "உள்நுழை",
    username: "தொலைபேசி எண்:",
    password: "கடவுச்சொல்:",
    loginButton: "உள்நுழை",
    callTelemedicineHub: "தொலை மருத்துவ மையத்திற்கு அழைக்கவும்",
    phoneNumber: "தொலைபேசி எண்:",
    callButton: "அழைக்கவும்",
    loggingIn: "உள்நுழைகிறது...",
    back: "பின்செல்",
    // medical-record
    medicalRecordSummary: "மருத்துவ பதிவு சுருக்கம்",
    patientInformation: "நோயாளர் தகவல்",
    firstName: "முதல் பெயர்",
    lastName: "கடைசி பெயர்",
    dateOfBirth: "பிறந்த தேதி",
    gender: "பாலினம்",
    height: "உயரம் (cm)",
    weight: "எடை (kg)",
    chronologicalSummary: "காலவரிசைப்படி மருத்துவ பதிவு சுருக்கம்",
    dateTime: "தேதி/நேரம்",
    encounterSummary: "சந்திப்பு சுருக்கம்",
    loading: "ஏற்றப்படுகிறது..."
    }
    
};

// Function to set language
function setLanguage(lang) {
    localStorage.setItem('language', lang);
}

// Function to get current language
function getLanguage() {
    return localStorage.getItem('language') || 'en';
}

// Function to translate the page
function translatePage() {
    var lang = getLanguage();
    var trans = translations[lang];

    if (!trans) return; // If no translations are available for the selected language

    // index
    var selectLanguageTitle = document.querySelector('.language-container h1');
    if (selectLanguageTitle) {
        selectLanguageTitle.textContent = trans.selectLanguage;
    }

    // login
    var languageBackButton = document.getElementById('language-back-button');
    if (languageBackButton) {
        languageBackButton.textContent = trans.back;
    }

    var loginTitle = document.getElementById('login-title');
    if (loginTitle) {
        loginTitle.textContent = trans.accessMedicalRecords;
    }

    var loginHeading = document.getElementById('login-heading');
    if (loginHeading) {
        loginHeading.textContent = trans.login;
    }

    var usernameLabel = document.getElementById('username-label');
    if (usernameLabel) {
        usernameLabel.textContent = trans.username;
    }

    var passwordLabel = document.getElementById('password-label');
    if (passwordLabel) {
        passwordLabel.textContent = trans.password;
    }

    var loginButton = document.getElementById('login-button');
    if (loginButton) {
        loginButton.textContent = trans.loginButton;
    }

    var callHeading = document.getElementById('call-heading');
    if (callHeading) {
        callHeading.textContent = trans.callTelemedicineHub;
    }

    var phoneLabel = document.getElementById('phone-label');
    if (phoneLabel) {
        phoneLabel.textContent = trans.phoneNumber;
    }

    var callButton = document.getElementById('call-button');
    if (callButton) {
        callButton.value = trans.callButton;
    }

    var toNumberInput = document.getElementById('to_number');
    if (toNumberInput) {
        toNumberInput.setAttribute('placeholder', trans.phoneNumber);
    }

    var usernameInput = document.getElementById('username');
    if (usernameInput) {
        usernameInput.setAttribute('placeholder', trans.username);
    }

    var passwordInput = document.getElementById('password');
    if (passwordInput) {
        passwordInput.setAttribute('placeholder', trans.password);
    }

    var loadingText = document.getElementById('loading-text');
    if (loadingText) {
        loadingText.textContent = trans.loggingIn;
    }

    // medical-record
    var medicalRecordTitle = document.getElementById('medical-record-title');
    if (medicalRecordTitle) {
        medicalRecordTitle.textContent = trans.medicalRecordSummary;
    }

    var patientInfoHeading = document.getElementById('patient-info-heading');
    if (patientInfoHeading) {
        patientInfoHeading.textContent = trans.patientInformation;
    }

    var firstNameLabel = document.getElementById('first-name-label');
    if (firstNameLabel) {
        firstNameLabel.textContent = trans.firstName;
    }

    var lastNameLabel = document.getElementById('last-name-label');
    if (lastNameLabel) {
        lastNameLabel.textContent = trans.lastName;
    }

    var dobLabel = document.getElementById('dob-label');
    if (dobLabel) {
        dobLabel.textContent = trans.dateOfBirth;
    }

    var genderLabel = document.getElementById('gender-label');
    if (genderLabel) {
        genderLabel.textContent = trans.gender;
    }

    var heightLabel = document.getElementById('height-label');
    if (heightLabel) {
        heightLabel.textContent = trans.height;
    }

    var weightLabel = document.getElementById('weight-label');
    if (weightLabel) {
        weightLabel.textContent = trans.weight;
    }

    var recordSummaryHeading = document.getElementById('record-summary-heading');
    if (recordSummaryHeading) {
        recordSummaryHeading.textContent = trans.chronologicalSummary;
    }

    var dateTimeHeader = document.getElementById('date-time-header');
    if (dateTimeHeader) {
        dateTimeHeader.textContent = trans.dateTime;
    }

    var encounterSummaryHeader = document.getElementById('encounter-summary-header');
    if (encounterSummaryHeader) {
        encounterSummaryHeader.textContent = trans.encounterSummary;
    }

    var loadingScreenText = document.getElementById('loading-text');
    if (loadingScreenText) {
        loadingScreenText.textContent = trans.loading;
    }

    var backButton = document.getElementById('back-button');
    if (backButton) {
        backButton.textContent = trans.back;
    }
}

// Event listeners for language selection buttons
document.addEventListener('DOMContentLoaded', function() {
    var languageButtons = document.querySelectorAll('.language-button');
    for (var i = 0; i < languageButtons.length; i++) {
        (function(button) {
            button.addEventListener('click', function() {
                var selectedLang = button.getAttribute('data-lang');
                setLanguage(selectedLang);
                // Redirect to login page
                window.location.href = 'login';
            });
        })(languageButtons[i]);
    }

    // Event listener for back button on login page
    var languageBackButton = document.getElementById('language-back-button');
    if (languageBackButton) {
        languageBackButton.addEventListener('click', function() {
            window.location.href = '/'; // Changed from 'index' to '/'
        });
    }

    // Call translatePage on page load
    translatePage();
});

JSON_CURR = 'user_history_+12223334444.json'
function fetchMedicalRecord() {
    return fetch('/static/user_data/user_history_+12223334444.json')  // Correct path to the file
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .catch(error => {
            console.error('Error fetching medical record:', error);
            alert("An error occurred while fetching data.");
        });
}


// Handle login form submission
var loginForm = document.getElementById('login-form');

if (loginForm) {
    loginForm.addEventListener('submit', function(event) {
        event.preventDefault();  // Prevent the form from submitting normally

        var enteredUsername = document.getElementById('username').value;
        var enteredPassword = document.getElementById('password').value;

        // Fetch the medical record JSON (assuming it contains the user credentials)
        fetchMedicalRecord().then(record => {
            if (record) {
                var storedUsername = record.username;
                var storedPassword = record.password;

                // Check if the entered credentials match the stored credentials
                if (enteredUsername === storedUsername && enteredPassword === storedPassword) {
                    // Show the loading screen
                    document.getElementById('loading-screen').style.display = 'flex';

                    // Simulate the login process
                    setTimeout(function() {
                        // After login process, redirect to medical records
                        window.location.href = "medical-record";
                    }, 1000);
                } else {
                    alert("Invalid username or password. Please try again.");
                }
            } else {
                alert("Failed to retrieve user data.");
            }
        });
    });
}

// Back button functionality on medical-record
function handleBackButtonClick() {
    // Show the loading screen
    document.getElementById('loading-screen').style.display = 'flex';

    // Simulate a brief delay before navigating back
    setTimeout(function() {
        window.history.back();
    }, 1000); // 1-second delay
}

// Check if back button exists on the page before adding the event listener
var backButton = document.getElementById('back-button');
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

function populateMedicalRecord(data) {
    // Fill patient info
    document.getElementById('first-name').textContent = data.fname || '';
    document.getElementById('last-name').textContent = data.lname || '';
    document.getElementById('dob').textContent = data.dob || '';
    document.getElementById('gender').textContent = data.gender || '';
    document.getElementById('height').textContent = data.height || '';
    document.getElementById('weight').textContent = data.weight || '';

    // Check if there are entries in the medical records
    const recordEntries = document.getElementById('record-entries');
    recordEntries.innerHTML = ''; // Clear previous entries

    if (data.entries && data.entries.length > 0) {
        // Loop over the entries (date -> entry pair)
        data.entries.forEach(entryObj => {
            for (const [date, entries] of Object.entries(entryObj)) {
                const row = document.createElement('tr');

                // Create date cell
                const dateCell = document.createElement('td');
                dateCell.textContent = date;
                row.appendChild(dateCell);

                // Create summary cell
                const summaryCell = document.createElement('td');
                summaryCell.textContent = entries.join('. '); // Join entry items into a sentence
                row.appendChild(summaryCell);

                recordEntries.appendChild(row);
            }
        });

        // Make sure the table and heading are displayed
        document.getElementById('record-summary-heading').style.display = 'block';
        document.getElementById('record-table').style.display = 'table';
    } else {
        // If no entries, hide the table and heading
        document.getElementById('record-summary-heading').style.display = 'none';
        document.getElementById('record-table').style.display = 'none';
    }
}