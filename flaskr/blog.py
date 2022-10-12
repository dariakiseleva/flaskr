from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

# Blog does not have a url prefix, as is the main feature
bp = Blueprint("blog", __name__)


@bp.route("/")
def index():
    # Extract post data and pass it to a template
    db = get_db()
    posts = db.execute(
        "SELECT p.id, title, body, created, author_id, username"
        " FROM post p JOIN user u ON p.author_id=u.id"
        " ORDER BY created DESC"
    ).fetchall()
    return render_template("blog/index.html", posts=posts)


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "INSERT INTO post (title, body, author_id) VALUES (?, ?, ?)",
                (title, body, g.user["id"]),
            )
            db.commit()
            return redirect(url_for("blog.index"))

    return render_template("blog/create.html")


# Helper function to retrieve post information based on post id
def get_post(id, check_author=True):
    post = (
        get_db()
        .execute(
            "SELECT p.id, title, body, created, author_id, username"
            " FROM post p JOIN user u ON p.author_id=u.id"
            " WHERE p.id = ?",
            (id,),
        )
        .fetchone()
    )

    # Abort to return a failed HTTP status and message
    if post is None:
        # not found
        abort(404, f"Post id {id} does not exist")
    if check_author and post["author_id"] != g.user["id"]:
        # forbidden
        abort(403)

    return post


@bp.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
# The update function takes the id from the endpoint params (flask ensures it is an int)
# The link to the update view is: url_for('blog.update', id=post['id'])
def update(id):
    post = get_post(id)

    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "Title can not be empty"

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "UPDATE post SET title = ?, body = ? WHERE id = ?", (title, body, id)
            )
            db.commit()
            return redirect(url_for("blog.index"))

    # Display the update page with retrieved post details
    return render_template("blog/update.html", post=post)
