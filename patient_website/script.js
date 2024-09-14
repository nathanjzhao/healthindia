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
        loading: "Loading...",
        // Medical history entries
        entry1Date: "02/14/2021 10:00am",
        entry1Ref: 'Pg 1-3, "Initial Consult Letter"',
        entry1Provider: "Dr. Aditya Shah, Radiation Oncologist",
        entry1Summary: "Patient saw Dr. Shah for initial consultation regarding radiation therapy for LHS glioblastoma",
        entry2Date: "02/17/2021 8:15am",
        entry2Ref: 'Pg 4, "CT Encounter"',
        entry2Provider: "CT Team, Radiation Oncology Department",
        entry2Summary: "Patient reported to CT department but was told she could not be scanned due to COVID-19 staffing issues"
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
        loading: "लोड हो रहा है...",
        // Medical history entries
        entry1Date: "14/02/2021 सुबह 10:00 बजे",
        entry1Ref: 'पृष्ठ 1-3, "प्रारंभिक परामर्श पत्र"',
        entry1Provider: "डॉ. आदित्य शाह, रेडिएशन ऑन्कोलॉजिस्ट",
        entry1Summary: "रोगी ने LHS ग्लियोब्लास्टोमा के लिए रेडिएशन थेरेपी के संबंध में प्रारंभिक परामर्श के लिए डॉ. शाह से मुलाकात की",
        entry2Date: "17/02/2021 सुबह 8:15 बजे",
        entry2Ref: 'पृष्ठ 4, "सीटी मुठभेड़"',
        entry2Provider: "सीटी टीम, रेडिएशन ऑन्कोलॉजी विभाग",
        entry2Summary: "रोगी सीटी विभाग में रिपोर्ट किया लेकिन उन्हें बताया गया कि COVID-19 स्टाफिंग मुद्दों के कारण उन्हें स्कैन नहीं किया जा सकता"
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
        loading: "लोड करत आहे...",
        // Medical history entries
        entry1Date: "१४/०२/२०२१ सकाळी १०:००",
        entry1Ref: 'पृष्ठ १-३, "प्रारंभिक सल्ला पत्र"',
        entry1Provider: "डॉ. आदित्य शाह, किरणोत्सर्ग ऑन्कोलॉजिस्ट",
        entry1Summary: "रुग्णाने LHS ग्लिओब्लास्टोमा साठी किरणोत्सर्ग उपचाराबद्दल प्रारंभिक सल्ल्यासाठी डॉ. शाह यांना भेट दिली",
        entry2Date: "१७/०२/२०२१ सकाळी ८:१५",
        entry2Ref: 'पृष्ठ ४, "सीटी सामना"',
        entry2Provider: "सीटी टीम, किरणोत्सर्ग ऑन्कोलॉजी विभाग",
        entry2Summary: "रुग्ण सीटी विभागात रिपोर्ट केला परंतु त्यांना सांगितले गेले की COVID-19 स्टाफिंग समस्यांमुळे त्यांना स्कॅन केले जाऊ शकत नाही"
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

    // Translate medical history entries
    var entry1Date = document.getElementById('entry1-date');
    if (entry1Date) {
        entry1Date.textContent = trans.entry1Date;
    }

    var entry1Ref = document.getElementById('entry1-ref');
    if (entry1Ref) {
        entry1Ref.textContent = trans.entry1Ref;
    }

    var entry1Provider = document.getElementById('entry1-provider');
    if (entry1Provider) {
        entry1Provider.textContent = trans.entry1Provider;
    }

    var entry1Summary = document.getElementById('entry1-summary');
    if (entry1Summary) {
        entry1Summary.textContent = trans.entry1Summary;
    }

    var entry2Date = document.getElementById('entry2-date');
    if (entry2Date) {
        entry2Date.textContent = trans.entry2Date;
    }

    var entry2Ref = document.getElementById('entry2-ref');
    if (entry2Ref) {
        entry2Ref.textContent = trans.entry2Ref;
    }

    var entry2Provider = document.getElementById('entry2-provider');
    if (entry2Provider) {
        entry2Provider.textContent = trans.entry2Provider;
    }

    var entry2Summary = document.getElementById('entry2-summary');
    if (entry2Summary) {
        entry2Summary.textContent = trans.entry2Summary;
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