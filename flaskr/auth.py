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
