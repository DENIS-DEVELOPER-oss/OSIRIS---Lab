# ============================================================================
# PRINCIPIOS SOLID - INTERFACES Y CONTRATOS
# ============================================================================
"""
Este módulo define interfaces y contratos siguiendo los principios SOLID:

1. SINGLE RESPONSIBILITY PRINCIPLE (SRP): Cada interfaz tiene una sola responsabilidad
2. OPEN/CLOSED PRINCIPLE (OCP): Las interfaces permiten extensión sin modificación
3. LISKOV SUBSTITUTION PRINCIPLE (LSP): Las implementaciones pueden sustituirse
4. INTERFACE SEGREGATION PRINCIPLE (ISP): Interfaces específicas y cohesivas
5. DEPENDENCY INVERSION PRINCIPLE (DIP): Dependencias hacia abstracciones
"""

from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any
from datetime import datetime


# ============================================================================
# ISP - INTERFACE SEGREGATION PRINCIPLE
# Interfaces pequeñas y específicas en lugar de una interfaz monolítica
# ============================================================================

class IRepositorioUsuario(ABC):
    """
    ISP: Interfaz específica para operaciones de repositorio de usuarios.
    
    Esta interfaz define solo las operaciones necesarias para la persistencia
    de usuarios, separando la responsabilidad del acceso a datos de la lógica
    de negocio.
    """
    
    @abstractmethod
    def obtener_por_id(self, usuario_id: int) -> Optional[Any]:
        """Obtiene un usuario por su ID"""
        pass
    
    @abstractmethod
    def obtener_por_dni(self, dni: str) -> Optional[Any]:
        """Obtiene un usuario por su DNI"""
        pass
    
    @abstractmethod
    def obtener_por_matricula(self, codigo_matricula: str) -> Optional[Any]:
        """Obtiene un usuario por su código de matrícula"""
        pass
    
    @abstractmethod
    def guardar(self, usuario: Any) -> Any:
        """Guarda un usuario en el repositorio"""
        pass
    
    @abstractmethod
    def listar_todos(self) -> List[Any]:
        """Lista todos los usuarios"""
        pass


class IHasheadorPassword(ABC):
    """
    ISP: Interfaz específica para el manejo de contraseñas.
    
    Separa la responsabilidad de hashear y verificar contraseñas,
    permitiendo diferentes implementaciones (bcrypt, argon2, etc.)
    """
    
    @abstractmethod
    def hashear_password(self, password: str) -> str:
        """Genera un hash seguro de la contraseña"""
        pass
    
    @abstractmethod
    def verificar_password(self, password: str, hash_password: str) -> bool:
        """Verifica si una contraseña coincide con su hash"""
        pass


class IValidadorUsuario(ABC):
    """
    ISP: Interfaz específica para validación de datos de usuario.
    
    Separa la lógica de validación de la lógica de negocio,
    permitiendo diferentes estrategias de validación.
    """
    
    @abstractmethod
    def validar_datos_creacion(self, datos: Dict[str, Any]) -> bool:
        """Valida los datos para crear un usuario"""
        pass
    
    @abstractmethod
    def validar_credenciales(self, identificador: str, password: str) -> bool:
        """Valida las credenciales de acceso"""
        pass


class INotificadorEventos(ABC):
    """
    ISP: Interfaz específica para notificación de eventos del sistema.
    
    Permite diferentes implementaciones de notificación (email, SMS, log, etc.)
    sin acoplar la lógica de negocio a una implementación específica.
    """
    
    @abstractmethod
    def notificar_usuario_creado(self, usuario: Any) -> None:
        """Notifica que se ha creado un nuevo usuario"""
        pass
    
    @abstractmethod
    def notificar_login_exitoso(self, usuario: Any) -> None:
        """Notifica un login exitoso"""
        pass
    
    @abstractmethod
    def notificar_login_fallido(self, identificador: str) -> None:
        """Notifica un intento de login fallido"""
        pass


# ============================================================================
# SRP + OCP - SERVICIOS BASE EXTENSIBLES
# ============================================================================

class IServicioAutenticacion(ABC):
    """
    SRP: Servicio con responsabilidad única de autenticación.
    OCP: Abierto para extensión (nuevos métodos de auth) cerrado para modificación.
    
    Define el contrato para servicios de autenticación, permitiendo
    diferentes implementaciones sin cambiar el código cliente.
    """
    
    @abstractmethod
    def autenticar(self, identificador: str, password: str) -> Optional[Any]:
        """Autentica un usuario con sus credenciales"""
        pass
    
    @abstractmethod
    def crear_usuario(self, datos: Dict[str, Any]) -> Any:
        """Crea un nuevo usuario en el sistema"""
        pass


class IServicioAutorizacion(ABC):
    """
    SRP: Servicio con responsabilidad única de autorización.
    
    Separa la autorización de la autenticación, permitiendo
    diferentes estrategias de control de acceso.
    """
    
    @abstractmethod
    def tiene_permiso(self, usuario: Any, recurso: str, accion: str) -> bool:
        """Verifica si un usuario tiene permiso para una acción en un recurso"""
        pass
    
    @abstractmethod
    def obtener_roles_usuario(self, usuario: Any) -> List[str]:
        """Obtiene los roles de un usuario"""
        pass


# ============================================================================
# FACTORY PATTERN PARA DIP
# ============================================================================

class IFactoriaServicios(ABC):
    """
    DIP: Factory que permite inyectar dependencias de forma flexible.
    
    Permite crear servicios sin acoplar el código a implementaciones específicas,
    facilitando testing y mantenimiento.
    """
    
    @abstractmethod
    def crear_servicio_autenticacion(self) -> IServicioAutenticacion:
        """Crea una instancia del servicio de autenticación"""
        pass
    
    @abstractmethod
    def crear_repositorio_usuario(self) -> IRepositorioUsuario:
        """Crea una instancia del repositorio de usuarios"""
        pass
    
    @abstractmethod
    def crear_hasheador_password(self) -> IHasheadorPassword:
        """Crea una instancia del hasheador de contraseñas"""
        pass
    
    @abstractmethod
    def crear_validador_usuario(self) -> IValidadorUsuario:
        """Crea una instancia del validador de usuarios"""
        pass
    
    @abstractmethod
    def crear_notificador_eventos(self) -> INotificadorEventos:
        """Crea una instancia del notificador de eventos"""
        pass


# ============================================================================
# COMMAND PATTERN PARA SRP Y OCP
# ============================================================================

class IComando(ABC):
    """
    SRP + OCP: Comando con responsabilidad única que es extensible.
    
    Encapsula una acción específica del sistema, permitiendo
    desacoplar la invocación de la ejecución.
    """
    
    @abstractmethod
    def ejecutar(self) -> Any:
        """Ejecuta el comando"""
        pass
    
    @abstractmethod
    def validar(self) -> bool:
        """Valida si el comando puede ejecutarse"""
        pass


class IManejadorComandos(ABC):
    """
    SRP: Maneja la ejecución de comandos.
    OCP: Extensible para nuevos tipos de comandos.
    """
    
    @abstractmethod
    def manejar(self, comando: IComando) -> Any:
        """Maneja la ejecución de un comando"""
        pass