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
        // let p_error = document.getElementById("error-message");
        // const json_err = await response.json();
        // p_error.textContent = json_err[""]
        console.error('Ошибка при выходе из системы');
    }
});