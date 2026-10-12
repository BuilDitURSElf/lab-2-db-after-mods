# Deploying the app online (bonus)

The app is ready to deploy: `Procfile` tells the host how to start it (`gunicorn run:app`),
and every setting comes from environment variables (the same names as in `.env.example`).
You need two things from a host: **a place to run Python** and **a MySQL database**.

## Option A: Render (web service) + a hosted MySQL

1. Create a MySQL database somewhere reachable from the internet. Free/cheap choices change
   often (for example Aiven, TiDB Cloud, Railway, PlanetScale-style services, or your host's own MySQL).
   Write down its host, port, user, password and database name.
2. Load the schema into it **from your computer** (this drops and recreates the `registration` database,
   so use a database where that is allowed, or create a database with the host's name and
   remove the first three lines of `schema.sql` (DROP/CREATE DATABASE/USE) before loading):
   ```bash
   mysql -h HOST -P PORT -u USER -p DBNAME < database/schema.sql
   ```
3. Push the project to GitHub (without `.env`).
4. On Render: **New > Web Service**, pick the repository, then set:
   - Runtime: Python 3
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn run:app`
5. Add these **environment variables** in Render:

   | Name | Value |
   |---|---|
   | `SECRET_KEY` | a long random text (for example `python -c "import secrets; print(secrets.token_hex(32))"`) |
   | `DB_HOST` | host of your hosted MySQL |
   | `DB_PORT` | its port (usually 3306) |
   | `DB_USER` | its user |
   | `DB_PASSWORD` | its password |
   | `DB_NAME` | the database name |
   | `COOKIE_SECURE` | `1` |

6. Deploy, open the address Render gives you, register a user and add a to-do.
7. Put the live address at the top of your README.

## Option B: PythonAnywhere (has MySQL built in)

1. Create an account, open **Databases**, set a MySQL password and create a database.
   Its name looks like `yourname$registration`.
2. In a **Bash console**: clone your repository, create a virtualenv and run `pip install -r requirements.txt`.
3. Load the schema (remove the first three lines `DROP DATABASE`, `CREATE DATABASE`, `USE` from the copy you load,
   because PythonAnywhere creates the database for you):
   ```bash
   mysql -u yourname -h yourname.mysql.pythonanywhere-services.com 'yourname$registration' < database/schema.sql
   ```
4. **Web** tab: add a new web app (manual configuration, same Python version), set the
   virtualenv path, and edit the WSGI file so it contains:
   ```python
   import sys
   sys.path.insert(0, "/home/yourname/your-repository")
   from run import app as application
   ```
5. In the project folder create `.env` with the PythonAnywhere database values and `COOKIE_SECURE=1`.
6. Press **Reload** and open `yourname.pythonanywhere.com`.

## Checklist before you submit

- [ ] The live address works and a new user can register, log in and add a to-do.
- [ ] `.env` is NOT in the repository (only `.env.example`).
- [ ] `SECRET_KEY` on the host is a long random value, not the sample.
- [ ] The live address is written in the README.
