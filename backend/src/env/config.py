import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config():
    NAME_DB = os.environ.get('NAME_DB','rmg_db')
    PORT_DB = os.getenv('PORT_DB','3306')
    PWD_DB = os.getenv('PWD_DB','SS12VuLmaNyLtl#123')
    HOST_DB = os.getenv('HOST_DB','65.1.199.29')
    USER_DB = os.getenv('USER_DB','lmsadmin')
    
    current_env = os.getenv('FLASK_ENV')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY',"super-secret")
    FERNET_KEY = b'cx9VhUbmHbJMrVBtSL4Isusu7aN1lJ25bMPlS2jefJE='
    
    # SECRET_KEY = 'Sm9obiBTY2hyb20ga2lja3MgYXNz'

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


    # FLASK_ENV=local
    # JWT_SECRET_KEY=secretkey
    #FERNET_KEY=b'cx9VhUbmHbJMrVBtSL4Isusu7aN1lJ25bMPlS2jefJE='
    # NAME_DB=postgres
    # PORT_DB=5432
    # PWD_DB=admin
    # HOST_DB=localhost
    # USER_DB=postgres
    # AWS_ACCESS_KEY=AKIARE3TT7TWTAWJC6ID
    # AWS_SECRET_KEY=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

    # AUTH_PARAMS_NAME = "authcred"
    #FERNET_ENCRYPT_FORMAT = 'utf-8'
    #AUTH_TOKEN_EXPIRY_DAYS = 1
    #AUTH_TOKEN_EXPIRY_SECS = 60
    # AWS_BUCKET_NAME = "lmsmediavault"

    # current_env = os.getenv('FLASK_ENV')
    # JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    #FERNET_KEY = b'cx9VhUbmHbJMrVBtSL4Isusu7aN1lJ25bMPlS2jefJE='

    # NAME_DB = os.environ.get('NAME_DB')
    # PORT_DB = os.getenv('PORT_DB')
    # PWD_DB = os.getenv('PWD_DB')
    # HOST_DB = os.getenv('HOST_DB')
    # USER_DB = os.getenv('USER_DB')

    # AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
    # AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")