# ============================================================================
# DECORADORES DE SEGURIDAD CON PRINCIPIOS SOLID
# ============================================================================
"""
PRINCIPIOS SOLID APLICADOS EN DECORADORES:

SRP: Cada decorador tiene una responsabilidad específica:
- requiere_login: Solo verifica autenticación
- requiere_rol: Solo verifica autorización por rol específico  
- requiere_administrador: Solo verifica rol de administrador
- requiere_profesional: Solo verifica rol de profesional

OCP: Los decoradores son extensibles:
- Se pueden crear nuevos decoradores sin modificar los existentes
- Composición de decoradores para requerimientos complejos

DIP: Los decoradores dependen de abstracciones:
- current_user (Flask-Login abstraction)
- RolUsuario (enumeración, no valores hardcodeados)
"""

# Importaciones necesarias para la creación de decoradores de seguridad
from functools import wraps  # Para preservar metadatos de funciones decoradas
from flask import abort, redirect, url_for, flash  # Funciones de Flask para control de flujo y mensajes
from flask_login import current_user  # Para acceder al usuario actualmente autenticado
from modelos import RolUsuario  # Enumeración de roles del sistema

def requiere_login(f):
    """
    PRINCIPIOS SOLID APLICADOS:
    
    SRP: Este decorador tiene una sola responsabilidad - verificar autenticación.
    No se mezcla con autorización ni otras preocupaciones de seguridad.
    
    OCP: Abierto para extensión - se puede combinar con otros decoradores.
    Cerrado para modificación - agregar nuevos tipos de auth no requiere cambiar este código.
    
    DIP: Depende de la abstracción current_user, no de implementaciones específicas
    de autenticación (sesiones, tokens, etc.).
    
    Decorador que requiere autenticación de usuario para acceder a una vista.
    
    Este decorador verifica que el usuario esté autenticado antes de permitir
    el acceso a la función decorada. Si no está autenticado, redirige al login.
    
    Args:
        f: Función de vista a decorar
        
    Returns:
        function: Función decorada con verificación de autenticación
    """
    @wraps(f)  # Preservar metadatos de la función original
    def decorated_function(*args, **kwargs):
        """
        Función interna que implementa la verificación de autenticación.
        
        Args:
            *args: Argumentos posicionales de la función original
            **kwargs: Argumentos de palabra clave de la función original
            
        Returns:
            Response: Respuesta de la función original o redirección al login
        """
        # Verificar si el usuario está autenticado
        if not current_user.is_authenticated:
            # Mostrar mensaje de advertencia al usuario
            flash('Debe iniciar sesión para acceder a esta página.', 'warning')
            # Redirigir a la página de login
            return redirect(url_for('auth.login'))
        
        # Si está autenticado, ejecutar la función original
        return f(*args, **kwargs)
    
    return decorated_function  # Retornar la función decorada

def requiere_rol(rol_requerido):
    """
    PRINCIPIOS SOLID APLICADOS:
    
    SRP: Responsabilidad única - verificar autorización por rol específico.
    No maneja autenticación (se asume) ni otros tipos de autorización.
    
    OCP: Extensible para cualquier nuevo rol sin modificar el código.
    Usa parámetro para especificar el rol requerido.
    
    ISP: Interfaz pequeña y específica - solo requiere un rol.
    No obliga a implementar verificaciones innecesarias.
    
    DIP: Depende de la abstracción RolUsuario, no de strings hardcodeados
    o implementaciones específicas de roles.
    
    Decorador que requiere un rol específico para acceder a una vista.
    
    Este decorador verifica que el usuario esté autenticado y tenga el rol
    específico requerido antes de permitir el acceso a la función decorada.
    
    Args:
        rol_requerido (RolUsuario): Rol específico requerido para acceso
        
    Returns:
        function: Decorador configurado para el rol específico
    """
    def decorator(f):
        """
        Decorador interno que implementa la verificación de rol.
        
        Args:
            f: Función de vista a decorar
            
        Returns:
            function: Función decorada con verificación de rol
        """
        @wraps(f)  # Preservar metadatos de la función original
        def decorated_function(*args, **kwargs):
            """
            Función interna que implementa la verificación de autenticación y rol.
            
            Args:
                *args: Argumentos posicionales de la función original
                **kwargs: Argumentos de palabra clave de la función original
                
            Returns:
                Response: Respuesta de la función original, redirección o error 403
            """
            # Verificar primero si el usuario está autenticado
            if not current_user.is_authenticated:
                flash('Debe iniciar sesión para acceder a esta página.', 'warning')
                return redirect(url_for('auth.login'))
            
            # Verificar si el usuario tiene el rol requerido
            if current_user.rol != rol_requerido:
                flash('No tiene permisos para acceder a esta página.', 'danger')
                abort(403)  # Error HTTP 403 Forbidden
            
            # Si cumple todos los requisitos, ejecutar la función original
            return f(*args, **kwargs)
        
        return decorated_function  # Retornar la función decorada
    
    return decorator  # Retornar el decorador configurado

def requiere_administrador(f):
    """
    Decorador específico que requiere rol de administrador para acceder a una vista.
    
    Este decorador es una especialización que verifica que el usuario sea
    administrador antes de permitir el acceso a funciones administrativas.
    
    Args:
        f: Función de vista a decorar
        
    Returns:
        function: Función decorada con verificación de rol administrador
    """
    @wraps(f)  # Preservar metadatos de la función original
    def decorated_function(*args, **kwargs):
        """
        Función interna que implementa la verificación de rol administrador.
        
        Args:
            *args: Argumentos posicionales de la función original
            **kwargs: Argumentos de palabra clave de la función original
            
        Returns:
            Response: Respuesta de la función original, redirección o error 403
        """
        # Verificar primero si el usuario está autenticado
        if not current_user.is_authenticated:
            flash('Debe iniciar sesión para acceder a esta página.', 'warning')
            return redirect(url_for('auth.login'))
        
        # Verificar si el usuario es administrador usando el método del modelo
        if not current_user.es_administrador():
            flash('Solo los administradores pueden acceder a esta página.', 'danger')
            abort(403)  # Error HTTP 403 Forbidden
        
        # Si es administrador, ejecutar la función original
        return f(*args, **kwargs)
    
    return decorated_function  # Retornar la función decorada

def requiere_profesional(f):
    """
    Decorador específico que requiere rol de profesional para acceder a una vista.
    
    Este decorador es una especialización que verifica que el usuario sea
    un profesional médico antes de permitir el acceso a funciones clínicas.
    
    Args:
        f: Función de vista a decorar
        
    Returns:
        function: Función decorada con verificación de rol profesional
    """
    @wraps(f)  # Preservar metadatos de la función original
    def decorated_function(*args, **kwargs):
        """
        Función interna que implementa la verificación de rol profesional.
        
        Args:
            *args: Argumentos posicionales de la función original
            **kwargs: Argumentos de palabra clave de la función original
            
        Returns:
            Response: Respuesta de la función original, redirección o error 403
        """
        # Verificar primero si el usuario está autenticado
        if not current_user.is_authenticated:
            flash('Debe iniciar sesión para acceder a esta página.', 'warning')
            return redirect(url_for('auth.login'))
        
        # Verificar si el usuario es profesional usando el método del modelo
        if not current_user.es_profesional():
            flash('Solo los profesionales pueden acceder a esta página.', 'danger')
            abort(403)  # Error HTTP 403 Forbidden
        
        # Si es profesional, ejecutar la función original
        return f(*args, **kwargs)
    
    return decorated_function  # Retornar la función decorada

def requiere_paciente(f):
    """
    Decorador específico que requiere rol de paciente para acceder a una vista.
    
    Este decorador es una especialización que verifica que el usuario sea
    un paciente (estudiante) antes de permitir el acceso a funciones específicas.
    
    Args:
        f: Función de vista a decorar
        
    Returns:
        function: Función decorada con verificación de rol paciente
    """
    @wraps(f)  # Preservar metadatos de la función original
    def decorated_function(*args, **kwargs):
        """
        Función interna que implementa la verificación de rol paciente.
        
        Args:
            *args: Argumentos posicionales de la función original
            **kwargs: Argumentos de palabra clave de la función original
            
        Returns:
            Response: Respuesta de la función original, redirección o error 403
        """
        # Verificar primero si el usuario está autenticado
        if not current_user.is_authenticated:
            flash('Debe iniciar sesión para acceder a esta página.', 'warning')
            return redirect(url_for('auth.login'))
        
        # Verificar si el usuario es paciente usando el método del modelo
        if not current_user.es_paciente():
            flash('Solo los pacientes pueden acceder a esta página.', 'danger')
            abort(403)  # Error HTTP 403 Forbidden
        
        # Si es paciente, ejecutar la función original
        return f(*args, **kwargs)
    
    return decorated_function  # Retornar la función decorada
