from fastapi import FastAPI

app = FastAPI()

students = [
    {"id": 1, "name": "An"},
    {"id": 2, "name": "Binh"},
    {"id": 3, "name": "Cuong"},
]

# Sửa endpoint thành "/students" dạng số nhiều đúng yêu cầu khách hàng
@app.get("/students")
def get_students():
    # return students[0]
    # Trả về toàn bộ danh sách sinh viên thay vì chỉ trả về students[0]
    return students