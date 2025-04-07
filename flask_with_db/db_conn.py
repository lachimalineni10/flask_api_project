from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost:5432/flask_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

try:
    with app.app_context():
        db.session.execute(text('SELECT 1'))
    print("Connection Successful")
except Exception as e:
    print(f"Connection Failed:{e}")

class Users(db.Model): # Inherit from db.Model
    __tablename__ = 'users'  # Table name in PostgreSQL

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(100), nullable = False, unique = True)
    age = db.Column(db.Integer)

    def __init__(self, name,email,age):
        self.name = name
        self.age = age
        self.email = email
    def __repr__(self):
        return f"<User {self.name} - {self.email}>"
    
with app.app_context():
    db.create_all() # Creates all tables in the database

@app.route("/add_user")
def add_user():
    user = Users(name="lachi", email="lachi@gmail.com", age=21)
    db.session.add(user) # Add user to session
    db.session.commit() # Save to database
    return "User Added :)"

@app.route("/get_users")
def get_users():
    users = Users.query.all()
    return {"users":[{"id": u.id, "name":u.name, "email":u.email, "age": u.age} for u in users]}

if __name__ == '__main__':
    app.run(debug=True)