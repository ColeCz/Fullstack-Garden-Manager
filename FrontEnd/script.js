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

function getAllPlants() {
    fetch(apiUrl + "/get_plants")
        .then(response => response.json())
        .then(plants => {
            // Handle the response (e.g., update the plant table)
            updatePlantTable(plants);
        })
        .catch(error => console.error("An error has occurred:", error));
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
        getAllPlants()
    });
}

function groupPlantsBy() {
    const selectedColumn = document.getElementById("columns").value;

    if (!selectedColumn) {
        alert("Please select a column for grouping");
        return;
    }

    const data = {
        column: selectedColumn
    };

    fetch("http://127.0.0.1:5000/group_plants_by", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(response => {
        // Clear existing grouped table
        console.log(response)
        const groupedTableBody = document.querySelector(".grouped-table tbody");
        groupedTableBody.innerHTML = "";

        // Populate the grouped table with the received data
        response.forEach(row => {
            const newRow = `<tr><td>${row.name}</td><td>${row.count}</td></tr>`;
            groupedTableBody.innerHTML += newRow;
        });
    })
    .catch(error => {
        console.error("Fetch error:", error);
    });
}

function updatePlantTable(plants) {
    // Clear existing table rows
    $(".plant-table tbody").empty();

    // Populate the table with the results
    plants.forEach(function (plant) {
        const row = `<tr>
                        <td>${plant.id}</td>
                        <td>${plant.name}</td>
                        <td>${plant.type}</td>
                        <td>${plant.stage}</td>
                        <td>${plant.health}</td>
                    </tr>`;
        $(".plant-table tbody").append(row);
    });
}

$(document).ready(function () {
    getAllPlants();
});

window.onload = function () {
    getAllPlants();
};


