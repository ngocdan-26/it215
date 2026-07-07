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
    }
]

@app.get("/health")
def health():
    return {"message": "Library API is running"}

@app.get("/books")
def get_books():
    return books

@app.get("/books/available")
def available():
    result = []
    for book in books:
        if book["is_available"] == True:
            result.append(book)
    return result

@app.get("/books/borrowed")
def borrowed():
    result = []
    for book in books:
        if book["is_available"] == False:
            result.append(book)
    return result