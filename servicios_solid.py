# ============================================================================
# IMPLEMENTACIÓN DE SERVICIOS SIGUIENDO PRINCIPIOS SOLID
# ============================================================================
"""
Este módulo implementa los servicios del sistema siguiendo estrictamente
los principios SOLID con comentarios explicativos de cada principio aplicado.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from modelos import Usuario, RolUsuario
from interfaces import (
    IRepositorioUsuario, IHasheadorPassword, IValidadorUsuario, 
    INotificadorEventos, IServicioAutenticacion, IServicioAutorizacion,
    IComando, IManejadorComandos
)


# ============================================================================
# SRP - SINGLE RESPONSIBILITY PRINCIPLE
# Cada clase tiene una sola razón para cambiar
# ============================================================================

class RepositorioUsuarioSQLAlchemy(IRepositorioUsuario):
    """
    SRP: Responsabilidad única - persistencia de usuarios con SQLAlchemy.
    
    Esta clase solo se ocupa de las operaciones CRUD de usuarios en la base
    de datos. Si cambia la forma de persistir datos, solo esta clase cambia.
    """
    
    def obtener_por_id(self, usuario_id: int) -> Optional[Usuario]:
        """
        SRP: Solo se ocupa de buscar por ID, sin lógica adicional.
        """
        return Usuario.query.get(usuario_id)
    
    def obtener_por_dni(self, dni: str) -> Optional[Usuario]:
        """
        SRP: Solo se ocupa de buscar por DNI, sin validaciones.
        """
        return Usuario.query.filter_by(dni=dni).first()
    
    def obtener_por_matricula(self, codigo_matricula: str) -> Optional[Usuario]:
        """
        SRP: Solo se ocupa de buscar por matrícula, sin validaciones.
        """
        return Usuario.query.filter_by(codigo_matricula=codigo_matricula).first()
    
    def guardar(self, usuario: Usuario) -> Usuario:
        """
        SRP: Solo se ocupa de persistir el usuario, sin lógica de negocio.
        """
        db.session.add(usuario)
        db.session.commit()
        return usuario
    
    def listar_todos(self) -> List[Usuario]:
        """
        SRP: Solo se ocupa de listar usuarios, sin filtros de negocio.
        """
        return Usuario.query.all()


class HasheadorPasswordWerkzeug(IHasheadorPassword):
    """
    SRP: Responsabilidad única - manejo de hashes de contraseñas.
    
    Esta clase solo se ocupa del hashing y verificación de contraseñas.
    Si cambia el algoritmo de hash, solo esta clase cambia.
    """
    
    def hashear_password(self, password: str) -> str:
        """
        SRP: Solo hashea contraseñas, sin validaciones adicionales.
        """
        return generate_password_hash(password)
    
    def verificar_password(self, password: str, hash_password: str) -> bool:
        """
        SRP: Solo verifica contraseñas, sin lógica de autenticación.
        """
        return check_password_hash(hash_password, password)


class ValidadorUsuario(IValidadorUsuario):
    """
    SRP: Responsabilidad única - validación de datos de usuario.
    
    Esta clase solo se ocupa de validar datos. Si cambian las reglas
    de validación, solo esta clase cambia.
    """
    
    def validar_datos_creacion(self, datos: Dict[str, Any]) -> bool:
        """
        SRP: Solo valida datos para creación, sin lógica de persistencia.
        """
        # Validar campos obligatorios
        if not datos.get('nombre') or not datos.get('password'):
            return False
        
        # Validar rol
        if datos.get('rol') not in [rol.value for rol in RolUsuario]:
            return False
        
        # Validar que tenga al menos DNI o código de matrícula
        if not datos.get('dni') and not datos.get('codigo_matricula'):
            return False
        
        return True
    
    def validar_credenciales(self, identificador: str, password: str) -> bool:
        """
        SRP: Solo valida formato de credenciales, sin autenticación.
        """
        return bool(identificador and password and len(password) >= 6)


class NotificadorEventosLog(INotificadorEventos):
    """
    SRP: Responsabilidad única - notificación de eventos del sistema.
    
    Esta clase solo se ocupa de notificar eventos. Si cambia el medio
    de notificación (email, SMS), solo esta clase cambia.
    """
    
    def notificar_usuario_creado(self, usuario: Usuario) -> None:
        """
        SRP: Solo notifica creación de usuario, sin lógica adicional.
        """
        print(f"[LOG] Usuario creado: {usuario.nombre} ({usuario.rol.value})")
    
    def notificar_login_exitoso(self, usuario: Usuario) -> None:
        """
        SRP: Solo notifica login exitoso, sin lógica de auditoría.
        """
        print(f"[LOG] Login exitoso: {usuario.nombre} - {datetime.now()}")
    
    def notificar_login_fallido(self, identificador: str) -> None:
        """
        SRP: Solo notifica login fallido, sin lógica de seguridad.
        """
        print(f"[LOG] Login fallido: {identificador} - {datetime.now()}")


# ============================================================================
# DIP - DEPENDENCY INVERSION PRINCIPLE
# Dependencias hacia abstracciones, no hacia concreciones
# ============================================================================

class ServicioAutenticacionSOLID(IServicioAutenticacion):
    """
    DIP: Depende de abstracciones (interfaces) no de implementaciones concretas.
    SRP: Responsabilidad única - autenticación de usuarios.
    OCP: Abierto para extensión (nuevos métodos) cerrado para modificación.
    
    Las dependencias se inyectan desde el exterior, permitiendo diferentes
    implementaciones sin cambiar esta clase.
    """
    
    def __init__(
        self,
        repositorio_usuario: IRepositorioUsuario,
        hasheador_password: IHasheadorPassword,
        validador_usuario: IValidadorUsuario,
        notificador_eventos: INotificadorEventos
    ):
        """
        DIP: Inyección de dependencias - todas las dependencias son abstracciones.
        
        Esto permite testing fácil y flexibilidad en las implementaciones.
        """
        self._repositorio_usuario = repositorio_usuario
        self._hasheador_password = hasheador_password
        self._validador_usuario = validador_usuario
        self._notificador_eventos = notificador_eventos
    
    def autenticar(self, identificador: str, password: str) -> Optional[Usuario]:
        """
        SRP: Solo se ocupa de autenticar usuarios.
        DIP: Usa abstracciones para todas las operaciones.
        """
        # Validar credenciales usando el validador inyectado
        if not self._validador_usuario.validar_credenciales(identificador, password):
            self._notificador_eventos.notificar_login_fallido(identificador)
            return None
        
        # Buscar usuario usando el repositorio inyectado
        usuario = None
        if identificador.isdigit():
            usuario = self._repositorio_usuario.obtener_por_dni(identificador)
        
        if not usuario:
            usuario = self._repositorio_usuario.obtener_por_matricula(identificador)
        
        # Verificar contraseña usando el hasheador inyectado
        if usuario and usuario.activo and self._hasheador_password.verificar_password(password, usuario.password_hash):
            self._notificador_eventos.notificar_login_exitoso(usuario)
            return usuario
        
        self._notificador_eventos.notificar_login_fallido(identificador)
        return None
    
    def crear_usuario(self, datos: Dict[str, Any]) -> Usuario:
        """
        SRP: Solo se ocupa de crear usuarios.
        DIP: Usa abstracciones para todas las operaciones.
        """
        # Validar datos usando el validador inyectado
        if not self._validador_usuario.validar_datos_creacion(datos):
            raise ValueError("Datos de usuario inválidos")
        
        # Crear usuario
        usuario = Usuario()
        usuario.nombre = datos['nombre']
        usuario.rol = RolUsuario[datos['rol']]
        usuario.dni = datos.get('dni')
        usuario.codigo_matricula = datos.get('codigo_matricula')
        usuario.password_hash = self._hasheador_password.hashear_password(datos['password'])
        
        # Guardar usando el repositorio inyectado
        usuario_guardado = self._repositorio_usuario.guardar(usuario)
        
        # Notificar usando el notificador inyectado
        self._notificador_eventos.notificar_usuario_creado(usuario_guardado)
        
        return usuario_guardado


class ServicioAutorizacionRBACSOLID(IServicioAutorizacion):
    """
    SRP: Responsabilidad única - autorización basada en roles.
    OCP: Extensible para nuevos roles y permisos.
    
    Implementa autorización basada en roles (RBAC) de forma extensible.
    """
    
    def __init__(self):
        """
        OCP: Los permisos están definidos de forma extensible.
        Nuevos roles y permisos se pueden agregar sin modificar el código existente.
        """
        self._permisos_por_rol = {
            RolUsuario.ADMINISTRADOR: {
                'usuarios': ['crear', 'leer', 'actualizar', 'eliminar'],
                'citas': ['crear', 'leer', 'actualizar', 'eliminar'],
                'consultas': ['crear', 'leer', 'actualizar', 'eliminar'],
                'reportes': ['leer', 'generar'],
            },
            RolUsuario.PROFESIONAL: {
                'citas': ['leer', 'actualizar'],
                'consultas': ['crear', 'leer', 'actualizar'],
                'pacientes': ['leer'],
            },
            RolUsuario.PACIENTE: {
                'citas': ['leer'],
                'consultas': ['leer'],
                'perfil': ['leer', 'actualizar'],
            }
        }
    
    def tiene_permiso(self, usuario: Usuario, recurso: str, accion: str) -> bool:
        """
        SRP: Solo verifica permisos, sin lógica adicional.
        OCP: Extensible para nuevos recursos y acciones.
        """
        if not usuario or not usuario.activo:
            return False
        
        permisos_usuario = self._permisos_por_rol.get(usuario.rol, {})
        acciones_permitidas = permisos_usuario.get(recurso, [])
        
        return accion in acciones_permitidas
    
    def obtener_roles_usuario(self, usuario: Usuario) -> List[str]:
        """
        SRP: Solo obtiene roles, sin lógica de permisos.
        """
        return [usuario.rol.value] if usuario else []


# ============================================================================
# COMMAND PATTERN PARA SRP Y OCP
# ============================================================================

class ComandoCrearUsuario(IComando):
    """
    SRP: Responsabilidad única - comando para crear usuario.
    OCP: Extensible para nuevos tipos de validaciones y procesamiento.
    
    Encapsula toda la lógica necesaria para crear un usuario.
    """
    
    def __init__(self, datos_usuario: Dict[str, Any], servicio_auth: IServicioAutenticacion):
        """
        DIP: Depende de abstracción del servicio de autenticación.
        """
        self._datos_usuario = datos_usuario
        self._servicio_auth = servicio_auth
    
    def validar(self) -> bool:
        """
        SRP: Solo valida si el comando puede ejecutarse.
        """
        campos_requeridos = ['nombre', 'rol', 'password']
        return all(self._datos_usuario.get(campo) for campo in campos_requeridos)
    
    def ejecutar(self) -> Usuario:
        """
        SRP: Solo ejecuta la creación del usuario.
        """
        if not self.validar():
            raise ValueError("Datos insuficientes para crear usuario")
        
        return self._servicio_auth.crear_usuario(self._datos_usuario)


class ManejadorComandos(IManejadorComandos):
    """
    SRP: Responsabilidad única - manejar ejecución de comandos.
    OCP: Extensible para nuevos tipos de comandos y manejo de errores.
    """
    
    def manejar(self, comando: IComando) -> Any:
        """
        SRP: Solo maneja la ejecución, sin lógica específica de comandos.
        LSP: Cualquier implementación de IComando puede ser manejada.
        """
        try:
            if not comando.validar():
                raise ValueError("Comando no válido")
            
            resultado = comando.ejecutar()
            print(f"[LOG] Comando ejecutado exitosamente: {type(comando).__name__}")
            return resultado
            
        except Exception as e:
            print(f"[ERROR] Error ejecutando comando {type(comando).__name__}: {e}")
            raise


# ============================================================================
# FACTORY PARA DIP E IOC
# ============================================================================

class FactoriaServiciosProduccion:
    """
    DIP: Factory que crea todas las dependencias del sistema.
    SRP: Responsabilidad única - creación de servicios.
    
    Centraliza la creación de servicios y sus dependencias,
    facilitando el testing y la configuración.
    """
    
    @staticmethod
    def crear_servicio_autenticacion() -> IServicioAutenticacion:
        """
        DIP: Crea el servicio de autenticación con todas sus dependencias inyectadas.
        
        Permite cambiar implementaciones sin modificar el código cliente.
        """
        repositorio = RepositorioUsuarioSQLAlchemy()
        hasheador = HasheadorPasswordWerkzeug()
        validador = ValidadorUsuario()
        notificador = NotificadorEventosLog()
        
        return ServicioAutenticacionSOLID(
            repositorio, hasheador, validador, notificador
        )
    
    @staticmethod
    def crear_servicio_autorizacion() -> IServicioAutorizacion:
        """
        SRP: Solo crea el servicio de autorización.
        """
        return ServicioAutorizacionRBACSOLID()
    
    @staticmethod
    def crear_manejador_comandos() -> IManejadorComandos:
        """
        SRP: Solo crea el manejador de comandos.
        """
        return ManejadorComandos()


# ============================================================================
# COMENTARIOS SOBRE PRINCIPIOS SOLID APLICADOS
# ============================================================================

"""
RESUMEN DE PRINCIPIOS SOLID APLICADOS:

1. SINGLE RESPONSIBILITY PRINCIPLE (SRP):
   ✓ RepositorioUsuarioSQLAlchemy: Solo maneja persistencia
   ✓ HasheadorPasswordWerkzeug: Solo maneja hashing
   ✓ ValidadorUsuario: Solo maneja validaciones
   ✓ NotificadorEventosLog: Solo maneja notificaciones
   ✓ ServicioAutenticacionSOLID: Solo maneja autenticación
   ✓ ServicioAutorizacionRBACSOLID: Solo maneja autorización

2. OPEN/CLOSED PRINCIPLE (OCP):
   ✓ Interfaces permiten extensión sin modificación
   ✓ Sistema de permisos extensible para nuevos roles
   ✓ Command pattern permite nuevos comandos sin cambiar el manejador

3. LISKOV SUBSTITUTION PRINCIPLE (LSP):
   ✓ Cualquier implementación de IRepositorioUsuario es intercambiable
   ✓ Cualquier implementación de IHasheadorPassword es intercambiable
   ✓ Todas las interfaces definen contratos que se deben cumplir

4. INTERFACE SEGREGATION PRINCIPLE (ISP):
   ✓ Interfaces pequeñas y específicas (IRepositorioUsuario, IHasheadorPassword, etc.)
   ✓ Clients solo dependen de métodos que realmente usan
   ✓ No hay interfaces "gordas" con métodos innecesarios

5. DEPENDENCY INVERSION PRINCIPLE (DIP):
   ✓ ServicioAutenticacionSOLID depende de abstracciones, no de concreciones
   ✓ Inyección de dependencias en constructores
   ✓ Factory pattern para crear dependencias
   ✓ Alto nivel no depende de bajo nivel, ambos dependen de abstracciones
"""