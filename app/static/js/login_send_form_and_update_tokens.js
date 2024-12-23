document.getElementById('loginForm').onsubmit = async (e) => {
    e.preventDefault();

    const error_tag = document.getElementById("error-message");
    const formData = new FormData(e.target);

    try {
        const response = await fetch('/auth/login', {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            const data = await response.json();

            document.cookie = `refresh_token=${data.refresh_token}; Secure; SameSite=Strict`;
            localStorage.setItem('access_token', data.access_token);
            window.location.href = '/profile';
        } else {
            const error = await response.json();
            error_tag.textContent = error.detail[0]['message'] || "Ошибка входа. Проверьте введённые данные.";
        }
    } catch (error) {
        error_tag.textContent = "Не удалось выполнить запрос. Проверьте подключение к интернету.";
    }
};



async function getAndSaveAccessToken() {
    try {
        const refreshResponse = await fetch("/auth/refresh", {
            method: 'POST',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
            }
        });

        if (!refreshResponse.ok) {
            console.error("Не удалось обновить токен. Необходима авторизация.");
            return null;
        }

        const { access_token: newAccessToken } = await refreshResponse.json();
        console.log("Новый access_token получен.");
        
        if (newAccessToken)
            localStorage.setItem("access_token", newAccessToken);
        else
            console.error(`newAccessToken is not defined...`);
        
        return newAccessToken;
    } catch (error) {
        console.error("Ошибка при обновлении токена:", error);
        return false;
    }
}

async function getUserData(accessToken) {
    try {
        const response = await fetch("/auth/get_user_data", {
            method: "GET",
            headers: {
                Authorization: `Bearer ${accessToken}`
            }
        });

        if (response.ok) {
            const data = await response.json();
            console.log("Ответ от защищённого маршрута:", data);

            if (data["message"] == "Access token data is incorrect") {
                localStorage.removeItem("access_token");
                return false;
            } else
                return data;

        } else if (response.status === 401) {
            console.log("Access token недействителен. Попытка обновить токен.");
            localStorage.removeItem("access_token");
            
            await getAndSaveAccessToken();
        } else {
            console.error("Ошибка при доступе к защищённому маршруту:", response.status);
        }
    } catch (error) {
        console.error("Ошибка при выполнении запроса:", error);
    }
}

const getFromStorageAccessToken = () => localStorage.getItem("access_token");


async function fetchProtectedRoute() {
    let refresh_counter = 0,
        user_data = false;

    do {
        let accessToken = getFromStorageAccessToken();
        
        if (!accessToken) {
            console.log("Access token отсутствует. Попытка обновить токен...");
            accessToken = await getAndSaveAccessToken();

            if (!accessToken)
                break;
        }

        user_data = await getUserData(accessToken);
    } while(!user_data && ++refresh_counter < 3);

    if (user_data)
        window.location.href = '/profile';
}


fetchProtectedRoute();

 async function check_password() {
    if (document.getElementById('show_password').checked){
        document.getElementById('password').setAttribute('type', 'text');
    } else {
        document.getElementById('password').setAttribute('type', 'password');
    }
}


async function check_password_confirm() {
    if (document.getElementById('show_password_confirm').checked){
        document.getElementById('password_confirm').setAttribute('type', 'text');
    } else {
        document.getElementById('password_confirm').setAttribute('type', 'password');
    }
}