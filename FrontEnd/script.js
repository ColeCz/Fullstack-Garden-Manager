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

function addGardenWorker() {
    const name = document.getElementById("worker-name").value;
    const proficiency = document.getElementById("worker-proficiency").value;

    if (!name || !proficiency) {
        alert("Name and proficiency are required fields");
        return;
    }

    const data = {
        name: name,
        proficiency: proficiency
    };

    fetch(apiUrl + "/add_garden_worker", {
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
        alert(response.message);
        // After adding, refresh the table
        getAllGardenWorkers();
    })
    .catch(error => {
        console.error("Fetch error:", error);
    });
}

function getAllGardenWorkers() {
    fetch(apiUrl + "/get_all_garden_workers")
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(response => {
        // Clear existing garden worker table
        const gardenWorkerTableBody = document.querySelector(".worker-table tbody");
        gardenWorkerTableBody.innerHTML = "";

        // Populate the garden worker table with the received data
        response.forEach(row => {
            const newRow = `<tr><td>${row.id}</td><td>${row.proficiency}</td><td>${row.name}</td></tr>`;
            gardenWorkerTableBody.innerHTML += newRow;
        });
    })
    .catch(error => {
        console.error("Fetch error:", error);
    });
}

function addGarden() {
    // Get form data
    const formData = {
        user_id: document.getElementById("user-id").value, // Assuming you have an input field with id "user-id" for user_id
        location: document.getElementById("garden-location").value,
        size: document.getElementById("garden-size").value,
        capacity: document.getElementById("garden-capacity").value,
        soil: document.getElementById("garden-soil").value
    };

    // Send a POST request to the server
    fetch(apiUrl + "/gardens", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message); // Display the server response
        // You can update the table or perform other actions as needed
        fetchGardens(); // Assuming you have a function to update the garden table
    })
    .catch(error => console.error("Error:", error));
}

function fetchGardens() {
    fetch('http://127.0.0.1:5000/get_gardens')
        .then(response => response.json())
        .then(gardens => updateGardenTable(gardens))
        .catch(error => console.error('Error fetching gardens:', error));
}

// Function to update the garden table with fetched data
function updateGardenTable(gardens) {
    const gardenTableBody = document.getElementById('garden-table-body');

    // Clear existing rows
    gardenTableBody.innerHTML = '';

    // Add rows for each garden
    gardens.forEach(garden => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${garden.garden_id}</td>
            <td>${garden.user_id}</td>
            <td>${garden.location}</td>
            <td>${garden.size}</td>
            <td>${garden.capacity}</td>
            <td>${garden.soil}</td>
        `;
        gardenTableBody.appendChild(row);
    });
}

function getUserGardens() {
    const userId = document.getElementById('user-id-input').value;

    const data = {
        user_id: userId
    };

    fetch('http://127.0.0.1:5000/get_user_gardens', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(userGardens => {
        // Create a new table for user gardens
        createGardenTable(userGardens, 'user-garden-table');
    })
    .catch(error => {
        console.error('Error fetching user gardens:', error);
    });
}

function createGardenTable(userGardens, tableId) {
    // Create a new table element
    const newTable = document.createElement('table');
    newTable.className = 'garden-table'; // You can apply additional classes if needed

    // Create table header
    const headerRow = document.createElement('tr');
    Object.keys(userGardens[0]).forEach(header => {
        const th = document.createElement('th');
        th.textContent = header;
        headerRow.appendChild(th);
    });
    newTable.appendChild(headerRow);

    // Create table body
    userGardens.forEach(userGarden => {
        const newRow = document.createElement('tr');
        Object.values(userGarden).forEach(value => {
            const newCell = document.createElement('td');
            newCell.textContent = value;
            newRow.appendChild(newCell);
        });
        newTable.appendChild(newRow);
    });
    const resultContainer = document.getElementById('result-container');
    resultContainer.innerHTML = ''; // Clear existing content
    resultContainer.appendChild(newTable);
}

$(document).ready(function () {
    getAllPlants();
    getAllGardenWorkers();
    fetchGardens();
});

window.onload = function () {
    getAllPlants();
    getAllGardenWorkers();
    fetchGardens();
};


