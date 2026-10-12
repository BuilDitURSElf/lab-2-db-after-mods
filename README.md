# Lab 2: Login & To-Do Application

## 1. Team

| Name | ID | Did what |
|------|----|----------|
| Amr Khaled Abdelrahim |  2304078 | Backend |
| Abdelrahman Mohamed | 2304056 | frontend & database |

## 2. Technology

- **Back end:** Python 3 + Flask (blueprints, sessions), PyMySQL (plain SQL, no ORM), bcrypt
- **Front end:** HTML (Jinja templates), CSS (own stylesheet), JavaScript (validation)
- **Database:** MySQL, database `registration`, tables `users` and `todos`

## 3. How to run it (from an empty machine)

1. Install **Python 3.10+**, **MySQL Server** and **Git**.
2. Get the code and enter the folder:
   ```bash
   git clone <your-repository-url>
   cd db-lab2-<names>
   ```
3. Create a virtual environment and install the packages:
   ```bash
   python -m venv venv
   source venv/bin/activate        # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
4. Build the database (this drops and recreates `registration`):
   ```bash
   mysql -u root -p < database/schema.sql
   ```
5. Copy the settings file and put your MySQL password in it:
   ```bash
   cp .env.example .env            # Windows: copy .env.example .env
   ```
6. Start the server:
   ```bash
   python run.py
   ```
7. Open <http://127.0.0.1:5000>.

Optional: `python -m pytest` runs the automated tests (they do not need MySQL).

## 4. Features

| # | Feature | Status |
|---|---------|--------|
| R1 | Register (name, e-mail, password, confirm), `Email Already Exists`, auto login | Done |
| R2 | Login with one single error message, logout | Done |
| R3 | Private list, redirect to login, newest first | Done |
| R4 | Add a to-do | Done |
| R5 | Edit a title | Done |
| R6 | Mark done / not done | Done |
| R7 | Delete with "are you sure?" | Done |
| R8 | Validation in the browser and on the server with the exact messages | Done |
| R9 | bcrypt hashes, parameterised queries only, `user_id` from the session | Done |
| R10 | Consistent, responsive UI with feedback and empty state | Done |
| Bonus | Open-to-do counter, dark mode, automated tests | Done |

The exact file and line of every requirement is in [REQUIREMENTS_MAP.md](REQUIREMENTS_MAP.md).

### Project structure

```
db-lab2/
  database/schema.sql        the DDL (both tables)
  app/
    __init__.py              builds the app
    config.py                settings from .env
    db.py                    MySQL connection
    security.py              bcrypt + session helpers
    validators.py            the validation rules and messages
    repositories/            ALL the SQL (users.py, todos.py)
    routes/                  web pages (auth.py, todos.py)
    templates/               HTML pages
    static/                  style.css, validation.js
  tests/test_app.py          automated tests
  run.py                     starts the server
```

Layers: **routes** (HTTP) call **validators** (rules), then **repositories** (SQL), which use **db** (connection). SQL exists only in `repositories/`.

## 5. Screenshots

Put the files in `screenshots/` and keep these four links:

1. `screenshots/register-errors.png` - register page with error messages
2. `screenshots/login.png` - login page
3. `screenshots/list.png` - list with some to-dos (one done)
4. `screenshots/phone.png` - the site in a phone-sized window (about 360 px)

## 6. Answers

**(a) Why do UPDATE and DELETE contain `AND user_id = ?`, and what changes if you remove it?**
The to-do number comes from the browser, so anybody can send somebody else's number. `AND user_id = ?` uses the id of the logged-in user (taken from the session), so a to-do that is not yours matches zero rows and nothing changes. Without it, any logged-in user could edit, mark or delete other users' to-dos just by changing the number.

**(b) What happens if you insert a to-do for a `user_id` that does not exist, and which constraint is that?**
MySQL refuses the INSERT with error 1452 (a foreign key constraint fails). It is the **foreign key constraint**, which enforces **referential integrity**: every `todos.user_id` must match an existing `users.user_id`.

**(c) Why do you store a hash and not the password?**
If the database leaks, the attacker must not get the real passwords (people reuse them). A bcrypt hash cannot be reversed, it is salted (equal passwords give different hashes), and it is slow on purpose, which makes guessing very expensive. To log in we compare the typed password with the hash using bcrypt.

**(d) `name` is NOT NULL: why did you still need your own check for an empty name?**
An empty text `''` is a value, not NULL, so `NOT NULL` accepts it (and so does a name made only of spaces). Only our own check (`validate_register` in `app/validators.py`, and the same rule in JavaScript) can refuse it.
