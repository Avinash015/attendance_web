from database import db  # Import db from the new database.py

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    roll_no = db.Column(db.String(50), unique=True, nullable=False)  # This will be the username
    year_of_study = db.Column(db.Integer, nullable=False)
    phone_number = db.Column(db.String(15), unique=True, nullable=False)
    branch = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    password = db.Column(db.String(100), nullable=False)  # Store hashed passwords

    
    # Define a relationship with the Attendance table
    attendances = db.relationship('Attendance', backref='student', lazy=True)


class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(10), nullable=False)  # Present/Absent
