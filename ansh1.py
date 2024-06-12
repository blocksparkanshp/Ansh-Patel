from flask import Flask
from flask import request 
from flask import jsonify 
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
from werkzeug.security import check_password_hash
import jwt

app = Flask(__name__)
CORS(app)

# Database connection parameters
db_host = 'localhost'
db_user = 'root'
db_password = 'Admin@123'
db_name = 'Ansh'

# Secret key for JWT token (replace with your own secret key)
SECRET_KEY = 'your_secret_key'

def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(host=db_host,
                                             database=db_name,
                                             user=db_user,
                                             password=db_password)
        return connection
    except Error as e:
        print("Error while connecting to MySQL", e)
        return connection

@app.route('/login', methods=['POST'])
def login_user():
    try:
        connection = create_connection()
        cursor = connection.cursor()
        print(connection)
        # Get POST data
        data = request.json
        print(data)
        username = data['username']
        password = data['password']

        # Validate input
        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400

        # Check if user exists
        cursor.execute("SELECT id, username, password FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if not user or not check_password_hash(user[2], password):
            return jsonify({"error": "Invalid username or password"}), 401

        # Generate JWT token
        token = jwt.encode({'user_id': user[0], 'username': user[1]}, SECRET_KEY, algorithm='HS256')

        return jsonify({"token": token.decode('UTF-8')}), 200

    except Error as e:
        print("Error while logging in user:", e)
        return jsonify({"error": "Failed to login user"}), 500

    finally:
        if connection:
            cursor.close()
            connection.close()

if __name__ == '__main__':
    app.run(debug=True)
