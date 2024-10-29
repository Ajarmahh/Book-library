from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey

db = SQLAlchemy()


class Author(db.Model):
    """
    Represents an author in the system. This model stores basic information
    about an author, including their name, birth date, and date of death.
    """
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    birth_date = Column(String)
    date_of_death = Column(String)

    def __repr__(self):
        return (f"<Author(name= {self.name}, birth_date= {self.birth_date}, "
                f"date_of_death= {self.date_of_death or 'Still Alive'})>")


class Book(db.Model):
    """
    Represents an author in the system. This model stores basic information
    about an author, including their name, birth date, and date of death.
    """
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True, autoincrement=True)
    isbn = Column(String)
    title = Column(String)
    publication_year = Column(String)
    author_id = Column(Integer, ForeignKey('authors.id'))

    def __repr__(self):
        return (f'Book(id= {self.id}, title= {self.title}, isbn= {self.isbn}, '
                f'publication_year= {self.publication_year}, author_id= {self.author_id}')
