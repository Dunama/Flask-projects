# signin_signout — Login & Registration System with Flask

A beginner-friendly authentication system built with Flask.
This project demonstrates secure user signup, signin/logout, session management, and database migrations using Flask-Migrate.

---

## Screenshots

![Home](image.png)
![Signup](image-1.png)
![Signin](image-2.png)
![Dashboard](image-3.png)

---

## Project Structure

```text
signin_signout/
│
├── app.py
├── config.py
├── wsgi.py
├── requirements.txt
├── migrations/
├── instance/
├── forms/
├── models/
├── routes/
├── templates/
├── tests/
└── README.md
```

## Endpoints

### Web (HTML)

- `GET /` — Home page
- `GET,POST /signup` — Register a new user
- `GET,POST /signin` — Sign in
- `GET /dashboard` — Dashboard (login required)
- `GET /logout` — Log out (login required)

### Test API (JSON)

These routes are registered under the `/test` prefix.

- `GET /test/` — Health check
- `POST /test/signup` — Create account (JSON/form)
- `POST /test/signin` — Log in (JSON/form)
- `POST /test/logout` — Log out (login required)
- `GET /test/status/<user_id>` — Lookup a single user
- `GET /test/status` — List all users

---

## Quickstart (Windows)

### 1) Create and activate a virtual environment

```bash
py -m venv .venv
.venv\Scripts\activate
```

### 2) Install dependencies

```bash
pip install -r requirements.txt
```

### 3) Create a `.env` file

Create `.env` in the project root (you can copy `.env.example`):

```env
SECRET_KEY=change-me
DATABASE_URL=sqlite:///app.db
```

### 4) Apply migrations

```bash
flask --app app db upgrade
```

### 5) Run the app

```bash
flask --app app run
```

Open: http://127.0.0.1:5000/


