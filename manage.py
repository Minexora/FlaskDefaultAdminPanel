import click
from flask.cli import FlaskGroup
from app.app import app, db
from admin.models import User, Role, Permission


def create_app():
    return app


cli = FlaskGroup(create_app=create_app)


@cli.command("create_superuser")
def create_superuser():
    with app.app_context():
        username = click.prompt("Kullanıcı adı")
        email = click.prompt("Email")
        password = click.prompt("Şifre", hide_input=True)

        user = User(username=username, email=email, is_admin=True)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()
        click.echo("Süper kullanıcı oluşturuldu!")


@cli.command("init_db")
def init_db():
    with app.app_context():
        db.create_all()
        click.echo("Veritabanı tabloları oluşturuldu!")


@cli.command("create_permissions")
def create_permissions():
    """Varsayılan yetkileri oluştur"""

    permissions = [
        {"code": "admin_access", "name": "Admin Erişimi", "description": "Admin paneline erişim"},
        {"code": "user_manage", "name": "Kullanıcı Yönetimi", "description": "Kullanıcıları yönetme yetkisi"},
        {"code": "role_manage", "name": "Rol Yönetimi", "description": "Rolleri yönetme yetkisi"},
        {"code": "permission_manage", "name": "Yetki Yönetimi", "description": "Yetkileri yönetme yetkisi"},
    ]

    for perm in permissions:
        if not Permission.query.filter_by(code=perm["code"]).first():
            permission = Permission(**perm)
            db.session.add(permission)

    db.session.commit()
    click.echo("Varsayılan yetkiler oluşturuldu!")


@cli.command("create_admin_role")
def create_admin_role():
    """Admin rolünü oluştur"""
    
    with app.app_context():
        role = Role.query.filter_by(name="Admin").first()
        if not role:
            role = Role(name="Admin", description="Tam yetkili yönetici")
            permissions = Permission.query.all()
            role.permissions = permissions
            db.session.add(role)
            db.session.commit()
            click.echo("Admin rolü oluşturuldu!")
        else:
            click.echo("Admin rolü zaten mevcut!")


if __name__ == "__main__":
    cli()
