# Importaciones necesarias para los modelos de la base de datos
from datetime import datetime, date  # Para manejo de fechas y tiempos
from enum import Enum  # Para crear enumeraciones con valores fijos
from flask_login import UserMixin  # Mixin que proporciona métodos necesarios para Flask-Login
from sqlalchemy import Column, Integer, String, DateTime, Date, Text, ForeignKey, Enum as SQLEnum  # Tipos de datos de SQLAlchemy
from sqlalchemy.orm import relationship  # Para definir relaciones entre modelos
from app import db  # Instancia de la base de datos desde la aplicación principal

class RolUsuario(Enum):
    """
    Enumeración que define los diferentes roles de usuario en el sistema.
    
    Roles disponibles:
    - PACIENTE: Estudiantes universitarios que reciben atención médica
    - PROFESIONAL: Médicos y psicólogos que brindan consultas
    - ADMINISTRADOR: Personal administrativo con acceso completo al sistema
    """
    PACIENTE = "PACIENTE"  # Rol para estudiantes que son pacientes
    PROFESIONAL = "PROFESIONAL"  # Rol para médicos y psicólogos
    ADMINISTRADOR = "ADMINISTRADOR"  # Rol para administradores del sistema

class TipoCita(Enum):
    """
    Enumeración que define los tipos de citas médicas disponibles.
    
    Tipos de cita:
    - MEDICINA: Consultas médicas generales
    - PSICOLOGIA: Consultas psicológicas y de salud mental
    - EMERGENCIA: Citas de emergencia que requieren atención inmediata
    """
    MEDICINA = "MEDICINA"  # Consultas médicas generales
    PSICOLOGIA = "PSICOLOGIA"  # Consultas psicológicas
    EMERGENCIA = "EMERGENCIA"  # Consultas de emergencia

class NivelRiesgo(Enum):
    """
    Enumeración que define los niveles de riesgo para las consultas médicas.
    
    Niveles de riesgo:
    - BAJO: Paciente estable, sin riesgos significativos
    - MEDIO: Paciente con factores de riesgo moderados que requieren seguimiento
    - ALTO: Paciente con factores de riesgo elevados que necesitan atención prioritaria
    - CRITICO: Paciente en situación crítica que requiere intervención inmediata
    """
    BAJO = "BAJO"  # Riesgo mínimo, paciente estable
    MEDIO = "MEDIO"  # Riesgo moderado, requiere seguimiento
    ALTO = "ALTO"  # Riesgo elevado, atención prioritaria
    CRITICO = "CRITICO"  # Riesgo crítico, intervención inmediata

class Usuario(UserMixin, db.Model):
    """
    Modelo de usuario personalizado para el sistema de gestión médica universitaria.
    
    Este modelo hereda de UserMixin (Flask-Login) y db.Model (SQLAlchemy) para proporcionar
    funcionalidades de autenticación y persistencia en base de datos.
    
    Características principales:
    - Soporte para múltiples tipos de identificación (DNI y código de matrícula)
    - Sistema de roles diferenciado
    - Gestión de contraseñas con hash seguro
    - Relaciones con otros modelos del sistema
    """
    
    # Nombre de la tabla en la base de datos
    __tablename__ = 'usuarios'
    
    # === CAMPOS DE LA TABLA ===
    
    # Campo ID: Clave primaria autoincremental única para cada usuario
    id = Column(Integer, primary_key=True)
    
    # Campo nombre: Nombre completo del usuario (obligatorio, máximo 100 caracteres)
    nombre = Column(String(100), nullable=False)
    
    # Campo DNI: Documento Nacional de Identidad para profesionales y administradores
    # Es único en la base de datos pero puede ser nulo (para estudiantes que usan matrícula)
    dni = Column(String(20), unique=True, nullable=True)
    
    # Campo código_matricula: Código de matrícula universitaria para estudiantes
    # Es único en la base de datos pero puede ser nulo (para profesionales que usan DNI)
    codigo_matricula = Column(String(20), unique=True, nullable=True)
    
    # Campo rol: Rol del usuario en el sistema usando la enumeración RolUsuario
    # Este campo determina los permisos y funcionalidades disponibles
    rol = Column(SQLEnum(RolUsuario), nullable=False)
    
    # Campo password_hash: Hash seguro de la contraseña del usuario
    # Nunca se almacena la contraseña en texto plano por seguridad
    password_hash = Column(String(256), nullable=False)
    
    # Campo fecha_creacion: Timestamp de cuando se creó el usuario
    # Se establece automáticamente al momento de la creación
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    
    # Campo activo: Indica si el usuario está activo en el sistema
    # Por defecto True, se puede desactivar sin eliminar el registro
    activo = Column(db.Boolean, default=True)
    
    # === RELACIONES CON OTROS MODELOS ===
    
    # Relación uno-a-uno con el modelo Paciente
    # Solo los usuarios con rol PACIENTE tendrán un registro asociado en la tabla pacientes
    paciente = relationship("Paciente", back_populates="usuario", uselist=False)
    
    # Relación uno-a-muchos con el modelo Cita como profesional
    # Los usuarios con rol PROFESIONAL pueden tener múltiples citas asignadas
    citas_profesional = relationship("Cita", foreign_keys="Cita.profesional_id", back_populates="profesional")
    
    # === MÉTODOS DE LA CLASE ===
    
    def __str__(self):
        """
        Representación en cadena del usuario.
        
        Returns:
            str: Nombre del usuario seguido de su identificador principal entre paréntesis
        """
        return f"{self.nombre} ({self.get_identificador()})"
    
    def get_identificador(self):
        """
        Retorna el identificador principal del usuario según su rol.
        
        Los pacientes (estudiantes) usan código de matrícula como identificador,
        mientras que profesionales y administradores usan DNI.
        
        Returns:
            str: Código de matrícula para pacientes, DNI para otros roles
        """
        if self.rol == RolUsuario.PACIENTE:  # Si es paciente/estudiante
            return self.codigo_matricula  # Retornar código de matrícula
        return self.dni  # Para profesionales y administradores, retornar DNI
    
    def es_administrador(self):
        """
        Verifica si el usuario tiene rol de administrador.
        
        Returns:
            bool: True si el usuario es administrador, False en caso contrario
        """
        return self.rol == RolUsuario.ADMINISTRADOR
    
    def es_profesional(self):
        """
        Verifica si el usuario tiene rol de profesional médico.
        
        Returns:
            bool: True si el usuario es profesional, False en caso contrario
        """
        return self.rol == RolUsuario.PROFESIONAL
    
    def es_paciente(self):
        """
        Verifica si el usuario tiene rol de paciente/estudiante.
        
        Returns:
            bool: True si el usuario es paciente, False en caso contrario
        """
        return self.rol == RolUsuario.PACIENTE

class Paciente(db.Model):
    """
    Modelo para información específica de los pacientes (estudiantes universitarios).
    
    Este modelo extiende la información básica del usuario para incluir datos
    específicos necesarios para la atención médica universitaria.
    
    Características:
    - Información académica (carrera)
    - Datos personales para atención médica
    - Contactos de emergencia
    - Historial de citas médicas
    """
    
    # Nombre de la tabla en la base de datos
    __tablename__ = 'pacientes'
    
    # === CAMPOS DE LA TABLA ===
    
    # Campo ID: Clave primaria autoincremental única para cada paciente
    id = Column(Integer, primary_key=True)
    
    # Campo usuario_id: Clave foránea que referencia al usuario en la tabla usuarios
    # Establece la relación uno-a-uno entre Usuario y Paciente
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    
    # Campo carrera: Carrera universitaria que estudia el paciente
    # Es obligatorio para identificar la facultad y servicios específicos
    carrera = Column(String(100), nullable=False)
    
    # Campo fecha_nacimiento: Fecha de nacimiento del paciente
    # Necesario para calcular la edad y determinar tratamientos apropiados
    fecha_nacimiento = Column(Date, nullable=False)
    
    # Campo telefono: Número de teléfono personal del paciente (opcional)
    # Para contacto directo en caso de citas o emergencias
    telefono = Column(String(20))
    
    # Campo direccion: Dirección de residencia del paciente (opcional)
    # Útil para servicios de salud que requieran visitas domiciliarias
    direccion = Column(String(200))
    
    # Campo contacto_emergencia: Nombre del contacto de emergencia (opcional)
    # Persona a contactar en caso de emergencias médicas
    contacto_emergencia = Column(String(100))
    
    # Campo telefono_emergencia: Teléfono del contacto de emergencia (opcional)
    # Número para contactar en situaciones de emergencia
    telefono_emergencia = Column(String(20))
    
    # Campo procedencia: Distrito o provincia de origen del paciente
    # Campo opcional para análisis geográfico y estadísticas de procedencia
    procedencia = Column(String(100), nullable=True)
    
    # === RELACIONES CON OTROS MODELOS ===
    
    # Relación uno-a-uno inversa con el modelo Usuario
    # Permite acceder a los datos del usuario desde el paciente
    usuario = relationship("Usuario", back_populates="paciente")
    
    # Relación uno-a-muchos con el modelo Cita
    # Un paciente puede tener múltiples citas médicas
    citas = relationship("Cita", back_populates="paciente")
    
    # === MÉTODOS DE LA CLASE ===
    
    def edad(self):
        """
        Calcula la edad actual del paciente basada en su fecha de nacimiento.
        
        El cálculo tiene en cuenta si ya pasó el cumpleaños en el año actual
        para determinar la edad exacta en años completos.
        
        Returns:
            int: Edad del paciente en años completos
        """
        hoy = date.today()  # Obtener la fecha actual
        
        # Calcular la diferencia de años
        edad_calculada = hoy.year - self.fecha_nacimiento.year
        
        # Ajustar si aún no ha llegado el cumpleaños este año
        # Si el mes y día actuales son menores que los de nacimiento, restar un año
        if (hoy.month, hoy.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day):
            edad_calculada -= 1
            
        return edad_calculada
    
    def __str__(self):
        """
        Representación en cadena del paciente.
        
        Returns:
            str: Nombre del paciente seguido de su carrera separados por guion
        """
        return f"{self.usuario.nombre} - {self.carrera}"

class Cita(db.Model):
    """
    Modelo para gestión de citas médicas en el sistema universitario.
    
    Este modelo representa las citas programadas entre pacientes (estudiantes)
    y profesionales médicos. Gestiona la programación, seguimiento y estado
    de las consultas médicas.
    
    Características:
    - Programación de citas con fecha y hora específicas
    - Clasificación por tipo de consulta médica
    - Seguimiento del estado de la cita
    - Relación con consultas médicas realizadas
    """
    
    # Nombre de la tabla en la base de datos
    __tablename__ = 'citas'
    
    # === CAMPOS DE LA TABLA ===
    
    # Campo ID: Clave primaria autoincremental única para cada cita
    id = Column(Integer, primary_key=True)
    
    # Campo paciente_id: Clave foránea que referencia al paciente
    # Identifica qué estudiante tiene programada esta cita médica
    paciente_id = Column(Integer, ForeignKey('pacientes.id'), nullable=False)
    
    # Campo profesional_id: Clave foránea que referencia al profesional médico
    # Identifica qué médico o psicólogo atenderá la cita
    profesional_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    
    # Campo fecha: Fecha programada para la cita médica
    # Almacena solo la fecha sin información de hora
    fecha = Column(Date, nullable=False)
    
    # Campo hora: Hora específica programada para la cita
    # Complementa el campo fecha para determinar el momento exacto
    hora = Column(db.Time, nullable=False)
    
    # Campo tipo_cita: Tipo de consulta médica usando la enumeración TipoCita
    # Determina si es medicina general, psicología o emergencia
    tipo_cita = Column(SQLEnum(TipoCita), nullable=False)
    
    # Campo motivo: Descripción del motivo de la cita (opcional)
    # Permite al paciente o administrador especificar la razón de la consulta
    motivo = Column(Text)
    
    # Campo estado: Estado actual de la cita (PROGRAMADA, COMPLETADA, CANCELADA)
    # Por defecto se establece como PROGRAMADA al crear la cita
    estado = Column(String(20), default='PROGRAMADA')
    
    # Campo fecha_creacion: Timestamp de cuando se programó la cita
    # Se establece automáticamente al momento de crear el registro
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    
    # === RELACIONES CON OTROS MODELOS ===
    
    # Relación muchos-a-uno con el modelo Paciente
    # Permite acceder a la información del paciente desde la cita
    paciente = relationship("Paciente", back_populates="citas")
    
    # Relación muchos-a-uno con el modelo Usuario (profesional)
    # Permite acceder a la información del profesional médico
    profesional = relationship("Usuario", foreign_keys=[profesional_id], back_populates="citas_profesional")
    
    # Relación uno-a-uno con el modelo Consulta
    # Una cita puede tener máximo una consulta médica registrada
    consulta = relationship("Consulta", back_populates="cita", uselist=False)
    
    # === MÉTODOS DE LA CLASE ===
    
    def __str__(self):
        """
        Representación en cadena de la cita médica.
        
        Returns:
            str: Descripción de la cita incluyendo tipo, fecha y hora
        """
        return f"Cita {self.tipo_cita.value} - {self.fecha} {self.hora}"
    
    def puede_crear_consulta(self):
        """
        Verifica si es posible crear una consulta médica para esta cita.
        
        Una consulta solo se puede crear si:
        1. La cita está en estado PROGRAMADA (no cancelada ni completada)
        2. No existe ya una consulta registrada para esta cita
        
        Returns:
            bool: True si se puede crear consulta, False en caso contrario
        """
        # Verificar que la cita esté programada y no tenga consulta ya registrada
        return self.estado == 'PROGRAMADA' and self.consulta is None

class Consulta(db.Model):
    """
    Modelo para registro de consultas médicas realizadas.
    
    Este modelo almacena la información clínica detallada de las consultas
    médicas realizadas durante las citas programadas. Incluye diagnósticos,
    tratamientos y evaluaciones de riesgo.
    
    Características:
    - Registro detallado de diagnósticos médicos
    - Documentación de tratamientos prescritos
    - Sistema de evaluación de niveles de riesgo
    - Historial clínico del paciente
    """
    
    # Nombre de la tabla en la base de datos
    __tablename__ = 'consultas'
    
    # === CAMPOS DE LA TABLA ===
    
    # Campo ID: Clave primaria autoincremental única para cada consulta
    id = Column(Integer, primary_key=True)
    
    # Campo cita_id: Clave foránea que referencia a la cita médica
    # Establece la relación uno-a-uno entre Cita y Consulta
    cita_id = Column(Integer, ForeignKey('citas.id'), nullable=False)
    
    # Campo diagnostico: Diagnóstico médico detallado (obligatorio)
    # Descripción profesional del estado de salud y condiciones del paciente
    diagnostico = Column(Text, nullable=False)
    
    # Campo tratamiento: Tratamiento prescrito o recomendado (opcional)
    # Incluye medicamentos, terapias, procedimientos o recomendaciones
    tratamiento = Column(Text)
    
    # Campo observaciones: Observaciones adicionales del profesional (opcional)
    # Notas complementarias, seguimiento requerido, o información relevante
    observaciones = Column(Text)
    
    # Campo nivel_riesgo: Evaluación del nivel de riesgo del paciente
    # Utiliza la enumeración NivelRiesgo, por defecto se establece como BAJO
    nivel_riesgo = Column(SQLEnum(NivelRiesgo), default=NivelRiesgo.BAJO)
    
    # Campo fecha_consulta: Timestamp de cuando se registró la consulta
    # Se establece automáticamente al momento de crear el registro
    fecha_consulta = Column(DateTime, default=datetime.utcnow)
    
    # === RELACIONES CON OTROS MODELOS ===
    
    # Relación uno-a-uno inversa con el modelo Cita
    # Permite acceder a la información de la cita desde la consulta
    cita = relationship("Cita", back_populates="consulta")
    
    # === MÉTODOS DE LA CLASE ===
    
    def __str__(self):
        """
        Representación en cadena de la consulta médica.
        
        Returns:
            str: ID de la consulta seguido del nombre del paciente
        """
        return f"Consulta {self.id} - {self.cita.paciente.usuario.nombre}"
    
    def es_riesgo_alto(self):
        """
        Verifica si la consulta tiene un nivel de riesgo alto o crítico.
        
        Este método es útil para identificar pacientes que requieren
        seguimiento prioritario o atención especializada.
        
        Returns:
            bool: True si el nivel de riesgo es ALTO o CRITICO, False en caso contrario
        """
        return self.nivel_riesgo in [NivelRiesgo.ALTO, NivelRiesgo.CRITICO]
