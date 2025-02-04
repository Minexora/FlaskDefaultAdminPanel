from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, AdminIndexView, expose
from flask_login import LoginManager, login_required, current_user
from .settings import config
from flask_migrate import Migrate

# ------------------------------------
# Flask
# ------------------------------------
app = Flask(__name__)
app.config.from_object(config["default"])


# ------------------------------------
# Database
# ------------------------------------
db = SQLAlchemy()
db.init_app(app)


# ------------------------------------
#  Admin
# ------------------------------------
class AdminPanelMixin(AdminIndexView):
    @expose("/")
    @login_required
    def index(self):
        if not current_user.has_permission("admin_access"):
            return redirect(url_for("admin_blueprint.login_view"))
        return super(AdminPanelMixin, self).index()


admin = Admin(app, name="Yönetim Paneli", template_mode="bootstrap4", index_view=AdminPanelMixin())


# ------------------------------------
#  Login manager
# ------------------------------------
login_manager = LoginManager()
login_manager.init_app(app)


# ------------------------------------
#  Migrations
# ------------------------------------
migrate = Migrate(app, db)
