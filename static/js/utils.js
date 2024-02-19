const dropdownToggle = () => {
    const dropdown = document.getElementById('dropdown');
    if (dropdown.classList.contains('lg:invisible')) {
        dropdown.classList.remove('lg:invisible', 'lg:opacity-0');
        dropdown.classList.add('lg:opacity-100');
    
    } else {
        dropdown.classList.add('lg:invisible', 'lg:opacity-0');
    }
}

const dropdownButton = document.getElementById('dropdown-button');

if (screen.width > 1024) {
    dropdownButton.addEventListener('click', dropdownToggle);
    document.documentElement.addEventListener('click', (event) => {
        if (event.target !== dropdownButton) {
            const dropdown = document.getElementById('dropdown');

            if (!dropdown.classList.contains('lg:invisible')) {
                dropdown.classList.add('lg:invisible', 'lg:opacity-0');
            }
        }
    });
}


const menuButton = document.getElementById('menu-button');
const openButton = document.getElementById('open-button');
const closeButton = document.getElementById('close-button');
const navItems = document.getElementById('nav-items');

const menuToggle = () => {
    if (navItems.classList.contains('invisible')) {
        navItems.classList.add('opacity-100');
        navItems.classList.remove('invisible', 'opacity-0');

        openButton.classList.toggle('hidden');
        closeButton.classList.toggle('hidden');
    
    } else {
        navItems.classList.add('invisible', 'opacity-0');
        navItems.classList.remove('opacity-100');

        openButton.classList.toggle('hidden');
        closeButton.classList.toggle('hidden');
    }
}

menuButton.addEventListener('click', menuToggle);
