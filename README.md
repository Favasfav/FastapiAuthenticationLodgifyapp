# FastAPI User Authentication

This project demonstrates a simple user authentication system using FastAPI, SQLAlchemy, and PostgreSQL.

## Features

- User signup
- User login with JWT authentication
- Health check endpoint
- CORS setup

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/your-repo.git


Change to the project directory:

bash
Copy code
cd your-repo
Create and activate a virtual environment:

bash
Copy code
python -m venv env
source env/bin/activate  # On Windows, use `env\Scripts\activate`
Install the dependencies:

bash
Copy code
pip install -r requirements.txt
Set up the PostgreSQL database and update the database URL in database.py.

Run the database migrations:

bash
Copy code
alembic upgrade head
Start the FastAPI server:

bash
Copy code
uvicorn main:app --reload




Usage
Access the API documentation at http://127.0.0.1:8000/docs.
Use the /signup endpoint to create a new user.
Use the /login endpoint to authenticate and receive a JWT token.
