from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, RadioField, SubmitField
from wtforms.validators import DataRequired
from werkzeug.security import generate_password_hash, check_password_hash
from models import Student, Attendance
from database import db  # Import db from the new database.py
import os
from dotenv import load_dotenv  # Import to load environment variables from .env file

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Application Configurations
app.secret_key = os.environ.get('SECRET_KEY', 'your_default_secret_key')  
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')  # Get the database URL from environment variable
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the Database
db.init_app(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Redirect to login if unauthorized

# Define a simple user model using Flask-Login
class Admin(UserMixin):
    def __init__(self, username):
        self.username = username

    def get_id(self):
        return self.username  # Unique identifier

# Load admin user
@login_manager.user_loader
def load_user(username):
    return Admin(username)

# Flask-WTF Forms
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class AttendanceForm(FlaskForm):
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    attendance = RadioField('Attendance', choices=[('Present', 'Present'), ('Absent', 'Absent')])
    submit = SubmitField('Submit Attendance')

class StudentUser(UserMixin):
    def __init__(self, roll_no):
        self.roll_no = roll_no

    def get_id(self):
        return self.roll_no

# Home Page
@app.route('/')
def index():
    return render_template('index.html')

# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # Static admin credentials for demo purposes
        if username == 'admin' and check_password_hash(generate_password_hash('adminpassword'), password):
            user = Admin(username)
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid credentials')
    return render_template('login.html', form=form)

# Dashboard (Protected Page)
@app.route('/dashboard')
@login_required
def dashboard():
    students = Student.query.all()  # Fetch all students from the database
    return render_template('dashboard.html', students=students)

# View students
@app.route('/students')
@login_required
def students():
    students = Student.query.all()  # Fetch all students
    return render_template('students.html', students=students)

# Student login form
class StudentLoginForm(FlaskForm):
    roll_no = StringField('Roll Number', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

@app.route('/student-login', methods=['GET', 'POST'])
def student_login():
    form = StudentLoginForm()

    if form.validate_on_submit():
        roll_no = form.roll_no.data
        password = form.password.data

        # Fetch the student from the database
        student = Student.query.filter_by(roll_no=roll_no).first()

        if student and check_password_hash(student.password, password):
            # Password is correct, log the user in
            student_user = StudentUser(roll_no)
            login_user(student_user)
            return redirect(url_for('student_dashboard'))
        else:
            flash('Invalid roll number or password', 'danger')
    
    return render_template('student_login.html', form=form)

@app.route('/student-dashboard')
@login_required
def student_dashboard():
    roll_no = current_user.get_id()
    attendances = Attendance.query.filter_by(student_id=Student.query.filter_by(roll_no=roll_no).first().id).all()
    return render_template('student_dashboard.html', attendances=attendances)

@app.route('/attendance/<roll_no>')
@login_required
def view_attendance(roll_no):
    student = Student.query.filter_by(roll_no=roll_no).first()
    attendance_records = Attendance.query.filter_by(student_id=student.id).all() if student else []
    return render_template('attendance.html', student=student, attendance_records=attendance_records)

@app.route('/attendance', methods=['GET'])
@login_required
def student_attendance():
    roll_no = current_user.get_id()
    student = Student.query.filter_by(roll_no=roll_no).first()
    attendance_records = Attendance.query.filter_by(student_id=student.id).all() if student else []
    return render_template('attendance.html', student=student, attendance_records=attendance_records)

# Attendance submission route
@app.route('/mark-attendance', methods=['POST'])
@login_required
def mark_attendance():
    date = request.form.get('date')
    for student in Student.query.all():
        status = request.form.get(f'student_{student.id}')
        if status:
            attendance_record = Attendance(student_id=student.id, date=date, status=status)
            db.session.add(attendance_record)
    db.session.commit()
    flash('Attendance has been recorded successfully!')
    return redirect(url_for('dashboard'))

# Logout Route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Create the database tables if they don't exist
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)
