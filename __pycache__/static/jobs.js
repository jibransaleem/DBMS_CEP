// 2. Add this JavaScript to debug and ensure links are working
document.addEventListener("DOMContentLoaded", () => {
    // Find all apply buttons
    const applyButtons = document.querySelectorAll(".apply-btn")
  
    // Add click event listeners to each button
    applyButtons.forEach((button) => {
      button.addEventListener("click", function (e) {
        // Log the URL to console for debugging
        console.log("Clicking apply button with URL:", this.getAttribute("href"))
  
        // Don't prevent default - let the link work normally
        // e.preventDefault();
  
        // Optional: Add visual feedback
        this.classList.add("clicked")
      })
    })
  })
  