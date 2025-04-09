from flask import Flask,jsonify,request
from sqlalchemy import text
from models import db,Users
import pandas as pd
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost:5432/flask_db'
app.config['UPLOAD_FOLDER'] = 'C:\Flask\flask_with_db\excel\uploads'

db.init_app(app)

try:
    with app.app_context():
        db.session.execute(text("SELECT 1"))
        print("Connection Successful :)")
except Exception as e:
    print(f"Connection Failed, {e}")

with app.app_context():
    db.create_all()


@app.route('/upload_users', methods = ['POST'])
def upload_users():
    if 'excel_file' not in request.files:
        return jsonify({"error": "No file part"}),400
    file = request.files['excel_file']  
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    response = {}
    if file and file.filename.endswith('.xlsx'):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'],file.filename)
        file.save(filepath)

        success_count, reject_count,row_number = 0
        reject_reason = ""
        df = pd.read_excel(filepath)
        for row in df.iterrows():
            row_number += 1
            try:
                user = Users(username = row['username'], mobilenumber = row['mobilenumber'], email = row['email'], address = row['address'])
                db.session.add(user)
                db.commit()
                success_count += 1
            except Exception as e:
                db.rollback()
                reject_count += 1
                response['row_number'] = row_number
                response['rejected _reason'] = e
        response

    return request.files

if __name__ == '__main__':
    app.run(debug=True)