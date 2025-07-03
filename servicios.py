# Importaciones necesarias para los servicios de negocio
from collections import defaultdict  # Para crear diccionarios con valores por defecto
from datetime import datetime, timedelta  # Para manejo de fechas y cálculos temporales
from sqlalchemy import func, extract  # Funciones SQL para agregaciones y extracciones
from app import db  # Instancia de la base de datos
from modelos import Usuario, Paciente, Cita, Consulta, TipoCita, NivelRiesgo, RolUsuario  # Modelos de datos

class ServicioAutenticacion:
    """
    Servicio encargado del manejo de autenticación y autorización de usuarios.
    
    Este servicio proporciona métodos para autenticar usuarios mediante diferentes
    tipos de identificadores (DNI para profesionales/admins, código de matrícula 
    para estudiantes) y para crear nuevos usuarios en el sistema.
    
    Características:
    - Autenticación dual (DNI o código de matrícula)
    - Verificación de contraseñas con hash seguro
    - Creación de usuarios con validación de roles
    - Verificación de usuarios activos
    """
    
    @staticmethod
    def autenticar_usuario(identificador, password):
        """
        Autentica un usuario en el sistema usando DNI o código de matrícula.
        
        El método intenta autenticar primero por DNI (si el identificador es numérico)
        y luego por código de matrícula. Verifica que el usuario esté activo y que
        la contraseña sea correcta.
        
        Args:
            identificador (str): DNI o código de matrícula del usuario
            password (str): Contraseña en texto plano del usuario
            
        Returns:
            Usuario: Instancia del usuario autenticado o None si falla la autenticación
        """
        from werkzeug.security import check_password_hash  # Importación local para verificar hash
        
        usuario = None  # Inicializar variable para el usuario encontrado
        
        # Estrategia 1: Intentar buscar por DNI si el identificador es completamente numérico
        if identificador.isdigit():
            usuario = Usuario.query.filter_by(dni=identificador).first()
        
        # Estrategia 2: Si no se encontró por DNI, intentar buscar por código de matrícula
        if not usuario:
            usuario = Usuario.query.filter_by(codigo_matricula=identificador).first()
        
        # Verificar que el usuario existe, está activo y la contraseña es correcta
        if usuario and usuario.activo and check_password_hash(usuario.password_hash, password):
            return usuario  # Retornar usuario autenticado exitosamente
        
        return None  # Retornar None si falla cualquier verificación
    
    @staticmethod
    def crear_usuario(datos_usuario):
        """
        Crea un nuevo usuario en el sistema con los datos proporcionados.
        
        Este método recibe un diccionario con los datos del usuario, genera
        un hash seguro de la contraseña y crea el registro en la base de datos.
        
        Args:
            datos_usuario (dict): Diccionario con los datos del usuario
                - nombre (str): Nombre completo del usuario
                - rol (str): Rol del usuario como string
                - dni (str, opcional): DNI para profesionales/administradores
                - codigo_matricula (str, opcional): Código para estudiantes
                - password (str): Contraseña en texto plano
                
        Returns:
            Usuario: Instancia del usuario recién creado
        """
        from werkzeug.security import generate_password_hash  # Importación local para generar hash
        
        # Crear nueva instancia de Usuario con los datos proporcionados
        usuario = Usuario()
        usuario.nombre = datos_usuario['nombre']  # Nombre completo del usuario
        usuario.rol = RolUsuario[datos_usuario['rol']]  # Convertir string a enum de rol
        usuario.dni = datos_usuario.get('dni')  # DNI opcional, None si no se proporciona
        usuario.codigo_matricula = datos_usuario.get('codigo_matricula')  # Código opcional
        usuario.password_hash = generate_password_hash(datos_usuario['password'])  # Hash seguro de contraseña
        
        # Guardar el usuario en la base de datos
        db.session.add(usuario)  # Agregar a la sesión de SQLAlchemy
        db.session.commit()  # Confirmar los cambios en la base de datos
        
        # Guardar respaldo en archivo CSV
        try:
            from respaldo_usuarios import ServicioRespaldoCSV
            ServicioRespaldoCSV.guardar_usuario_en_csv(usuario)
        except Exception as e:
            print(f"Error al guardar respaldo CSV: {e}")
        
        return usuario  # Retornar el usuario creado

class ServicioPaciente:
    """
    Servicio encargado de la gestión completa de pacientes (estudiantes universitarios).
    
    Este servicio maneja todas las operaciones relacionadas con los pacientes,
    incluyendo la consulta, creación, actualización y gestión de su información
    personal y académica.
    
    Características:
    - Consulta de pacientes con filtros de usuarios activos
    - Creación de perfiles de pacientes con información completa
    - Actualización flexible de datos de pacientes
    - Gestión de información académica y de contacto
    """
    
    @staticmethod
    def obtener_pacientes():
        """
        Obtiene todos los pacientes activos del sistema.
        
        Realiza un JOIN entre las tablas Paciente y Usuario para asegurar
        que solo se retornen pacientes cuyos usuarios estén activos en el sistema.
        
        Returns:
            list[Paciente]: Lista de todas las instancias de pacientes activos
        """
        # Realizar consulta con JOIN para filtrar solo usuarios activos
        return Paciente.query.join(Usuario).filter(Usuario.activo == True).all()
    
    @staticmethod
    def obtener_paciente_por_id(paciente_id):
        """
        Obtiene un paciente específico por su ID.
        
        Args:
            paciente_id (int): ID único del paciente a buscar
            
        Returns:
            Paciente: Instancia del paciente encontrado o None si no existe
        """
        # Buscar paciente por su clave primaria
        return Paciente.query.get(paciente_id)
    
    @staticmethod
    def crear_paciente(usuario_id, datos_paciente):
        """
        Crea un nuevo registro de paciente en el sistema.
        
        Este método crea la información extendida de un usuario que tiene rol
        de paciente, incluyendo datos académicos, personales y de contacto.
        
        Args:
            usuario_id (int): ID del usuario al que se asociará el paciente
            datos_paciente (dict): Diccionario con la información del paciente
                - carrera (str): Carrera universitaria del estudiante
                - fecha_nacimiento (date): Fecha de nacimiento
                - telefono (str, opcional): Número de teléfono personal
                - direccion (str, opcional): Dirección de residencia
                - contacto_emergencia (str, opcional): Nombre del contacto de emergencia
                - telefono_emergencia (str, opcional): Teléfono del contacto de emergencia
                
        Returns:
            Paciente: Instancia del paciente recién creado
        """
        # Crear nueva instancia de Paciente con los datos proporcionados
        paciente = Paciente()
        paciente.usuario_id = usuario_id  # Asociar con el usuario existente
        paciente.carrera = datos_paciente['carrera']  # Carrera universitaria (obligatorio)
        paciente.fecha_nacimiento = datos_paciente['fecha_nacimiento']  # Fecha de nacimiento (obligatorio)
        paciente.telefono = datos_paciente.get('telefono')  # Teléfono opcional
        paciente.direccion = datos_paciente.get('direccion')  # Dirección opcional
        paciente.contacto_emergencia = datos_paciente.get('contacto_emergencia')  # Contacto opcional
        paciente.telefono_emergencia = datos_paciente.get('telefono_emergencia')  # Teléfono de emergencia opcional
        
        # Guardar el paciente en la base de datos
        db.session.add(paciente)  # Agregar a la sesión de SQLAlchemy
        db.session.commit()  # Confirmar los cambios
        
        return paciente  # Retornar el paciente creado
    
    @staticmethod
    def actualizar_paciente(paciente_id, datos_paciente):
        """
        Actualiza la información de un paciente existente.
        
        Este método permite actualizar cualquier campo del paciente de forma
        flexible, actualizando solo los campos que se proporcionen en el diccionario.
        
        Args:
            paciente_id (int): ID del paciente a actualizar
            datos_paciente (dict): Diccionario con los campos a actualizar
            
        Returns:
            Paciente: Instancia del paciente actualizado o None si no existe
        """
        # Buscar el paciente por su ID
        paciente = Paciente.query.get(paciente_id)
        
        # Verificar que el paciente existe
        if not paciente:
            return None  # Retornar None si el paciente no existe
        
        # Actualizar dinámicamente todos los campos proporcionados
        for campo, valor in datos_paciente.items():
            # Verificar que el campo existe en el modelo antes de asignarlo
            if hasattr(paciente, campo):
                setattr(paciente, campo, valor)  # Asignar el nuevo valor
        
        # Confirmar los cambios en la base de datos
        db.session.commit()
        
        return paciente  # Retornar el paciente actualizado

class ServicioCita:
    """
    Servicio encargado de la gestión completa de citas médicas.
    
    Este servicio maneja todas las operaciones relacionadas con las citas médicas,
    incluyendo la programación, consulta, actualización de estados y filtros
    por paciente o profesional.
    
    Características:
    - Programación de citas entre pacientes y profesionales
    - Consultas filtradas por paciente o profesional
    - Actualización de estados de citas
    - Ordenamiento cronológico de citas
    """
    
    @staticmethod
    def obtener_citas():
        """
        Obtiene todas las citas del sistema ordenadas cronológicamente.
        
        Las citas se ordenan por fecha descendente (más recientes primero) y luego
        por hora descendente para mostrar las citas más actuales al inicio.
        
        Returns:
            list[Cita]: Lista de todas las citas ordenadas cronológicamente
        """
        # Realizar consulta ordenada por fecha y hora descendente
        return Cita.query.order_by(Cita.fecha.desc(), Cita.hora.desc()).all()
    
    @staticmethod
    def obtener_citas_por_paciente(paciente_id):
        """
        Obtiene todas las citas de un paciente específico.
        
        Filtra las citas por el ID del paciente y las ordena por fecha
        descendente para mostrar las citas más recientes primero.
        
        Args:
            paciente_id (int): ID del paciente cuyas citas se desean consultar
            
        Returns:
            list[Cita]: Lista de citas del paciente ordenadas por fecha
        """
        # Filtrar por paciente específico y ordenar por fecha descendente
        return Cita.query.filter_by(paciente_id=paciente_id).order_by(Cita.fecha.desc()).all()
    
    @staticmethod
    def obtener_citas_por_profesional(profesional_id):
        """
        Obtiene todas las citas asignadas a un profesional específico.
        
        Filtra las citas por el ID del profesional médico y las ordena por fecha
        descendente para mostrar las citas más recientes primero.
        
        Args:
            profesional_id (int): ID del profesional cuyas citas se desean consultar
            
        Returns:
            list[Cita]: Lista de citas del profesional ordenadas por fecha
        """
        # Filtrar por profesional específico y ordenar por fecha descendente
        return Cita.query.filter_by(profesional_id=profesional_id).order_by(Cita.fecha.desc()).all()
    
    @staticmethod
    def crear_cita(datos_cita):
        """
        Crea una nueva cita médica en el sistema.
        
        Este método programa una nueva cita entre un paciente y un profesional
        médico, estableciendo fecha, hora, tipo de consulta y motivo.
        
        Args:
            datos_cita (dict): Diccionario con los datos de la cita
                - paciente_id (int): ID del paciente
                - profesional_id (int): ID del profesional médico
                - fecha (date): Fecha de la cita
                - hora (time): Hora de la cita
                - tipo_cita (str): Tipo de cita (MEDICINA, PSICOLOGIA, EMERGENCIA)
                - motivo (str, opcional): Motivo de la consulta
                
        Returns:
            Cita: Instancia de la cita recién creada
        """
        # Crear nueva instancia de Cita con los datos proporcionados
        cita = Cita()
        cita.paciente_id = datos_cita['paciente_id']  # ID del paciente
        cita.profesional_id = datos_cita['profesional_id']  # ID del profesional
        cita.fecha = datos_cita['fecha']  # Fecha de la cita
        cita.hora = datos_cita['hora']  # Hora de la cita
        cita.tipo_cita = TipoCita[datos_cita['tipo_cita']]  # Convertir string a enum
        cita.motivo = datos_cita.get('motivo')  # Motivo opcional
        
        # Guardar la cita en la base de datos
        db.session.add(cita)  # Agregar a la sesión
        db.session.commit()  # Confirmar los cambios
        
        return cita  # Retornar la cita creada
    
    @staticmethod
    def actualizar_estado_cita(cita_id, nuevo_estado):
        """
        Actualiza el estado de una cita específica.
        
        Este método permite cambiar el estado de una cita existente
        (PROGRAMADA, COMPLETADA, CANCELADA).
        
        Args:
            cita_id (int): ID de la cita a actualizar
            nuevo_estado (str): Nuevo estado de la cita
            
        Returns:
            Cita: Instancia de la cita actualizada o None si no existe
        """
        # Buscar la cita por su ID
        cita = Cita.query.get(cita_id)
        
        # Verificar que la cita existe
        if not cita:
            return None  # Retornar None si no existe
        
        # Actualizar el estado de la cita
        cita.estado = nuevo_estado
        
        # Confirmar los cambios en la base de datos
        db.session.commit()
        
        return cita  # Retornar la cita actualizada

class ServicioConsulta:
    """
    Servicio encargado de la gestión completa de consultas médicas.
    
    Este servicio maneja el registro y consulta de las consultas médicas realizadas
    durante las citas programadas. Incluye la documentación de diagnósticos,
    tratamientos y evaluaciones de riesgo.
    
    Características:
    - Registro de consultas médicas detalladas
    - Actualización automática del estado de citas
    - Consultas filtradas por paciente
    - Gestión de niveles de riesgo
    """
    
    @staticmethod
    def crear_consulta(cita_id, datos_consulta):
        """
        Crea una nueva consulta médica para una cita programada.
        
        Este método registra los detalles de una consulta realizada, incluyendo
        diagnóstico, tratamiento, observaciones y nivel de riesgo. También actualiza
        automáticamente el estado de la cita a 'COMPLETADA'.
        
        Args:
            cita_id (int): ID de la cita para la cual se registra la consulta
            datos_consulta (dict): Diccionario con los datos de la consulta
                - diagnostico (str): Diagnóstico médico detallado
                - tratamiento (str, opcional): Tratamiento prescrito
                - observaciones (str, opcional): Observaciones adicionales
                - nivel_riesgo (str): Nivel de riesgo (BAJO, MEDIO, ALTO, CRITICO)
                
        Returns:
            Consulta: Instancia de la consulta recién creada
        """
        # Crear nueva instancia de Consulta con los datos proporcionados
        consulta = Consulta()
        consulta.cita_id = cita_id  # ID de la cita asociada
        consulta.diagnostico = datos_consulta['diagnostico']  # Diagnóstico médico (obligatorio)
        consulta.tratamiento = datos_consulta.get('tratamiento')  # Tratamiento opcional
        consulta.observaciones = datos_consulta.get('observaciones')  # Observaciones opcionales
        consulta.nivel_riesgo = NivelRiesgo[datos_consulta['nivel_riesgo']]  # Convertir string a enum
        
        # Agregar la consulta a la sesión de la base de datos
        db.session.add(consulta)
        
        # Actualizar automáticamente el estado de la cita a COMPLETADA
        cita = Cita.query.get(cita_id)
        if cita:
            cita.estado = 'COMPLETADA'  # Marcar cita como completada
        
        # Confirmar todos los cambios en la base de datos
        db.session.commit()
        
        return consulta  # Retornar la consulta creada
    
    @staticmethod
    def obtener_consultas():
        """
        Obtiene todas las consultas médicas del sistema.
        
        Las consultas se ordenan por fecha de consulta descendente para mostrar
        las consultas más recientes primero.
        
        Returns:
            list[Consulta]: Lista de todas las consultas ordenadas cronológicamente
        """
        # Realizar consulta ordenada por fecha de consulta descendente
        return Consulta.query.order_by(Consulta.fecha_consulta.desc()).all()
    
    @staticmethod
    def obtener_consultas_por_paciente(paciente_id):
        """
        Obtiene todas las consultas médicas de un paciente específico.
        
        Realiza un JOIN entre las tablas Consulta y Cita para filtrar las consultas
        por el ID del paciente, ordenadas por fecha de consulta descendente.
        
        Args:
            paciente_id (int): ID del paciente cuyas consultas se desean obtener
            
        Returns:
            list[Consulta]: Lista de consultas del paciente ordenadas cronológicamente
        """
        # Realizar JOIN explícito con tabla Cita para filtrar por paciente y ordenar por fecha
        return Consulta.query.join(Cita, Consulta.cita_id == Cita.id).filter(Cita.paciente_id == paciente_id).order_by(Consulta.fecha_consulta.desc()).all()

class ServicioReporte:
    """
    Servicio encargado de la generación de reportes y estadísticas del sistema.
    
    Este servicio proporciona métodos para obtener estadísticas y análisis de datos
    para el dashboard administrativo y reportes del sistema médico universitario.
    
    Características:
    - Estadísticas de citas por tipo de consulta
    - Análisis de consultas por carrera universitaria
    - Tendencias mensuales de citas médicas
    - Evaluación de niveles de riesgo de pacientes
    - Resumen ejecutivo para dashboard
    """
    
    @staticmethod
    def obtener_estadisticas_citas():
        """
        Obtiene estadísticas de citas agrupadas por tipo de consulta.
        
        Realiza una consulta agregada para contar el número total de citas
        por cada tipo de consulta (MEDICINA, PSICOLOGIA, EMERGENCIA).
        
        Returns:
            dict: Diccionario con tipos de cita como claves y totales como valores
        """
        # Realizar consulta agregada agrupando por tipo de cita
        estadisticas = db.session.query(
            Cita.tipo_cita,  # Campo por el cual agrupar
            func.count(Cita.id).label('total')  # Contar registros y etiquetar como 'total'
        ).group_by(Cita.tipo_cita).all()  # Agrupar por tipo de cita
        
        # Convertir resultado a diccionario para fácil acceso
        return {str(tipo): total for tipo, total in estadisticas}
    
    @staticmethod
    def obtener_estadisticas_consultas_por_carrera():
        """
        Obtiene estadísticas de consultas agrupadas por carrera universitaria.
        
        Realiza JOINs entre las tablas Paciente, Cita y Consulta para obtener
        el número total de consultas realizadas por estudiantes de cada carrera.
        
        Returns:
            dict: Diccionario con carreras como claves y totales de consultas como valores
        """
        # Realizar consulta con JOINs explícitos para relacionar pacientes con consultas
        estadisticas = db.session.query(
            Paciente.carrera,  # Campo por el cual agrupar (carrera universitaria)
            func.count(Consulta.id).label('total')  # Contar consultas
        ).select_from(Paciente).join(Cita, Paciente.id == Cita.paciente_id).join(Consulta, Cita.id == Consulta.cita_id).group_by(Paciente.carrera).all()  # JOINs explícitos y agrupación
        
        # Convertir resultado a diccionario para fácil acceso
        return {carrera: total for carrera, total in estadisticas}
    
    @staticmethod
    def obtener_tendencia_mensual_citas():
        """
        Obtiene la tendencia mensual de citas de los últimos 12 meses.
        
        Calcula el número de citas programadas por mes para mostrar tendencias
        temporales en la demanda de servicios médicos universitarios.
        
        Returns:
            dict: Diccionario con listas de meses y totales para gráficos
        """
        # Calcular fecha límite para los últimos 12 meses
        fecha_limite = datetime.now() - timedelta(days=365)
        
        # Realizar consulta agregada por año y mes
        estadisticas = db.session.query(
            extract('year', Cita.fecha).label('año'),  # Extraer año de la fecha
            extract('month', Cita.fecha).label('mes'),  # Extraer mes de la fecha
            func.count(Cita.id).label('total')  # Contar citas por mes
        ).filter(
            Cita.fecha >= fecha_limite  # Filtrar solo últimos 12 meses
        ).group_by(
            extract('year', Cita.fecha),  # Agrupar por año
            extract('month', Cita.fecha)  # Agrupar por mes
        ).order_by(
            extract('year', Cita.fecha),  # Ordenar por año ascendente
            extract('month', Cita.fecha)  # Ordenar por mes ascendente
        ).all()
        
        # Listas para almacenar los datos formatados
        meses = []  # Lista de etiquetas de meses
        totales = []  # Lista de totales correspondientes
        
        # Procesar cada registro de estadísticas
        for año, mes, total in estadisticas:
            meses.append(f"{int(año)}-{int(mes):02d}")  # Formatear como YYYY-MM
            totales.append(total)  # Agregar total del mes
        
        # Retornar estructura de datos lista para gráficos
        return {'meses': meses, 'totales': totales}
    
    @staticmethod
    def obtener_niveles_riesgo():
        """
        Obtiene estadísticas de consultas agrupadas por nivel de riesgo.
        
        Realiza una consulta agregada para contar el número de consultas
        según su nivel de riesgo (BAJO, MEDIO, ALTO, CRITICO).
        
        Returns:
            dict: Diccionario con niveles de riesgo como claves y totales como valores
        """
        # Realizar consulta agregada agrupando por nivel de riesgo
        estadisticas = db.session.query(
            Consulta.nivel_riesgo,  # Campo por el cual agrupar
            func.count(Consulta.id).label('total')  # Contar consultas por nivel
        ).group_by(Consulta.nivel_riesgo).all()  # Agrupar por nivel de riesgo
        
        # Convertir resultado a diccionario para fácil acceso
        return {str(nivel): total for nivel, total in estadisticas}
    
    @staticmethod
    def obtener_resumen_dashboard():
        """
        Obtiene un resumen ejecutivo general para el dashboard administrativo.
        
        Calcula métricas clave del sistema incluyendo totales de entidades,
        actividad del mes actual y alertas de riesgo para proporcionar una
        vista general del estado del sistema médico universitario.
        
        Returns:
            dict: Diccionario con métricas clave para el dashboard
        """
        # Contar totales generales de cada entidad principal
        total_pacientes = Paciente.query.count()  # Total de pacientes registrados
        total_citas = Cita.query.count()  # Total de citas programadas
        total_consultas = Consulta.query.count()  # Total de consultas realizadas
        
        # Calcular métricas del mes actual
        hoy = datetime.now()  # Fecha y hora actuales
        primer_dia_mes = hoy.replace(day=1)  # Primer día del mes actual
        
        # Contar citas programadas en el mes actual
        citas_mes = Cita.query.filter(Cita.fecha >= primer_dia_mes).count()
        
        # Contar consultas con nivel de riesgo alto o crítico
        # Estas requieren seguimiento prioritario
        consultas_riesgo_alto = Consulta.query.filter(
            Consulta.nivel_riesgo.in_([NivelRiesgo.ALTO, NivelRiesgo.CRITICO])
        ).count()
        
        # Retornar diccionario con todas las métricas calculadas
        return {
            'total_pacientes': total_pacientes,  # Total de estudiantes registrados
            'total_citas': total_citas,  # Total de citas en el sistema
            'total_consultas': total_consultas,  # Total de consultas realizadas
            'citas_mes': citas_mes,  # Citas del mes actual
            'consultas_riesgo_alto': consultas_riesgo_alto  # Consultas que requieren atención
        }
    
    @staticmethod
    def obtener_estadisticas_profesionales():
        """
        Obtiene estadísticas de actividad de profesionales médicos.
        
        Calcula el número de citas atendidas por cada profesional para
        evaluar la carga de trabajo y distribución de servicios.
        
        Returns:
            dict: Diccionario con nombres de profesionales y número de citas
        """
        # Realizar consulta para contar citas por profesional
        estadisticas = db.session.query(
            Usuario.nombre,  # Nombre del profesional
            func.count(Cita.id).label('total_citas')  # Contar citas atendidas
        ).join(Cita, Usuario.id == Cita.profesional_id).filter(
            Usuario.rol == RolUsuario.PROFESIONAL  # Solo profesionales médicos
        ).group_by(Usuario.nombre).all()  # Agrupar por nombre del profesional
        
        # Convertir resultado a diccionario
        return {profesional: total for profesional, total in estadisticas}
    
    @staticmethod
    def obtener_estadisticas_citas_por_tipo():
        """
        Obtiene estadísticas detalladas de citas por tipo de consulta.
        
        Proporciona un análisis más detallado de la distribución de citas
        por tipo de consulta para planificación de recursos.
        
        Returns:
            dict: Diccionario con tipos de cita y estadísticas detalladas
        """
        # Realizar consulta agregada por tipo de cita
        estadisticas = db.session.query(
            Cita.tipo_cita,  # Tipo de consulta
            func.count(Cita.id).label('total'),  # Total de citas
            func.avg(func.extract('hour', Cita.hora)).label('hora_promedio')  # Hora promedio
        ).group_by(Cita.tipo_cita).all()
        
        # Convertir resultado a diccionario estructurado
        return {
            str(tipo): {
                'total': total,
                'hora_promedio': float(hora_promedio or 0)
            }
            for tipo, total, hora_promedio in estadisticas
        }
    
    @staticmethod
    def obtener_horarios_populares():
        """
        Obtiene estadísticas de horarios más populares para citas.
        
        Analiza las horas más demandadas para programar citas médicas
        y ayudar en la planificación de horarios del personal.
        
        Returns:
            dict: Diccionario con horas y frecuencia de citas
        """
        # Realizar consulta para contar citas por hora
        estadisticas = db.session.query(
            func.extract('hour', Cita.hora).label('hora'),  # Extraer hora
            func.count(Cita.id).label('total')  # Contar citas por hora
        ).group_by(
            func.extract('hour', Cita.hora)  # Agrupar por hora
        ).order_by(
            func.count(Cita.id).desc()  # Ordenar por popularidad
        ).all()
        
        # Convertir resultado a diccionario
        return {f"{int(hora)}:00": total for hora, total in estadisticas}
    
    @staticmethod
    def obtener_rendimiento_profesionales():
        """
        Obtiene métricas de rendimiento de profesionales médicos.
        
        Calcula estadísticas de productividad y calidad de atención
        para cada profesional médico del sistema.
        
        Returns:
            dict: Diccionario con métricas de rendimiento por profesional
        """
        # Obtener todos los profesionales
        profesionales = Usuario.query.filter_by(rol=RolUsuario.PROFESIONAL).all()
        
        rendimiento = {}
        
        for profesional in profesionales:
            # Contar citas atendidas
            total_citas = Cita.query.filter_by(profesional_id=profesional.id).count()
            
            # Contar consultas completadas
            consultas_completadas = db.session.query(Consulta).join(Cita).filter(
                Cita.profesional_id == profesional.id
            ).count()
            
            # Calcular tasa de completitud
            tasa_completitud = (consultas_completadas / total_citas * 100) if total_citas > 0 else 0
            
            # Calcular promedio de nivel de riesgo
            promedio_riesgo = db.session.query(
                func.avg(
                    func.case(
                        (Consulta.nivel_riesgo == NivelRiesgo.BAJO, 1),
                        (Consulta.nivel_riesgo == NivelRiesgo.MEDIO, 2),
                        (Consulta.nivel_riesgo == NivelRiesgo.ALTO, 3),
                        (Consulta.nivel_riesgo == NivelRiesgo.CRITICO, 4),
                        else_=0
                    )
                )
            ).join(Cita).filter(Cita.profesional_id == profesional.id).scalar()
            
            rendimiento[profesional.nombre] = {
                'total_citas': total_citas,
                'consultas_completadas': consultas_completadas,
                'tasa_completitud': round(tasa_completitud, 2),
                'promedio_riesgo': round(float(promedio_riesgo or 0), 2)
            }
        
        return rendimiento
    
    @staticmethod
    def obtener_alertas_sistema():
        """
        Obtiene alertas importantes del sistema para el dashboard.
        
        Identifica situaciones que requieren atención administrativa
        como consultas de alto riesgo, citas pendientes, etc.
        
        Returns:
            list: Lista de alertas con información detallada
        """
        alertas = []
        
        # Consultas de alto riesgo sin seguimiento
        consultas_criticas = Consulta.query.filter(
            Consulta.nivel_riesgo == NivelRiesgo.CRITICO
        ).count()
        
        if consultas_criticas > 0:
            alertas.append({
                'tipo': 'critico',
                'mensaje': f'{consultas_criticas} consultas críticas requieren seguimiento',
                'enlace': '/reportes/estadisticas-detalladas'
            })
        
        # Citas pendientes para hoy
        hoy = datetime.now().date()
        citas_hoy = Cita.query.filter(Cita.fecha == hoy).count()
        
        if citas_hoy > 0:
            alertas.append({
                'tipo': 'info',
                'mensaje': f'{citas_hoy} citas programadas para hoy',
                'enlace': '/citas/'
            })
        
        # Usuarios inactivos
        usuarios_inactivos = Usuario.query.filter_by(activo=False).count()
        
        if usuarios_inactivos > 0:
            alertas.append({
                'tipo': 'warning',
                'mensaje': f'{usuarios_inactivos} usuarios inactivos en el sistema',
                'enlace': '/reportes/usuarios'
            })
        
        return alertas
    
    @staticmethod
    def obtener_configuracion_sistema():
        """
        Obtiene configuración del sistema para el panel administrativo.
        
        Proporciona información sobre el estado del sistema y configuraciones
        importantes para el administrador.
        
        Returns:
            dict: Diccionario con configuración del sistema
        """
        # Obtener estadísticas generales del sistema
        total_usuarios = Usuario.query.count()
        usuarios_activos = Usuario.query.filter_by(activo=True).count()
        usuarios_por_rol = db.session.query(
            Usuario.rol,
            func.count(Usuario.id).label('total')
        ).group_by(Usuario.rol).all()
        
        # Información de base de datos
        ultima_cita = Cita.query.order_by(Cita.fecha_creacion.desc()).first()
        ultima_consulta = Consulta.query.order_by(Consulta.fecha_consulta.desc()).first()
        
        return {
            'total_usuarios': total_usuarios,
            'usuarios_activos': usuarios_activos,
            'usuarios_por_rol': {str(rol): total for rol, total in usuarios_por_rol},
            'ultima_cita': ultima_cita.fecha_creacion if ultima_cita else None,
            'ultima_consulta': ultima_consulta.fecha_consulta if ultima_consulta else None,
            'version_sistema': '1.0.0',
            'base_datos': 'PostgreSQL',
            'estado_sistema': 'Operativo'
        }
