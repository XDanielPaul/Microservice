import click
from flask.cli import with_appcontext
from models import Posts
from extensions import db


@click.command(name='restart_tables')
@with_appcontext
def restart_tables():
    db.drop_all()
    db.create_all()