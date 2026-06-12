from flask import Blueprint, render_template, request, redirect, url_for, flash, session

raum_bp = Blueprint("raum", __name__)


class RaumController:
    def __init__(self, raum_anzeigen_service, geraet_installieren_service, user_repo):
        self.raum_anzeigen_service = raum_anzeigen_service
        self.geraet_installieren_service = geraet_installieren_service
        self.user_repo = user_repo

    def register(self, app):
        controller = self

        def _get_user():
            uid = session.get("user_id")
            if uid:
                return controller.user_repo.findById(uid)
            return None

        @raum_bp.route("/")
        @raum_bp.route("/raeume")
        def raeume():
            user = _get_user()
            if not user:
                return redirect(url_for("login.login"))
            try:
                raeume_list = controller.raum_anzeigen_service.execute(user)
                return render_template("raeume.html", raeume=raeume_list)
            except PermissionError as e:
                flash(str(e), "danger")
                return redirect(url_for("login.login"))

        @raum_bp.route("/raeume/<int:raum_id>")
        def raum_detail(raum_id):
            user = _get_user()
            if not user:
                return redirect(url_for("login.login"))
            try:
                raum = controller.raum_anzeigen_service.execute(user, raumId=raum_id)
                if not raum:
                    flash("Raum nicht gefunden.", "warning")
                    return redirect(url_for("raum.raeume"))
                return render_template("raum_detail.html", raum=raum)
            except PermissionError as e:
                flash(str(e), "danger")
                return redirect(url_for("raum.raeume"))

        @raum_bp.route("/raeume/<int:raum_id>/installieren", methods=["POST"])
        def installieren(raum_id):
            user = _get_user()
            if not user:
                return redirect(url_for("login.login"))
            geraet_id = request.form.get("geraet_id", type=int)
            try:
                controller.geraet_installieren_service.execute(user, geraet_id, raum_id)
                flash("Geraet erfolgreich installiert.", "success")
            except (PermissionError, ValueError) as e:
                flash(str(e), "danger")
            return redirect(url_for("raum.raum_detail", raum_id=raum_id))

        app.register_blueprint(raum_bp)
