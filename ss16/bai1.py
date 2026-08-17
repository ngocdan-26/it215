from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base # Giả định Base đã được khai báo từ hệ thống

# 1. Bảng trung gian cho quan hệ Nhiều - Nhiều (Student - Course)
student_course = Table(
    "student_course", 
    Base.metadata,
    Column("student_id", Integer, ForeignKey("students.id"), primary_key=True),
    Column("course_id", Integer, ForeignKey("courses.id"), primary_key=True)
)

# 2. Khai báo các Model
class Department(Base):
    __tablename__ = "departments"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    # Cấu hình liên kết đến Student
    # students = relationship("Student", back_populates="department_id") 
    # Thuộc tính relationship là department, không phải department_id.
    # SQLAlchemy sẽ không thể đồng bộ hai chiều giữa Department.students và Student.department.
    students = relationship("Student", back_populates="department")

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    # Thiết lập khóa ngoại trỏ về Department
    department_id = Column(Integer, ForeignKey("departments.id"))
    # department = relationship("Department", back_populates="students")
    student_id = Column(Integer, ForeignKey("students.id"))
    # Quan hệ 1 - 1 với Profile
    # profile = relationship("Profile", back_populates="student")
    # Một Student có thể có nhiều Profile, Cột student_id không có ràng buộc unique=True, Relationship không khai báo uselist=False.
    profile = relationship("Profile",back_populates="student",uselist=False)
    # Quan hệ N - N với Course
    courses = relationship("Course", back_populates="students")

class Profile(Base):
    __tablename__ = "profiles"
    id = Column(Integer, primary_key=True, index=True)
    bio = Column(String(255))
    # Khóa ngoại liên kết 1-1 với Student
    student_id = Column(Integer, ForeignKey("students.id"))
    student = relationship("Student", back_populates="profile")

class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    # Quan hệ N - N với Student
    students = relationship("Student", back_populates="courses")