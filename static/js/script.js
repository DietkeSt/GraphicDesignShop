document.addEventListener("DOMContentLoaded", function() {
    // Toggle navbar
    document.querySelector('.navbar-toggler').addEventListener('click', function() {
        this.classList.toggle('active');
        document.querySelector('.navbar-collapse').classList.toggle('show');
    });

    // Dropdown toggle for mobile
    document.querySelectorAll('.nav-item.dropdown').forEach(function(dropdown) {
        dropdown.addEventListener('click', function() {
            this.querySelector('.dropdown-menu').classList.toggle('show');
        });
    });
});