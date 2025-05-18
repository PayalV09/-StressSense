// Wait for the document to fully load before running the script
document.addEventListener('DOMContentLoaded', function() {
    // Example: Recommendations data, can be dynamically loaded from a server
    const recommendationsData = {
        stress_monitoring: "Track your stress levels using our daily questionnaire to monitor your emotional and mental well-being.",
        personalized_insights: "Based on your answers, we provide personalized insights to help you understand your stress triggers better.",
        relaxation_techniques: "We suggest effective relaxation techniques like deep breathing, meditation, and mindfulness.",
        healthy_lifestyle: "Adopting a healthier lifestyle can greatly reduce stress. Regular exercise, proper nutrition, and adequate sleep are key."
    };

    // Dynamically populate the recommendations in the HTML
    const recommendations = document.querySelectorAll('.recommendation-text');

    recommendations[0].innerHTML = recommendationsData.stress_monitoring;
    recommendations[1].innerHTML = recommendationsData.personalized_insights;
    recommendations[2].innerHTML = recommendationsData.relaxation_techniques;
    recommendations[3].innerHTML = recommendationsData.healthy_lifestyle;

    // Example of a smooth scrolling effect when clicking on the "Go Back to Dashboard" button
    const goBackButton = document.querySelector('.btn');

    goBackButton.addEventListener('click', function(event) {
        event.preventDefault();  // Prevent the default action (if needed)
        document.body.scrollIntoView({ behavior: 'smooth' });
    });
});
