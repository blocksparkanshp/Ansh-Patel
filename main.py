from flask import Flask, request, jsonify
import jwt
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'


users = [{'username': 'Blockspark', 'password': 'Blockspark12'}]
books = [{'id': 1, 'title': 'Python', 'author': 'Ansh', 'price': 10.99},
         {'id': 2, 'title': 'Java', 'author': 'Parshva', 'price': 12.99}]
cart = []


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token.split()[1], app.config['SECRET_KEY'])
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(*args, **kwargs)

    return decorated


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    users.append({'username': data['username'], 'password': data['password']})
    return jsonify({'message': 'User registered successfully!'})

@app.route('/login', methods=['POST'])
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return jsonify({'message': 'Could not verify!'}), 401

    user = [user for user in users if user['username'] == auth.username and user['password'] == auth.password]

    if user:
        token = jwt.encode({'username': auth.username}, app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('UTF-8')})

    return jsonify({'message': 'Invalid credentials!'}), 401


@app.route('/books', methods=['GET'])
def get_books():
    return jsonify({'books': books})

@app.route('/books/<int:id>', methods=['GET'])
def get_book(id):
    book = [book for book in books if book['id'] == id]
    return jsonify({'book': book[0]}) if book else jsonify({'message': 'Book not found!'}), 404


@app.route('/cart', methods=['GET'])
@token_required
def get_cart():
    return jsonify({'cart': cart})

@app.route('/cart/add/<int:id>', methods=['POST'])
@token_required
def add_to_cart(id):
    book = [book for book in books if book['id'] == id]
    if book:
        cart.append(book[0])
        return jsonify({'message': 'Book added to cart successfully!'})
    return jsonify({'message': 'Book not found!'}), 404

@app.route('/cart/remove/<int:id>', methods=['DELETE'])
@token_required
def remove_from_cart(id):
    book = [book for book in cart if book['id'] == id]
    if book:
        cart.remove(book[0])
        return jsonify({'message': 'Book removed from cart successfully!'})
    return jsonify({'message': 'Book not found in cart!'}), 404

@app.route('/cart/checkout', methods=['POST'])
@token_required
def checkout():
   
    cart.clear()
    return jsonify({'message': 'Order placed successfully!'})

if __name__ == '__main__':
    app.run(debug=True)
