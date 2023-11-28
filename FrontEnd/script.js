// const existing_username_field = document.getElementById("existing_username_field");
// const existing_password_field = document.getElementById("existing_password_field");

// document.getElementById("sign_in_button").addEventListener("click", function () {
//     const username = existing_username_field.value;
//     const password = existing_password_field.value;

//     if (username === "admin" && password === "admin") {
//         window.location.href = "GMS HTML Structure.html";
//     }
// });

/*
var username_field = document.getElementById("signin_field_username");
var username = "";
username_field.addEventListener("input", function() {
    username = username_field.value;
    console.log("User input changed: " + username);
});
*/
const apiUrl = "http://127.0.0.1:5000";

// Function to handle API requests
function makeRequest(method, endpoint, data, successCallback) {
    $.ajax({
        method: method,
        url: apiUrl + endpoint,
        contentType: "application/json",
        data: JSON.stringify(data),
        success: successCallback,
        error: function (xhr, status, error) {
            console.error("An error has occurred:", error);
        }
    });
}

function registerUser() {
    const username = $("#email").val();
    const password = $("#password").val();

    const data = {
        email: username,
        password: password
    };

    makeRequest("POST", "/register_user", data, function (response) {
        alert(response.message);
    });
}

function addPlant() {
    const plantName = $("#plant-name").val();
    const plantType = $("#plant-type").val();
    const plantStage = $("#plant-stage").val();
    const plantHealth = $("#plant-health").val();

    // Check if all fields are filled
    if (!plantName || !plantType || !plantStage || !plantHealth) {
        alert("Please fill in all fields");
        return;
    }

    const data = {
        name: plantName,
        type: plantType,
        stage: plantStage,
        health: plantHealth
    };

    makeRequest("POST", "/add_plant", data, function (response) {
        alert(response.message);
    });
}
