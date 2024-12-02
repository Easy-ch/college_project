let unauthNavbar = document.querySelectorAll('.unauth-navbar');
let authNavbar = document.querySelectorAll('.auth-navbar');

unauthNavbar.forEach(nav => nav.style.display = "flex");
authNavbar.forEach(nav => nav.style.display = "none");

if (localStorage.getItem('access_token')) {
    authNavbar.forEach(nav => nav.style.display = "flex");
    unauthNavbar.forEach(nav => nav.style.display = "none");
}
