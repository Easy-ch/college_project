function editPhone() {
    const phoneInput = document.getElementById('phone');
    phoneInput.removeAttribute('readonly');
    phoneInput.focus();
    phoneInput.style.border = '1px solid #007BFF';
    
    // Сменить текст кнопки на "Сохранить" после активации редактирования
    const editButton = document.querySelector('.edit-btn');
    editButton.textContent = 'Сохранить';
    
    editButton.onclick = () => {
        phoneInput.setAttribute('readonly', true);
        phoneInput.style.border = 'none';
        editButton.textContent = 'Редактировать';
        editButton.onclick = editPhone; // Снова связываем с функцией редактирования
    };
}
