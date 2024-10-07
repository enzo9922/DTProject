function validateParticipantCount() { //VALIDATE THE MINIMUM NUMBER OF PARTICIPANT
    var participantCountInput = document.getElementById('participantCount');

    if (participantCountInput.value < 2) {
        participantCountInput.value = 2;
        alert('At least 2 participants are required to participate in the properties settlement.')
    }
    createParticipantForms();
}

function validatePropertyCount() { //VALIDATE THE MINIMUM AND MAXIMUM NUMBER OF PROPERTY
    var propertiesCountInput = document.getElementById('propertiesCount');

    if (propertiesCountInput.value < 1) {
        propertiesCountInput.value = 1;
        alert('There must be a minimum of one property available for settlement');
    }
    else if (propertiesCountInput.value > 15) {
        propertiesCountInput.value = 15;
        alert('The maximum number of properties allowed for settlement is limited to ten.');
    }
    createPropertyForms();
}

function createParticipantForms() { //GUMAGAWA NG PARTICIPANT CONTAINER AND FORMS
    var participantCount = document.getElementById('participantCount').value;
    var container = document.getElementById('participantsContainer');
    container.innerHTML = ''; // Clear previous content

    for (var i = 0; i < participantCount; i++) {
        var participantDiv = document.createElement('div');
        participantDiv.className = 'participant-container';

        var participantNum = document.createElement('h3');
        participantNum.className = 'participantNum';
        participantNum.textContent = 'Participant ' + (i + 1);

        var firstNameInput = document.createElement('input');
        firstNameInput.type = 'text';
        firstNameInput.placeholder = 'First Name';
        firstNameInput.required = true;
        firstNameInput.name = 'firstName';

        var lastNameInput = document.createElement('input');
        lastNameInput.type = 'text';
        lastNameInput.placeholder = 'Last Name';
        lastNameInput.required = true;
        lastNameInput.name = 'lastName';

        var emailInput = document.createElement('input');
        emailInput.type = 'email';
        emailInput.placeholder = 'Email';
        emailInput.required = true;
        emailInput.name = 'email';

        var passwordInput = document.createElement('input');
        passwordInput.type = 'password';
        passwordInput.placeholder = 'Password';
        passwordInput.required = true;
        passwordInput.className = 'passwordInput'
        passwordInput.name = 'pass';

        var hideButton = document.createElement('button');
        hideButton.innerHTML = '<i class="fa-solid fa-eye"></i> Show Password';
        hideButton.className = 'hideButton';

        (function (input, button) {
            button.addEventListener('click', function () {
                input.type = input.type === 'password' ? 'text' : 'password';
                button.innerHTML = input.type === 'password' ? '<i class="fa-solid fa-eye"></i> Show Password' : '<i class="fa-solid fa-eye-slash"></i> Hide Password';
            });
        })(passwordInput, hideButton);

        participantDiv.appendChild(participantNum);
        participantDiv.appendChild(firstNameInput);
        participantDiv.appendChild(lastNameInput);
        participantDiv.appendChild(emailInput);
        participantDiv.appendChild(passwordInput);
        participantDiv.appendChild(hideButton);

        container.appendChild(participantDiv);
    }
}

function createPropertyForms() { //GUMAGAWA NG PROPERTY CONTAINER AND FORMS
    var propertyCount = document.getElementById('propertiesCount').value;
    var container = document.getElementById('propertiesContainer');
    container.innerHTML = ''; // Clear previous content

    var propHead = document.createElement('h3');
    propHead.className = 'propHead';
    propHead.textContent = 'Property Name';
    propHead.name = 'item';
    container.appendChild(propHead);

    var minBidHead = document.createElement('h3');
    minBidHead.className = 'minBidHead';
    minBidHead.textContent = 'Minimum Bid (Optional)';
    minBidHead.name = 'minBid';
    container.appendChild(minBidHead);

    for (var i = 0; i < propertyCount; i++) {
        var propertyDiv = document.createElement('div');
        propertyDiv.className = 'property-container';

        var propertyNameInput = document.createElement('input');
        propertyNameInput.type = 'text';
        propertyNameInput.className = 'property-name';
        propertyNameInput.placeholder = 'Property Name';
        propertyNameInput.required = true;

        var propertyMinBidInput = document.createElement('input');
        propertyMinBidInput.type = 'number';
        propertyMinBidInput.className = 'property-min';
        propertyMinBidInput.placeholder = 'Minimum Bid';

        var propertyDelete = document.createElement('button')
        propertyDelete.type = 'button';
        propertyDelete.className = 'property-delete';

        var trashIcon = document.createElement('i');
        trashIcon.className = 'fa-solid fa-trash';
        propertyDelete.appendChild(trashIcon);

        propertyDelete.addEventListener('click', function() {
            var containers = document.querySelectorAll('.property-container');
            if (containers.length > 1) {
                var parentContainer = this.closest('.property-container');
                if (parentContainer) {
                    parentContainer.remove();
                    updatePropertyCount();
                }
            } else {
                alert('There must be a minimum of one property available for settlement.');
            }
        });
        
        propertyDiv.appendChild(propertyNameInput);
        propertyDiv.appendChild(propertyMinBidInput);
        propertyDiv.appendChild(propertyDelete);
        container.appendChild(propertyDiv);
    }
}

function updatePropertyCount() { //UPDATE PROPERTY COUNT WHEN THE USER DELETE A PROPERTY USING DELETE ICON
    var propertiesCountInput = document.getElementById('propertiesCount');
    propertiesCountInput.value = document.querySelectorAll('.property-container').length;
}

function submitForm() { //WHEN THE USER CLICK THE SUBMIT BUTTON, IT DOES THIS
    if (!validateForm()) {
        highlightRequiredFields('participantsContainer');
        highlightRequiredFields('propertiesContainer');
        return;
    }

    var formData = collectFormData();

    // Convert formData to JSON and update the form fields
    var participantFormInput = document.getElementById('id_participants');
    var propertyFormInput = document.getElementById('id_properties');

    participantFormInput.value = JSON.stringify(formData.participants);
    propertyFormInput.value = JSON.stringify(formData.properties);

    document.getElementById('registrationForm').submit();
    
    resetForm();

}

function collectFormData() {
    var participantForms = document.querySelectorAll('.participant-container');
    var propertyForms = document.querySelectorAll('.property-container');

    var formData = {
        participants: [],
        properties: []
    };

    // Collect participant data
    participantForms.forEach(function (participantForm, index) {
        formData.participants.push({
            firstName: participantForm.querySelector('input[placeholder="First Name"]').value,
            lastName: participantForm.querySelector('input[placeholder="Last Name"]').value,
            email: participantForm.querySelector('input[placeholder="Email"]').value,
            password: participantForm.querySelector('input[placeholder="Password"]').value
        });
    });

    // Collect property data
    propertyForms.forEach(function (propertyForm, index) {
        formData.properties.push({
            propertyName: propertyForm.querySelector('input[placeholder="Property Name"]').value,
            minBid: propertyForm.querySelector('input[placeholder="Minimum Bid"]').value
        });
    });

    return formData;
}

function validateForm() { //TINITIGNAN NETO KUNG LAHAT NG REQUIRED FIELDS AY MAY LAMAN
    var participantForms = document.querySelectorAll('.participant-container');
    var propertyForms = document.querySelectorAll('.property-container');

    // Validate participant forms
    for (var i = 0; i < participantForms.length; i++) {
        var firstNameInput = participantForms[i].querySelector('input[placeholder="First Name"]');
        var lastNameInput = participantForms[i].querySelector('input[placeholder="Last Name"]');
        var emailInput = participantForms[i].querySelector('input[placeholder="Email"]');
        var passwordInput = participantForms[i].querySelector('input[placeholder="Password"]');

        if (
            firstNameInput.value.trim() === '' ||
            lastNameInput.value.trim() === '' ||
            emailInput.value.trim() === '' ||
            passwordInput.value.trim() === ''
        ) {
            alert('Please fill in all required fields in participant forms.');
            return false;
        }
    }

    // Validate property forms
    for (var j = 0; j < propertyForms.length; j++) {
        var propertyNameInput = propertyForms[j].querySelector('input[placeholder="Property Name"]');
        var propertyMinBidInput = propertyForms[j].querySelector('input[placeholder="Minimum Bid"]');

        if (propertyNameInput.value.trim() === '') {
            alert('Please fill in all required fields in property forms.');
            return false;
        }
    }

    return true;
}

function highlightRequiredFields(containerId) { //HIGHLIGHT REQUIRED FIELDS THAT ARE EMPTY
    var container = document.getElementById(containerId);
    var inputFields = container.querySelectorAll('input[required]');

    inputFields.forEach(function (input) {
        input.style.border = '2px solid rgb(190, 27, 27)';

        input.addEventListener('input', function () {
            
            if (input.value.trim()) {
                input.style.border = '2px solid #624F21'; 
            } else {
                input.style.border = '2px solid rgb(190, 27, 27)';
            }
        });

        if (input.value.trim()) {
            input.style.border = '2px solid #624F21'; 
        }
    });
}

function resetForm() { //RESET THE PARTICIPANT AND PROPERTY FORMS
    var participantForms = document.querySelectorAll('.participant-container');
    var propertiesForms = document.querySelectorAll('.property-container');

    participantForms.forEach(function (participantForm) {
        var inputs = participantForm.querySelectorAll('input');
        inputs.forEach(function (input) {
            input.value = '';
            input.style.border = '2px solid #624F21';
        });
    });

    propertiesForms.forEach(function (propertiesForms) {
        var inputs = propertiesForms.querySelectorAll('input');
        inputs.forEach(function (input) {
            input.value = '';
            input.style.border = '2px solid #624F21';
        });
    });

}

window.onload = function () { //PARA MAG CREATE AGAD NG FORMS ON LOAD
    createParticipantForms();
    createPropertyForms();
}

function goHome(){ //WHEN THE LOGO OR "PROPERTIES SETTLEMENT" IS CLICKED
    window.location.href = "{% url 'home' %}";
 }

function hidePreloader() { //HIDE THE PRELOADER
     var preloader = document.getElementById('preloader');
     preloader.style.display = 'none';
 }

document.addEventListener('DOMContentLoaded', function () { //HIDE LOADER AFTER 3.5 SECS
     setTimeout(hidePreloader, 3500); 
 });