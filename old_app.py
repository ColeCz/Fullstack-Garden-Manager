#!/usr/bin/env python
# coding: utf-8

# In[1]:


# pip install mysql-connector-python


# In[3]:


from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import mysql.connector
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from flask import render_template, request, redirect, url_for
#from flask_login import login_user, current_user, login_required, logout_user


# In[4]:


db_config = {
    "host": "localhost",
    "user": "root",
    "password": "Wilcome88111710348",
    "database": "garden_management_system",
}

# Establish a database connection
try:
    connection = mysql.connector.connect(**db_config)

    if connection.is_connected():
        print("Connected to the MySQL database")
    else:
        print("Connection failed")

except mysql.connector.Error as err:
    print(f"Error: {err}")

# # Close the database connection when done
# finally:
#     if 'connection' in locals():
#         connection.close()
#         print("Connection closed")


# In[2]:




Base = declarative_base()

# Define the User model
class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)

    # Relationships
    gardens = relationship('Garden', back_populates='operator')
    owned_plants = relationship('Plant', back_populates='owner')
    employed_workers = relationship('Worker', secondary='employs', back_populates='employers')

# Define the Plants model
class Plant(Base):
    __tablename__ = 'plants'

    plant_id = Column(Integer, primary_key=True)
    stage = Column(String(50))
    health = Column(String(50))
    name = Column(String(255), nullable=False)
    type = Column(String(50))

    # Relationships
    owner_id = Column(Integer, ForeignKey('users.user_id'))
    owner = relationship('User', back_populates='owned_plants')

# Define the Workers model
class Worker(Base):
    __tablename__ = 'workers'

    worker_id = Column(Integer, primary_key=True)
    proficiency = Column(String(50))
    name = Column(String(255), nullable=False)

    # Relationships
    employers = relationship('User', secondary='employs', back_populates='employed_workers')

# Define the Gardens model
class Garden(Base):
    __tablename__ = 'gardens'

    garden_id = Column(Integer, primary_key=True)
    location = Column(String(255))
    size = Column(Integer)
    capacity = Column(Integer)
    soil = Column(String(255))

    # Relationships
    operator_id = Column(Integer, ForeignKey('users.user_id'))
    operator = relationship('User', back_populates='gardens')
    plants = relationship('Plant', secondary='contains', back_populates='gardens')
    workers = relationship('Worker', secondary='gardens_relationship', back_populates='gardens')

# Define the Many-to-Many relationship table 'employs'
employs = Table('employs', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.user_id')),
    Column('worker_id', Integer, ForeignKey('workers.worker_id'))
)

# Define the Many-to-Many relationship table 'contains'
contains = Table('contains', Base.metadata,
    Column('garden_id', Integer, ForeignKey('gardens.garden_id')),
    Column('plant_id', Integer, ForeignKey('plants.plant_id'))
)

# Define the Many-to-Many relationship table 'gardens_relationship'
gardens_relationship = Table('gardens_relationship', Base.metadata,
    Column('garden_id', Integer, ForeignKey('gardens.garden_id')),
    Column('worker_id', Integer, ForeignKey('workers.worker_id'))
)


# In[6]:




# Create a database connection
engine = create_engine('mysql+mysqlconnector://username:password@localhost/database')
Session = sessionmaker(bind=engine)
session = Session()



# In[7]:


#User Class CRUD Operations 

# Create a new user
def create_user(email, password):
    user = User(email=email, password=password)
    session.add(user)
    session.commit()
    return user

# Retrieve a user by ID
def get_user_by_id(user_id):
    return session.query(User).filter_by(user_id=user_id).first()

# Retrieve a user by email
def get_user_by_email(email):
    return session.query(User).filter_by(email=email).first()

# Update user information
def update_user(user_id, new_email, new_password):
    user = session.query(User).filter_by(user_id=user_id).first()
    if user:
        user.email = new_email
        user.password = new_password
        session.commit()
        return True
    return False

# Delete a user
def delete_user(user_id):
    user = session.query(User).filter_by(user_id=user_id).first()
    if user:
        session.delete(user)
        session.commit()
        return True
    return False


# In[ ]:





# In[8]:


#Plant Class CRUD Operations

# Create a new plant
def create_plant(stage, health, name, type, owner_id):
    plant = Plant(stage=stage, health=health, name=name, type=type, owner_id=owner_id)
    session.add(plant)
    session.commit()
    return plant

# Retrieve a plant by ID
def get_plant_by_id(plant_id):
    return session.query(Plant).filter_by(plant_id=plant_id).first()

# Update plant information
def update_plant(plant_id, new_stage, new_health, new_name, new_type):
    plant = session.query(Plant).filter_by(plant_id=plant_id).first()
    if plant:
        plant.stage = new_stage
        plant.health = new_health
        plant.name = new_name
        plant.type = new_type
        session.commit()
        return True
    return False

# Delete a plant
def delete_plant(plant_id):
    plant = session.query(Plant).filter_by(plant_id=plant_id).first()
    if plant:
        session.delete(plant)
        session.commit()
        return True
    return False


# In[9]:


#Worker Class CRUD Operations

# Create a new worker
def create_worker(proficiency, name):
    worker = Worker(proficiency=proficiency, name=name)
    session.add(worker)
    session.commit()
    return worker

# Retrieve a worker by ID
def get_worker_by_id(worker_id):
    return session.query(Worker).filter_by(worker_id=worker_id).first()

# Update worker information
def update_worker(worker_id, new_proficiency, new_name):
    worker = session.query(Worker).filter_by(worker_id=worker_id).first()
    if worker:
        worker.proficiency = new_proficiency
        worker.name = new_name
        session.commit()
        return True
    return False

# Delete a worker
def delete_worker(worker_id):
    worker = session.query(Worker).filter_by(worker_id=worker_id).first()
    if worker:
        session.delete(worker)
        session.commit()
        return True
    return False


# In[ ]:


#Garden Class CRUD Operations

# Create a new garden
def create_garden(location, size, capacity, soil, operator_id):
    garden = Garden(location=location, size=size, capacity=capacity, soil=soil, operator_id=operator_id)
    session.add(garden)
    session.commit()
    return garden

# Retrieve a garden by ID
def get_garden_by_id(garden_id):
    return session.query(Garden).filter_by(garden_id=garden_id).first()

# Update garden information
def update_garden(garden_id, new_location, new_size, new_capacity, new_soil):
    garden = session.query(Garden).filter_by(garden_id=garden_id).first()
    if garden:
        garden.location = new_location
        garden.size = new_size
        garden.capacity = new_capacity
        garden.soil = new_soil
        session.commit()
        return True
    return False

# Delete a garden
def delete_garden(garden_id):
    garden = session.query(Garden).filter_by(garden_id=garden_id).first()
    if garden:
        session.delete(garden)
        session.commit()
        return True
    return False


# User Authentication with Flask-Login:

# In[8]:


# pip install flask-login


# In[5]:


# pip show flask


# In[13]:


#Configure Flask-Login:

from flask import Flask
# from flask_login import LoginManager

app = Flask(__name__)
# login_manager = LoginManager(app)
# login_manager.login_view = 'login'  # Set the login view route


# In[21]:


#User Login:
#Create a login route where users can submit their credentials (email and password).
#If valid, log the user in using Flask-Login:

app.run(host='0.0.0.0', port=81, debug=True)


@app.route('/login', methods=['GET', 'POST'])
def login():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']
#         user = User.query.filter_by(email=email).first()
#         if user and user.password == password:
#             login_user(user)
#             return redirect(url_for('dashboard'))
    print("ihihihi")
    #return render_template('GMS HTML Structure.html')

print("hi")
input()

# In[22]:


# get_ipython().run_line_magic('tb', '')


# In[ ]:


# User Registration:

# Create a registration route where users can provide their email and password.
# Create a new user and add them to the database:
'''
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('GMS HTML Structure.html')


# In[ ]:


# User Logout:

# Create a logout route to log the user out:

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# User Authorization with Roles and Permissions:

# To implement authorization with roles and permissions, you can add a role attribute to your User model, and based on the user's role, you can restrict access to certain routes or actions in your application.
# In[ ]:


# To add a role attribute to your User model, you can modify the existing model definition as follows:

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from flask_login import UserMixin  # Import UserMixin for Flask-Login integration

Base = declarative_base()

class User(Base, UserMixin):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False, default='user')  # Added 'role' attribute with default value 'user'

    # Relationships (if needed)
    gardens = relationship('Garden', back_populates='operator')
    owned_plants = relationship('Plant', back_populates='owner')
    employed_workers = relationship('Worker', secondary='employs', back_populates='employers')

    def __init__(self, email, password, role='user'):
        self.email = email
        self.password = password
        self.role = role  # Assign the 'role' attribute during user creation


# In[ ]:


# With this role attribute, you can assign roles to users when they are created. 

# Creating an admin user
admin_user = User(email='admin@example.com', password='adminpassword', role='admin')

# Creating a regular user (role defaults to 'user')
regular_user = User(email='user@example.com', password='userpassword')

# Creating a worker user
worker_user = User(email='worker@example.com', password='workerpassword', role='worker')

# Adding users to the database
db.session.add(admin_user)
db.session.add(regular_user)
db.session.add(worker_user)
db.session.commit()


# In[ ]:


# In your routes and views, check the user's role before allowing them to perform certain actions.

from functools import wraps
from flask import abort
from flask_login import current_user

# Custom decorator to check for 'admin' role
def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.role != 'admin':
            abort(403)  # Forbidden
        return func(*args, **kwargs)
    return decorated_view

# Custom decorator to check for 'user' role
def user_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.role != 'user':
            abort(403)  # Forbidden
        return func(*args, **kwargs)
    return decorated_view

# Custom decorator to check for 'worker' role
def worker_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.role != 'worker':
            abort(403)  # Forbidden
        return func(*args, **kwargs)
    return decorated_view

# Example route protected by roles
@app.route('/admin_dashboard')
@login_required
@admin_required
def admin_dashboard():
    # Only users with 'admin' role can access this route
    return render_template('admin_dashboard.html')

@app.route('/user_profile')
@login_required
@user_required
def user_profile():
    # Only users with 'user' role can access this route
    return render_template('user_profile.html')

@app.route('/worker_dashboard')
@login_required
@worker_required
def worker_dashboard():
    # Only users with 'worker' role can access this route
    return render_template('worker_dashboard.html')'''

