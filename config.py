import os 
# from app import app, db
from datetime import timedelta, timezone

class Configuration:
    SQLALCHEMY_DATABASE_URI = "sqlite:///placementdatabase.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "thisisdemo"
    JWT_VERIFY_SUB=False
    API_TITLE = "Grocery API"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/api/docs"
    OPENAPI_SWAGGER_UI_PATH = "/swagger"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    JWT_ACCESS_TOKEN_EXPIRES= timedelta(minutes=10)
    JWT_REFRESH_TOKEN_EXPIRES= timedelta(days=7)
    # JWT_DECODE_LEEWAY=30
    JWT_ENCODE_NBF=False
    JWT_ENCODE_ISSUER=None
    JWT_ENCODE_AUDIENCE=None
    JWT_SECRET_KEY = os.getenv("JWT_KEY") # This is demo applicatoin, in production take this from .env file ...Pal