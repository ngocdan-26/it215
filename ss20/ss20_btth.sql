create database btth_ss20;
use btth_ss20;

CREATE TABLE classrooms (
    id INT AUTO_INCREMENT PRIMARY KEY,
    class_code VARCHAR(50) NOT NULL UNIQUE,
    class_name VARCHAR(100) NOT NULL,
    max_students INT NOT NULL,
    status VARCHAR(50) NOT NULL
);

CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_code VARCHAR(50) NOT NULL UNIQUE,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    age INT,
    gender VARCHAR(20),
    class_id INT,
    CONSTRAINT fk_students_classrooms
        FOREIGN KEY (class_id)
        REFERENCES classrooms(id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE user_profiles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    full_name VARCHAR(100),
    phone VARCHAR(20),
    address VARCHAR(255),
    CONSTRAINT fk_user_profiles_users
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE courses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    course_code VARCHAR(50) NOT NULL UNIQUE,
    course_name VARCHAR(100) NOT NULL,
    credits INT NOT NULL
);

CREATE TABLE enrollments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    course_id INT NOT NULL,
    enrollment_date DATE,
    CONSTRAINT fk_enrollments_students
        FOREIGN KEY (student_id)
        REFERENCES students(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT fk_enrollments_courses
        FOREIGN KEY (course_id)
        REFERENCES courses(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT unique_student_course
        UNIQUE (student_id, course_id)
);
INSERT INTO classrooms
(class_code, class_name, max_students, status)
VALUES
('CNTT01', 'Công nghệ thông tin 01', 40, 'active'),
('CNTT02', 'Công nghệ thông tin 02', 35, 'active');

INSERT INTO students
(student_code, full_name, email, age, gender, class_id)
VALUES
('SV001', 'Nguyen Van An', 'an@gmail.com', 20, 'Nam', 1),
('SV002', 'Tran Thi Binh', 'binh@gmail.com', 21, 'Nu', 1),
('SV003', 'Le Van Cuong', 'cuong@gmail.com', 20, 'Nam', 2);

INSERT INTO users
(username, password, email)
VALUES
('admin', '123456', 'admin@gmail.com'),
('student01', '123456', 'student01@gmail.com');

INSERT INTO user_profiles
(user_id, full_name, phone, address)
VALUES
(1, 'Admin', '0900000001', 'Ha Noi'),
(2, 'Nguyen Van An', '0900000002', 'Ha Noi');

INSERT INTO courses
(course_code, course_name, credits)
VALUES
('CSDL', 'Co so du lieu', 3),
('LTHDT', 'Lap trinh huong doi tuong', 3),
('WEB', 'Lap trinh Web', 4);

INSERT INTO enrollments
(student_id, course_id, enrollment_date)
VALUES
(1, 1, '2026-08-20'),
(1, 2, '2026-08-20'),
(2, 1, '2026-08-20'),
(2, 3, '2026-08-20'),
(3, 2, '2026-08-20');
