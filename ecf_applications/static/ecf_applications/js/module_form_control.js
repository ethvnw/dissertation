const addButton = document.getElementById('add-button');
const moduleForm = document.getElementById('assessment_formset-0-container');
const buttonContainer = document.getElementById('button-container');
var numForms = document.getElementById('id_assessment_formset-TOTAL_FORMS');

// Handle the display of the extension date input
var moduleFormSelect = moduleForm.getElementsByTagName('select')[0];
moduleFormSelect.parentElement.nextElementSibling.style.display = 'none';
moduleFormSelect.onchange = (evt) => extensionDateDisplayToggle(evt);

const extensionDateDisplayToggle = (e) => {
    const dateContainer = e.target.parentElement.nextElementSibling;
    const dateInput = dateContainer.getElementsByTagName('input')[0];
    
    if (e.target.value === '3') {
        dateContainer.style.display = 'block';
        dateInput.required = true;
        
    } else {
        dateContainer.style.display = 'none';
        dateInput.required = false;
    }
}


// New module form
addButton.onclick= (e) => {
    e.preventDefault();
    
    var formNum = Number(numForms.getAttribute('value'));
    var newForm = moduleForm.cloneNode(true);
    var formRegex = RegExp(`formset-(\\d){1}-`,'g');

    newForm.id = `assessment_formset-${formNum}-container`;
    newForm.innerHTML = newForm.innerHTML.replace(formRegex, `formset-${formNum}-`);
    newForm.getElementsByTagName('h2')[0].innerText = `Module Asessment ${formNum+1}`;

    const actionSelect = newForm.getElementsByTagName('select')[0];
    actionSelect.onchange = (evt) => extensionDateDisplayToggle(evt);

    numForms.setAttribute('value', formNum + 1);
    moduleForm.parentNode.insertBefore(newForm, buttonContainer);
}
