document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form");
    const passwordField = document.getElementById("password");
    const usernameField = document.getElementById("username");
    const phoneField = document.getElementById("phone");

    // Create error message container for phone
    let phoneError = document.createElement("div");
    phoneError.style.color = "red";
    phoneError.style.fontSize = "0.9rem";
    phoneError.style.marginTop = "5px";
    phoneField.parentNode.appendChild(phoneError);

    // Focus and blur effects on password field
    if (passwordField) {
        passwordField.addEventListener("focus", () => {
            passwordField.style.border = "1px solid #0088cc";
        });

        passwordField.addEventListener("blur", () => {
            passwordField.style.border = "1px solid #ddd";
        });
    }

    // Prevent non-digit input in phone field and show error
    if (phoneField) {
        phoneField.addEventListener("input", () => {
            phoneField.value = phoneField.value.replace(/\D/g, '');
            const phone = phoneField.value;

            if (phone.length !== 10) {
                phoneError.textContent = "Phone number must be exactly 10 digits.";
                phoneField.style.border = "1px solid red";
            } else {
                phoneError.textContent = "";
                phoneField.style.border = "1px solid #0088cc";
            }
        });
    }

    // Validation on form submission
    if (form && usernameField && phoneField && passwordField) {
        form.addEventListener("submit", function (e) {
            const username = usernameField.value.trim();
            const phone = phoneField.value.trim();
            const password = passwordField.value;

            const usernameRegex = /^[a-zA-Z0-9]+$/;
            const phoneRegex = /^\d{10}$/;
            const passwordRegex = /^[A-Za-z0-9]{1,10}$/;

            let hasError = false;

            if (!usernameRegex.test(username)) {
                alert("Username must contain only letters and numbers.");
                hasError = true;
            }

            if (!phoneRegex.test(phone)) {
                phoneError.textContent = "Phone number must be exactly 10 digits.";
                phoneField.style.border = "1px solid red";
                hasError = true;
            }

            if (!passwordRegex.test(password)) {
                alert("Password must be alphanumeric and up to 10 characters.");
                hasError = true;
            }

            if (hasError) {
                e.preventDefault();
            }
        });
    }
});
