from flask import Flask,jsonify,request

app = Flask(__name__)
# In-memory database (for now)
users = {}
@app.route('/user',methods=['GET'])
def get_user():
    user_id = request.args.get('id')
    if int(user_id) in users:
        return jsonify(users[int(user_id)])
    return jsonify({"error":"user not found"}),404

@app.route('/user',methods = ['POST'])
def create_user():
    data = request.json # Get data sent in the request body
    user_id = len(users) + 1
    users[user_id] = {"id":user_id,"name":data['name'],"email":data['email']}
    return jsonify({"message":"user created successfully","user":users[user_id]}),201

if __name__ == "__main__":
    app.run(debug=True)
