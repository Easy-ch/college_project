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
            window.location.href = '/login';
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
                window.location.href = '/login';
            }
               
            else
                return data;

        } else if (response.status === 401) {
            console.log("Access token недействителен. Попытка обновить токен.");
            localStorage.removeItem("access_token");
            
            accessToken = await getAndSaveAccessToken();
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
        }

        user_data = await getUserData(accessToken);
    } while(!user_data && ++refresh_counter < 3);

    if (user_data) {
        document.getElementById("username").textContent = user_data['username'];
        document.getElementById("email").textContent = user_data['email'];
    } else 
        window.location.href = '/login';
}


fetchProtectedRoute();