from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required, get_jwt
from datetime import datetime
from models import db, TokenBlocklist

blp = Blueprint("Logout", "logout", url_prefix="/api/v1/logout")


@blp.route("/")
class Logout(MethodView):

    @jwt_required(verify_type=False)
    def post(self):
        jti = get_jwt()["jti"]
        token_type=get_jwt()["type"]

        blocked = TokenBlocklist(
            jti=jti,
            created_at=datetime.utcnow()
        )

        db.session.add(blocked)
        db.session.commit()

        return {"msg": f"{token_type} Token revoked"}