import os

HERE = os.path.abspath(os.path.dirname("."))

HOST = "127.0.0.1"
PORT = 5000
TESTING = True

FRESHERMEAT_INSTANCE_NAME = "Open Source Security Software"
FRESHERMEAT_INSTANCE_URL = "https://open-source-security-software.net"

DB_CONFIG_DICT = {
    "user": "pgsqluser",
    "password": "pgsqlpwd",
    "host": "localhost",
    "port": 5432,
}
DATABASE_NAME = "freshermeat_dev"
SQLALCHEMY_DATABASE_URI = "postgresql://{user}:{password}@{host}:{port}/{name}".format(
    name=DATABASE_NAME, **DB_CONFIG_DICT
)
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = "SECRET KEY"
SECURITY_PASSWORD_SALT = "SECURITY PASSWORD SALT"

UPLOAD_FOLDER = "./freshermeat/web/public/pictures/"
ALLOWED_EXTENSIONS = {"png"}

LOG_PATH = "./var/log/freshermeat.log"
LOG_LEVEL = "info"

CSRF_ENABLED = True
# slow database query threshold (in seconds)
DATABASE_QUERY_TIMEOUT = 0.5

MAIL_SERVER = "localhost"
MAIL_PORT = 25
MAIL_USE_TLS = False
MAIL_USE_SSL = False
MAIL_DEBUG = True
MAIL_USERNAME = None
MAIL_PASSWORD = None
MAIL_DEFAULT_SENDER = ""

GITHUB_CLIENT_ID = ""
GITHUB_CLIENT_SECRET = ""

CVE_SEARCH_INSTANCE = "https://cvepremium.circl.lu"
