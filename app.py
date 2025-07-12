# Importaciones necesarias para la aplicación Flask
import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Configuración del sistema de logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

# Inicialización de extensiones
db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()

def crear_app():
    """
    Crea y configura la aplicación Flask.
    """
    app = Flask(__name__)

    # ✅ Desactivar CSRF (para desarrollo, no recomendado en producción)
    app.config['WTF_CSRF_ENABLED'] = False

    # Configuración de clave secreta (aunque esté desactivado CSRF, sigue siendo útil para sesiones)
    app.secret_key = os.environ.get("SESSION_SECRET", "clave_predeterminada_para_dev")

    # Configuración de base de datos
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///mediconsult.db")
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Middleware para entornos con proxy reverso
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

    # Inicialización de extensiones
    db.init_app(app)
    login_manager.init_app(app)

    # Configuración de Flask-Login
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Debe iniciar sesión para acceder a esta página.'
    login_manager.login_message_category = 'warning'

    @login_manager.user_loader
    def cargar_usuario(usuario_id):
        from modelos import Usuario
        return Usuario.query.get(int(usuario_id))

    # Registro de rutas
    from rutas import registrar_rutas
    registrar_rutas(app)

    # Inicialización de base de datos
    with app.app_context():
        import modelos
        db.create_all()

        from modelos import Usuario, RolUsuario
        admin_existente = Usuario.query.filter_by(dni='12345678').first()
        if not admin_existente:
            from werkzeug.security import generate_password_hash
            admin = Usuario()
            admin.nombre = 'DENIS ADMIN'
            admin.dni = '12345678'
            admin.rol = RolUsuario.ADMINISTRADOR
            admin.password_hash = generate_password_hash('admin123')
            db.session.add(admin)
            db.session.commit()

            try:
                from respaldo_usuarios import ServicioRespaldoCSV
                ServicioRespaldoCSV.guardar_usuario_en_csv(admin)
                logging.info('Usuario administrador creado y guardado en CSV: DNI=12345678, Contraseña=admin123')
            except Exception as e:
                logging.error(f'Usuario administrador creado: DNI=12345678, Contraseña=admin123 (Error CSV: {e})')

    return app

# Instanciar aplicación
app = crear_app()
