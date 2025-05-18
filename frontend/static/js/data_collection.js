document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("dataForm");
    const inputs = form.querySelectorAll("input, select, textarea");
    const messageBox = document.getElementById("messageBox");
    const recommendationsList = document.getElementById("recommendationsList");

    // Validate field
    function validateField(input) {
        const errorMessage = input.nextElementSibling;
        let isValid = true;

        if (input.hasAttribute("required") && !input.value.trim()) {
            errorMessage.textContent = "This field is required";
            input.classList.add("error");
            isValid = false;
        } else if (input.type === "email" && !/\S+@\S+\.\S+/.test(input.value)) {
            errorMessage.textContent = "Enter a valid email address";
            input.classList.add("error");
            isValid = false;
        } else if (input.type === "number" && isNaN(input.value)) {
            errorMessage.textContent = "Enter a valid number";
            input.classList.add("error");
            isValid = false;
        } else {
            errorMessage.textContent = "";
            input.classList.remove("error");
        }

        return isValid;
    }

    // Add validation span and listener
    inputs.forEach((input) => {
        const errorMsg = document.createElement("span");
        errorMsg.style.color = "red";
        errorMsg.style.fontSize = "0.9rem";
        input.insertAdjacentElement("afterend", errorMsg);

        input.addEventListener("input", () => validateField(input));
    });

    // Form submission
    form.addEventListener("submit", async function (event) {
        event.preventDefault();
        let isFormValid = true;

        inputs.forEach((input) => {
            if (!validateField(input)) {
                isFormValid = false;
            }
        });

        if (!isFormValid) return;

        const formData = new FormData(form);
        const data = {
            user_id: formData.get("user_id"),
            stress_level: formData.get("stress_level"),
            sleep_hours: formData.get("sleep_hours"),
            diet_score: formData.get("diet_score"),
            exercise_minutes: formData.get("exercise_minutes"),
            mood: formData.get("mood")
        };

        try {
            const response = await fetch("http://127.0.0.1:5000/submit-stress-data", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (result.success) {
                messageBox.innerHTML = `<p class="success">✅ Your data was submitted successfully!</p>`;
                form.reset();

                // Optional: Show stress prediction
                recommendationsList.innerHTML = `
                    <li>Stay hydrated and take breaks</li>
                    <li>Engage in physical activities</li>
                    <li>Practice mindfulness & deep breathing</li>
                `;

                // Redirect to prediction if needed:
                if (result.stress_level) {
                    setTimeout(() => {
                        window.location.href = `/prediction?level=${result.stress_level}`;
                    }, 1000);
                }
            } else {
                messageBox.innerHTML = `<p class="error">⚠️ ${result.message}</p>`;
            }
        } catch (error) {
            console.error("Error submitting data:", error);
            messageBox.innerHTML = `<p class="error">⚠️ Failed to submit data. Try again.</p>`;
        }
    });
});
