from flask import Blueprint, render_template, request, redirect, url_for, flash, session, send_file
from domain.enums import Rolle
import os

admin_bp = Blueprint("admin", __name__)


class AdminController:
    def __init__(self, user_verwalten_service, daten_backup_service,
                 daten_export_service, daten_import_service,
                 backup_repo, import_service, user_repo):
        self.user_verwalten_service = user_verwalten_service
        self.daten_backup_service = daten_backup_service
        self.daten_export_service = daten_export_service
        self.daten_import_service = daten_import_service
        self.backup_repo = backup_repo
        self.import_service = import_service
        self.user_repo = user_repo

    def register(self, app):
        controller = self

        def _get_user():
            uid = session.get("user_id")
            if uid:
                return controller.user_repo.findById(uid)
            return None

        @admin_bp.route("/admin")
        def admin():
            user = _get_user()
            if not user:
                return redirect(url_for("login.login"))
            if user.rolle != Rolle.ADMIN:
                flash("Nur Admins haben Zugriff auf die Verwaltung.", "danger")
                return redirect(url_for("raum.raeume"))
            try:
                users = controller.user_verwalten_service.execute(user, "alle_anzeigen")
                jobs = controller.backup_repo.findJobs()
                import_files = controller.import_service.list_files()
                return render_template(
                    "admin.html", users=users, jobs=jobs,
                    import_files=import_files,
                    rollen=[r.value for r in Rolle],
                )
            except PermissionError as e:
                flash(str(e), "danger")
                return redirect(url_for("raum.raeume"))

        @admin_bp.route("/admin/user/anlegen", methods=["POST"])
        def user_anlegen():
            user = _get_user()
            if not user:
                return redirect(url_for("login.login"))
            try:
                controller.user_verwalten_service.execute(
                    user, "anlegen",
                    username=request.form["username"].strip(),
                    password=request.form["password"],
                    anzeigename=request.form.get("anzeigename", "").strip(),
                    rolle=request.form.get("rolle", "VIEWER"),
                )
                flash("Benutzer angelegt.", "success")
            except (PermissionError, ValueError, Exception) as e:
                flash(str(e), "danger")
            return redirect(url_for("admin.admin"))

        @admin_bp.route("/admin/user/<int:user_id>/rolle", methods=["POST"])
        def user_rolle(user_id):
            user = _get_user()
            if not user:
                return redirect(url_for("login.login"))
            try:
                controller.user_verwalten_service.execute(
                    user, "rolle_aendern",
                    userId=user_id,
                    rolle=request.form["rolle"],
                )
                flash("Rolle geaendert.", "success")
            except (PermissionError, ValueError) as e:
                flash(str(e), "danger")
            return redirect(url_for("admin.admin"))

        @admin_bp.route("/admin/user/<int:user_id>/toggle", methods=["POST"])
        def user_toggle(user_id):
            user = _get_user()
            if not user:
                return redirect(url_for("login.login"))
            aktion = request.form.get("aktion", "deaktivieren")
            try:
                controller.user_verwalten_service.execute(user, aktion, userId=user_id)
                flash(f"Benutzer {aktion}.", "success")
            except (PermissionError, ValueError) as e:
                flash(str(e), "danger")
            return redirect(url_for("admin.admin"))

        @admin_bp.route("/admin/backup", methods=["POST"])
        def backup():
            user = _get_user()
            if not user:
                return redirect(url_for("login.login"))
            try:
                filepath = controller.daten_backup_service.execute(user)
                flash(f"Backup erstellt: {os.path.basename(filepath)}", "success")
            except PermissionError as e:
                flash(str(e), "danger")
            return redirect(url_for("admin.admin"))

        @admin_bp.route("/admin/export", methods=["POST"])
        def export():
            user = _get_user()
            if not user:
                return redirect(url_for("login.login"))
            export_typ = request.form.get("export_typ", "vollstaendig")
            format = request.form.get("format", "json")
            try:
                filepath = controller.daten_export_service.execute(
                    user, export_typ=export_typ, format=format
                )
                flash(f"Export erstellt: {os.path.basename(filepath)}", "success")
            except PermissionError as e:
                flash(str(e), "danger")
            return redirect(url_for("admin.admin"))

        @admin_bp.route("/admin/import", methods=["POST"])
        def import_data():
            user = _get_user()
            if not user:
                return redirect(url_for("login.login"))
            filename = request.form.get("filename", "")
            if not filename:
                uploaded = request.files.get("file")
                if uploaded and uploaded.filename:
                    import_dir = controller.import_service.import_dir
                    os.makedirs(import_dir, exist_ok=True)
                    filepath = os.path.join(import_dir, uploaded.filename)
                    uploaded.save(filepath)
                    filename = uploaded.filename
            if not filename:
                flash("Keine Datei ausgewaehlt.", "warning")
                return redirect(url_for("admin.admin"))
            try:
                protokoll = controller.daten_import_service.execute(user, filename)
                if protokoll.get("fehler"):
                    for fehler in protokoll["fehler"]:
                        flash(f"Import-Fehler: {fehler}", "danger")
                else:
                    flash(
                        f"Import erfolgreich: {protokoll.get('importiert_raeume', 0)} Raeume, "
                        f"{protokoll.get('importiert_geraete', 0)} Geraete",
                        "success",
                    )
            except (PermissionError, FileNotFoundError) as e:
                flash(str(e), "danger")
            return redirect(url_for("admin.admin"))

        @admin_bp.route("/admin/download/<path:filename>")
        def download(filename):
            user = _get_user()
            if not user or user.rolle != Rolle.ADMIN:
                flash("Kein Zugriff.", "danger")
                return redirect(url_for("login.login"))
            for base_dir in ["/app/backups", "/app/exports"]:
                filepath = os.path.join(base_dir, os.path.basename(filename))
                if os.path.exists(filepath):
                    return send_file(filepath, as_attachment=True)
            flash("Datei nicht gefunden.", "warning")
            return redirect(url_for("admin.admin"))

        app.register_blueprint(admin_bp)
