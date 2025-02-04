from .models import User, Role, Permission
from app.app import db, admin, login_manager
from wtforms import PasswordField, StringField, TextAreaField
from wtforms.validators import DataRequired
from wtforms_sqlalchemy.fields import QuerySelectMultipleField
from flask_wtf import FlaskForm
from .mixins import BaseSecureModelMixin


class UserModelView(BaseSecureModelMixin):
    required_permission = "user_manage"
    can_create = True
    can_edit = True
    can_delete = True

    column_exclude_list = ["password_hash"]
    column_searchable_list = ["username", "email"]
    column_filters = ["is_admin"]
    column_list = ["username", "email", "is_admin", "roles"]

    form_excluded_columns = ["password_hash"]

    def scaffold_form(self):
        form_class = super(UserModelView, self).scaffold_form()
        form_class.password = PasswordField("Şifre")
        return form_class

    def on_model_change(self, form, model, is_created):
        if form.password.data:
            model.set_password(form.password.data)


class RoleForm(FlaskForm):
    name = StringField("İsim", validators=[DataRequired()])
    description = TextAreaField("Açıklama")
    permissions = QuerySelectMultipleField("Yetkiler", query_factory=lambda: Permission.query.all(), get_label="name")


class RoleModelView(BaseSecureModelMixin):
    required_permission = "role_manage"
    form = RoleForm
    can_create = True
    can_edit = True
    can_delete = True

    column_list = ["name", "description", "permissions"]
    column_searchable_list = ["name"]

    def create_form(self, obj=None):
        form = super(RoleModelView, self).create_form(obj)
        if hasattr(form, "permissions"):
            form.permissions.query_factory = lambda: Permission.query.all()
        return form

    def edit_form(self, obj=None):
        form = super(RoleModelView, self).edit_form(obj)
        if hasattr(form, "permissions"):
            form.permissions.query_factory = lambda: Permission.query.all()
        return form


class PermissionModelView(BaseSecureModelMixin):
    required_permission = "permission_manage"
    can_create = True
    can_edit = True
    can_delete = True

    column_list = ["name", "code", "description"]
    column_searchable_list = ["name", "code"]
    form_columns = ["name", "code", "description"]


def init_admin():
    # ------------------------------------
    # Admin panel tables to show
    # ------------------------------------
    admin.add_view(UserModelView(User, db.session, name="Kullanıcılar"))
    admin.add_view(RoleModelView(Role, db.session, name="Roller"))
    admin.add_view(PermissionModelView(Permission, db.session, name="Yetkiler"))

    # ------------------------------------
    # Login manager set user and login url
    # ------------------------------------
    login_manager.login_view = "admin_blueprint.login_view"

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return admin
