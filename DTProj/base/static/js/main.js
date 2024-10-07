function goHome(){ //WHEN THE LOGO OR "PROPERTIES SETTLEMENT" IS CLICKED
    window.location.href = '';
} 

function hidePreloader() { //HIDE THE PRELOADER
    var preloader = document.getElementById('preloader');
    preloader.style.display = 'none';
}

document.addEventListener('DOMContentLoaded', function () { //HIDE LOADER AFTER 3.5 SECS
    setTimeout(hidePreloader, 1); 
});

