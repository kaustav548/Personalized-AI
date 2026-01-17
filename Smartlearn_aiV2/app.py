from flask import Flask
from routes.student import student_bp
from routes.instructor import instructor_bp
from flask import session
from routes.auth import auth_bp
from flask import redirect, url_for

def create_app():
    app = Flask(__name__)

    # Basic configuration
    app.config["JSON_SORT_KEYS"] = False
    app.config["SECRET_KEY"] = "chemE_ai_learning"

    # Register Blueprints
    app.register_blueprint(student_bp, url_prefix="/student")
    app.register_blueprint(instructor_bp, url_prefix="/instructor")
    app.register_blueprint(auth_bp, url_prefix="/auth")


    @app.route("/")
    def home():
        return  redirect(url_for("auth.login_page"))
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
