from flask_smorest import Blueprint
from flask.views import MethodView
from flask_jwt_extended import create_access_token
from models import User
from flask import request
from werkzeug.security import check_password_hash
from flask import jsonify
from flask_smorest import Blueprint
from flask.views import MethodView
from flask_jwt_extended import create_access_token, create_refresh_token

from flask import request

blp = Blueprint(
    "Auth",
    "auth",
    url_prefix="/api/v1/auth"
)

@blp.route("/login")
class Login(MethodView):

    def post(self):
        data = request.get_json()

        username = data.get("username")
        password = data.get("password")

        user = User.query.filter_by(username=username).first()

        if not user:
            return jsonify(message="Invalid credentials"), 401

        if not user.check_password(password):
            return jsonify(message="Invalid credentials"), 401

        access_token = create_access_token(
            identity=user.id,
            additional_claims={"role": user.is_admin}
        )

        refresh_token = create_refresh_token(identity=user.id)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }

        # return jsonify(access_token= access_token, refresh_token=refresh_token), 200