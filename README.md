# Blog Management System

This is a blog management web application built with Python and Django. It allows users to create, manage, and update blog posts with authentication and user-specific access.

---

## Features

* User authentication (signup, login)
* Create blog posts
* View all blog posts
* Update and edit blog posts
* Delete blog posts
* User-specific blog management (users can manage their own posts)

---

## API Endpoints (if applicable)

| Method | URL          | Description         |
| ------ | ------------ | ------------------- |
| POST   | /register/   | Register a new user |
| POST   | /login/      | Login user          |
| GET    | /blogs/      | List all blog posts |
| POST   | /blogs/      | Create a new blog   |
| PUT    | /blogs/{id}/ | Update a blog       |
| DELETE | /blogs/{id}/ | Delete a blog       |

---

## Technologies Used

* Python
* Django
* SQLite (database)
* Django Authentication System

---

## How to Run Locally

Clone the repository:

```bash
git clone https://github.com/Nishant18-gif/blog_management.git
```

Navigate to the project directory:

```bash
cd blog_management
```

Create and activate a virtual environment:

```bash
python -m venv venv
```

On Windows:

```bash
venv\Scripts\activate
```

On macOS/Linux:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Apply migrations:

```bash
python manage.py migrate
```

Run the development server:

```bash
python manage.py runserver
```

Open your browser and go to:

```
http://127.0.0.1:8000/
```

---

## Notes

* Make sure Python is installed on your system
* Ensure virtual environment is activated before installing dependencies
* Update `.env` file if required

---

## Author

Nishant Pareek

GitHub: https://github.com/Nishant18-gif
