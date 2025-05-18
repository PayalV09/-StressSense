document.addEventListener("DOMContentLoaded", () => {
    // Example: Smooth scroll for nav links
    const navLinks = document.querySelectorAll('.nav-links a');
    
    navLinks.forEach(link => {
      link.addEventListener('click', (e) => {
        // Only smooth scroll for same-page anchors
        if (link.hash !== "") {
          e.preventDefault();
          const target = document.querySelector(link.hash);
          target.scrollIntoView({ behavior: "smooth" });
        }
      });
    });
  });
  