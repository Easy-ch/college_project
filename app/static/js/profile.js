import { getUserData } from './profile_update_token.js';
const accessToken = localStorage.getItem('access_token');
getUserData(accessToken)
.then(userData => {
    if (userData && userData.username) {
        generateAvatar(userData.username.trim());
    } else {
        console.error("Имя пользователя отсутствует.");
    }
})
.catch(error => {
    console.error("Ошибка при получении данных пользователя:", error);
});
function generateAvatar(username) {
    const avatarElement = document.getElementById("avatar");
    if (!avatarElement) {
        console.error("Элемент с id='avatar' не найден.");
        return;
    }

    const initials = username.replace(/\s+/g, '').slice(0, 2).toUpperCase();

    avatarElement.textContent = initials;
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

