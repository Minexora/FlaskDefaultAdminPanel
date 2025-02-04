from flask import redirect, url_for, flash
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user


class BaseSecureModelMixin(ModelView):
    required_permission = None

    def is_accessible(self):
        if current_user.is_authenticated:
            if self.required_permission:
                return current_user.has_permission(self.required_permission)
            return True
        return False

    def inaccessible_callback(self, name, **kwargs):
        flash("Bu sayfaya erişim yetkiniz yok.", "error")
        return redirect(url_for("admin_blueprint.login_view"))
