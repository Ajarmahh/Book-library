from flask import Flask, render_template, request, redirect, url_for
from data_models import Author, Book, db
import os
import requests
from sqlalchemy import or_

# Initialize the Flask application
app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))  # Determine the base directory of the current file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data/library.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)  # Initialize the SQLAlchemy object with the Flask app


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    """
    Handles POST requests to retrieve author details from the form and save them.
    On success, it renders the form with a success message; on error, it rolls back
    the transaction and shows a failure message. For GET requests, it renders the form
    without any messages.
    """
    if request.method == 'POST':
        print('A POST request is processing')

        # Retrieve form data
        name = request.form.get('name')
        birth_date = request.form.get('birthdate')
        date_of_death = request.form.get('date_of_death')

        try:
            # Add the new author to the database
            new_author = Author(name=name, birth_date=birth_date, date_of_death=date_of_death)
            db.session.add(new_author)
            db.session.commit()

            message = "Author added successfully!"
            return render_template('add_author.html', success_message=message)
        except Exception as e:
            print(f"Error adding author: {e}")
            db.session.rollback()  # Rollback if there's an error
            message = "Failed to add author."
            return render_template('add_author.html', failed_message=message)

    # For GET requests
    return render_template('add_author.html')


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    """
    Basically this function will do the same thing as adding author function
    """
    # Fetching all the authors for the dropdown list
    authors = Author.query.all()

    if request.method == 'POST':
        title = request.form.get('title')
        isbn = request.form['isbn']  # The request here will access the phone to fetch the isbn number
        publication_year = request.form.get('publication_year')
        author_id = request.form.get('author')

        try:
            new_book = Book(title=title, isbn=isbn, publication_year=publication_year, author_id=author_id)
            db.session.add(new_book)
            db.session.commit()

            message = "Book added Successfully"
            return render_template('add_book.html', success_message=message, authors=authors)
        except Exception as e:
            print(f"Error adding book: {e}")
            db.session.rollback()
            message = 'Failed to add book'
            return render_template('add_book.html', failed_message=message, authors=authors)
    return render_template('add_book.html', authors=authors)


def fetch_cover_image(isbn):
    """
    Fetch cover image URL using Open Library API.
    """
    if isbn:
        url = f"https://covers.openlibrary.org/b/isbn/{isbn}.jpg"  # Use the isbn directly from the database
        response = requests.get(url)
        if response.status_code == 200:
            return url


@app.route('/', methods=['GET'])
def home_page():
    # Get the sorting parameter from the query string
    sort_by = request.args.get('sort_by', 'title')

    # Start a query with a join between Book and Author
    query = db.session.query(Book).join(Author)

    # Fetch books and join with authors
    if sort_by == 'author':
        query = query.order_by(Author.name)
    else:
        query = query.order_by(Book.title)

    search = request.args.get('search', '')

    if search:
        # Using the query to search based on title or author
        search_pattern = f"%{search}%"
        query = query.filter(or_(
            Book.title.like(search_pattern),
            Author.name.like(search_pattern)
        ))

    # querying all while applying the search/sort filter
    books = query.all()
    books_data = []
    for book in books:
        # Fetch the author based on author_id
        author = Author.query.get(book.author_id)
        author_name = author.name
        books_data.append({
            "id": book.id,
            "title": book.title,
            "author": author_name,
            "cover_image": fetch_cover_image(book.isbn)
        })

    return render_template('home.html', books=books_data, sort_by=sort_by)


@app.route('/book/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    book = Book.query.get(book_id)

    # this will save the book's author
    author_id = book.author_id

    db.session.delete(book)
    db.session.commit()

    # Check if the author has any other books
    remaining_books = Book.query.filter_by(author_id=author_id).count()
    if remaining_books == 0:
        """
        Checks if the author_id count in the books table is 0,
        then delete the author from the authors table as well.
        """
        author = Author.query.get(author_id)  # Primary key in Author table is 'id'
        if author:
            db.session.delete(author)
            db.session.commit()
    print(f'the book: {book.title} has been successfully deleted.')

    return redirect(url_for('home_page'))


# Creating the tables
# with app.app_context():
#     db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
