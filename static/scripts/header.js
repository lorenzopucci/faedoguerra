function toggle_collapse_navbar() {
    document.getElementById('header-links').classList.toggle('nav-visible');
}

function redirect_to_dashboard() {
    window.location.href = '/dashboard';
}

function redirect_to_about() {
    window.location.href = '/about';
}

function redirect_to_login() {
    window.location.href = '/auth/login';
}
