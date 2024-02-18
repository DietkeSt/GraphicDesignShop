document.addEventListener('DOMContentLoaded', function() {
    var mobileNavToggle = document.querySelector('.mobile-nav');
    var navMenu = document.querySelector('.navigation ul');

    mobileNavToggle.addEventListener('click', function() {
        navMenu.style.display = navMenu.style.display === 'block' ? 'none' : 'block';
    });
});
  
  // You'd also need JavaScript to dynamically update the login text and item counter based on user state.
document.addEventListener('DOMContentLoaded', function() {
    var dropdown = document.querySelector('.arrow-down');
    dropdown.onclick = function() {
        var dropdownContent = this.nextElementSibling;
        if (dropdownContent.style.display === "block") {
            dropdownContent.style.display = "none";
        } else {
            dropdownContent.style.display = "block";
        }
    }
});