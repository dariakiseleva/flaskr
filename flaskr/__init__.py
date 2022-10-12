import os

from flask import Flask


# ---The "application factory" function which return the app
# (For configuration, registration, and other setup)
# Note: Since using a factory function, the instance of the Flask app itself is not available


def create_app(test_config=None):
    # Create flask instance
    # __name__ = name of current Python module
    # True -> Configuration files are relative to the instance folder (outside the flaskr package)
    app = Flask(__name__, instance_relative_config=True)

    # Default configuration of the app
    # Secret key keeps data safe, 'dev' should be overriden with a random value when deploying
    # The SQLite database is under the Flask instance folder (called 'instance')
    app.config.from_mapping(
        SECRET_KEY="dev", DATABASE=os.path.join(app.instance_path, "flaskr.sqlite")
    )

    if test_config is None:
        # If not testing, load the instance config (override any values) if it exists
        # (For example, load a real SECRET_KEY when deploying)
        app.config.from_pyfile("config.py", silent=True)
    else:
        # If the test config (for testing the app) is passed in, load it
        app.config.from_mapping(test_config)

    # If the instance folder does not exist, create it, otherwise pass
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # --Simple page
    @app.route("/hello")
    def hello():
        return "Hello, Daria!"

    # Call the init_app function on the app -> this tells the app to run close_db when after each response, and adds a CLI command to init the db
    from . import db

    db.init_app(app)

    # Register blueprints
    from . import auth, blog

    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)

    # Associate a view with a url of a different name
    # url_for('index') and url_for('blog.index') both generate the '/' URL
    app.add_url_rule("/", endpoint="index")

    return app
