# 📚 Book Library - Digital Book Management System

Welcome to the **Book Library Project**! This is a digital book management platform where users can add, search, and manage books, integrating an ISBN-based cover retrieval system.  

## 🚀 Features  
- 🔍 **Book Search & Management** – Add, delete, and update book records effortlessly.  
- 📄 **ISBN-Based Cover Retrieval** – Automatically fetch book covers and metadata for better user experience.  
- 🔐 **Database Integration** – Store book and author data securely using SQLAlchemy ORM.  
- ⚡ **Fast & Efficient** – Optimized queries for quick book retrieval.  
- 🌍 **RESTful API** – Enables easy frontend integration.  

## 🛠️ Tech Stack  
- **Backend Framework:** Flask (Python)  
- **Database:** SQLite + SQLAlchemy ORM  
- **API Integration:** Open-source book APIs  
- **Deployment:** Docker (Optional)  

## 🛋️ Installation & Setup  

1️⃣ **Clone the Repository**  
```bash
git clone https://github.com/Ajarmahh/Book-library.git
cd Book-library
```

2️⃣ **Create a Virtual Environment & Install Dependencies**  
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

3️⃣ **Run the Application**  
```bash
python app.py
```

4️⃣ **Test the API**  
Use **Postman** or **cURL** to interact with the API and test endpoints.

## 🔗 API Endpoints  

| Method | Endpoint               | Description                          |
|--------|------------------------|---------------------------------     |
| GET    | `/books`               | Fetch all books                      |
| POST   | `/books`               | Add a new book                       |
| GET    | `/books/<id>`          | Fetch a single book by ID            |
| PUT    | `/books/<id>`          | Update a book                        |
| DELETE | `/books/<id>`          | Delete a book                        |
| GET    | `/authors`             | Fetch all authors                    |
           |











Message Stefka









