from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from domain.enums import GeraeteTyp, GeraeteStatus

geraete_bp = Blueprint("geraete", __name__)


class GeraeteController:
    def __init__(self, geraet_anzeigen_service, geraet_steuern_service,
                 geraet_konfigurieren_service, geraet_kalibrieren_service,
                 raum_anzeigen_service, geraet_repo, user_repo):
        self.geraet_anzeigen_service = geraet_anzeigen_service
        self.geraet_steuern_service = geraet_steuern_service
        self.geraet_konfigurieren_service = geraet_konfigurieren_service
        self.geraet_kalibrieren_service = geraet_kalibrieren_service
        self.raum_anzeigen_service = raum_anzeigen_service
        self.geraet_repo = geraet_repo
        self.user_repo = user_repo

    def register(self, app):
        controller = self

        def _get_user():
            uid = session.get("user_id")
            if uid:
                return controller.user_repo.findById(uid)
            return None

        @geraete_bp.route("/geraete")
        def geraete():
            user = _get_user()
            if not user:
                return redirect(url_for("login.login"))
            status_filter = request.args.get("status")
            try:
                geraete_list = controller.geraet_anzeigen_service.execute(
                    user, status_filter=status_filter
                )
                return render_template(
                    "geraete.html", geraete=geraete_list,
                    status_filter=status_filter,
                    alle_status=[s.value for s in GeraeteStatus],
                    alle_typen=[t.value for t in GeraeteTyp],
                )
            except PermissionError as e:
                flash(str(e), "danger")
                return redirect(url_for("login.login"))

        @geraete_bp.route("/geraete/anlegen", methods=["POST"])
        def geraet_anlegen():
            user = _get_user()
            if not user:
                return redirect(url_for("login.login"))
            from domain.enums import Berechtigung
            try:
                from application.berechtigungs_service import BerechtigungsService
                bs = BerechtigungsService()
                bs.execute(user, Berechtigung.GERAET_INSTALLIEREN)
                from domain.smart_geraet_factory import SmartGeraetFactory
                typ = GeraeteTyp(request.form["typ"])
                name = request.form["name"].strip()
                if not name:
                    raise ValueError("Name darf nicht leer sein")
                geraet = SmartGeraetFactory.create(typ, name)
                controller.geraet_repo.save(geraet)
                flash(f"Geraet '{name}' angelegt.", "success")
            except (PermissionError, ValueError) as e:
                flash(str(e), "danger")
            return redirect(url_for("geraete.geraete"))

        @geraete_bp.route("/geraete/<int:geraet_id>/steuern", methods=["POST"])
        def steuern(geraet_id):
            user = _get_user()
            if not user:
                return redirect(url_for("login.login"))
            aktion = request.form.get("aktion", "einschalten")
            try:
                controller.geraet_steuern_service.execute(user, geraet_id, aktion)
                flash(f"Geraet {aktion}.", "success")
            except (PermissionError, ValueError) as e:
                flash(str(e), "danger")
            return redirect(url_for("geraete.geraete"))

        @geraete_bp.route("/geraete/<int:geraet_id>/konfigurieren", methods=["POST"])
        def konfigurieren(geraet_id):
            user = _get_user()
            if not user:
                return redirect(url_for("login.login"))
            config = {}
            geraet = controller.geraet_repo.findById(geraet_id)
            if geraet:
                if geraet.typ == GeraeteTyp.LAMPE:
                    h = request.form.get("helligkeit")
                    if h:
                        config["helligkeit"] = int(h)
                    farbe = request.form.get("farbe")
                    if farbe:
                        config["farbe"] = farbe
                elif geraet.typ == GeraeteTyp.HEIZUNG:
                    temp = request.form.get("zieltemperatur")
                    if temp:
                        config["zieltemperatur"] = float(temp)
                elif geraet.typ == GeraeteTyp.KAMERA:
                    modus = request.form.get("modus")
                    if modus:
                        config["modus"] = modus
            try:
                controller.geraet_konfigurieren_service.execute(user, geraet_id, **config)
                flash("Konfiguration gespeichert.", "success")
            except (PermissionError, ValueError) as e:
                flash(str(e), "danger")
            return redirect(url_for("geraete.geraete"))

        @geraete_bp.route("/geraete/<int:geraet_id>/kalibrieren", methods=["POST"])
        def kalibrieren(geraet_id):
            user = _get_user()
            if not user:
                return redirect(url_for("login.login"))
            try:
                controller.geraet_kalibrieren_service.execute(user, geraet_id)
                flash("Geraet kalibriert.", "success")
            except (PermissionError, ValueError) as e:
                flash(str(e), "danger")
            return redirect(url_for("geraete.geraete"))

        app.register_blueprint(geraete_bp)
