const startYear = 2024;
const currentYear = new Date().getFullYear();

// Set the start year
document.getElementById('start-year').textContent = startYear;

// Check and set the current year only if it's different from start year
if (startYear !== currentYear) {
  document.getElementById('current-year').textContent = "-" + currentYear;
} else {
  // Optionally, you can hide the current year span if they are the same
  document.getElementById('current-year').style.display = 'none';
}
// for admin-panel
document.addEventListener("DOMContentLoaded", function() {
    var links = document.querySelectorAll('.sidebar ul li a');
    links.forEach(function(link) {
        link.addEventListener('click', function() {
            var siblings = this.parentNode.parentNode.querySelectorAll('a');
            siblings.forEach(function(sibling) {
                sibling.classList.remove('active');
            });
            this.classList.add('active');
        });
    });
});


// TODO To show logo website in the search results
// type="application/ld+json">
// {
//   "@context": "https://schema.org",
//   "@type": "Organization",
//   "url": "https://www.example.com",
//   "logo": "https://www.example.com/logo.png"
// }

