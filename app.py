# Importaciones necesarias para la aplicación Flask
import os  # Para acceder a variables de entorno del sistema
import logging  # Para configurar y manejar logs de depuración
from flask import Flask  # Framework web principal de la aplicación
from flask_sqlalchemy import SQLAlchemy  # ORM para manejo de base de datos
from flask_login import LoginManager  # Extensión para manejo de sesiones de usuario

from sqlalchemy.orm import DeclarativeBase  # Clase base para modelos de SQLAlchemy
from werkzeug.middleware.proxy_fix import ProxyFix  # Middleware para deployment detrás de proxy

# Configurar el sistema de logging para mostrar mensajes de depuración
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    """
    Clase base declarativa para todos los modelos de SQLAlchemy.
    Esta clase proporcionará funcionalidades comunes a todos los modelos de la base de datos.
    """
    pass

# Inicializar las extensiones de Flask sin asociarlas aún a una aplicación específica
db = SQLAlchemy(model_class=Base)  # Instancia de SQLAlchemy con nuestra clase base personalizada
login_manager = LoginManager()  # Gestor de sesiones de usuario para autenticación


def crear_app():
    """
    Función factory para crear y configurar la aplicación Flask.
    Este patrón permite crear múltiples instancias de la aplicación con diferentes configuraciones.
    
    Returns:
        Flask: Instancia configurada de la aplicación Flask
    """
    # Crear la instancia principal de la aplicación Flask
    app = Flask(__name__)
    
    # === CONFIGURACIÓN DE LA APLICACIÓN ===
    # Establecer la clave secreta para sesiones desde variable de entorno
    app.secret_key = os.environ.get("SESSION_SECRET")
    
    # Configurar la URI de conexión a la base de datos
    # Si no existe DATABASE_URL en el entorno, usar SQLite como fallback
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///mediconsult.db")
    
    # Configurar opciones del motor de base de datos para PostgreSQL
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,  # Reciclar conexiones cada 5 minutos para evitar timeouts
        "pool_pre_ping": True,  # Verificar conexiones antes de usarlas
    }
    
    # Desactivar el seguimiento de modificaciones para mejorar rendimiento
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    # Configurar middleware ProxyFix para deployment detrás de un proxy reverso
    # Esto es necesario para que Flask genere URLs correctas con HTTPS
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
    
    # === INICIALIZACIÓN DE EXTENSIONES ===
    # Asociar las extensiones previamente creadas con esta instancia de la aplicación
    db.init_app(app)  # Conectar SQLAlchemy con la aplicación
    login_manager.init_app(app)  # Configurar el gestor de login

    
    # === CONFIGURACIÓN DE FLASK-LOGIN ===
    # Definir la vista de login por defecto cuando se requiere autenticación
    login_manager.login_view = 'auth.login'
    
    # Mensaje mostrado cuando el usuario necesita autenticarse
    login_manager.login_message = 'Debe iniciar sesión para acceder a esta página.'
    
    # Categoría del mensaje (para estilos de Bootstrap)
    login_manager.login_message_category = 'warning'
    
    @login_manager.user_loader
    def cargar_usuario(usuario_id):
        """
        Función callback requerida por Flask-Login para cargar un usuario por su ID.
        Esta función se ejecuta en cada request para cargar el usuario actual de la sesión.
        
        Args:
            usuario_id (str): ID del usuario a cargar desde la base de datos
            
        Returns:
            Usuario: Instancia del modelo Usuario o None si no existe
        """
        from modelos import Usuario  # Importación local para evitar dependencias circulares
        return Usuario.query.get(int(usuario_id))  # Buscar usuario por ID
    
    # === REGISTRO DE BLUEPRINTS ===
    # Importar y registrar todas las rutas de la aplicación
    from rutas import registrar_rutas
    registrar_rutas(app)  # Función que registra todos los blueprints de rutas
    
    # === INICIALIZACIÓN DE BASE DE DATOS ===
    with app.app_context():  # Crear contexto de aplicación para operaciones de BD
        # Importar todos los modelos para asegurar que las tablas se creen correctamente
        import modelos
        
        # Crear todas las tablas definidas en los modelos
        db.create_all()
        
        # === CREACIÓN DE USUARIO ADMINISTRADOR POR DEFECTO ===
        from modelos import Usuario, RolUsuario
        
        # Verificar si ya existe un administrador con el DNI por defecto
        admin_existente = Usuario.query.filter_by(dni='12345678').first()
        
        if not admin_existente:  # Si no existe, crear el usuario administrador
            from werkzeug.security import generate_password_hash
            
            # Crear instancia del usuario administrador
            admin = Usuario()
            admin.nombre = 'Administrador Sistema'  # Nombre completo del administrador
            admin.dni = '12345678'  # DNI por defecto para login
            admin.rol = RolUsuario.ADMINISTRADOR  # Asignar rol de administrador
            admin.password_hash = generate_password_hash('admin123')  # Hash seguro de la contraseña
            
            # Guardar el usuario en la base de datos
            db.session.add(admin)  # Agregar a la sesión
            db.session.commit()  # Confirmar los cambios
            
            # Guardar inmediatamente en CSV
            try:
                from respaldo_usuarios import ServicioRespaldoCSV
                ServicioRespaldoCSV.guardar_usuario_en_csv(admin)
                logging.info('Usuario administrador creado y guardado en CSV: DNI=12345678, Contraseña=admin123')
            except Exception as e:
                logging.error(f'Usuario administrador creado: DNI=12345678, Contraseña=admin123 (Error CSV: {e})')
    
    # Retornar la aplicación completamente configurada
    return app

# Crear la instancia principal de la aplicación usando el patrón factory
app = crear_app()
