const openForm = document.getElementById('open-evidence-form');
const closeForm = document.getElementById('close-evidence-form');
var form = document.getElementById('evidence-form');

openForm.onclick = () => {
    form.classList.toggle('hidden');
}

closeForm.onclick = () => {
    form.classList.toggle('hidden');
}