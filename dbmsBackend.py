from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

# import mysql.connector
# from flask import render_template, request, redirect, url_for
# from flask_login import login_user, current_user, login_required, logout_user

app = Flask(__name__)
CORS(app)

# Connect to MySQL
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Schwalbegraze0!",
    database="gardenproject"
)

# Create a cursor object
mycursor = mydb.cursor()

def user_exists(email):
    query = "SELECT COUNT(*) FROM User WHERE email = %s"
    values = (email,)
    mycursor.execute(query, values)
    result = mycursor.fetchone()[0]
    return result > 0

# Create
@app.route('/register_user', methods=['POST'])
def register_user():
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
    data = request.get_json()
    query = "UPDATE User SET email = %s, password = %s WHERE user_id = %s"
    values = (data['email'], data['password'], user_id)
    mycursor.execute(query, values)
    mydb.commit()
    return jsonify({"message": "User updated successfully"})

# Delete
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    query = "DELETE FROM User WHERE user_id = %s"
    values = (user_id,)
    mycursor.execute(query, values)
    mydb.commit()
    return jsonify({"message": "User deleted successfully"})

# Add plant to the database
@app.route('/add_plant', methods=['POST'])
def add_plant():
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
    query = "INSERT INTO plants (stage, health, name, type) VALUES (%s, %s, %s, %s)"
    values = (name, type, stage, health)
    mycursor.execute(query, values)
    mydb.commit()

    return jsonify({"message": "Plant added successfully"})

@app.route('/get_plants', methods=['GET'])
def get_plants():
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
    print(plant_list)

    return jsonify(plant_list)

@app.route('/group_plants_by', methods=['POST'])
def group_plants_by():
    data = request.get_json()
    selected_column = data.get('column')
    print(selected_column)
    if not selected_column:
        return jsonify({"error": "Please provide a valid column for grouping"}), 400

    try:
        # Assuming 'plants' is your table name
        query = f"SELECT {selected_column}, COUNT(plant_id) AS count FROM plants GROUP BY {selected_column}"
        print(query)
        mycursor.execute(query)
        result = mycursor.fetchall()
        print(result)
        grouped_data = [{"name": row[0], "count": row[1]} for row in result]

        return jsonify(grouped_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True)
