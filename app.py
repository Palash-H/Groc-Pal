# This is the main file of the project this is the main controller of the project here all the logic is implemented.
from flask import Flask
from models import db, User
from config import Configuration
from flask_migrate import Migrate
from routes import bprint
from api.auth import blp as AuthBlueprint
from flask_smorest import Api
from flask_cors import CORS
from werkzeug.exceptions import HTTPException
from flask import jsonify
from flask_jwt_extended import JWTManager
from datetime import datetime
from api.token_api import blp as TokenBlueprint
from api.logout_api import blp as LogoutBlueprint
# import datetime as dt
from models import TokenBlocklist
from dotenv import load_dotenv
import os

load_dotenv()
migrate = Migrate()
def create_app():
    app = Flask(__name__)
        
    CORS(
    app,
    resources={r"/api/*": {"origins": "*"}},
    supports_credentials=True
    )
    
    app.config.from_object(Configuration)
    db.init_app(app)
    api=Api(app)
    migrate.init_app(app,db)
    app.register_blueprint(bprint)
    from api.product_api import blp as ProductBlueprint
    api.register_blueprint(ProductBlueprint)
    api.register_blueprint(AuthBlueprint)
    api.register_blueprint(TokenBlueprint)
    api.register_blueprint(LogoutBlueprint)
    with app.app_context():
        # db.create_all()
        admin = User.query.filter_by(is_admin = True).first()
        if not admin:
            admin = User(username = "admin1", password = "admin12345", name = "admin1", is_admin = True)
            db.session.add(admin)
            db.session.commit()
    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        response = e.get_response()
        response.data = jsonify({
            "code": e.code,
            "name": e.name,
            "description": e.description
        }).data
        response.content_type = "application/json"
        return response


    @app.errorhandler(Exception)
    def handle_general_exception(e):
        return jsonify({
            "code": 500,
            "name": "Internal Server Error",
            "description": str(e)
        }), 500
    
    jwt=JWTManager(app)

    

    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        token = TokenBlocklist.query.filter_by(jti=jti).first()
        return token is not None

    @jwt.user_identity_loader
    # @jwt.user_identity_loader
    def user_identity_lookup(user):
        return str(user)


    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        from models import User
        identity = jwt_data["sub"]
        return User.query.get(int(identity))
    return app

app = create_app()

# if __name__ == "__main__":
#     app.run(host = "0.0.0.0", port = 5000,debug = True)