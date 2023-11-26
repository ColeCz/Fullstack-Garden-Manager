from flask import Flask, request, jsonify
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

if __name__ == '__main__':
    app.run(debug=True)
