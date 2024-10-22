
# Attendance System

## Overview

This is a web application built with Flask that allows administrators to manage student attendance efficiently. The application includes user authentication for both administrators and students, enabling secure access to attendance records and management features.

## Features

- Admin Login: Admins can log in to manage student records and attendance.
- Student Login: Students can log in to view their attendance records.
- Attendance Management: Admins can mark attendance for students.
- Database Integration: Uses PostgreSQL for storing student and attendance data.

## Technologies Used

- Flask: A lightweight WSGI web application framework for Python.
- Flask-Login: Manages user sessions for admin and student logins.
- Flask-WTF: Provides integration with WTForms for form handling.
- SQLAlchemy: An ORM for database management.
- PostgreSQL: A relational database for data storage.

## Installation

### Prerequisites

- Python 3.9 or higher
- PostgreSQL
- Git (for version control)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/Avinash015/attendance_web.git
   cd attendance_web
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure the database:
   - Set up a PostgreSQL database and update the `SQLALCHEMY_DATABASE_URI` in `app.py` with your database credentials.

5. Create the database tables:
   ```bash
   python -c "from app import db; db.create_all()"
   ```

6. Run the application:
   ```bash
   python app.py
   ```

   The application will run on `http://localhost:5000`.

