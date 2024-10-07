//SAMPLE LANG YUNG FIRST NAME, PAPALIT NA LANG PO NG MISMONG VARIABLE FROM DATABASE TY
// var firstName = "Ericka Joy";
// document.querySelector(".joinContainer h1").textContent = "Hello, " + firstName + "!"; 

function goHome(){ //WHEN THE LOGO OR "PROPERTIES SETTLEMENT" IS CLICKED
    window.location.href = '';
}

function togglePassword() { //FOR HIDING AND SHOWING OF PASSWORD
    var passwordInput = document.getElementById('password');
    var eyeIcon = document.getElementById('eye-icon');

    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        eyeIcon.className = 'fa-solid fa-eye-slash';
    } else {
        passwordInput.type = 'password';
        eyeIcon.className = 'fa-solid fa-eye';
    }
}

function hidePreloader() { //HIDE THE PRELOADER
    var preloader = document.getElementById('preloader');
    preloader.style.display = 'none';
}

document.addEventListener('DOMContentLoaded', function () { //HIDE LOADER AFTER 3.5 SECS
    setTimeout(hidePreloader, 1); 
});