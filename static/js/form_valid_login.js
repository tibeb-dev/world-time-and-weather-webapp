let userName = document.getElementById("txtUserName");
let password = document.getElementById("txtPwd");

let form = document.getElementById("form")



document.getElementById("submit")
    .addEventListener("click", (event) => {
        validateForm(event);
    });

function validateForm(event) {
    let reg_name = /^[A-Za-z]+[A-Za-z0-9]*$/;

    if (userName.value == "") {
        event.preventDefault();
        setUsernameError("Username must not be empty");
    } else if (!reg_name.test(userName.value)) {
        event.preventDefault();
        setUsernameError("name should only starts with letter");
    } else {
        setUsernameError("");
    }

    if (password.value == "") {
        event.preventDefault();
        setPasswordError("Password must not be empty");

    } else {
        setPasswordError("");
    }
}


function setUsernameError(message) {
    let errorMessage = document.getElementById("username-message");
    if (message) {
        errorMessage.style.visibility = "visible";
        errorMessage.style.color = "red";
        errorMessage.innerText = message;
    } else {
        errorMessage.style.visibility = "hidden";
        errorMessage.innerText = "";
    }
}

function setPasswordError(message) {
    let errorMessage = document.getElementById("password-message");
    if (message) {
        errorMessage.style.visibility = "visible";
        errorMessage.style.color = "red";
        errorMessage.innerText = message;
    } else {
        errorMessage.style.visibility = "hidden";
        errorMessage.innerText = "";
    }
}