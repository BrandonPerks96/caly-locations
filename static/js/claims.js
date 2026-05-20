"use strict";

class App {
    constructor() {
        this.setupFormValidation();
    }

    setupFormValidation() {
        // Attach a submit event listener to the form for validation
        const form = document.getElementById('claims_form');
        if (form) {
            form.addEventListener('submit', (e) => {
                if (!form.checkValidity()) {
                    e.preventDefault();  // Prevent form submission
                    e.stopPropagation(); // Stop the event from propagating further
                }
                form.classList.add('was-validated');
                console.log('Form submitted');
            }, false);
        } 
    }
}

// Create an instance of the App class to ensure everything initializes correctly
new App();




