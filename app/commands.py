import click
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from .extensions import db
from .models import User


def _raise_database_error(error):
    message = str(error)
    hints = [
        "Database connection failed.",
        "",
        "Azure SQL checklist:",
        "1. Confirm AZURE_SQL_SERVER is the full host, for example xxx.database.windows.net.",
        "2. Confirm AZURE_SQL_DATABASE is the target database name, not the server name.",
        "3. Confirm AZURE_SQL_USERNAME and AZURE_SQL_PASSWORD are valid SQL authentication credentials.",
        "4. If the login is a server-level Azure SQL login, try AZURE_SQL_USERNAME=user@server-name.",
        "5. In Azure Portal, confirm SQL authentication is enabled and your client IP is allowed by the SQL server firewall.",
        "6. Confirm the database user exists and has permission to create tables.",
    ]
    if "18456" in message or "Login failed" in message:
        hints.insert(1, "Detected: SQL Server login failed, error 18456.")
    raise click.ClickException("\n".join(hints))


def register_commands(app):
    @app.cli.command("check-db")
    def check_db():
        """Check the Azure SQL database connection."""
        try:
            result = db.session.execute(
                text("SELECT DB_NAME() AS database_name, SYSTEM_USER AS login_name")
            ).mappings().one()
        except SQLAlchemyError as exc:
            _raise_database_error(exc)

        click.echo("Database connection OK.")
        click.echo(f"Database: {result['database_name']}")
        click.echo(f"Login: {result['login_name']}")

    @app.cli.command("init-db")
    def init_db():
        """Create database tables."""
        try:
            db.create_all()
        except SQLAlchemyError as exc:
            _raise_database_error(exc)
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
