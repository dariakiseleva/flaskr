import sqlite3
import click
from flask import current_app, g

# A connection to the database is created when handling the request, and closed before sending the response


def geb_db():
    # "g" is an object unique for each request, stores data accessed during the request
    # The connection is stored and can be reused if called again in the same request
    if "db" not in g:
        g.db = sqlite3.connect(
            # Connect to the file pointed to by the DATABASE key in config
            current_app.config["DATABASE"],
            detect_types=sqlite3.PARSE_DECLTYPES,
        )
        # Return rows that behave like dicts to access columns by name
        g.db.row_factory = sqlite3.Row

    return g.db


# If the connection exists, close it
def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()
