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
