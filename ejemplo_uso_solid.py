# ============================================================================
# EJEMPLO DE USO DE IMPLEMENTACIONES SOLID
# ============================================================================
"""
Este archivo demuestra cómo usar las nuevas implementaciones SOLID
en lugar de las versiones legacy.

BENEFICIOS DE LA ARQUITECTURA SOLID:
- Testeo más fácil (inyección de dependencias)
- Mantenimiento simplificado (responsabilidades separadas)
- Extensibilidad sin modificar código existente
- Código más legible y comprensible
"""

from servicios_solid import (
    FactoriaServiciosProduccion,
    ComandoCrearUsuario,
    ManejadorComandos
)


def ejemplo_autenticacion_solid():
    """
    Ejemplo de cómo usar el servicio de autenticación SOLID.
    
    BENEFICIOS SOLID DEMOSTRADOS:
    - DIP: Todas las dependencias se inyectan automáticamente
    - SRP: Cada componente tiene una sola responsabilidad
    - OCP: Extensible sin modificar código existente
    """
    
    # Factory crea todas las dependencias necesarias (DIP)
    servicio_auth = FactoriaServiciosProduccion.crear_servicio_autenticacion()
    
    # Autenticar usuario usando el servicio SOLID
    usuario = servicio_auth.autenticar("12345678", "password123")
    
    if usuario:
        print(f"✓ Usuario autenticado: {usuario.nombre}")
        return usuario
    else:
        print("✗ Autenticación fallida")
        return None


def ejemplo_creacion_usuario_solid():
    """
    Ejemplo de cómo crear usuarios usando Command Pattern.
    
    BENEFICIOS SOLID DEMOSTRADOS:
    - SRP: Comando encapsula solo la lógica de creación
    - OCP: Nuevos comandos se pueden agregar sin modificar el manejador
    - DIP: Comando depende de abstracciones, no de implementaciones
    """
    
    # Crear dependencias usando Factory (DIP)
    servicio_auth = FactoriaServiciosProduccion.crear_servicio_autenticacion()
    manejador = FactoriaServiciosProduccion.crear_manejador_comandos()
    
    # Datos del usuario a crear
    datos_usuario = {
        'nombre': 'Dr. Juan Pérez',
        'rol': 'PROFESIONAL',
        'dni': '12345678',
        'password': 'password123'
    }
    
    # Crear comando específico (SRP)
    comando = ComandoCrearUsuario(datos_usuario, servicio_auth)
    
    try:
        # Ejecutar comando usando el manejador (OCP)
        usuario_creado = manejador.manejar(comando)
        print(f"✓ Usuario creado exitosamente: {usuario_creado.nombre}")
        return usuario_creado
        
    except Exception as e:
        print(f"✗ Error creando usuario: {e}")
        return None


def ejemplo_autorizacion_solid():
    """
    Ejemplo de cómo usar el servicio de autorización.
    
    BENEFICIOS SOLID DEMOSTRADOS:
    - SRP: Servicio se enfoca solo en autorización
    - OCP: Nuevos permisos se pueden agregar sin modificar código
    """
    
    # Crear servicio de autorización
    servicio_autorizacion = FactoriaServiciosProduccion.crear_servicio_autorizacion()
    
    # Primero necesitamos un usuario autenticado
    usuario = ejemplo_autenticacion_solid()
    
    if usuario:
        # Verificar permisos específicos
        puede_crear_usuarios = servicio_autorizacion.tiene_permiso(
            usuario, 'usuarios', 'crear'
        )
        puede_ver_reportes = servicio_autorizacion.tiene_permiso(
            usuario, 'reportes', 'leer'
        )
        
        print(f"Usuario {usuario.nombre}:")
        print(f"  ✓ Puede crear usuarios: {puede_crear_usuarios}")
        print(f"  ✓ Puede ver reportes: {puede_ver_reportes}")
        
        return {
            'puede_crear_usuarios': puede_crear_usuarios,
            'puede_ver_reportes': puede_ver_reportes
        }
    
    return None


def ejemplo_testing_solid():
    """
    Ejemplo de cómo el diseño SOLID facilita el testing.
    
    BENEFICIOS PARA TESTING:
    - DIP: Se pueden inyectar mocks de dependencias
    - SRP: Cada componente se puede testear aisladamente
    - ISP: Interfaces pequeñas fáciles de mockear
    """
    
    # En un test real, podríamos crear mocks:
    # mock_repositorio = Mock(spec=IRepositorioUsuario)
    # mock_hasheador = Mock(spec=IHasheadorPassword)
    # mock_validador = Mock(spec=IValidadorUsuario)
    # mock_notificador = Mock(spec=INotificadorEventos)
    
    # servicio_auth = ServicioAutenticacionSOLID(
    #     mock_repositorio, mock_hasheador, mock_validador, mock_notificador
    # )
    
    print("✓ Diseño SOLID permite testing fácil con mocks")
    print("  - Cada dependencia se puede simular independientemente")
    print("  - Tests más rápidos (no requieren base de datos)")
    print("  - Tests más confiables (resultados predecibles)")


def comparacion_legacy_vs_solid():
    """
    Comparación entre implementación legacy y SOLID.
    """
    
    print("\n" + "="*60)
    print("COMPARACIÓN: LEGACY vs SOLID")
    print("="*60)
    
    print("\n🔴 IMPLEMENTACIÓN LEGACY (servicios.py):")
    print("  ✗ Múltiples responsabilidades en una clase")
    print("  ✗ Dependencias hardcodeadas (Werkzeug, SQLAlchemy)")
    print("  ✗ Difícil de testear")
    print("  ✗ Difícil de extender")
    print("  ✗ Acoplamiento alto")
    
    print("\n🟢 IMPLEMENTACIÓN SOLID (servicios_solid.py):")
    print("  ✓ Una responsabilidad por clase")
    print("  ✓ Dependencias inyectadas")
    print("  ✓ Fácil de testear con mocks")
    print("  ✓ Extensible sin modificar código existente")
    print("  ✓ Bajo acoplamiento")
    
    print("\n📋 PRINCIPIOS APLICADOS:")
    print("  ✓ SRP: Clases con responsabilidad única")
    print("  ✓ OCP: Abierto para extensión, cerrado para modificación")
    print("  ✓ LSP: Implementaciones intercambiables")
    print("  ✓ ISP: Interfaces específicas y cohesivas")
    print("  ✓ DIP: Dependencias hacia abstracciones")


if __name__ == "__main__":
    """
    Ejecutar todos los ejemplos para demostrar la arquitectura SOLID.
    """
    
    print("🚀 DEMOSTRACIÓN DE ARQUITECTURA SOLID")
    print("="*50)
    
    # Ejemplo 1: Autenticación
    print("\n1️⃣ EJEMPLO DE AUTENTICACIÓN:")
    ejemplo_autenticacion_solid()
    
    # Ejemplo 2: Creación de usuario con Command Pattern
    print("\n2️⃣ EJEMPLO DE CREACIÓN DE USUARIO (Command Pattern):")
    ejemplo_creacion_usuario_solid()
    
    # Ejemplo 3: Autorización
    print("\n3️⃣ EJEMPLO DE AUTORIZACIÓN:")
    ejemplo_autorizacion_solid()
    
    # Ejemplo 4: Testing
    print("\n4️⃣ EJEMPLO DE TESTING:")
    ejemplo_testing_solid()
    
    # Comparación
    comparacion_legacy_vs_solid()
    
    print("\n" + "="*60)
    print("✅ DEMOSTRACIÓN COMPLETADA")
    print("Para usar en producción, reemplazar gradualmente")
    print("servicios legacy con implementaciones SOLID.")
    print("="*60)