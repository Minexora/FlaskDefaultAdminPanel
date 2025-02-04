from flask import Blueprint
from .views import index_view, login_view, logout_view


admin_routes = Blueprint("admin_blueprint", __name__, url_prefix="/admin", template_folder="templates")

routes = [
    {"url": "/", "view_func": index_view, "endpoint": "index_view", "methods": ["GET"]},
    {"url": "/login", "view_func": login_view, "endpoint": "login_view", "methods": ["GET", "POST"]},
    {"url": "/logout", "view_func": logout_view, "endpoint": "logout_view", "methods": ["GET"]},
]

for route in routes:
    admin_routes.add_url_rule(route["url"], endpoint=route["endpoint"], view_func=route["view_func"], methods=route["methods"])
