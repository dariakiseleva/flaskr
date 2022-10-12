import functools

from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db

# Create a bluepint named "auth", defined in the current module, with /auth prepended to URLs
bp = Blueprint("auth", __name__, url_prefix="/auth")

# Register route in the Auth blueprint

# Associate auth/register with the "register" view function
@bp.route("/register", methods=("GET", "POST"))
def register():
    # The POST route will submit a form
    if request.method == "POST":
        # request.form is a dictionary
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None

        if not username:
            error = "Username is required"
        elif not password:
            error = "Password is required"

        if error is None:
            try:
                # Insert data, avoid SQL injection, hash the password
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                # Save the sQLite changes
                db.commit()
            # If a db error occurs
            except db.IntegrityError:
                error = f"User {username} is already registered."
            # IF no error -> Redirect to the URL for the auth.login route
            else:
                return redirect(url_for("auth.login"))

        # Flash whatever error has occurred
        flash(error)

    # If navigating to auth/register (GET)
    return render_template("auth/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None

        # Return one row based on the query, or None if nothing matches
        user = db.execute(
            "SELECT * FROM user WHERE username = ?", (username,)
        ).fetchone()

        if user is None:
            error = "Incorrect username."
        elif not check_password_hash(user["password"], password):
            error = "Incorrect password"

        # Session is a dictionary that stores data in a cookie
        if error is None:
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("index"))

        flash(error)

    return render_template("auth/login.html")


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


# The function runs before any view function in the vlueprint
# Based on the id stored in the cookie, get the user's data from the database
# Store the data in g.user which lasts for the length of the request
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = (
            get_db().execute("SELECT * FROM user WHERE id = ?", (user_id,)).fetchone()
        )


# Authenticating views with a decorator
# Return a new view function that wraps the original
# If user is not logged in, redirect
# If user is logged in, return original


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view
