const navbar = document.querySelector('.navbar');

navbar.addEventListener('mouseenter', async () => {
    navbar.classList.add('active');
});

navbar.addEventListener('mouseleave', async () => {
    navbar.classList.remove('active');
});

async function sleepNavbar() {
    setTimeout(() => { navbar.classList.add('active'); }, 40);
    setTimeout(() => { navbar.classList.remove('active'); }, 1000);
}

document.addEventListener('DOMContentLoaded', sleepNavbar());