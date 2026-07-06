from fastapi import FastAPI

app = FastAPI()

students = ["An", "Binh", "Cuong"]

@app.get("/getStudents")
def get_students():
    # return "Danh sach sinh vien: " + str(students)
    # Trả về trực tiếp list, FastAPI sẽ tự động convert sang JSON Array
    return students