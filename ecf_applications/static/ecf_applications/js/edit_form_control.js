const backButton = document.getElementById('back-button');
const continueButton = document.getElementById('continue-button');
const submitButton = document.getElementById('submit-button');
const forms = document.querySelectorAll('[id^="form-"]');
const comments = document.querySelectorAll('[id^="comment-"]');

var currentStep = document.getElementById('current-step');

window.onload = () => {
    forms[0].classList.toggle('hidden');
    comments[0].classList.toggle('hidden');
    currentStep.value = 0;    

    if (forms.length == 1) {
        continueButton.classList.toggle('hidden');
        submitButton.classList.toggle('hidden');
    }
}

continueButton.onclick = (e) => {
    e.preventDefault();
    const current = parseInt(currentStep.value);

    if (current < forms.length - 1) {
        forms[current].classList.toggle('hidden');
        comments[current].classList.toggle('hidden');
        forms[current + 1].classList.toggle('hidden');
        comments[current + 1].classList.toggle('hidden');
        currentStep.value = current + 1;

        backButton.classList.remove('hidden');
    }

    // show submit button if at end of form list
    if (current === forms.length - 2) {
        continueButton.classList.toggle('hidden');
        submitButton.classList.toggle('hidden');
    }
}

backButton.onclick = (e) => {
    e.preventDefault();
    const current = parseInt(currentStep.value);

    if (current > 0) {
        forms[current].classList.toggle('hidden');
        comments[current].classList.toggle('hidden');
        forms[current - 1].classList.toggle('hidden');
        comments[current - 1].classList.toggle('hidden');
        currentStep.value = current - 1;
    }

    // hide submit button if not at end of form list
    if (current === forms.length - 1) {
        continueButton.classList.toggle('hidden');
        submitButton.classList.toggle('hidden');
    }

    // hide back button if at start of form list
    if (current === 1) {
        backButton.classList.toggle('hidden');
    }
}
