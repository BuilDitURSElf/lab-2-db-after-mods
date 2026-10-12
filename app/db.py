"""Database connection helper: one MySQL connection per request."""
import pymysql
from flask import current_app, g


def get_db():
    """Open the connection the first time it is needed in a request."""
    if "db" not in g:
        g.db = pymysql.connect(
            host=current_app.config["DB_HOST"],
            port=current_app.config["DB_PORT"],
            user=current_app.config["DB_USER"],
            password=current_app.config["DB_PASSWORD"],
            database=current_app.config["DB_NAME"],
            cursorclass=pymysql.cursors.DictCursor,  # rows come back as dicts
            autocommit=True,
        )
    return g.db


def close_db(error=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_app(app):
    app.teardown_appcontext(close_db)  # close the connection after every request
