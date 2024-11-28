const navbar = document.querySelector('.navbar');
const main = document.querySelector('main');

window.addEventListener('resize', resetMargin);

function applyMarginOnHover() {
    navbar.removeEventListener('mouseenter', increaseMargin);
    navbar.removeEventListener('mouseleave', resetMargin);

    if (window.innerWidth > 700) {
        navbar.addEventListener('mouseenter', increaseMargin);
        navbar.addEventListener('mouseleave', resetMargin);
    } else {
        main.style.marginTop = '60px';
        navbar.classList.remove('force-hover');
    }
}

function increaseMargin() {
    main.style.marginTop = '110px';
}

function resetMargin() {
    if (window.scrollY !== 0) {
        main.style.marginTop = '70px';
    }
}

applyMarginOnHover();
window.addEventListener('resize', applyMarginOnHover);


document.addEventListener('DOMContentLoaded', () => {
    function checkScrollPosition() {
        if (window.innerWidth > 700) {
            if (window.scrollY === 0) {
                navbar.classList.add('force-hover');
                increaseMargin();
            } else {
                navbar.classList.remove('force-hover');
                resetMargin();
            }
        } else {

        }
    }

    checkScrollPosition();
    window.addEventListener('scroll', checkScrollPosition);
});


access_token = localStorage.getItem('access_token');