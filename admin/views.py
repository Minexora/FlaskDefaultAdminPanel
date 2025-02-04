from flask import redirect, url_for, render_template, request, flash
from flask_login import login_user, logout_user, current_user
from .models import User


def index_view():
    if not current_user.is_authenticated:
        return redirect(url_for("admin_blueprint.login_view"))
    return redirect(url_for("admin.index"))


def login_view():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for("admin.index"))
        flash("Geçersiz kullanıcı adı veya şifre")
    return render_template("admin/login.html")


def logout_view():
    logout_user()
    return redirect(url_for("admin_blueprint.login_view"))
