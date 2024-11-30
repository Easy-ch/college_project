document.getElementById('logout').addEventListener('click', logout);

function logout() {
    localStorage.removeItem('access_token');
    document.cookie = "refresh_token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    window.location.href = '/login';
}
