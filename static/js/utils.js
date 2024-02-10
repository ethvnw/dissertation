const dropdownToggle = () => {
    const dropdown = document.getElementById('dropdown');
    if (dropdown.classList.contains('invisible')) {
        dropdown.classList.remove('invisible');
    } else {
        dropdown.classList.add('invisible');}

    if (dropdown.classList.contains('opacity-0')) {
        dropdown.classList.remove('opacity-0');
        dropdown.classList.add('opacity-100');
    } else {
        dropdown.classList.remove('opacity-100');
        dropdown.classList.add('opacity-0');
    }


}

const dropdownButton = document.getElementById('dropdown-button');
dropdownButton.addEventListener('click', dropdownToggle);

document.documentElement.addEventListener('click', (event) => {
    if (event.target !== dropdownButton) {
        const dropdown = document.getElementById('dropdown');
        if (dropdown.classList.contains('opacity-100')) {
            dropdown.classList.remove('opacity-100');
            
            dropdown.classList.add('invisible');
            dropdown.classList.add('opacity-0');
        }
    }
});
