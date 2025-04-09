from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost:5432/flask_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

try:
    with app.app_context():
        db.session.execute(text("SELECT 1"))
        print("Connection Successful")
except Exception as e:
    print(f"Connection Failed, {e}")

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key =True)
    username = db.Column(db.String(100),nullable = False)
    posts = db.relationship('Post', backref = 'user',lazy = True)

class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer,primary_key =True)
    title = db.Column(db.String(100),nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable =False)

with app.app_context():
    db.create_all()

@app.route('/create_user',methods = ['POST'])
def create_user():
    try:
        data = request.json
        if not data or not 'username' in data:
            return jsonify({"error":"username required"}), 400
        if data['username'] == "":
            return jsonify({"error":"username should not be empty"}), 400
        user = User(username = data['username'])
        db.session.add(user)
        db.session.commit()
        return jsonify({"message":f"User {data['username']} added successfully"}),201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error":f"User {e}"})

@app.route('/retrieve_users', methods = ['GET'])
def retrieve_users():
    users = User.query.all()
    

if __name__ == '__main__':
    app.run(debug=True)
