from flask import Flask
from flask import jsonify
import sqlite3

app = Flask(__name__)

# Function to fetch books from the database
def get_books_from_database():
    conn = sqlite3.connect('ansh')
    print(conn)  
    cursor = conn.cursor()
    print(cursor)
    cursor.execute("SELECT * FROM user_book")
    books = cursor.fetchall()
    print(books)
    conn.close()
    return books

@app.route('/books', methods=['GET'])
def get_books():
    books = get_books_from_database()
    books_list = []
    print (books_list)
    print(books)
    for book in books:
        book_dict = {
            "id": book[0],
            "title": book[1],
            "author": book[2],
            "price": book[3],
            "quantity_available": book[4],
            "created_at": book[5]
        }
        books_list.append(book_dict)
        print (books_list)
    return jsonify(books_list)

if __name__ == '__main__':
    app.run(debug=True)
