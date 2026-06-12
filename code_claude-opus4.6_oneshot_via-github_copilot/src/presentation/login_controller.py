from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash

login_bp = Blueprint("login", __name__)


class LoginController:
    def __init__(self, user_repo):
        self.user_repo = user_repo

    def register(self, app):
        controller = self

        @login_bp.route("/login", methods=["GET", "POST"])
        def login():
            if request.method == "POST":
                username = request.form.get("username", "").strip()
                password = request.form.get("password", "")
                user = controller.user_repo.findByUsername(username)
                if user and user.active and check_password_hash(user.passwordHash, password):
                    session["user_id"] = user.userId
                    session["username"] = user.username
                    session["rolle"] = user.rolle.value
                    session["anzeigename"] = user.anzeigename
                    flash(f"Willkommen, {user.anzeigename}!", "success")
                    return redirect(url_for("raum.raeume"))
                flash("Ungueltige Anmeldedaten oder Benutzer deaktiviert.", "danger")
            return render_template("login.html")

        @login_bp.route("/logout")
        def logout():
            session.clear()
            flash("Abgemeldet.", "info")
            return redirect(url_for("login.login"))

        app.register_blueprint(login_bp)
