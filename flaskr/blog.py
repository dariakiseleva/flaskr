from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

# Blog does not have a url prefix, as is the main feature
bp = Blueprint("blog", __name__)
