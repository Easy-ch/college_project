document.getElementById('logout').addEventListener('click', async (event) => {
    event.preventDefault(); 

    const response = await fetch('/logout', {
        method: 'GET',
        credentials: 'include' 
    });

    if (response.ok) {
        
        localStorage.removeItem('access_token');
        window.location.href = '/login';
    } else {
        console.error('Ошибка при выходе из системы');
    }
});