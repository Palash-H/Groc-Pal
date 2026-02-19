# This is the main file of the project this is the main controller of the project here all the logic is implemented.
from flask import Flask
from models import db, User
from config import Configuration
from flask_migrate import Migrate
from routes import bprint


migrate = Migrate()
def create_app():
    app = Flask(__name__)
    app.config.from_object(Configuration)
    db.init_app(app)
    migrate.init_app(app,db)
    app.register_blueprint(bprint)
    with app.app_context():
        # db.create_all()
        admin = User.query.filter_by(is_admin = True).first()
        if not admin:
            admin = User(username = "admin1", password = "admin12345", name = "admin1", is_admin = True)
            db.session.add(admin)
            db.session.commit()

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 5000,debug = True)