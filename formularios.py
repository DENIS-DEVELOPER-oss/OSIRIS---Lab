# Importaciones necesarias para la creación de formularios web
from flask_wtf import FlaskForm  # Clase base para formularios con protección CSRF
from wtforms import StringField, PasswordField, SelectField, DateField, TimeField, TextAreaField, TelField  # Tipos de campos de formulario
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp  # Validadores de campos
from datetime import date, datetime  # Para manejo de fechas y validaciones temporales
from modelos import Usuario, RolUsuario, TipoCita, NivelRiesgo  # Modelos y enumeraciones del sistema

class FormularioLogin(FlaskForm):
    """
    Formulario de inicio de sesión con autenticación diferenciada por rol.
    
    Este formulario permite a los usuarios autenticarse usando diferentes tipos
    de identificadores según su rol en el sistema:
    - Estudiantes: Código de matrícula + contraseña
    - Profesionales y Administradores: DNI + contraseña
    
    Características:
    - Validación de longitud y formato de identificadores
    - Verificación de existencia y estado activo del usuario
    - Mensajes de error personalizados en español
    """
    
    # Campo identificador: Acepta DNI o código de matrícula según el rol del usuario
    identificador = StringField('Identificador', validators=[
        DataRequired(message='Este campo es obligatorio'),  # Campo obligatorio
        Length(min=6, max=8, message='Debe tener 6 dígitos (matrícula) o 8 dígitos (DNI)')  # Validación de longitud
    ], render_kw={'placeholder': 'DNI o Código de Matrícula'})  # Texto de ayuda para el usuario
    
    # Campo contraseña: Contraseña del usuario con validación de longitud mínima
    password = PasswordField('Contraseña', validators=[
        DataRequired(message='Este campo es obligatorio'),  # Campo obligatorio
        Length(min=6, message='La contraseña debe tener al menos 6 caracteres')  # Longitud mínima de seguridad
    ])
    
    def validate_identificador(self, field):
        """
        Validación personalizada del campo identificador.
        
        Este método verifica que el identificador ingresado corresponda a un usuario
        válido y activo en el sistema. Busca primero por DNI (si es numérico) y luego
        por código de matrícula.
        
        Args:
            field: Campo del formulario que contiene el identificador a validar
            
        Raises:
            ValidationError: Si el identificador no existe o el usuario está inactivo
        """
        usuario = None  # Inicializar variable para el usuario encontrado
        
        # Estrategia 1: Si el identificador es completamente numérico
        if field.data.isdigit():
            # Si son 8 dígitos, buscar por DNI
            if len(field.data) == 8:
                usuario = Usuario.query.filter_by(dni=field.data).first()
            # Si son 6 dígitos, buscar por código de matrícula  
            elif len(field.data) == 6:
                usuario = Usuario.query.filter_by(codigo_matricula=field.data).first()
        
        # Estrategia 2: Si no se encontró aún, buscar por código de matrícula (por compatibilidad)
        if not usuario:
            usuario = Usuario.query.filter_by(codigo_matricula=field.data).first()
        
        # Verificar que se encontró un usuario con ese identificador
        if not usuario:
            raise ValidationError('Identificador no válido')
        
        # Verificar que el usuario esté activo en el sistema
        if not usuario.activo:
            raise ValidationError('Usuario inactivo')

class FormularioRegistro(FlaskForm):
    """
    Formulario de registro de usuarios con validación diferenciada por rol.
    
    Este formulario permite registrar nuevos usuarios en el sistema con campos
    específicos según el rol seleccionado:
    - Estudiantes: Requieren código de matrícula
    - Profesionales y Administradores: Requieren DNI
    
    Características:
    - Validación condicional de campos según el rol
    - Verificación de unicidad de identificadores
    - Confirmación de contraseña para seguridad
    - Mensajes de error específicos en español
    """
    
    # Campo nombre: Nombre completo del usuario
    nombre = StringField('Nombre Completo', validators=[
        DataRequired(message='Este campo es obligatorio'),  # Campo obligatorio
        Length(min=2, max=100, message='Debe tener entre 2 y 100 caracteres')  # Validación de longitud
    ])
    
    # Campo rol: Selector del rol del usuario en el sistema
    rol = SelectField('Rol', choices=[
        ('PACIENTE', 'Estudiante'),  # Opción para estudiantes universitarios
        ('PROFESIONAL', 'Profesional'),  # Opción para médicos y psicólogos
        ('ADMINISTRADOR', 'Administrador')  # Opción para personal administrativo
    ], validators=[DataRequired(message='Seleccione un rol')])  # Selección obligatoria
    
    # Campo DNI: Documento Nacional de Identidad (obligatorio para profesionales y administradores)
    dni = StringField('DNI', validators=[
        Length(min=8, max=20, message='DNI debe tener entre 8 y 20 caracteres')  # Validación de longitud
    ])
    
    # Campo código_matricula: Código universitario (obligatorio para estudiantes)
    codigo_matricula = StringField('Código de Matrícula', validators=[
        Length(min=6, max=6, message='Código debe tener exactamente 6 dígitos'),  # Validación de longitud exacta
        Regexp(r'^\d{6}$', message='Código debe contener solo números (6 dígitos)')  # Validación de formato
    ])
    
    # Campos adicionales para pacientes (estudiantes)
    telefono = TelField('Teléfono', validators=[
        Length(max=15, message='Teléfono no puede exceder 15 caracteres')
    ])
    
    direccion = StringField('Dirección', validators=[
        Length(max=200, message='Dirección no puede exceder 200 caracteres')
    ])
    
    carrera = StringField('Carrera', validators=[
        Length(max=100, message='Carrera no puede exceder 100 caracteres')
    ])
    
    procedencia = SelectField('Procedencia', choices=[
        ('', 'Seleccionar procedencia'),
        ('Puno', 'Puno (Ciudad)'),
        ('Juliaca', 'Juliaca'),
        ('Ilave', 'Ilave'),
        ('Yunguyo', 'Yunguyo'),
        ('Desaguadero', 'Desaguadero'),
        ('Ayaviri', 'Ayaviri'),
        ('Putina', 'Putina'),
        ('Sandia', 'Sandia'),
        ('Macusani', 'Macusani'),
        ('Crucero', 'Crucero'),
        ('Azángaro', 'Azángaro'),
        ('Lampa', 'Lampa'),
        ('Juli', 'Juli'),
        ('Pomata', 'Pomata'),
        ('Zepita', 'Zepita'),
        ('Pilcuyo', 'Pilcuyo'),
        ('Huancané', 'Huancané'),
        ('Moho', 'Moho'),
        ('Conima', 'Conima'),
        ('Tilali', 'Tilali'),
        ('Taraco', 'Taraco'),
        ('Otro', 'Otro lugar')
    ])
    
    # Campo password: Contraseña del usuario con requisitos de seguridad
    password = PasswordField('Contraseña', validators=[
        DataRequired(message='Este campo es obligatorio'),  # Campo obligatorio
        Length(min=6, message='La contraseña debe tener al menos 6 caracteres')  # Longitud mínima de seguridad
    ])
    
    # Campo confirm_password: Confirmación de contraseña para evitar errores de escritura
    confirm_password = PasswordField('Confirmar Contraseña', validators=[
        DataRequired(message='Este campo es obligatorio'),  # Campo obligatorio
        EqualTo('password', message='Las contraseñas deben coincidir')  # Debe coincidir con el campo password
    ])
    
    def validate_dni(self, field):
        """
        Validación personalizada del campo DNI.
        
        Verifica que el DNI sea obligatorio para profesionales y administradores,
        y que no esté ya registrado en el sistema.
        
        Args:
            field: Campo del formulario que contiene el DNI a validar
            
        Raises:
            ValidationError: Si el DNI es requerido pero falta, o si ya está registrado
        """
        # Verificar que el DNI sea obligatorio para profesionales y administradores
        if self.rol.data in ['PROFESIONAL', 'ADMINISTRADOR'] and not field.data:
            raise ValidationError('DNI es obligatorio para profesionales y administradores')
        
        # Verificar que el DNI no esté ya registrado en el sistema
        if field.data and Usuario.query.filter_by(dni=field.data).first():
            raise ValidationError('DNI ya registrado')
    
    def validate_codigo_matricula(self, field):
        """
        Validación personalizada del campo código de matrícula.
        
        Verifica que el código de matrícula sea obligatorio para estudiantes,
        y que no esté ya registrado en el sistema.
        
        Args:
            field: Campo del formulario que contiene el código de matrícula a validar
            
        Raises:
            ValidationError: Si el código es requerido pero falta, o si ya está registrado
        """
        # Verificar que el código de matrícula sea obligatorio para estudiantes
        if self.rol.data == 'PACIENTE' and not field.data:
            raise ValidationError('Código de matrícula es obligatorio para estudiantes')
        
        # Verificar que el código de matrícula no esté ya registrado en el sistema
        if field.data and Usuario.query.filter_by(codigo_matricula=field.data).first():
            raise ValidationError('Código de matrícula ya registrado')

class FormularioPaciente(FlaskForm):
    """
    Formulario para capturar información específica de pacientes (estudiantes).
    
    Este formulario recopila información académica, personal y de contacto
    necesaria para la atención médica universitaria de los estudiantes.
    
    Características:
    - Campos obligatorios: carrera y fecha de nacimiento
    - Campos opcionales: datos de contacto y emergencia
    - Validación de fecha de nacimiento lógica
    - Longitudes máximas para campos de texto
    """
    
    # Campo carrera: Carrera universitaria del estudiante (obligatorio)
    carrera = StringField('Carrera', validators=[
        DataRequired(message='Este campo es obligatorio'),  # Campo obligatorio
        Length(min=2, max=100, message='Debe tener entre 2 y 100 caracteres')  # Validación de longitud
    ])
    
    # Campo fecha_nacimiento: Fecha de nacimiento del estudiante (obligatorio)
    fecha_nacimiento = DateField('Fecha de Nacimiento', validators=[
        DataRequired(message='Este campo es obligatorio')  # Campo obligatorio para calcular edad
    ])
    
    # Campo telefono: Número de teléfono personal del estudiante (opcional)
    telefono = TelField('Teléfono', validators=[
        Length(max=20, message='Máximo 20 caracteres')  # Límite de caracteres para teléfono
    ])
    
    # Campo direccion: Dirección de residencia del estudiante (opcional)
    direccion = StringField('Dirección', validators=[
        Length(max=200, message='Máximo 200 caracteres')  # Límite de caracteres para dirección
    ])
    
    # Campo contacto_emergencia: Nombre del contacto de emergencia (opcional)
    contacto_emergencia = StringField('Contacto de Emergencia', validators=[
        Length(max=100, message='Máximo 100 caracteres')  # Límite de caracteres para nombre
    ])
    
    # Campo telefono_emergencia: Teléfono del contacto de emergencia (opcional)
    telefono_emergencia = TelField('Teléfono de Emergencia', validators=[
        Length(max=20, message='Máximo 20 caracteres')  # Límite de caracteres para teléfono
    ])
    
    procedencia = SelectField('Procedencia', choices=[
        ('', 'Seleccione una opción'),
        ('Puno', 'Puno (Ciudad)'),
        ('Juliaca', 'Juliaca'),
        ('Ilave', 'Ilave'),
        ('Yunguyo', 'Yunguyo'),
        ('Desaguadero', 'Desaguadero'),
        ('Ayaviri', 'Ayaviri'),
        ('Putina', 'Putina'),
        ('Sandia', 'Sandia'),
        ('Macusani', 'Macusani'),
        ('Crucero', 'Crucero'),
        ('Azángaro', 'Azángaro'),
        ('Lampa', 'Lampa'),
        ('Juli', 'Juli'),
        ('Pomata', 'Pomata'),
        ('Zepita', 'Zepita'),
        ('Pilcuyo', 'Pilcuyo'),
        ('Huancané', 'Huancané'),
        ('Moho', 'Moho'),
        ('Conima', 'Conima'),
        ('Tilali', 'Tilali'),
        ('Taraco', 'Taraco'),
        ('Otro', 'Otro lugar')
    ], validators=[
        Length(max=100, message='Máximo 100 caracteres')
    ])
    
    def validate_fecha_nacimiento(self, field):
        """
        Validación personalizada de la fecha de nacimiento.
        
        Verifica que la fecha de nacimiento sea lógica (anterior a la fecha actual)
        para evitar errores de captura de datos.
        
        Args:
            field: Campo del formulario que contiene la fecha de nacimiento
            
        Raises:
            ValidationError: Si la fecha de nacimiento es igual o posterior a hoy
        """
        # Verificar que la fecha de nacimiento sea anterior a la fecha actual
        if field.data and field.data >= date.today():
            raise ValidationError('La fecha de nacimiento debe ser anterior a hoy')

class FormularioCita(FlaskForm):
    """
    Formulario para programar citas médicas entre pacientes y profesionales.
    
    Este formulario permite a los administradores programar citas médicas
    especificando el paciente, profesional, fecha, hora y tipo de consulta.
    
    Características:
    - Selección de paciente y profesional mediante listas desplegables
    - Validación de fecha futura para la cita
    - Categorización por tipo de consulta médica
    - Campo opcional para especificar motivo de la consulta
    """
    
    # Campo paciente_id: Selector del paciente que tendrá la cita
    paciente_id = SelectField('Paciente', coerce=int, validators=[
        DataRequired(message='Seleccione un paciente')  # Selección obligatoria del paciente
    ])
    
    # Campo profesional_id: Selector del profesional médico que atenderá
    profesional_id = SelectField('Profesional', coerce=int, validators=[
        DataRequired(message='Seleccione un profesional')  # Selección obligatoria del profesional
    ])
    
    # Campo fecha: Fecha en que se realizará la cita médica
    fecha = DateField('Fecha', validators=[
        DataRequired(message='Este campo es obligatorio')  # Fecha obligatoria para programar
    ])
    
    # Campo hora: Hora específica de la cita médica
    hora = TimeField('Hora', validators=[
        DataRequired(message='Este campo es obligatorio')  # Hora obligatoria para programar
    ])
    
    # Campo tipo_cita: Tipo de consulta médica a realizar
    tipo_cita = SelectField('Tipo de Cita', choices=[
        ('MEDICINA', 'Medicina'),  # Consulta médica general
        ('PSICOLOGIA', 'Psicología'),  # Consulta psicológica
        ('EMERGENCIA', 'Emergencia')  # Consulta de emergencia
    ], validators=[DataRequired(message='Seleccione un tipo de cita')])  # Tipo obligatorio
    
    # Campo motivo: Descripción opcional del motivo de la consulta
    motivo = TextAreaField('Motivo', validators=[
        Length(max=500, message='Máximo 500 caracteres')  # Límite de caracteres para el motivo
    ])
    
    def validate_fecha(self, field):
        """
        Validación personalizada de la fecha de la cita.
        
        Verifica que la fecha de la cita no sea anterior a la fecha actual
        para evitar programar citas en el pasado.
        
        Args:
            field: Campo del formulario que contiene la fecha de la cita
            
        Raises:
            ValidationError: Si la fecha es anterior a la fecha actual
        """
        # Verificar que la fecha de la cita no sea anterior a hoy
        if field.data and field.data < date.today():
            raise ValidationError('La fecha no puede ser anterior a hoy')

class FormularioConsulta(FlaskForm):
    """
    Formulario para registrar consultas médicas realizadas durante las citas.
    
    Este formulario permite a los profesionales médicos documentar los detalles
    de las consultas realizadas, incluyendo diagnósticos, tratamientos y
    evaluaciones de riesgo para el seguimiento de pacientes.
    
    Características:
    - Campo obligatorio para diagnóstico médico detallado
    - Campos opcionales para tratamiento y observaciones
    - Sistema de evaluación de niveles de riesgo
    - Validaciones de longitud para campos de texto
    """
    
    # Campo diagnostico: Diagnóstico médico detallado (obligatorio)
    diagnostico = TextAreaField('Diagnóstico', validators=[
        DataRequired(message='Este campo es obligatorio'),  # Campo obligatorio para consulta
        Length(min=10, max=1000, message='Debe tener entre 10 y 1000 caracteres')  # Longitud adecuada para diagnóstico
    ])
    
    # Campo tratamiento: Tratamiento prescrito o recomendado (opcional)
    tratamiento = TextAreaField('Tratamiento', validators=[
        Length(max=1000, message='Máximo 1000 caracteres')  # Límite para descripción de tratamiento
    ])
    
    # Campo observaciones: Observaciones adicionales del profesional (opcional)
    observaciones = TextAreaField('Observaciones', validators=[
        Length(max=1000, message='Máximo 1000 caracteres')  # Límite para observaciones adicionales
    ])
    
    # Campo nivel_riesgo: Evaluación del nivel de riesgo del paciente
    nivel_riesgo = SelectField('Nivel de Riesgo', choices=[
        ('BAJO', 'Bajo'),  # Paciente estable, sin riesgos significativos
        ('MEDIO', 'Medio'),  # Paciente con factores de riesgo moderados
        ('ALTO', 'Alto'),  # Paciente con factores de riesgo elevados
        ('CRITICO', 'Crítico')  # Paciente en situación crítica
    ], validators=[DataRequired(message='Seleccione un nivel de riesgo')])  # Evaluación obligatoria
