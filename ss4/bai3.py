from fastapi import FastAPI
app = FastAPI()

products = [
    {"id": 1, "name": "Laptop", "price": 15000000},
    {"id": 2, "name": "Mouse", "price": 200000},
    {"id": 3, "name": "Keyboard", "price": 500000},
    {"id": 4, "name": "Monitor", "price": 3000000}
]

@app.get("/products")
def get_student(keyword:str = None, max_price:float = None):
    if not keyword and not max_price:
        return products
    if keyword:
        resust =[]
        for product in products:
            if product["name"] == keyword.lower().title():
                resust.append(product)
        if not resust:
            return {
                "messege":f"kh co du lieu co ten {keyword}"
            }
        return resust
    if max_price:
        resust=[]
        if max_price <= 0:
            return {"detail": "max_price không được âm" }
        for product in products:
            if product["price"] <= max_price:
                resust.append(product)
        if not resust:
            return {
                "messege":f"kh cos sp gia duoi {max_price}"
            }
        return resust
            
        