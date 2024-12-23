document.addEventListener("DOMContentLoaded", () => {
    const token = new URLSearchParams(window.location.search).get("token");

    if (!token) {
        alert("Токен не найден. Проверьте ссылку.");
        window.location.href = "/forgot-password";
        return;
    }

    document.getElementById("reset-password").addEventListener("submit", async (event) => {
        event.preventDefault();

        const newPassword = document.getElementById("new_password").value;
        const errorMessage = document.getElementById("error-message");
        errorMessage.textContent = "";

        try {
            const response = await fetch(`/auth/reset-password?token=${token}`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    new_password: newPassword,
                }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                errorMessage.textContent =
                    errorData.detail || "Не удалось сменить пароль. Попробуйте снова.";
            } else {
                const successData = await response.json();
                alert(successData.message || "Пароль успешно сменен");
                window.location.href = "/login";
            }
        } catch (error) {
            console.error("Ошибка:", error);
            errorMessage.textContent = "Произошла ошибка. Попробуйте позже.";
        }
    });
});