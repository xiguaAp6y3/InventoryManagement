import os
from urllib.parse import quote_plus

from dotenv import load_dotenv


load_dotenv()


def _build_azure_sql_uri():
    server = os.getenv("AZURE_SQL_SERVER", "")
    database = os.getenv("AZURE_SQL_DATABASE", "")
    username = os.getenv("AZURE_SQL_USERNAME", "")
    password = os.getenv("AZURE_SQL_PASSWORD", "")
    driver = os.getenv("AZURE_SQL_DRIVER", "ODBC Driver 18 for SQL Server")
    encrypt = os.getenv("AZURE_SQL_ENCRYPT", "yes")
    trust_cert = os.getenv("AZURE_SQL_TRUST_SERVER_CERTIFICATE", "no")

    odbc = (
        f"DRIVER={{{driver}}};"
        f"SERVER=tcp:{server},1433;"
        f"DATABASE={database};"
        f"UID={username};"
        f"PWD={password};"
        f"Encrypt={encrypt};"
        f"TrustServerCertificate={trust_cert};"
        "Connection Timeout=30;"
    )
    return f"mssql+pyodbc:///?odbc_connect={quote_plus(odbc)}"


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-jwt-secret")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL") or _build_azure_sql_uri()
