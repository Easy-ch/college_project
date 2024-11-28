const API_BASE_URL = "http://127.0.0.1:8000";

// Получение токенов из localStorage
const getAccessToken = () => localStorage.getItem("access_token");
const getRefreshToken = () => localStorage.getItem("refresh_token");

// Сохранение токенов в localStorage
const saveTokens = (accessToken, refreshToken) => {
    if (accessToken) localStorage.setItem("access_token", accessToken);
    if (refreshToken) localStorage.setItem("refresh_token", refreshToken);
};

// Проверка токена и отправка запроса
async function fetchProtectedRoute() {
    let accessToken = getAccessToken();

    if (!accessToken) {
        console.log("Access token отсутствует. Попытка обновить токен...");
        const refreshToken = getRefreshToken();

        if (!refreshToken) {
            window.location.href = '/login';
            return;
        }

        try {
            // Запрос на обновление токена
            const refreshResponse = await fetch("/auth/refresh", {
                method: "POST",
                credentials: "include", // Если токен передаётся в cookie
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ refresh_token: refreshToken })
            });

            if (!refreshResponse.ok) {
                console.error("Не удалось обновить токен. Необходима авторизация.");
                return;
            }

            const { access_token: newAccessToken } = await refreshResponse.json();
            console.log("Новый access_token получен.");
            saveTokens(newAccessToken);
            accessToken = newAccessToken;
        } catch (error) {
            console.error("Ошибка при обновлении токена:", error);
            return;
        }
    }

    try {
        const response = await fetch("/auth/protected", {
            method: "GET",
            headers: {
                Authorization: `Bearer ${accessToken}`
            }
        });

        if (response.ok) {
            const data = await response.json();
            console.log("Ответ от защищённого маршрута:", data);
        } else if (response.status === 401) {
            console.error("Access token недействителен. Попробуйте обновить токен.");
            localStorage.removeItem("access_token");
        } else {
            console.error("Ошибка при доступе к защищённому маршруту:", response.status);
        }
    } catch (error) {
        console.error("Ошибка при выполнении запроса:", error);
    }
}

// Вызов функции для проверки токенов и получения данных
fetchProtectedRoute();