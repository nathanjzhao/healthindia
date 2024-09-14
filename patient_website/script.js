// script.js

// Translation data
var translations = {
    en: {
        // index.html
        selectLanguage: "Select Your Language",
        // login.html
        accessMedicalRecords: "Access Medical Records",
        login: "Login",
        username: "Username/ID:",
        password: "Password:",
        loginButton: "Log In",
        callTelemedicineHub: "Call Telemedicine Hub",
        phoneNumber: "Phone Number:",
        callButton: "Call",
        loggingIn: "Logging in...",
        back: "Back",
        // medical-record.html
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
        referencePage: "Reference/Page No.",
        provider: "Provider",
        encounterSummary: "Encounter Summary",
        loading: "Loading..."
    },
    hi: {
        // index.html
        selectLanguage: "अपनी भाषा चुनें",
        // login.html
        accessMedicalRecords: "मेडिकल रिकॉर्ड तक पहुंचें",
        login: "लॉगिन",
        username: "उपयोगकर्ता नाम/आईडी:",
        password: "पासवर्ड:",
        loginButton: "लॉग इन करें",
        callTelemedicineHub: "टेलीमेडिसिन हब को कॉल करें",
        phoneNumber: "फोन नंबर:",
        callButton: "कॉल करें",
        loggingIn: "लॉग इन हो रहा है...",
        back: "वापस",
        // medical-record.html
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
        referencePage: "संदर्भ/पृष्ठ संख्या",
        provider: "प्रदाता",
        encounterSummary: "मुठभेड़ सारांश",
        loading: "लोड हो रहा है..."
    },
    mr: {
        // index.html
        selectLanguage: "आपली भाषा निवडा",
        // login.html
        accessMedicalRecords: "वैद्यकीय नोंदी प्रवेश करा",
        login: "लॉगिन",
        username: "वापरकर्ता नाव/आयडी:",
        password: "पासवर्ड:",
        loginButton: "लॉग इन",
        callTelemedicineHub: "टेलिमेडिसिन हबला कॉल करा",
        phoneNumber: "फोन नंबर:",
        callButton: "कॉल",
        loggingIn: "लॉग इन करत आहे...",
        back: "मागे",
        // medical-record.html
        medicalRecordSummary: "वैद्यकीय नोंदींचा सारांश",
        patientInformation: "रुग्णाची माहिती",
        firstName: "पहिले नाव",
        lastName: "आडनाव",
        dateOfBirth: "जन्मतारीख",
        gender: "लिंग",
        height: "उंची (सेमी)",
        weight: "वजन (कि.ग्रॅ.)",
        chronologicalSummary: "कालानुक्रमिक वैद्यकीय नोंदींचा सारांश",
        dateTime: "दिनांक/वेळ",
        referencePage: "संदर्भ/पृष्ठ क्रमांक",
        provider: "प्रदाता",
        encounterSummary: "सामना सारांश",
        loading: "लोड करत आहे..."
    },
    gu: {
        // index.html
        selectLanguage: "તમારી ભાષા પસંદ કરો",
        // login.html
        accessMedicalRecords: "મેડિકલ રેકોર્ડ્સ ઍક્સેસ કરો",
        login: "લૉગિન",
        username: "વપરાશકર્તા નામ/આઈડી:",
        password: "પાસવર્ડ:",
        loginButton: "લૉગિન કરો",
        callTelemedicineHub: "ટેલિમેડિસિન હબને કૉલ કરો",
        phoneNumber: "ફોન નંબર:",
        callButton: "કૉલ કરો",
        loggingIn: "લૉગિન કરી રહ્યું છે...",
        back: "પાછળ",
        // medical-record.html
        medicalRecordSummary: "મેડિકલ રેકોર્ડનો સારાંશ",
        patientInformation: "રોગીની માહિતી",
        firstName: "પ્રથમ નામ",
        lastName: "છેલ્લું નામ",
        dateOfBirth: "જન્મ તારીખ",
        gender: "લિંગ",
        height: "ઊંચાઈ (સેમી)",
        weight: "વજન (કિગ્રા)",
        chronologicalSummary: "કાલક્રમ મુજબ મેડિકલ રેકોર્ડ્સનો સારાંશ",
        dateTime: "તારીખ/સમય",
        referencePage: "સંદર્ભ/પૃષ્ઠ નંબર",
        provider: "પ્રદાતા",
        encounterSummary: "મળવા નો સારાંશ",
        loading: "લોડ કરી રહ્યું છે..."
    },
    ta: {
        // index.html
        selectLanguage: "உங்கள் மொழியை தேர்ந்தெடுக்கவும்",
        // login.html
        accessMedicalRecords: "மருத்துவ பதிவுகளை அணுகவும்",
        login: "உள்நுழைய",
        username: "பயனர்பெயர்/அடையாளம்:",
        password: "கடவுச்சொல்:",
        loginButton: "உள்நுழைய",
        callTelemedicineHub: "தொலைவழி மருத்துவ மையத்தை அழைக்கவும்",
        phoneNumber: "தொலைபேசி எண்:",
        callButton: "அழைக்க",
        loggingIn: "உள்நுழையிறது...",
        back: "மீண்டும்",
        // medical-record.html
        medicalRecordSummary: "மருத்துவ பதிவு சுருக்கம்",
        patientInformation: "நோயாளி தகவல்",
        firstName: "முதல் பெயர்",
        lastName: "கடைசி பெயர்",
        dateOfBirth: "பிறந்த தேதி",
        gender: "பாலினம்",
        height: "உயரம் (செ.மீ)",
        weight: "எடை (கி.கி)",
        chronologicalSummary: "காலவரிசைப்படியான மருத்துவ பதிவு சுருக்கம்",
        dateTime: "தேதி/நேரம்",
        referencePage: "குறிப்பு/பக்கம் எண்",
        provider: "வழங்குநர்",
        encounterSummary: "என்கவுண்டர் சுருக்கம்",
        loading: "ஏற்றுகிறது..."
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

    // index.html
    var selectLanguageTitle = document.querySelector('.language-container h1');
    if (selectLanguageTitle) {
        selectLanguageTitle.textContent = trans.selectLanguage;
    }

    // login.html
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

    // medical-record.html
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

    var referenceHeader = document.getElementById('reference-header');
    if (referenceHeader) {
        referenceHeader.textContent = trans.referencePage;
    }

    var providerHeader = document.getElementById('provider-header');
    if (providerHeader) {
        providerHeader.textContent = trans.provider;
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
                window.location.href = 'login.html';
            });
        })(languageButtons[i]);
    }

    // Event listener for back button on login page
    var languageBackButton = document.getElementById('language-back-button');
    if (languageBackButton) {
        languageBackButton.addEventListener('click', function() {
            window.location.href = 'index.html';
        });
    }

    // Call translatePage on page load
    translatePage();
});

// Existing login functionality
var users = {
    "admin": "password123",
    "doctor": "securepass",
    "nurse": "nursepassword"
};

// Handle login form submission
var loginForm = document.getElementById('login-form');
if (loginForm) {
    loginForm.addEventListener('submit', function(event) {
        event.preventDefault();  // Prevent the form from submitting normally

        var username = document.getElementById('username').value;
        var password = document.getElementById('password').value;

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

// Back button functionality on medical-record.html
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

// Phone number validation function
function validatePhoneNumber() {
    var phoneNumber = document.getElementById('to_number').value;
    var regex = /^\+?\d{10,15}$/;  // Corrected regex for E.164 format
    if (!regex.test(phoneNumber)) {
        alert("Invalid phone number format. Please use E.164 format.");
        return false;
    }
    return true;
}
