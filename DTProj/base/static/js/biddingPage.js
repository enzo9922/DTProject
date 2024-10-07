function submitForm() {
    // Your form submission logic here
}

function goHome() {
    window.location.href = '/';
}

function hidePreloader() {
    var preloader = document.getElementById('preloader');
    preloader.style.display = 'none';
}

document.addEventListener('DOMContentLoaded', function () {
    setTimeout(hidePreloader, 3500);
});