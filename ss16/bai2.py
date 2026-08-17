from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base # Giả định Base đã được khai báo từ hệ thống

# 1. Bảng trung gian cho quan hệ Nhiều - Nhiều (Employee - Project)
employee_project = Table(
    "employee_project", 
    Base.metadata,
    Column("employee_id", Integer, ForeignKey("employees.id"), primary_key=True),
    Column("project_id", Integer, ForeignKey("projects.id"), primary_key=True)
)

# 2. Khai báo các Model
class Department(Base):
    __tablename__ = "departments"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    
    # Cấu hình liên kết đến Employee
    # employees = relationship("Employee", back_populates="department_id")
    # Thuộc tính relationship là department, còn department_id chỉ là cột ForeignKey
    # Khi khai báo như hiện tại, SQLAlchemy không thể đồng bộ quan hệ hai chiều giữa Department.employees và Employee.department
    employees = relationship("Employee", back_populates="department")
class Employee(Base):
    __tablename__ = "employees"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    
    # Thiết lập khóa ngoại trỏ về Department
    department_id = Column(Integer, ForeignKey("departments.id"))
    department = relationship("Department", back_populates="employees")
    
    # Quan hệ 1 - 1 với Device
    # device = relationship("Device", back_populates="employee")
    device = relationship("Device",back_populates="employee",uselist=False)
    # Quan hệ N - N với Project
    projects = relationship("Project",secondary=employee_project,back_populates="employees")

class Device(Base):
    __tablename__ = "devices"
    
    id = Column(Integer, primary_key=True, index=True)
    serial_number = Column(String(50), unique=True, nullable=False)
    
    # Khóa ngoại liên kết 1-1 với Employee
    employee_id = Column(Integer,ForeignKey("employees.id"),unique=True)
    employee = relationship("Employee", back_populates="device")

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    
    # Quan hệ N - N với Employee
    employees = relationship("Employee",secondary=employee_project,back_populates="projects")