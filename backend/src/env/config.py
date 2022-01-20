import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config():
    current_env = os.getenv('FLASK_ENV')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY',"super-secret")
    FERNET_KEY = b'cx9VhUbmHbJMrVBtSL4Isusu7aN1lJ25bMPlS2jefJE='

    JWT_SECRET_KEY = "super-secret"
    FERNET_KEY=b'cx9VhUbmHbJMrVBtSL4Isusu7aN1lJ25bMPlS2jefJE='
    

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'test@email'
    MAIL_PASSWORD = 'password'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    FERNET_ENCRYPT_FORMAT = 'utf-8'
    AUTH_TOKEN_EXPIRY_DAYS = 1
    AUTH_TOKEN_EXPIRY_SECS = 60
    FERNET_KEY = b'cx9VhUbmHbJMrVBtSL4Isusu7aN1lJ25bMPlS2jefJE='

    NAME_DB = os.getenv('NAME_DB','rmg_db')
    PORT_DB = os.getenv('PORT_DB','3306')
    PWD_DB = os.getenv('PWD_DB','SS12VuLmaNyLtl#123')
    HOST_DB = os.getenv('HOST_DB','localhost')
    USER_DB = os.getenv('USER_DB','lmsadmin')
    
