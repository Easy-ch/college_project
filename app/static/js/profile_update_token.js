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

export async function getUserData(accessToken) {
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
        document.getElementById("number").textContent = user_data['phone'];
    } else 
        window.location.href = '/login';
}


fetchProtectedRoute();


function putPhoneNumber() {
    document.getElementById("phone_form").addEventListener("submit", async (event) => {
        event.preventDefault();
    
        const phone_number = document.getElementById("phone_number").value;
        const errorMessage = document.getElementById("error-message");
        const response = await fetch("/changes/upload_phone_field", {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${localStorage.getItem("access_token")}`,
            },
            body: JSON.stringify({ phone_number }),
        });
    


        if (!response.ok) {
            const errorData = await response.json();
            if (errorData.detail) {
                const errorText = errorData.detail[0]?.message || "Введите номер телефона в формате +7XXXXXXXXXX";
                errorMessage.textContent = errorText;
                console.log(errorData);
            } else {
                errorMessage.textContent = "Не удалось обновить телефон. Проверьте данные.";
            }
        } else {
            const successData = await response.json();
            errorMessage.textContent = successData.message || "Успешно добавлен телефон"
            errorMessage.style = "height: min-content; color: green;";
            document.getElementById("phone_form").reset();
        }
    });
}
document.addEventListener("DOMContentLoaded", putPhoneNumber);


