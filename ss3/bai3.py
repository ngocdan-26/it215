from fastapi import FastAPI
app = FastAPI()

books = [
    {
        "id": 1,
        "title": "Python Basic",
        "author": "Nguyen Van A",
        "category": "programming",
        "year": 2022,
        "is_available": True
    },
    {
        "id": 2,
        "title": "Web API Design",
        "author": "Tran Van B",
        "category": "web",
        "year": 2021,
        "is_available": False
    },
    {
        "id": 3,
        "title": "Database System",
        "author": "Le Van C",
        "category": "database",
        "year": 2020,
        "is_available": True
    },
    {
        "id": 4,
        "title": "Clean Code",
        "author": "Robert Martin",
        "category": "programming",
        "year": 2008,
        "is_available": False
    },
    {
        "id": 5,
        "title": "Computer Network",
        "author": "Vu Van D",
        "category": "network",
        "year": 2019,
        "is_available": True
    },
    {
        "id": 6,
        "title": "FastAPI Basic",
        "author": "Nguyen Van A",
        "category": "web",
        "year": 2023,
        "is_available": True
    }
]

@app.get("/health")
def health():
    return {"message": "Library API is running"}

@app.get("/books")
def get_books():
    return books

@app.get("/books/statistics")
def statistics():
    total_books = 0
    available_books = 0
    borrowed_books = 0
    for book in books:
        total_books += 1
        if book["is_available"] == True:
            available_books += 1
        else:
            borrowed_books += 1
    book = {
        "total_books" : total_books,
        "available_books" : available_books,
        "borrowed_books" : borrowed_books
    }
    return book

@app.get("/books/categories")
def categiries():
    resust = []
    for book in books:
        if book["category"] not in resust:
            resust.append(book["category"])
    return {"categories" : resust}

@app.get("/books/latest")
def latest():
    if len(books) == 0:
        return {
            "message": "No books available"
        }
    
    max = books[0]

    for book in books:
        if book["year"] > max["year"]:
            max = book
    return max
           