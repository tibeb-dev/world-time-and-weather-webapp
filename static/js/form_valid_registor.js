let form = document.getElementById("form")
let userName = document.getElementById("userName")
let password = document.getElementById("Password")
let date = document.getElementById("date")
let errorMessageUserName = document.getElementById("username-message")
let errorMessagePassword = document.getElementById("password-message")
let errorMessageDate = document.getElementById("date-message")
let submitButton = document.getElementById("submit")

document.getElementById("submit")
    .addEventListener("click", (event) => {
        validateForm(event)
    })



function validateForm(event) {
    let reg_name = /^[A-Za-z]+[A-Za-z0-9 _]*$/;
    let reg_date = /^2021-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[0])$/;

    if (userName.value == "") {
        event.preventDefault();
        setUserNameError("user name must not be empty");
    } else if (!reg_name.test(userName.value)) {
        event.preventDefault();
        setUserNameError("name should start with letter");
    } else {
        setUserNameError("");
    }

    if (password.value == "") {
        event.preventDefault();
        setPasswordError("password must not be empty");
    } else {
        setPasswordError("");
    }

    if (date.value == "") {
        event.preventDefault()
        setDateError("date must not be empty")
    } else if (!reg_date.test(date.value)) {
        event.preventDefault()
        setDateError("enter valid date formate")
    } else {
        setDateError("")
    }

}


function setUserNameError(message) {
    if (message) {
        errorMessageUserName.style.visibility = "visible";
        errorMessageUserName.style.color = "red";
        errorMessageUserName.innerText = message
    } else {
        errorMessageUserName.style.visibility = "hidden";
        errorMessageUserName.innerText = ""
    }

}

function setPasswordError(message) {
    if (message) {
        errorMessagePassword.style.visibility = "visible"
        errorMessagePassword.style.color = "red"
        errorMessagePassword.innerText = message
    } else {
        errorMessagePassword.style.visibility = "hidden"
        errorMessagePassword.innerText = message
    }
}

function setDateError(message) {
    if (message) {
        errorMessageDate.style.visibility = "visible"
        errorMessageDate.style.color = "red"
        errorMessageDate.innerText = message
    } else {
        errorMessageDate.style.visibility = "hidden"
        errorMessageDate.innerText = message
    }
}