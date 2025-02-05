from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.app import db

# Rol ve Yetki ilişki tablosu
role_permissions = db.Table("role_permissions", db.Column("role_id", db.Integer, db.ForeignKey("role.id")), db.Column("permission_id", db.Integer, db.ForeignKey("permission.id")))


# Kullanıcı ve Rol ilişki tablosu
user_roles = db.Table("user_roles", db.Column("user_id", db.Integer, db.ForeignKey("user.id")), db.Column("role_id", db.Integer, db.ForeignKey("role.id")))


class Permission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    code = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Permission {self.name}>"


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255))
    permissions = db.relationship("Permission", secondary=role_permissions, backref=db.backref("roles", lazy="dynamic"))

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Role {self.name}>"


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    roles = db.relationship("Role", secondary=user_roles, backref=db.backref("users", lazy="dynamic"))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def has_permission(self, permission_code):
        if self.is_admin:
            return True
        for role in self.roles:
            for permission in role.permissions:
                if permission.code == permission_code:
                    return True
        return False

    def __str__(self):
        return self.username

    def __repr__(self):
        return f"<User {self.username}>"
