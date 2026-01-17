from flask import Blueprint, request, session, redirect, url_for, render_template
from utils.auth import authenticate

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html", title="Login")

@auth_bp.route("/login", methods=["POST"])
def login():
    user = authenticate(
        request.form.get("username"),
        request.form.get("password")
    )

    if not user:
        return render_template(
            "login.html",
            title="Login",
            error="Invalid credentials"
        )

    session["username"] = user["username"]
    session["role"] = user["role"]

    if user["role"] == "student":
        return redirect(url_for("student.dashboard"))
    else:
        return redirect(url_for("instructor.dashboard"))

@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("auth.login_page"))
