import click

from .extensions import db
from .models import User


def register_commands(app):
    @app.cli.command("init-db")
    def init_db():
        """Create database tables."""
        db.create_all()
        click.echo("Database tables created.")

    @app.cli.command("create-admin")
    @click.argument("username")
    @click.argument("email")
    @click.argument("password")
    def create_admin(username, email, password):
        """Create an admin user."""
        existing = User.query.filter(
            (User.username == username) | (User.email == email)
        ).first()
        if existing:
            raise click.ClickException("User with this username or email already exists.")

        user = User(username=username, email=email, role="admin")
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        click.echo(f"Admin user created: {username}")

