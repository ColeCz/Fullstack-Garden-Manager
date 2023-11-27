from flask import Flask, request, jsonify, render_template
import mysql.connector


app = Flask(__name__)

# Connect to MySQL
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Wilcome88111710348",
    database="garden_management_system"
)

# Create a cursor object
mycursor = mydb.cursor()

@app.route('/')
def index():
    return render_template('index.html')

# User Registration:

# Create a registration route where users can provide their email and password.
# Create a new user and add them to the database:


#1 contains table API
# Create for the Contains table
@app.route('/contains', methods=['POST'])
def create_contains():
    data = request.get_json()
    query = "INSERT INTO Contains (garden_id, plant_id) VALUES (%s, %s)"
    values = (data['garden_id'], data['plant_id'])
    mycursor.execute(query, values)
    mydb.commit()
    return jsonify({"message": "Relation added successfully to Contains table"})

# Read for the Contains table
@app.route('/contains/<int:garden_id>/<int:plant_id>', methods=['GET'])
def get_contains(garden_id, plant_id):
    query = "SELECT * FROM Contains WHERE garden_id = %s AND plant_id = %s"
    values = (garden_id, plant_id)
    mycursor.execute(query, values)
    relation = mycursor.fetchone()
    if relation:
        relation_data = {
            "garden_id": relation[0],
            "plant_id": relation[1]
        }
        return jsonify(relation_data)
    else:
        return jsonify({"message": "Relation not found in Contains table"}), 404

# Delete for the Contains table
@app.route('/contains/<int:garden_id>/<int:plant_id>', methods=['DELETE'])
def delete_contains(garden_id, plant_id):
    query = "DELETE FROM Contains WHERE garden_id = %s AND plant_id = %s"
    values = (garden_id, plant_id)
    mycursor.execute(query, values)
    mydb.commit()
    return jsonify({"message": "Relation deleted successfully from Contains table"})

#2 employs table API
# Create for the Employs table
@app.route('/employs', methods=['POST'])
def create_employ():
    data = request.get_json()
    query = "INSERT INTO Employs (user_id, worker_id) VALUES (%s, %s)"
    values = (data['user_id'], data['worker_id'])
    mycursor.execute(query, values)
    mydb.commit()
    return jsonify({"message": "Employ relationship created successfully"})

# Read for the Employs table
@app.route('/employs/<int:user_id>/<int:worker_id>', methods=['GET'])
def get_employ(user_id, worker_id):
    query = "SELECT * FROM Employs WHERE user_id = %s AND worker_id = %s"
    values = (user_id, worker_id)
    mycursor.execute(query, values)
    employ = mycursor.fetchone()
    if employ:
        employ_data = {
            "user_id": employ[0],
            "worker_id": employ[1]
        }
        return jsonify(employ_data)
    else:
        return jsonify({"message": "Employ relationship not found"}), 404

# Update for the Employs table
@app.route('/employs/<int:user_id>/<int:worker_id>', methods=['PUT'])
def update_employ(user_id, worker_id):
    data = request.get_json()
    query = "UPDATE Employs SET user_id = %s, worker_id = %s WHERE user_id = %s AND worker_id = %s"
    values = (data['user_id'], data['worker_id'], user_id, worker_id)
    mycursor.execute(query, values)
    mydb.commit()
    return jsonify({"message": "Employ relationship updated successfully"})

# Delete for the Employs table
@app.route('/employs/<int:user_id>/<int:worker_id>', methods=['DELETE'])
def delete_employ(user_id, worker_id):
    query = "DELETE FROM Employs WHERE user_id = %s AND worker_id = %s"
    values = (user_id, worker_id)
    mycursor.execute(query, values)
    mydb.commit()
    return jsonify({"message": "Employ relationship deleted successfully"})

#3 gardens table API
# Create for 'Gardens' table
@app.route('/gardens', methods=['POST'])
def create_garden():
    data = request.get_json()
    query = "INSERT INTO Gardens (location, size, capacity, soil, user_id) VALUES (%s, %s, %s, %s, %s)"
    values = (data['location'], data['size'], data['capacity'], data['soil'], data['user_id'])
    mycursor.execute(query, values)
    mydb.commit()
    return jsonify({"message": "Garden created successfully"})

# Read for 'Gardens' table
@app.route('/gardens/<int:garden_id>', methods=['GET'])
def get_garden(garden_id):
    query = "SELECT * FROM Gardens WHERE garden_id = %s"
    values = (garden_id,)
    mycursor.execute(query, values)
    garden = mycursor.fetchone()
    if garden:
        garden_data = {
            "garden_id": garden[0],
            "location": garden[1],
            "size": garden[2],
            "capacity": garden[3],
            "soil": garden[4],
            "user_id": garden[5]
        }
        return jsonify(garden_data)
    else:
        return jsonify({"message": "Garden not found"}), 404

# Update for 'Gardens' table
@app.route('/gardens/<int:garden_id>', methods=['PUT'])
def update_garden(garden_id):
    data = request.get_json()
    query = "UPDATE Gardens SET location = %s, size = %s, capacity = %s, soil = %s, user_id = %s WHERE garden_id = %s"
    values = (data['location'], data['size'], data['capacity'], data['soil'], data['user_id'], garden_id)
    mycursor.execute(query, values)
    mydb.commit()
    return jsonify({"message": "Garden updated successfully"})

# Delete for 'Gardens' table
@app.route('/gardens/<int:garden_id>', methods=['DELETE'])
def delete_garden(garden_id):
    query = "DELETE FROM Gardens WHERE garden_id = %s"
    values = (garden_id,)
    mycursor.execute(query, values)
    mydb.commit()
    return jsonify({"message": "Garden deleted successfully"})

#4 gardens_relationship table API
# Create for gardens_relationship table
@app.route('/gardens_relationship', methods=['POST'])
def create_gardens_relationship():
    data = request.get_json()
    query = "INSERT INTO Gardens_Relationship (garden_id, worker_id) VALUES (%s, %s)"
    values = (data['garden_id'], data['worker_id'])
    mycursor.execute(query, values)
    mydb.commit()
    return jsonify({"message": "Gardens relationship created successfully"})

# Read for gardens_relationship table
@app.route('/gardens_relationship/<int:garden_id>/<int:worker_id>', methods=['GET'])
def get_gardens_relationship(garden_id, worker_id):
    query = "SELECT * FROM Gardens_Relationship WHERE garden_id = %s AND worker_id = %s"
    values = (garden_id, worker_id)
    mycursor.execute(query, values)
    gardens_relationship = mycursor.fetchone()
    if gardens_relationship:
        gardens_relationship_data = {
            "garden_id": gardens_relationship[0],
            "worker_id": gardens_relationship[1]
        }
        return jsonify(gardens_relationship_data)
    else:
        return jsonify({"message": "Gardens relationship not found"}), 404

# Update for gardens_relationship table
@app.route('/gardens_relationship/<int:garden_id>/<int:worker_id>', methods=['PUT'])
def update_gardens_relationship(garden_id, worker_id):
    data = request.get_json()
    query = "UPDATE Gardens_Relationship SET garden_id = %s, worker_id = %s WHERE garden_id = %s AND worker_id = %s"
    values = (data['garden_id'], data['worker_id'], garden_id, worker_id)
    mycursor.execute(query, values)
    mydb.commit()
    return jsonify({"message": "Gardens relationship updated successfully"})

# Delete for gardens_relationship table
@app.route('/gardens_relationship/<int:garden_id>/<int:worker_id>', methods=['DELETE'])
def delete_gardens_relationship(garden_id, worker_id):
    query = "DELETE FROM Gardens_Relationship WHERE garden_id = %s AND worker_id = %s"
    values = (garden_id, worker_id)
    mycursor.execute(query, values)
    mydb.commit()
    return jsonify({"message": "Gardens relationship deleted successfully"})

#5 operates table API
# Create for Operates table
@app.route('/operates', methods=['POST'])
def create_operates():
    data = request.get_json()
    query = "INSERT INTO Operates (user_id, garden_id) VALUES (%s, %s)"
    values = (data['user_id'], data['garden_id'])
    mycursor.execute(query, values)
    mydb.commit()
    return jsonify({"message": "Operates relationship created successfully"})

# Read for Operates table
@app.route('/operates/<int:user_id>/<int:garden_id>', methods=['GET'])
def get_operates(user_id, garden_id):
    query = "SELECT * FROM Operates WHERE user_id = %s AND garden_id = %s"
    values = (user_id, garden_id)
    mycursor.execute(query, values)
    operates = mycursor.fetchone()
    if operates:
        operates_data = {
            "user_id": operates[0],
            "garden_id": operates[1]
        }
        return jsonify(operates_data)
    else:
        return jsonify({"message": "Operates relationship not found"}), 404

# Update for Operates table (Optional)
# Since Operates table has a composite primary key, updates might not be applicable.

# Delete for Operates table
@app.route('/operates/<int:user_id>/<int:garden_id>', methods=['DELETE'])
def delete_operates(user_id, garden_id):
    query = "DELETE FROM Operates WHERE user_id = %s AND garden_id = %s"
    values = (user_id, garden_id)
    mycursor.execute(query, values)
    mydb.commit()
    return jsonify({"message": "Operates relationship deleted successfully"})

#6 owns table API
# Create for the Owns table (Create relationship between User and Plant)
@app.route('/owns', methods=['POST'])
def create_ownership():
    data = request.get_json()
    query = "INSERT INTO Owns (user_id, plant_id) VALUES (%s, %s)"
    values = (data['user_id'], data['plant_id'])
    mycursor.execute(query, values)
    mydb.commit()
    return jsonify({"message": "Ownership created successfully"})

# Read for the Owns table (Retrieve ownership details by user_id)
@app.route('/owns/user/<int:user_id>', methods=['GET'])
def get_owned_plants_by_user(user_id):
    query = "SELECT Plants.plant_id, Plants.name, Plants.type FROM Owns \
             INNER JOIN Plants ON Owns.plant_id = Plants.plant_id \
             WHERE Owns.user_id = %s"
    values = (user_id,)
    mycursor.execute(query, values)
    owned_plants = mycursor.fetchall()
    if owned_plants:
        plant_list = []
        for plant in owned_plants:
            plant_data = {
                "plant_id": plant[0],
                "name": plant[1],
                "type": plant[2]
            }
            plant_list.append(plant_data)
        return jsonify(plant_list)
    else:
        return jsonify({"message": "No plants owned by this user"}), 404

# Delete for the Owns table (Delete ownership of a plant by user_id and plant_id)
@app.route('/owns/<int:user_id>/<int:plant_id>', methods=['DELETE'])
def delete_ownership(user_id, plant_id):
    query = "DELETE FROM Owns WHERE user_id = %s AND plant_id = %s"
    values = (user_id, plant_id)
    mycursor.execute(query, values)
    mydb.commit()
    return jsonify({"message": "Ownership deleted successfully"})

#7 plants table API
# Create a plant
@app.route('/plants', methods=['POST'])
def create_plant():
    data = request.get_json()
    query = "INSERT INTO plants (name, type, stage, health) VALUES (%s, %s, %s, %s)"
    values = (data['name'], data['type'], data['stage'], data['health'])
    mycursor.execute(query, values)
    mydb.commit()
    return jsonify({"message": "Plant created successfully"})

# Read a plant
@app.route('/plants/<int:plant_id>', methods=['GET'])
def get_plant(plant_id):
    query = "SELECT * FROM plants WHERE plant_id = %s"
    values = (plant_id,)
    mycursor.execute(query, values)
    plant = mycursor.fetchone()
    if plant:
        plant_data = {
            "plant_id": plant[0],
            "name": plant[1],
            "type": plant[2],
            "stage": plant[3],
            "health": plant[4]
        }
        return jsonify(plant_data)
    else:
        return jsonify({"message": "Plant not found"}), 404

# Update a plant
@app.route('/plants/<int:plant_id>', methods=['PUT'])
def update_plant(plant_id):
    data = request.get_json()
    query = "UPDATE plants SET name = %s, type = %s, stage = %s, health = %s WHERE plant_id = %s"
    values = (data['name'], data['type'], data['stage'], data['health'], plant_id)
    mycursor.execute(query, values)
    mydb.commit()
    return jsonify({"message": "Plant updated successfully"})

# Delete a plant
@app.route('/plants/<int:plant_id>', methods=['DELETE'])
def delete_plant(plant_id):
    query = "DELETE FROM plants WHERE plant_id = %s"
    values = (plant_id,)
    mycursor.execute(query, values)
    mydb.commit()
    return jsonify({"message": "Plant deleted successfully"})


#8 plants_relationship table API
# Create for plants_relationship table
@app.route('/plants_relationship', methods=['POST'])
def create_plants_relationship():
    data = request.get_json()
    query = "INSERT INTO plants_relationship (worker_id, plant_id) VALUES (%s, %s)"
    values = (data['worker_id'], data['plant_id'])
    mycursor.execute(query, values)
    mydb.commit()
    return jsonify({"message": "Plants relationship created successfully"})

# Read for plants_relationship table
@app.route('/plants_relationship/<int:worker_id>/<int:plant_id>', methods=['GET'])
def get_plants_relationship(worker_id, plant_id):
    query = "SELECT * FROM plants_relationship WHERE worker_id = %s AND plant_id = %s"
    values = (worker_id, plant_id)
    mycursor.execute(query, values)
    relationship = mycursor.fetchone()
    if relationship:
        relationship_data = {
            "worker_id": relationship[0],
            "plant_id": relationship[1]
        }
        return jsonify(relationship_data)
    else:
        return jsonify({"message": "Plants relationship not found"}), 404

# Update for plants_relationship table (You may need to redefine your update logic based on your use case)
@app.route('/plants_relationship/<int:worker_id>/<int:plant_id>', methods=['PUT'])
def update_plants_relationship(worker_id, plant_id):
    data = request.get_json()
    query = "UPDATE plants_relationship SET worker_id = %s WHERE plant_id = %s"
    values = (data['worker_id'], plant_id)
    mycursor.execute(query, values)
    mydb.commit()
    return jsonify({"message": "Plants relationship updated successfully"})

# Delete for plants_relationship table
@app.route('/plants_relationship/<int:worker_id>/<int:plant_id>', methods=['DELETE'])
def delete_plants_relationship(worker_id, plant_id):
    query = "DELETE FROM plants_relationship WHERE worker_id = %s AND plant_id = %s"
    values = (worker_id, plant_id)
    mycursor.execute(query, values)
    mydb.commit()
    return jsonify({"message": "Plants relationship deleted successfully"})

#9 seeds table API
# Create for seeds table
@app.route('/seeds', methods=['POST'])
def create_seed():
    data = request.get_json()
    query = "INSERT INTO seeds (parent_plant_id, child_plant_id) VALUES (%s, %s)"
    values = (data['parent_plant_id'], data['child_plant_id'])
    mycursor.execute(query, values)
    mydb.commit()
    return jsonify({"message": "Seed created successfully"})

# Read for seeds table
@app.route('/seeds/<int:parent_plant_id>/<int:child_plant_id>', methods=['GET'])
def get_seed(parent_plant_id, child_plant_id):
    query = "SELECT * FROM seeds WHERE parent_plant_id = %s AND child_plant_id = %s"
    values = (parent_plant_id, child_plant_id)
    mycursor.execute(query, values)
    seed = mycursor.fetchone()
    if seed:
        seed_data = {
            "parent_plant_id": seed[0],
            "child_plant_id": seed[1]
        }
        return jsonify(seed_data)
    else:
        return jsonify({"message": "Seed not found"}), 404

# Update for seeds table
@app.route('/seeds/<int:parent_plant_id>/<int:child_plant_id>', methods=['PUT'])
def update_seed(parent_plant_id, child_plant_id):
    data = request.get_json()
    query = "UPDATE seeds SET parent_plant_id = %s, child_plant_id = %s WHERE parent_plant_id = %s AND child_plant_id = %s"
    values = (data['parent_plant_id'], data['child_plant_id'], parent_plant_id, child_plant_id)
    mycursor.execute(query, values)
    mydb.commit()
    return jsonify({"message": "Seed updated successfully"})

# Delete for seeds table
@app.route('/seeds/<int:parent_plant_id>/<int:child_plant_id>', methods=['DELETE'])
def delete_seed(parent_plant_id, child_plant_id):
    query = "DELETE FROM seeds WHERE parent_plant_id = %s AND child_plant_id = %s"
    values = (parent_plant_id, child_plant_id)
    mycursor.execute(query, values)
    mydb.commit()
    return jsonify({"message": "Seed deleted successfully"})

#10 tends table API
# Create - Add a record to the "tends" table
@app.route('/tends', methods=['POST'])
def create_tends():
    data = request.get_json()
    query = "INSERT INTO tends (worker_id, plant_id) VALUES (%s, %s)"
    values = (data['worker_id'], data['plant_id'])
    mycursor.execute(query, values)
    mydb.commit()
    return jsonify({"message": "Tends record created successfully"})

# Read - Get a record from the "tends" table by worker_id
@app.route('/tends/<int:worker_id>', methods=['GET'])
def get_tends(worker_id):
    query = "SELECT * FROM tends WHERE worker_id = %s"
    values = (worker_id,)
    mycursor.execute(query, values)
    tends_records = mycursor.fetchall()
    if tends_records:
        tends_list = []
        for record in tends_records:
            tends_data = {
                "worker_id": record[0],
                "plant_id": record[1]
                # Include other fields if needed
            }
            tends_list.append(tends_data)
        return jsonify(tends_list)
    else:
        return jsonify({"message": "No tends records found for this worker_id"}), 404

# Update - Modify a record in the "tends" table
@app.route('/tends/<int:worker_id>/<int:plant_id>', methods=['PUT'])
def update_tends(worker_id, plant_id):
    data = request.get_json()
    query = "UPDATE tends SET plant_id = %s WHERE worker_id = %s"
    values = (data['new_plant_id'], worker_id)
    mycursor.execute(query, values)
    mydb.commit()
    return jsonify({"message": "Tends record updated successfully"})

# Delete - Remove a record from the "tends" table
@app.route('/tends/<int:worker_id>/<int:plant_id>', methods=['DELETE'])
def delete_tends(worker_id, plant_id):
    query = "DELETE FROM tends WHERE worker_id = %s AND plant_id = %s"
    values = (worker_id, plant_id)
    mycursor.execute(query, values)
    mydb.commit()
    return jsonify({"message": "Tends record deleted successfully"})

#11 user table API 
# Create
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    query = "INSERT INTO User (email, password) VALUES (%s, %s)"
    values = (data['email'], data['password'])
    mycursor.execute(query, values)
    mydb.commit()
    return jsonify({"message": "User created successfully"})

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

#12 worker table API
# Create for workers table
@app.route('/workers', methods=['POST'])
def create_worker():
    data = request.get_json()
    query = "INSERT INTO Workers (name, proficiency) VALUES (%s, %s)"
    values = (data['name'], data['proficiency'])
    mycursor.execute(query, values)
    mydb.commit()
    return jsonify({"message": "Worker created successfully"})

# Read for workers table
@app.route('/workers/<int:worker_id>', methods=['GET'])
def get_worker(worker_id):
    query = "SELECT * FROM Workers WHERE worker_id = %s"
    values = (worker_id,)
    mycursor.execute(query, values)
    worker = mycursor.fetchone()
    if worker:
        worker_data = {
            "worker_id": worker[0],
            "name": worker[1],
            "proficiency": worker[2]
        }
        return jsonify(worker_data)
    else:
        return jsonify({"message": "Worker not found"}), 404

# Update for workers table
@app.route('/workers/<int:worker_id>', methods=['PUT'])
def update_worker(worker_id):
    data = request.get_json()
    query = "UPDATE Workers SET name = %s, proficiency = %s WHERE worker_id = %s"
    values = (data['name'], data['proficiency'], worker_id)
    mycursor.execute(query, values)
    mydb.commit()
    return jsonify({"message": "Worker updated successfully"})

# Delete for workers table
@app.route('/workers/<int:worker_id>', methods=['DELETE'])
def delete_worker(worker_id):
    query = "DELETE FROM Workers WHERE worker_id = %s"
    values = (worker_id,)
    mycursor.execute(query, values)
    mydb.commit()
    return jsonify({"message": "Worker deleted successfully"})

if __name__ == '__main__':
    app.run(debug=True)
