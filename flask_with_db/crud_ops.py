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
        print("Connection Successful :)")
except Exception as e:
    print(f"Connection Failed, {e}")

class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(100), nullable= False)
    email = db.Column(db.String(100), nullable = False, unique = True)
    mobile = db.Column(db.String(100),nullable = False, unique = True)
    age = db.Column(db.Integer)

    def __init__(self,name,email,mobile,age):
        self.name = name
        self.email = email
        self.mobile = mobile
        self.age = age
    
    def __repr__(self):
        return f"<name: {self.name}  email:{self.email} mobile{self.mobile}>"
    
    def to_dict(self):
        return {""}
    
with app.app_context():
    db.create_all()

@app.route('/add_or_update_user',methods = ["POST"])
def add_or_update_user():
    data = request.json
    
    if 'id' in data:
        user_id = data['id']
        user = Users.query.get(user_id)
        if not user:
            return jsonify({"error":"User Not Found"}), 404
        
        if 'name' not in data or 'mobile' not in data or 'email' not in data or 'age' not in data:
            user.name = data.get("name",user.name)#If name is provided in the request, update it.
                                                #If name is missing, keep the existing value (user.name).
            user.mobile = data.get("mobile",user.mobile)
            user.email = data.get("email",user.email)
            user.age = data.get("age",user.age)
        else:
            user.name = data["name"]
            user.mobile = data["mobile"]
            user.email = data["email"]
            user.age = data["age"]

        db.session.commit()
        return jsonify({"message":"updated succesfully", "user":{"id":user.id,"name":user.name,"email":user.email,"mobile":user.mobile,"age":user.age}}), 200
    
    if 'name' not in data or 'mobile' not in data or 'email' not in data or 'age' not in data:
        return jsonify({"error":"name, mobile and email required"}), 400
    
    
    user = Users(name = data["name"], email=data["email"], mobile = data["mobile"], age = data["age"])
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "user added", "user":{"id":user.id,"name":user.name,"email":user.email,"mobile":user.mobile,"age":user.age}}), 201

@app.route('/get_all_users', methods=["GET"])
def get_users():
    users = Users.query.all()
    return jsonify({"users":[{"id":user.id,"name":user.name,"email":user.email,"age":user.age,"mobile":user.mobile,"age":user.age} for user in users]})

@app.route('/get_user_by_id', methods=["GET"])
def get_user_by_id():
    user_id = request.args.get('id')
    if not user_id:
        return jsonify({"error": "user id required"}),400
    user = Users.query.get(user_id)
    if not user:
        return jsonify({"error": "user not found"}),404
    return jsonify({"user":{"id":user.id,"name":user.name,"email":user.email,"age":user.age,"mobile":user.mobile,"age":user.age}}),200


if __name__ == "__main__":
    app.run(debug=True)