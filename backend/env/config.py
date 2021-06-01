import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = 'Sm9obiBTY2hyb20ga2lja3MgYXNz'
    STRIPE_API_KEY = 'SmFjb2IgS2FwbGFuLU1vc3MgaXMgYSBoZXJv'
    SQLALCHEMY_DATABASE_URI = "postgresql://user:TWljaGHFgiBCYXJ0b3N6a2lld2ljeiEh@localhost/databasename"
    JWT_SECRET_KEY = "super-secret"


    MAIL_SERVER = 'smtp.gmail.com'

    MAIL_PORT = 465
    MAIL_USERNAME = 'please enter your email id'
    MAIL_PASSWORD = 'password'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL')

