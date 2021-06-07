import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = 'Sm9obiBTY2hyb20ga2lja3MgYXNz'
    SQLALCHEMY_DATABASE_URI = "mssql+pyodbc://ADD_SQL_SERVER_NAME/master?driver=SQL Server?Trusted_Connection=yes"
    JWT_SECRET_KEY = "super-secret"

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'test@email'
    MAIL_PASSWORD = 'password'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
