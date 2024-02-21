// ECF application form control

// Hide end date if ongoing is selected
var yes = document.getElementById('id_ongoing_0');
var no = document.getElementById('id_ongoing_1');
var enddate = document.getElementById('id_end_date').parentElement;
enddate.classList.add('hidden');

no.onclick = function() {
    enddate.classList.remove('hidden');
}
yes.onclick = function() {
    enddate.classList.add('hidden');
}



// Handles form navigation buttons
var nextButton = document.getElementById('next-button');
var backButton = document.getElementById('back-button');
var addFormButton = document.getElementById('add-module-form');
var activeForm = document.getElementById('form-container');

nextButton.onclick = function(e) {
    e.preventDefault();
    
    var form = document.getElementById(activeForm.dataset.activeForm);
    var nextForm = form.nextElementSibling;
    
    if (nextForm.dataset.isForm) {
        form.classList.add('hidden');
        backButton.classList.remove('hidden');
        nextForm.classList.remove('hidden');
        activeForm.dataset.activeForm = nextForm.id;
    }

    if (!nextForm.nextElementSibling.dataset.isForm) {
        nextButton.classList.add('hidden');
        backButton.classList.remove('hidden');
        addFormButton.classList.remove('hidden');
        document.getElementById('submit-button').classList.remove('hidden');
    }
}

backButton.onclick = function(e) {
    e.preventDefault();

    var form = document.getElementById(activeForm.dataset.activeForm);
    var prevForm = form.previousElementSibling;

    if (prevForm.dataset.isForm) {
        form.classList.add('hidden');
        nextButton.classList.remove('hidden');
        addFormButton.classList.add('hidden');
        document.getElementById('submit-button').classList.add('hidden');

        prevForm.classList.remove('hidden');
        activeForm.dataset.activeForm = prevForm.id;
    }

    if (!prevForm.previousElementSibling.dataset.isForm) {
        backButton.classList.add('hidden');
        nextButton.classList.remove('hidden');
        addFormButton.classList.add('hidden');
    }
}


// Handles adding new module forms to the page
var moduleForm = document.getElementById('module-0');
var formContainer = document.getElementById('form-container');
var buttonContainer = document.getElementById('button-container');
var numForms = document.getElementById('id_form-TOTAL_FORMS');
var formCount = 0;

addFormButton.onclick = function(e) {
    e.preventDefault();

    var newForm = moduleForm.cloneNode(true);
    var formRegex = RegExp(`form-(\\d){1}-`,'g');

    formCount++;
    newForm.id = `module-${formCount}`;
    newForm.innerHTML = newForm.innerHTML.replace(formRegex, `form-${formCount}-`);
    formContainer.insertBefore(newForm, buttonContainer);

    numForms.setAttribute('value', formCount+1);

    nextButton.click();
}

