"""
Phần 1: Phân tích và đề xuất đa giải pháp cấu hình

6.1. Phân tích truy xuất quan hệ
1. Vai trò của ForeignKey trong quan hệ N-N
Quan hệ giữa Student và Course là quan hệ Nhiều - Nhiều:
- Một sinh viên có thể đăng ký nhiều khóa học.
- Một khóa học có thể có nhiều sinh viên.
Trong cơ sở dữ liệu quan hệ, không đặt trực tiếp ForeignKey giữa Student và Course, mà phải tạo bảng trung gian Enrollment.
-> Vì Enrollment là bảng trung gian đại diện cho từng lần đăng ký.

2. back_populates không cần giống tên bảng
Nó phải trùng với tên thuộc tính relationship() ở Model đối diện.

6.2. Đề xuất hai giải pháp cấu hình Model
Giải pháp 1: Sử dụng secondary

Đây là cách cấu hình trực tiếp quan hệ N-N.
Ta vẫn có bảng vật lý:enrollments
với: student_id,course_id
Sau đó khai báo:
phía Student:
courses = relationship(
    "Course",
    secondary="enrollments",
    back_populates="students"
)
Phía Course:
students = relationship(
    "Student",
    secondary="enrollments",
    back_populates="courses"
)
Khi đó có thể truy cập trực tiếp:course.students
hoặc: student.courses
Nếu không có sinh viên nào đăng ký: course.students
sẽ trả về: []

Giải pháp 2: Hai quan hệ 1-N song song

Không sử dụng secondary.
Ta chỉ thiết lập quan hệ giữa:
Student → Enrollment
Course  → Enrollment
Trong Enrollment:
student = relationship(
    "Student",
    back_populates="enrollments"
)
course = relationship(
    "Course",
    back_populates="enrollments"
)

Khi cần lấy sinh viên của một khóa học:
students = [
    enrollment.student
    for enrollment in course.enrollments
]
-> Cách này rõ ràng hơn về mặt cấu trúc bảng trung gian, nhưng code truy xuất dài hơn.

Phần 2: So sánh và lựa chọn cấu hình
6.3. Lập bảng so sánh
Sinh viên hoàn thành bảng so sánh dưới đây để đánh giá sự đánh đổi giữa 2 giải pháp cấu hình:

| Tiêu chí                                          | Giải pháp 1: `secondary`            | Giải pháp 2: Hai quan hệ 1-N                             |
| ------------------------------------------------- | ----------------------------------- | -------------------------------------------------------- |
| Độ ngắn gọn của code                              | **Ngắn gọn hơn**                    | Dài hơn                                                  |
| Lấy sinh viên của Course                          | `course.students`                   | `course.enrollments` rồi duyệt từng `enrollment.student` |
| Lấy Course của Student                            | `student.courses`                   | `student.enrollments` rồi duyệt từng `enrollment.course` |
| Độ dễ sử dụng                                     | **Dễ sử dụng**                      | Phải hiểu Enrollment                                     |
| Độ dễ hiểu với người mới                          | Ban đầu hơi khó hiểu do `secondary` | Dễ hình dung quan hệ 1-N                                 |
| Truy cập trực tiếp N-N                            | **Có**                              | Không                                                    |
| Phù hợp với quan hệ N-N đơn giản                  | **Rất phù hợp**                     | Phù hợp                                                  |
| Khi bảng Enrollment có nhiều thuộc tính nghiệp vụ | Hạn chế hơn                         | **Linh hoạt hơn**                                        |

Giải pháp 1 sử dụng secondary.
Thay vì:
students = [
    enrollment.student
    for enrollment in course.enrollments
]
chỉ cần: course.students
Giải pháp nào được khuyến khích trong bài học về quan hệ N-N?
Với quan hệ N-N thông thường, trong đó bảng trung gian chủ yếu dùng để liên kết hai bảng, giải pháp secondary là lựa chọn phù hợp và thường được khuyến khích.
Nó thể hiện trực tiếp trong ORM rằng:
Student N ←→ N Course
             │
             └── Enrollment

6.4. Lựa chọn giải pháp
lựa chọn Giải pháp 1 - sử dụng secondary.
Lý do : 
- giải pháp này cho phép truy cập trực tiếp đối tượng liên quan: course.students,student.courses
- code ngắn gọn hơn so với việc phải truy cập Enrollment rồi sử dụng vòng lặp
- secondary phù hợp với bài toán hiện tại vì yêu cầu chủ yếu là quản lý mối quan hệ đăng ký giữa Student và Course

Phần 3: Thiết kế và triển khai source code model

6.5. Thiết kế các bước thực hiện
Bước 1: Khai báo Base
Bước 2: Khai báo Model Student
Bước 3: Khai báo Model Course
Bước 4: Tạo bảng trung gian Enrollment
Bước 5: Khai báo quan hệ Enrollment
Bước 6: Khai báo quan hệ N-N
Bước 7: Kiểm tra truy xuất
"""

# 6.6. Yêu cầu source code Model (models.py)
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer,primary_key=True,index=True)
    student_id = Column(Integer,ForeignKey("students.id"),nullable=False)
    course_id = Column(Integer,ForeignKey("courses.id"),nullable=False)
    student = relationship("Student",back_populates="enrollments")
    course = relationship( "Course",back_populates="enrollments")

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer,primary_key=True,index=True)
    full_name = Column(String(100),nullable=False)
    email = Column(String(100),nullable=False,unique=True)
    enrollments = relationship("Enrollment",back_populates="student")
    courses = relationship("Course",secondary="enrollments",back_populates="students",viewonly=True)

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer,primary_key=True,index=True)
    name = Column(String(100),nullable=False)
    enrollments = relationship("Enrollment",back_populates="course")
    students = relationship("Student",secondary="enrollments",back_populates="courses",viewonly=True)
