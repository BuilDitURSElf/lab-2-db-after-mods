# Requirements map: where each requirement is in the code

Line numbers were checked against the files in this project. If you edit a file the numbers move,
but every place is also tagged in the code with a comment like `[R1]` or `[Bonus: search]`, so you can
search for the tag (for example `[R9]`) to find it again.

## Database (`database/schema.sql`)

| Requirement | File : line | What you see there |
|---|---|---|
| Re-runnable script | `database/schema.sql:4` | `DROP DATABASE IF EXISTS registration;` |
| Primary key (`users`) | `database/schema.sql:15` | `PRIMARY KEY (user_id)` (with `AUTO_INCREMENT` on line 10) |
| UNIQUE e-mail | `database/schema.sql:16` | `UNIQUE (email)` |
| NOT NULL, defaults | `database/schema.sql:10-14`, `21-26` | `NOT NULL`, `DEFAULT CURRENT_TIMESTAMP`, `DEFAULT 0` |
| Foreign key | `database/schema.sql:28` | `FOREIGN KEY (user_id) REFERENCES users (user_id)` |
| `users` created before `todos` | `database/schema.sql:9` then `:20` | a table can only point at one that exists |

## R1 - Register

| Part | File : line |
|---|---|
| The four form fields are read | `app/routes/auth.py:24-28` |
| Duplicate e-mail: MySQL error 1062 is caught | `app/repositories/users.py:22-24` (code constant on line 6) |
| `Email Already Exists` is shown | `app/routes/auth.py:37-39` |
| User is logged in after registering | `app/routes/auth.py:41` |
| Redirect after POST (refresh-safe) | `app/routes/auth.py:42` |
| Register form (HTML) | `app/templates/register.html:8-21` |

## R2 - Login / Logout

| Part | File : line |
|---|---|
| Find user by e-mail (SQL) | `app/repositories/users.py:28-35` |
| Compare typed password with the hash | `app/security.py:13-15` |
| Same message for wrong e-mail AND wrong password | `app/routes/auth.py:61-64` |
| Session is created (user_id stored) | `app/security.py:18-22` |
| Logout destroys the session | `app/security.py:25-27`, route at `app/routes/auth.py:70-73` |
| Logout button | `app/templates/base.html:13-21` |

## R3 - Private list

| Part | File : line |
|---|---|
| Not logged in -> redirect to login | `app/security.py:35-44` (the `login_required` decorator) |
| Decorator applied to the list page | `app/routes/todos.py:74` |
| Only this user's to-dos, newest first | `app/repositories/todos.py:11-19` (`WHERE user_id = %s ORDER BY todo_id DESC`) |
| `user_id` passed from the session | `app/routes/todos.py:40` |

## R4 - R7 - To-do actions (the lab's queries; only INSERT/UPDATE-title also carry the bonus `due_date`)

| Req | Action | Route | SQL |
|---|---|---|---|
| R4 | Add | `app/routes/todos.py:88` | `app/repositories/todos.py:22-28` |
| R5 | Edit title | `app/routes/todos.py:102` | `app/repositories/todos.py:31-37` (`AND user_id = %s` on line 35) |
| R6 | Mark done / not done | `app/routes/todos.py:110` | `app/repositories/todos.py:40-46` (`AND user_id = %s` on line 44) |
| R7 | Delete | `app/routes/todos.py:117` | `app/repositories/todos.py:49-55` (`AND user_id = %s` on line 53) |

| Detail | File : line |
|---|---|
| Add form | `app/templates/todos.html:10-21` |
| Edit form (title + date + Save) | `app/templates/todos.html:63-74` |
| Done toggle button (sends the new value 1/0) | `app/templates/todos.html:56-60` |
| Delete form with `data-confirm` | `app/templates/todos.html:77-80` |
| "Are you sure?" dialog | `app/static/js/validation.js:54-58` |

## R8 - Validation in the browser AND on the server

| Part | File : line |
|---|---|
| Register messages (server) | `app/validators.py:18`, `23`, `28`, `33`, `35` |
| Login messages (server) | `app/validators.py:42`, `44` |
| Title messages (server) | `app/validators.py:51`, `53` |
| Server stops BEFORE the database (register) | `app/routes/auth.py:30-33` |
| Server stops BEFORE the database (login) | `app/routes/auth.py:55-58` |
| Server stops BEFORE the database (add / edit) | `app/routes/todos.py:84-87`, `97-101` |
| Browser check of one input | `app/static/js/validation.js:5-20` |
| Browser shows the message under the field | `app/static/js/validation.js:23-27` |
| Browser blocks the submit when something is wrong | `app/static/js/validation.js:42-45` |
| Browser's own messages switched off (so ours show) | `novalidate` in `register.html:8`, `login.html:9`, `todos.html:10` and `:63` |
| Rules written next to each input | `app/templates/_macros.html` (the `data-*` attributes) |

Extra rules I added so MySQL never raises a raw error: name max 100 (`validators.py:20`),
e-mail max 255 (`:25`), password max 72 bytes because bcrypt ignores the rest (`:30`).

## R9 - Security

| Part | File : line |
|---|---|
| bcrypt hash (salted, slow) | `app/security.py:8-10` |
| Hash is created before the INSERT | `app/routes/auth.py:36` |
| Parameters (`%s`) in every statement | `app/repositories/users.py:18`, `32`; `app/repositories/todos.py:16`, `26`, `35`, `44`, `53` |
| `user_id` comes only from the session | `app/security.py:30-32` |
| Secrets live in `.env` | `app/config.py:13`, `18-22`; `.gitignore:1`; `.env.example` |

## R10 - User interface

| Part | File : line |
|---|---|
| One style for all pages | `app/static/css/style.css` (variables at the top, used everywhere) |
| Phone-friendly (viewport) | `app/templates/base.html:5` |
| Phone-friendly (wrapping rows, 360 px safe) | `app/static/css/style.css:114-130`, `163-172` |
| Error messages next to the form | `app/templates/_macros.html`, `app/static/css/style.css:83-84` |
| Visible state for done to-dos | `app/templates/todos.html:51-53` (class), `app/static/css/style.css:147-148` |
| Friendly empty list text | `app/templates/todos.html:38-47` |
| Name and logout button | `app/templates/base.html:13-21` |
| No raw error pages | `app/errors.py:6-14` |

---

# Bonus items (6 of 6)

| Bonus item | Status | Where |
|---|---|---|
| Due dates | Done | below |
| Filters | Done | below |
| Search | Done | below |
| Open count | Done | `app/templates/todos.html:7` ("X open · Y total", counts the whole list) |
| Dark mode | Done | `app/static/css/style.css:16-27` (follows the device setting) |
| Tests | Done | `tests/test_app.py`, 30 tests, run `python -m pytest` |
| Deploy online | Files and guide ready; **you** must publish it | below |

## Bonus: due dates

The `due_date` column is optional (`NULL`). Because of it the lab's INSERT and the title-UPDATE
have one extra column; `AND user_id = %s` is unchanged.

| Part | File : line |
|---|---|
| New column | `database/schema.sql:25` |
| Read it in the list query | `app/repositories/todos.py:15` |
| INSERT with `due_date` | `app/repositories/todos.py:22-28` |
| UPDATE with `due_date` | `app/repositories/todos.py:31-37` |
| Validate: empty is fine, wrong text gives `Due date is not a valid date` | `app/validators.py:57-65` |
| Add route reads + validates it | `app/routes/todos.py:82-88` |
| Edit route reads + validates it | `app/routes/todos.py:95-102` |
| Today's date for the "overdue" check | `app/routes/todos.py:62` |
| Date field in the add form | `app/templates/todos.html:16-17` |
| Date field in the edit form | `app/templates/todos.html:69-71` |
| Overdue class (past date and not done) | `app/templates/todos.html:52-53` |
| Overdue style (red) and field sizing | `app/static/css/style.css:163-168` |
| Tests | `tests/test_app.py:248-285` |

## Bonus: filters (All / Open / Done)

No new SQL: the route fetches the user's list with the lab's SELECT and filters it in Python.

| Part | File : line |
|---|---|
| The three allowed values | `app/routes/todos.py:12` |
| Read `?filter=...` (unknown value = all) | `app/routes/todos.py:15-18` |
| Split into open / done and pick the visible part | `app/routes/todos.py:46-49` |
| Keep the tab after add / edit / done / delete | `app/routes/todos.py:26-34` (used at lines 89, 103, 111, 118) |
| Tabs with counts | `app/templates/todos.html:31-36` |
| Tab styles | `app/static/css/style.css:150-161` |
| Tests | `tests/test_app.py:194-245` |

## Bonus: search

No new SQL either: matching is done in Python on the user's own list (case-insensitive, part of the title).

| Part | File : line |
|---|---|
| Read `?q=...` | `app/routes/todos.py:21-23` |
| Match the text in the titles | `app/routes/todos.py:44-45` |
| Search box (a normal GET form) | `app/templates/todos.html:23-29` |
| Text is kept after add / edit / done / delete, and works with the tabs | `app/routes/todos.py:26-34`, tab links `app/templates/todos.html:33-35` |
| Message when nothing matches | `app/templates/todos.html:42-43` |
| Styles | `app/static/css/style.css:170-172` |
| Tests | `tests/test_app.py:288-331` |

## Bonus: deploy online

| Part | File |
|---|---|
| How the host starts the app | `Procfile` (`gunicorn run:app`) |
| Production web server package | `requirements.txt:5` |
| Secure cookie on https | `app/config.py:15-16` and `COOKIE_SECURE` in `.env.example` |
| Step-by-step guide (Render or PythonAnywhere, hosted MySQL) | `DEPLOY.md` |

I cannot publish the site for you: it needs your own hosting account and a MySQL database.
After you deploy, write the live address at the top of `README.md`.
