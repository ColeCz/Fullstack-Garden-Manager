from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

# import mysql.connector
# from flask import render_template, request, redirect, url_for
# from flask_login import login_user, current_user, login_required, logout_user

app = Flask(__name__)
CORS(app)
CORS(app,origins="http://127.0.0.1:5500")


def user_exists(email):
    # Connect to MySQL
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Schwalbegraze0!",
        database="new_gardenproject"
    )

    # Create a cursor object
    mycursor = mydb.cursor()
    query = "SELECT COUNT(*) FROM User WHERE email = %s"
    values = (email,)
    mycursor.execute(query, values)
    result = mycursor.fetchone()[0]
    return result > 0

# Create
@app.route('/register_user', methods=['POST'])
def register_user():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Schwalbegraze0!",
        database="new_gardenproject"
    )

    # Create a cursor object
    mycursor = mydb.cursor()
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    if email is None or password is None:
        return jsonify({"error": "Email and password are required"}), 400

    if user_exists(email):
        return jsonify({"message": "User already exists"}), 400

    query = "INSERT INTO User (email, password) VALUES (%s, %s)"
    values = (email, password)
    mycursor.execute(query, values)
    mydb.commit()
    
    return jsonify({"message": "User registered successfully"})

# Read
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Schwalbegraze0!",
        database="new_gardenproject"
    )

    # Create a cursor object
    mycursor = mydb.cursor()
    query = "SELECT * FROM User WHERE user_id = %s"
    values = (user_id,)
    mycursor.execute(query, values)
    user = mycursor.fetchone()
    if user:
        user_data = {
            "user_id": user[0],
            "email": user[1],
            "password": user[2]
        }
        return jsonify(user_data)
    else:
        return jsonify({"message": "User not found"}), 404

# Update
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Schwalbegraze0!",
        database="new_gardenproject"
    )

    # Create a cursor object
    mycursor = mydb.cursor()
    data = request.get_json()
    query = "UPDATE User SET email = %s, password = %s WHERE user_id = %s"
    values = (data['email'], data['password'], user_id)
    mycursor.execute(query, values)
    mydb.commit()
    return jsonify({"message": "User updated successfully"})

# Delete
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Schwalbegraze0!",
        database="new_gardenproject"
    )

    # Create a cursor object
    mycursor = mydb.cursor()
    query = "DELETE FROM User WHERE user_id = %s"
    values = (user_id,)
    mycursor.execute(query, values)
    mydb.commit()
    return jsonify({"message": "User deleted successfully"})

# Add plant to the database
@app.route('/add_plant', methods=['POST'])
def add_plant():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Schwalbegraze0!",
        database="new_gardenproject"
    )

    # Create a cursor object
    mycursor = mydb.cursor()
    data = request.get_json()

    name = data.get('name')
    type = data.get('type')
    stage = data.get('stage')
    health = data.get('health')

    if name is None or type is None or stage is None or health is None:
        print("field missing")
        return jsonify({"error": "Missing required fields"}), 400
    

    query = "SELECT COUNT(*) FROM plants WHERE name = %s"
    values = (name,)
    mycursor.execute(query, values)
    result = mycursor.fetchone()[0]
    if result > 0:
        print("plant already exists")
        return jsonify({"error": "Plant already exists"}), 400
    
    # Perform the database insertion here
    query = "INSERT INTO plants (name, type, stage, health) VALUES (%s, %s, %s, %s)"
    values = (name, type, stage, health)
    mycursor.execute(query, values)
    mydb.commit()

    return jsonify({"message": "Plant added successfully"})

@app.route('/get_plants', methods=['GET'])
def get_plants():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Schwalbegraze0!",
        database="new_gardenproject"
    )

    # Create a cursor object
    mycursor = mydb.cursor()
    query = "SELECT * FROM Plants"
    mycursor.execute(query)
    plants = mycursor.fetchall()

    plant_list = []
    for plant in plants:
        plant_data = {
            'id': plant[0],
            'name': plant[1],
            'type': plant[2],
            'stage': plant[3],
            'health': plant[4]
        }
        plant_list.append(plant_data)
    # print(plant_list)

    return jsonify(plant_list)

@app.route('/group_plants_by', methods=['POST'])
def group_plants_by():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Schwalbegraze0!",
        database="new_gardenproject"
    )

    # Create a cursor object
    mycursor = mydb.cursor()
    data = request.get_json()
    selected_column = data.get('column')
    print(selected_column)
    if not selected_column:
        return jsonify({"error": "Please provide a valid column for grouping"}), 400

    try:
        # Assuming 'plants' is your table name
        query = f"SELECT {selected_column}, COUNT(plant_id) AS count FROM plants GROUP BY {selected_column}"
        # print(query)
        mycursor.execute(query)
        result = mycursor.fetchall()
        # print(result)
        grouped_data = [{"name": row[0], "count": row[1]} for row in result]

        return jsonify(grouped_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        
@app.route('/add_garden_worker', methods=['POST'])
def add_garden_worker():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Schwalbegraze0!",
        database="new_gardenproject"
    )

    # Create a cursor object
    mycursor = mydb.cursor()
    data = request.get_json()
    query = "INSERT INTO workers (proficiency, name) VALUES (%s, %s)"
    values = (data['proficiency'], data['name'])
    mycursor.execute(query, values)
    mydb.commit()
    return jsonify({"message": "Garden worker added successfully"})

# Read all
@app.route('/get_all_garden_workers', methods=['GET'])
def get_all_garden_workers():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Schwalbegraze0!",
        database="new_gardenproject"
    )

    # Create a cursor object
    mycursor = mydb.cursor()
    query = "SELECT * FROM workers"
    mycursor.execute(query)
    garden_workers = mycursor.fetchall()
    # print(garden_workers)
    workers_data = [{"id": row[0], "proficiency": row[1], "name": row[2]} for row in garden_workers]
    return jsonify(workers_data)

@app.route('/gardens', methods=['POST'])
def create_garden():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Schwalbegraze0!",
        database="new_gardenproject"
    )

    # Create a cursor object
    mycursor = mydb.cursor()
    data = request.get_json()

    user_id = data.get('user_id')
    location = data.get('location')
    size = data.get('size')
    capacity = data.get('capacity')
    soil = data.get('soil')

    # Validate that all required fields are provided
    if not (user_id and location and size and capacity and soil):
        return jsonify({"message": "All fields are required"}), 400

    # Insert data into the ugardens table
    query = "INSERT INTO ugardens (user_id, location, size, capacity, soil) VALUES (%s, %s, %s, %s, %s)"
    values = (user_id, location, size, capacity, soil)

    try:
        mycursor.execute(query, values)
        mydb.commit()
        return jsonify({"message": "Garden added successfully"})
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500
    
@app.route('/get_gardens', methods=['GET'])
def get_gardens():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Schwalbegraze0!",
        database="new_gardenproject"
    )

    # Create a cursor object
    mycursor = mydb.cursor()
    query = "SELECT * FROM ugardens"
    mycursor.execute(query)
    gardens = mycursor.fetchall()

    garden_list = []
    for garden in gardens:
        plant_data = {
            'garden_id': garden[0],
            'user_id': garden[1],
            'location': garden[2],
            'size': garden[3],
            'capacity': garden[4],
            'soil' : garden[5]
        }
        garden_list.append(plant_data)
    # print(plant_list)

    return jsonify(garden_list)

@app.route('/get_user_gardens', methods=['POST'])
def get_user_gardens():
    # Get data from the request JSON
    data = request.get_json()

    # Extract user_id from the data
    user_id = data.get('user_id')

    # Establish a database connection
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Schwalbegraze0!",
        database="new_gardenproject"
    )

    # Create a cursor object
    mycursor = mydb.cursor()

    # Execute the parameterized query
    query = "SELECT user.email, ugardens.* FROM user JOIN ugardens ON user.user_id = ugardens.user_id WHERE user.user_id = %s"
    mycursor.execute(query, (user_id,))
    
    # Fetch all results
    user_gardens = mycursor.fetchall()

    # Convert the results to a list of dictionaries
    user_gardens_list = []
    for user_garden in user_gardens:
        user_garden_data = {
            'email': user_garden[0],  # Assuming email is the first column in the user table
            'garden_id': user_garden[1],  # Assuming user_id is the second column in the user table
            # Add other columns from the user table as needed

            'user_id': user_garden[2],  # Assuming garden_id is the first column in the ugardens table
            'location': user_garden[3],  # Assuming location is the second column in the ugardens table
            'size' : user_garden[4],
            'capacity' : user_garden[5],
            'soil' : user_garden[6]
        }
        user_gardens_list.append(user_garden_data)

    # Close the database connection
    mydb.close()

    # Return the results as JSON
    return jsonify(user_gardens_list)

if __name__ == '__main__':
    app.run(debug=True)
