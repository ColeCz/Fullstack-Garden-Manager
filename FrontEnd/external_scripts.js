const existing_username_field = document.getElementById("existing_username_field");
const existing_password_field = document.getElementById("existing_password_field");

document.getElementById("sign_in_button").addEventListener("click", function () {
    const username = existing_username_field.value;
    const password = existing_password_field.value;

    if (username === "admin" && password === "admin") {
        window.location.href = "GMS HTML Structure.html";
    }
});

/*
var username_field = document.getElementById("signin_field_username");
var username = "";
username_field.addEventListener("input", function() {
    username = username_field.value;
    console.log("User input changed: " + username);
});
*/

