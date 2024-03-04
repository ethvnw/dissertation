const navButton = document.getElementById('nav-button');
navButton.onclick = () => {
    const navBar = document.getElementById('nav-bar');
    const navButtonIcon = navButton.querySelector('i');

    navBar.classList.toggle('p-4');
    navBar.classList.toggle('h-0');
    navButtonIcon.classList.toggle('fa-bars');
    navButtonIcon.classList.toggle('fa-times');
}

const dropdownButton = document.getElementById('dropdown-button');
const dropdownToggle = () => {
    const dropdown = document.getElementById('dropdown');
    
    if (dropdownButton.lastChild.style.transform === 'rotate(180deg)') {
        dropdownButton.lastChild.style.transform = ('rotate(0deg)');
    } else {
        dropdownButton.lastChild.style.transform = ('rotate(180deg)');
    }
    
    dropdown.classList.toggle('lg:h-0');
    dropdown.classList.toggle('lg:p-4');
}

dropdownButton.onclick = dropdownToggle;
document.documentElement.onclick = (event) => {
    if (event.target !== dropdownButton) {
        const dropdown = document.getElementById('dropdown');
        if (!dropdown.classList.contains('lg:h-0')) {
            dropdownToggle();
        }
    }
}
