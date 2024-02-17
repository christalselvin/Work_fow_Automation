from urllib.parse import quote


class Config():
    SECRET_KEY = 'Th1s1ss3cr3t'
    SQLALCHEMY_POOL_SIZE = 10
    SQLALCHEMY_MAX_OVERFLOW = 20
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:1234@localhost/christal"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
