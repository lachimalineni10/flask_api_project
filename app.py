from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/user', methods=['GET'])
def get_user():
    return jsonify({"id": 1, "name": "Alice", "email": "alice@example.com"})

if __name__ == '__main__':
    app.run(debug=True)

# 📌 Explanation of the Code:

# from flask import Flask → Imports the Flask framework.
# app = Flask(__name__) → Creates a Flask application instance.
# @app.route('/') → Defines a route (/) that returns a simple message.
# def home(): return "Hello, Flask API is running!" → A function that runs when users visit the / endpoint.
# if __name__ == '__main__': → Ensures that the script runs only when executed directly.
# app.run(debug=True) → Runs the Flask application in debug mode (helps in development).