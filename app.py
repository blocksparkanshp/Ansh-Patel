from flask import Flask
from flask import request 
from flask import jsonify 
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
import jwt
import cursor


app = Flask(__name__)
CORS(app)

# Database connection parameters
db_host = '192.168.0.105'
db_user = 'root'
db_password = 'Admin@123'
db_name = 'ansh'
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

@app.route('/register', methods=['POST'])
def register_user():
    try:
        connection = create_connection()
        cursor = connection.cursor()
        print(connection)
        
        # Get POST data
        data = request.json
        print(data)
        username = data['username']
        email = data['email']
        password = data['password']

        # Validate input
        if not username or not email or not password:
            return jsonify({"error": "All fields are required"}), 400

        # Hash the password
        # hashed_password = generate_password_hash(password)
        # print(hashed_password)
        # Check if user already exists
        cursor.execute("SELECT id FROM user WHERE username = %s OR email = %s", (username, email))
        if cursor.fetchone():
            return jsonify({"error": "User with the provided username or email already exists"}), 409

        # Insert user data into the database
        cursor.execute("INSERT INTO user (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
        connection.commit()

        return jsonify({"message": "User registered successfully"}), 201

    except Error as e:
        print("Error while registering user:", e)
        return jsonify({"error": "Failed to register user"}), 500

    finally:
        if connection:
            cursor.close()
            connection.close()
            
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
        cursor.execute("SELECT id, username, password FROM user WHERE username = %s", (username,))
        user = cursor.fetchone()

        if not user:
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

@app.route('/books', methods=['GET'])
def user_book():
    try:
        connection = create_connection()
        cursor = connection.cursor()
        print(connection)
        
        # Check if user exists
        cursor.execute("SELECT * FROM user_book")
        books = cursor.fetchall()

        if not books:
            return jsonify({"error": "Sorry, No books found. "}), 401

        return jsonify(books), 200

    except Error as e:
        print("Error while fetching Books:", e)
        return jsonify({"error": "Failed to fetch Books"}), 500
    finally:
        if connection:
            cursor.close()
            connection.close()


            
def get_book_details(book_id):
    try:
        connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        cursor = connection.cursor()
        query = ("SELECT * FROM user_book WHERE id = %s")
        cursor.execute("SELECT * FROM user_book")
        book = cursor.fetchone()
        print(book)
      
        return book
    except mysql.connector.Error as e:
        print("Error:", e)
        return None

@app.route('/books/<book_id>', methods=['GET'])
def get_book(book_id):
    books = get_book_details(book_id)
    if books:
        return jsonify(books)
    else:
        return jsonify({'error': 'Book not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
