from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token

blp = Blueprint(
    "Token",
    "token",
    url_prefix="/api/v1/token"
)


@blp.route("/refresh")
class TokenRefresh(MethodView):

    @jwt_required(refresh=True)
    def post(self):
        identity = get_jwt_identity()

        new_access = create_access_token(identity=identity)

        return {"access_token": new_access}