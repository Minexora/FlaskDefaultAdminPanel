from app.app import app
from admin.admin import init_admin
from admin.urls import admin_routes


# Admin panel başlatma
admin = init_admin()

# Blueprint kayıt
app.register_blueprint(admin_routes)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
