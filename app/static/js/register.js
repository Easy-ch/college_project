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

document.getElementById("registrationForm").addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const passwordConfirm = document.getElementById("password_confirm").value;
    const loading = document.getElementById("loading")
    const submitButton = document.querySelector('button[type="submit"]');
    const errorMessage = document.getElementById("error-message");
    errorMessage.style = "color: red; height: min-content;";
    errorMessage.textContent = "";
    submitButton.disabled = true;
    loading.style.display = "flex";
    try {
        const response = await fetch("/auth/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                email,
                username,
                password,
                password_confirm: passwordConfirm,
            }),
        });
        if (!response.ok) {
            const errorData = await response.json();
            loading.style.display = "none"; 
            submitButton.disabled = false; 
            if (errorData.detail) {
                const errorText = errorData.detail.message || "Ошибка регистрации";
                errorMessage.textContent = errorText;
            } else {
                loading.style.display = "none"; 
                submitButton.disabled = false; 
                errorMessage.textContent = "Не удалось зарегистрироваться. Проверьте данные.";
            }
        } else {
            const successData = await response.json();
            loading.style.display = "none"; 
            submitButton.disabled = false; 
            errorMessage.textContent = successData.message || "Подтвердите регистрацию по ссылке, отправленной по электронной почте"
            errorMessage.style = "height: min-content; color: green;";
            document.getElementById("registrationForm").reset();
        }
    } catch (error) {
        loading.style.display = "none"; 
        submitButton.disabled = false; 
        console.error("Ошибка:", error);
        errorMessage.textContent = "Произошла ошибка. Попробуйте позже.";
    }

});

