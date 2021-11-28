let nameOfTheCity = document.getElementById("city")


document.getElementById("submit").addEventListener("click", (event) => [
    validateForm(event)
])

function validateForm(event) {
    if (nameOfTheCity.value == "" || nameOfTheCity.value == null) {
        event.preventDefault();
        setCityNameError()
    }
}

function setCityNameError() {
    let errorMessage = document.getElementById("username-message")
    errorMessage.style.visibility = "visible"
    errorMessage.style.color = "red"
    errorMessage.innerText = "city name must not be empty"

}