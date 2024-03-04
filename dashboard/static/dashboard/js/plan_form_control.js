const openForm = document.getElementById('open-support-form');
const closeForm = document.getElementById('close-support-form');
var form = document.getElementById('support-form');

openForm.onclick = () => {
    form.classList.toggle('hidden');
}

closeForm.onclick = () => {
    form.classList.toggle('hidden');
}