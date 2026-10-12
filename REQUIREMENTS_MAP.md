# Requirements map: where each requirement is in the code

Line numbers were checked against the files in this project. If you edit a file the numbers move,
but every place is also tagged in the code with a comment like `[R1]`, so you can search for the tag
(for example `[R9]`) to find it again.

## Database (`database/schema.sql`)

| Requirement | File : line | What you see there |
|---|---|---|
| Re-runnable script | `database/schema.sql:4` | `DROP DATABASE IF EXISTS registration;` |
| Primary key (`users`) | `database/schema.sql:15` | `PRIMARY KEY (user_id)` (with `AUTO_INCREMENT` on line 10) |
| UNIQUE e-mail | `database/schema.sql:16` | `UNIQUE (email)` |
| NOT NULL, defaults | `database/schema.sql:10-14`, `22-25` | `NOT NULL`, `DEFAULT CURRENT_TIMESTAMP`, `DEFAULT 0` |
| Foreign key | `database/schema.sql:27` | `FOREIGN KEY (user_id) REFERENCES users (user_id)` |
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
| Decorator applied to the list page | `app/routes/todos.py:26` |
| Only this user's to-dos, newest first | `app/repositories/todos.py:10-18` (`WHERE user_id = %s ORDER BY todo_id DESC`) |
| `user_id` passed from the session | `app/routes/todos.py:13` |

## R4 - R7 - To-do actions (queries exactly as given in the lab)

| Req | Action | Route | SQL |
|---|---|---|---|
| R4 | Add | `app/routes/todos.py:38` | `app/repositories/todos.py:21-27` |
| R5 | Edit title | `app/routes/todos.py:49` | `app/repositories/todos.py:30-36` (`AND user_id = %s` on line 34) |
| R6 | Mark done / not done | `app/routes/todos.py:57` | `app/repositories/todos.py:39-45` (`AND user_id = %s` on line 43) |
| R7 | Delete | `app/routes/todos.py:64` | `app/repositories/todos.py:48-54` (`AND user_id = %s` on line 52) |

| Detail | File : line |
|---|---|
| Add form | `app/templates/todos.html:9-18` |
| Edit form (title + Save) | `app/templates/todos.html:38-46` |
| Done toggle button (sends the new value 1/0) | `app/templates/todos.html:30-35` |
| Delete form with `data-confirm` | `app/templates/todos.html:48-52` |
| "Are you sure?" dialog | `app/static/js/validation.js:54-58` |

## R8 - Validation in the browser AND on the server

| Part | File : line |
|---|---|
| Register messages (server) | `app/validators.py:17`, `22`, `27`, `32`, `34` |
| Login messages (server) | `app/validators.py:41`, `43` |
| Title messages (server) | `app/validators.py:50`, `52` |
| Server stops BEFORE the database (register) | `app/routes/auth.py:30-33` |
| Server stops BEFORE the database (login) | `app/routes/auth.py:55-58` |
| Server stops BEFORE the database (add / edit) | `app/routes/todos.py:35-37`, `46-48` |
| Browser check of one input | `app/static/js/validation.js:5-20` |
| Browser shows the message under the field | `app/static/js/validation.js:23-27` |
| Browser blocks the submit when something is wrong | `app/static/js/validation.js:42-45` |
| Browser's own messages switched off (so ours show) | `novalidate` in `register.html:8`, `login.html:9`, `todos.html:9` and `:38` |
| Rules written next to each input | `app/templates/_macros.html` (the `data-*` attributes) |

Extra rules I added so MySQL never raises a raw error: name max 100 (`validators.py:19`),
e-mail max 255 (`:24`), password max 72 bytes because bcrypt ignores the rest (`:29`).

## R9 - Security

| Part | File : line |
|---|---|
| bcrypt hash (salted, slow) | `app/security.py:8-10` |
| Hash is created before the INSERT | `app/routes/auth.py:36` |
| Parameters (`%s`) in every statement | `app/repositories/users.py:18`, `32`; `app/repositories/todos.py:15`, `25`, `34`, `43`, `52` |
| `user_id` comes only from the session | `app/security.py:30-32` |
| Secrets live in `.env` | `app/config.py:13`, `16-20`; `.gitignore:1`; `.env.example` |

## R10 - User interface

| Part | File : line |
|---|---|
| One style for all pages | `app/static/css/style.css` (variables at the top, used everywhere) |
| Phone-friendly (viewport) | `app/templates/base.html:5` |
| Phone-friendly (wrapping rows, 360 px safe) | `app/static/css/style.css:114-130` (`flex-wrap`, `min-width: 0`) |
| Error messages next to the form | `app/templates/_macros.html`, `app/static/css/style.css:82-84` |
| Visible state for done to-dos | `app/templates/todos.html:27-28` (class), `app/static/css/style.css:146-148` |
| Friendly empty list text | `app/templates/todos.html:20-23` |
| Name and logout button | `app/templates/base.html:13-21` |
| No raw error pages | `app/errors.py:6-14` |

## Bonus

| Item | Where |
|---|---|
| Dark mode | `app/static/css/style.css:16-27` |
| Open to-do counter | `app/templates/todos.html:6` |
| Automated tests | `tests/test_app.py` (14 tests, run `python -m pytest`) |
