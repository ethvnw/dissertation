const navButton = document.getElementById('nav-button');
navButton.onclick = () => {
    const navBar = document.getElementById('nav-bar');
    const navButtonIcon = navButton.querySelector('i');

    navBar.classList.toggle('p-4');
    navBar.classList.toggle('max-h-48');
    navButtonIcon.classList.toggle('fa-bars');
    navButtonIcon.classList.toggle('fa-times');
}

const dropdownButton = document.getElementById('dropdown-button');
const dropdownToggle = () => {
    const dropdown = document.getElementById('dropdown');
    const dropdownButtonChevron = dropdownButton.children[1];

    dropdownButtonChevron.style.transform = dropdown.classList.contains('lg:h-0') ? 'rotate(180deg)' : 'rotate(0deg';    
    dropdown.classList.toggle('lg:max-h-32');
}

dropdownButton.onclick = dropdownToggle;
