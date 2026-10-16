# Student Management System

A web-based Student Management System built using Python and Django to manage student records and attendance.

## Features

- Student record management
- Create, view, update, and delete student records (CRUD)
- Student attendance management
- Dashboard for viewing student-related information
- Database integration using Django ORM
- HTML and CSS-based user interface

## Technologies Used

- **Backend:** Python, Django
- **Frontend:** HTML, CSS, JavaScript
- **Database:** Configure the database used by your project (SQLite or MySQL)
- **Version Control:** Git and GitHub

## Getting Started

Follow these steps to run the project locally.

### 1. Clone the Repository

```bash
git clone https://github.com/shalugupta-dev/student-management.git
cd student-management
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
.\venv\Scripts\Activate
```

### 3. Install Dependencies

If the project contains a `requirements.txt` file, run:

```bash
pip install -r requirements.txt
```

Otherwise, install Django in the activated environment:

```bash
pip install django
```

Install any other dependencies required by the project.

### 4. Apply Database Migrations

```bash
python manage.py migrate
```

### 5. Run the Development Server

```bash
python manage.py runserver
```

Open the local development address shown in the terminal, usually http://127.0.0.1:8000/.

## Project Structure

The project contains Django application files, templates, static assets, and configuration files. The exact structure depends on the repository.

## Future Improvements

- Improve form validation and error handling
- Add automated tests
- Improve responsive design
- Add further reporting and dashboard features

## Author

**Shalu Gupta**

- GitHub: https://github.com/shalugupta-dev
- LinkedIn: https://www.linkedin.com/in/shalu-gupta76

## Note

This project was developed for learning and demonstrating web application development with Python and Django.