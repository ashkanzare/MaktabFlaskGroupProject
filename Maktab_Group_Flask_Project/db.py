from flask_mongoengine import MongoEngine
import click
from flask import current_app
from flask import g
from flask.cli import with_appcontext


# bakhshe ejade database va vasl shodan be database

def get_db():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    if "db" not in g:
        db = MongoEngine()
        db.init_app(current_app)
        g.db = db

    return g.db


def close_db(e=None):
    """If this request connected to the database, close the
    connection.
    """
    g.pop("db", None)


def init_db():
    """Clear existing data and create new tables."""
    get_db()


@click.command("init-db")
@with_appcontext
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


def init_app(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
