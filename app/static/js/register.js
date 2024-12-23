async function check_password() {
    if (document.getElementById('show_password').checked){
        document.getElementById('password').setAttribute('type', 'text');
    } else {
        document.getElementById('password').setAttribute('type', 'password');
    }
}


async function check_password_confirm() {
    if (document.getElementById('show_password_confirm').checked){
        document.getElementById('password_confirm').setAttribute('type', 'text');
    } else {
        document.getElementById('password_confirm').setAttribute('type', 'password');
    }
}