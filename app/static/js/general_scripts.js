const navbar = document.querySelector('.navbar');
let is_nav_hover = false;

navbar.addEventListener('mouseenter', async () => {
    navbar.classList.add('active');
    is_nav_hover = true;
});

navbar.addEventListener('mouseleave', async () => {
    navbar.classList.remove('active');
});

async function sleepNavbar() {
    setTimeout(async () => { navbar.classList.add('active'); }, 40);
    setTimeout(async () => { if (!is_nav_hover) { navbar.classList.remove('active'); } }, 1000);
}

document.addEventListener('DOMContentLoaded', sleepNavbar());