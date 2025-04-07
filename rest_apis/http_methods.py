from flask import Flask,jsonify,request

app = Flask(__name__)
# In-memory database (for now)
users = {}

@app.route('/user',methods = ['POST'])
def create_user():
    data = request.json # Get data sent in the request body
    if('name' not in data or 'email' not in data):
        return jsonify({"error":"name and email required"}),400
    
    if data['id']:
        user_id = data['id']
        if user_id in users:
            users[user_id] = {"id":user_id,"name":data['name'],"email":data['email']}
            return jsonify({"message":"user updated successfully","user":users[user_id]}),201
        else:
            return jsonify({"message":"user not found"}),422
        
    user_id = len(users) + 1
    users[user_id] = {"id":user_id,"name":data['name'],"email":data['email']}
    return jsonify({"message":"user created successfully","user":users[user_id]}),201

@app.route('/user',methods=['GET'])
def get_user():
    user_id = request.args.get('id')
    if not user_id or int(user_id) not in users:
        return jsonify({"error":"user not found"}),404
    return jsonify(users[int(user_id)])

if __name__ == "__main__":
    app.run(debug=True)
