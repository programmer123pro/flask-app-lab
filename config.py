# SECRET_KEY = "secret-key-sdsfs"

# SQLALCHEMY_DATABASE_URI = 'sqlite:///data.sqlite'
# SQLALCHEMY_TRACK_MODIFICATIONS = False  

class DevConfig():
   SECRET_KEY = "secret-key-sdsfs"
   SQLALCHEMY_DATABASE_URI = 'sqlite:///data.sqlite'
   SQLALCHEMY_TRACK_MODIFICATIONS = False 

class TestingConfig():
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    SECRET_KEY = "secret-key-sdsfs"
