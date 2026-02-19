import os 
# from app import app, db

class Configuration:
    SQLALCHEMY_DATABASE_URI = "sqlite:///placementdatabase.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "thisisdemo"

