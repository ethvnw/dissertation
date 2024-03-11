// ECF application form control

// Hide end date if ongoing is selected
var yes = document.getElementById('id_application_form-ongoing_0');
var no = document.getElementById('id_application_form-ongoing_1');
var enddate = document.getElementById('id_application_form-end_date');
enddate.parentElement.classList.add('hidden');

no.onclick = function() {
    enddate.parentElement.classList.remove('hidden');
    enddate.required = true;
}

yes.onclick = function() {
    enddate.parentElement.classList.add('hidden');
    enddate.required = false;
}
