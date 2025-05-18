document.addEventListener("DOMContentLoaded", () => {
    const stressLevelEl = document.querySelector("h3");
    const tip = document.querySelector(".tip");

    if (stressLevelEl) {
        const level = stressLevelEl.textContent.trim().toLowerCase();

        // Set background color based on stress level
        switch (level) {
            case "high":
                document.body.style.backgroundColor = "#ffe5e5"; // light red
                break;
            case "moderate":
                document.body.style.backgroundColor = "#fff7cc"; // light yellow
                break;
            case "low":
                document.body.style.backgroundColor = "#e0ffe0"; // light green
                break;
            default:
                document.body.style.backgroundColor = "#f5f5f5"; // fallback
                console.warn("Unknown stress level:", level);
        }

        // Animate tip appearance safely
        if (tip) {
            tip.style.opacity = 0;
            tip.style.transition = "opacity 0.6s ease-in-out, transform 0.6s ease-in-out";
            tip.style.transform = "translateY(10px)";

            setTimeout(() => {
                tip.style.opacity = 1;
                tip.style.transform = "translateY(0)";
                tip.classList.add('visible'); // Moved inside to avoid null errors
            }, 300);
        }
    } else {
        console.warn("Stress level <h3> not found.");
    }

    // Optional redirect
    // setTimeout(() => {
    //     window.location.href = "/dashboard";
    // }, 5000);
});
