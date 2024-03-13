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
dropdownButton.onclick  = () => {
    const dropdown = document.getElementById('dropdown');
    const dropdownButtonChevron = dropdownButton.children[1];

    dropdownButtonChevron.style.transform = dropdown.classList.contains('lg:max-h-32') ? 'rotate(0deg)' : 'rotate(180deg)';    
    dropdown.classList.toggle('lg:max-h-32');
}

const notificationButton = document.getElementById('notification-button');
notificationButton.onclick = () => {
    const notifications = document.getElementById('notifications');
    notifications.classList.toggle('max-h-fit');
}

document.onclick = (event) => {
    if (!navButton.contains(event.target)) {
        const navBar = document.getElementById('nav-bar');
        const navButtonIcon = navButton.querySelector('i');

        navBar.classList.remove('p-4');
        navBar.classList.remove('max-h-48');
        navButtonIcon.classList.remove('fa-times');
        navButtonIcon.classList.add('fa-bars');
    }

    if (!dropdownButton.contains(event.target)) {
        const dropdown = document.getElementById('dropdown');
        dropdown.classList.remove('lg:max-h-32');
        dropdownButton.children[1].style.transform = 'rotate(0deg)';
    }

    if (!notificationButton.contains(event.target)) {
        const notifications = document.getElementById('notifications');
        notifications.classList.remove('max-h-fit');
    }
}
