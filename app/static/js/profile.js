export async function generateAvatar(username){
        const avatarElement = document.getElementById("avatar");
        if (!avatarElement) {
            console.error("Элемент с id='avatar' не найден.");
            return;
        }
        const initials = username.replace(/\s+/g, '').slice(0, 2).toUpperCase();
        avatarElement.textContent = initials;
}

async function putChanges() {
    document.getElementById("form").addEventListener("submit", async (event) => {
        event.preventDefault();
        
        const phone_number = document.getElementById("phone_number").value;
        const username_change = document.getElementById("username_change").value
        const phone = document.getElementById("number");
        const password = document.getElementById("password").value;
        const new_password = document.getElementById("new_password").value;
        const errorMessage = document.getElementById("error-message");
        const bodyData = {};
        console.log(bodyData);
        if (phone_number) bodyData.phone_number = phone_number;
        if (password) bodyData.password = password;
        if (new_password) bodyData.new_password = new_password;
        if (username_change) bodyData.username_change = username_change
        const response = await fetch("/changes/upload_change_profile", {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${localStorage.getItem("access_token")}`,
            },
            body: JSON.stringify(
                bodyData
             )
        });
        

        const responseData = await response.json();
        console.log(responseData);

        if (!response.ok) {   
            if (responseData.detail) {
                const errorText = responseData.detail.message || "Ошибка обновления. Попробуйте позже.";
                errorMessage.textContent = errorText;
            } else {
                errorMessage.textContent = "Не удалось обновить информацию. Проверьте данные..";
            }
        } else {
            if (bodyData.phone_number) {
                phone.textContent = responseData.phone_number;
            }
            if (bodyData.username_change) {
                document.getElementById("username").textContent = responseData.username;
            }
            errorMessage.textContent = responseData.message || "Успешно обновлено!"
            document.getElementById("form").reset();
            errorMessage.style = "color: green;";
            localStorage.setItem("access_token", responseData.access_token);
            console.log(phone.value);

        }
    });
}

document.addEventListener("DOMContentLoaded", putChanges);


document.querySelectorAll('.old-password, .new-password').forEach(container => {
    const passwordInput = container.querySelector('input');
    const viewIcon = container.querySelector('img[src*="view"]');
    const noViewIcon = container.querySelector('img[src*="noview"]');

    viewIcon.addEventListener('click', (e) => {
        e.preventDefault();
        togglePasswordVisibility(passwordInput, viewIcon, noViewIcon);
    });

    noViewIcon.addEventListener('click', (e) => {
        e.preventDefault();
        togglePasswordVisibility(passwordInput, viewIcon, noViewIcon);
    });
});

function togglePasswordVisibility(passwordInput, viewIcon, noViewIcon) {
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        viewIcon.style.display = 'none';
        noViewIcon.style.display = 'inline-block';
    } else {
        passwordInput.type = 'password';
        viewIcon.style.display = 'inline-block';
        noViewIcon.style.display = 'none';
    }
}























// const API_BASE_URL = "http://127.0.0.1:8000"; // Базовый URL вашего API
// const PROFILE_ROUTE = "/profile"; // Эндпоинт для получения данных профиля
// const LOGIN_PAGE = "/login.html"; // Страница входа

// // Получение токена из localStorage
// const getAccessToken = () => localStorage.getItem("access_token");

// // Обновление данных профиля
// async function updateUserProfile() {
//   const accessToken = getAccessToken();

//   if (!accessToken) {
//     console.error("Access token отсутствует. Перенаправление на страницу входа.");
//     window.location.href = LOGIN_PAGE;
//     return;
//   }

//   try {
//     // Запрос данных профиля
//     const response = await fetch(`${API_BASE_URL}${PROFILE_ROUTE}`, {
//       method: "GET",
//       headers: {
//         Authorization: `Bearer ${accessToken}`,
//         "Content-Type": "application/json",
//       },
//     });

//     if (response.ok) {
//       const userData = await response.json();

//       // Обновление UI с данными профиля
//       document.querySelector(".user-info .card .block:nth-child(1) p").innerHTML = 
//         `<strong>Username:</strong> ${userData.username}`;
//       document.querySelector(".user-info .card .block:nth-child(2) p").innerHTML = 
//         `<strong>Email:</strong> ${userData.email}`;
//       document.querySelector(".user-info .card .block:nth-child(3) p").innerHTML = 
//         `<strong>Телефон:</strong> ${userData.phone}`;
//     } else if (response.status === 401) {
//       console.error("Access token недействителен. Перенаправление на страницу входа.");
//       localStorage.removeItem("access_token");
//       window.location.href = LOGIN_PAGE;
//     } else {
//       console.error("Ошибка при загрузке профиля:", response.statusText);
//     }
//   } catch (error) {
//     console.error("Ошибка при выполнении запроса:", error);
//   }
// }

// // Инициализация загрузки профиля
// document.addEventListener("DOMContentLoaded", updateUserProfile);

