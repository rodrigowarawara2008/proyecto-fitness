import os

class Config:
    SECRET_KEY = "ironbeast2026"
    
    # URL completa para SQLAlchemy
    SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://uubucg4b6hktzrfl:zl5EYMYL1vbz6wVKcvXO@bh6rjsd2rc2ekh3icakb-mysql.services.clever-cloud.com:3306/bh6rjsd2rc2ekh3icakb"
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Si necesitas los datos separados para otra cosa
    MYSQL_HOST = "bh6rjsd2rc2ekh3icakb-mysql.services.clever-cloud.com"
    MYSQL_USER = "uubucg4b6hktzrfl"
    MYSQL_PASSWORD = "zl5EYMYL1vbz6wVKcvXO"
    MYSQL_DATABASE = "bh6rjsd2rc2ekh3icakb"
    MYSQL_PORT = 3306