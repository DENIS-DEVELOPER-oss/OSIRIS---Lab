from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
import plotly.graph_objects as go
import plotly.express as px
import json
import plotly
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from app import db
from modelos import Usuario, Paciente, Cita, Consulta, RolUsuario
from formularios import FormularioLogin, FormularioRegistro, FormularioPaciente, FormularioCita, FormularioConsulta
from servicios import ServicioAutenticacion, ServicioPaciente, ServicioCita, ServicioConsulta, ServicioReporte
from decoradores import requiere_login, requiere_administrador, requiere_profesional

def registrar_rutas(app):
    """Registra todas las rutas de la aplicación"""
    
    # Blueprint para autenticación
    auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
    
    @auth_bp.route('/login', methods=['GET', 'POST'])
    def login():
        """Vista de inicio de sesión"""
        if current_user.is_authenticated:
            return redirect(url_for('main.dashboard'))
        
        form = FormularioLogin()
        if form.validate_on_submit():
            usuario = ServicioAutenticacion.autenticar_usuario(
                form.identificador.data,
                form.password.data
            )
            
            if usuario:
                login_user(usuario)
                flash(f'Bienvenido, {usuario.nombre}!', 'success')
                return redirect(url_for('main.dashboard'))
            else:
                flash('Identificador o contraseña incorrectos', 'danger')
        
        return render_template('login.html', form=form)
    
    @auth_bp.route('/logout')
    @login_required
    def logout():
        """Cerrar sesión"""
        logout_user()
        flash('Sesión cerrada correctamente', 'info')
        return redirect(url_for('auth.login'))
    
    @auth_bp.route('/registro', methods=['GET', 'POST'])
    def registro():
        """Vista de registro de usuarios"""
        form = FormularioRegistro()
        if form.validate_on_submit():
            try:
                usuario = ServicioAutenticacion.crear_usuario({
                    'nombre': form.nombre.data,
                    'rol': form.rol.data,
                    'dni': form.dni.data,
                    'codigo_matricula': form.codigo_matricula.data,
                    'password': form.password.data
                })
                
                flash('Usuario registrado exitosamente', 'success')
                return redirect(url_for('auth.login'))
            except Exception as e:
                flash(f'Error al registrar usuario: {str(e)}', 'danger')
                print(f"Error en registro: {e}")  # Para debugging
        
        return render_template('registro.html', form=form)
    
    # Blueprint principal
    main_bp = Blueprint('main', __name__)
    
    @main_bp.route('/')
    def index():
        """Página principal"""
        if current_user.is_authenticated:
            return redirect(url_for('main.dashboard'))
        return render_template('index.html')
    
    @main_bp.route('/inicio')
    def inicio():
        """Página de inicio moderna"""
        return render_template('index.html')
    
    @main_bp.route('/dashboard')
    @login_required
    def dashboard():
        """Dashboard principal basado en el rol del usuario"""
        if current_user.es_administrador():
            return redirect(url_for('reportes.dashboard_admin'))
        elif current_user.es_profesional():
            # Obtener resumen para profesionales
            resumen = ServicioReporte.obtener_resumen_dashboard()
            return render_template('dashboard.html', resumen=resumen)
        else:  # Paciente
            # Obtener resumen para pacientes
            resumen = ServicioReporte.obtener_resumen_dashboard()
            return render_template('dashboard.html', resumen=resumen)
    
    # Blueprint para pacientes
    pacientes_bp = Blueprint('pacientes', __name__, url_prefix='/pacientes')
    
    @pacientes_bp.route('/')
    @requiere_login
    def lista():
        """Lista de pacientes"""
        if current_user.es_paciente():
            # Los pacientes solo ven su propio perfil
            return redirect(url_for('pacientes.perfil'))
        
        pacientes = ServicioPaciente.obtener_pacientes()
        return render_template('pacientes/lista.html', pacientes=pacientes)
    
    @pacientes_bp.route('/perfil')
    @requiere_login
    def perfil():
        """Perfil del paciente actual"""
        if current_user.es_paciente():
            paciente = current_user.paciente
            if not paciente:
                flash('Complete su información de paciente', 'warning')
                return redirect(url_for('pacientes.completar_perfil'))
        else:
            flash('Solo los pacientes pueden ver esta página', 'danger')
            return redirect(url_for('main.dashboard'))
        
        return render_template('pacientes/perfil.html', paciente=paciente)
    
    @pacientes_bp.route('/completar-perfil', methods=['GET', 'POST'])
    @requiere_login
    def completar_perfil():
        """Completar perfil del paciente"""
        if not current_user.es_paciente():
            flash('Solo los pacientes pueden completar este formulario', 'danger')
            return redirect(url_for('main.dashboard'))
        
        form = FormularioPaciente()
        if form.validate_on_submit():
            try:
                ServicioPaciente.crear_paciente(current_user.id, {
                    'carrera': form.carrera.data,
                    'fecha_nacimiento': form.fecha_nacimiento.data,
                    'telefono': form.telefono.data,
                    'direccion': form.direccion.data,
                    'contacto_emergencia': form.contacto_emergencia.data,
                    'telefono_emergencia': form.telefono_emergencia.data
                })
                
                flash('Perfil completado exitosamente', 'success')
                return redirect(url_for('pacientes.perfil'))
            except Exception as e:
                flash(f'Error al completar perfil: {str(e)}', 'danger')
                print(f"Error en completar perfil: {e}")
        
        return render_template('pacientes/completar_perfil.html', form=form)
    
    # Blueprint para citas
    citas_bp = Blueprint('citas', __name__, url_prefix='/citas')
    
    @citas_bp.route('/')
    @requiere_login
    def lista():
        """Lista de citas basada en el rol"""
        if current_user.es_administrador():
            citas = ServicioCita.obtener_citas()
        elif current_user.es_profesional():
            citas = ServicioCita.obtener_citas_por_profesional(current_user.id)
        else:  # Paciente
            if not current_user.paciente:
                flash('Complete su perfil de paciente primero', 'warning')
                return redirect(url_for('pacientes.completar_perfil'))
            citas = ServicioCita.obtener_citas_por_paciente(current_user.paciente.id)
        
        return render_template('citas/lista.html', citas=citas)
    
    @citas_bp.route('/lista-profesional')
    @requiere_profesional
    def lista_profesional():
        """Lista de citas para profesionales"""
        citas = ServicioCita.obtener_citas_por_profesional(current_user.id)
        return render_template('citas/lista.html', citas=citas, es_profesional=True)
    
    @citas_bp.route('/lista-paciente')
    @requiere_login
    def lista_paciente():
        """Lista de citas para pacientes"""
        if not current_user.es_paciente():
            flash('Solo los pacientes pueden ver esta página', 'danger')
            return redirect(url_for('main.dashboard'))
        
        if not current_user.paciente:
            flash('Complete su perfil de paciente primero', 'warning')
            return redirect(url_for('pacientes.completar_perfil'))
        
        citas = ServicioCita.obtener_citas_por_paciente(current_user.paciente.id)
        return render_template('citas/lista.html', citas=citas, es_paciente=True)
    
    @citas_bp.route('/crear', methods=['GET', 'POST'])
    @requiere_login
    def crear():
        """Crear nueva cita"""
        form = FormularioCita()
        
        # Poblar choices para select fields
        pacientes = ServicioPaciente.obtener_pacientes()
        profesionales = Usuario.query.filter_by(rol=RolUsuario.PROFESIONAL, activo=True).all()
        
        form.paciente_id.choices = [(p.id, f"{p.usuario.nombre} - {p.carrera}") for p in pacientes]
        form.profesional_id.choices = [(p.id, p.nombre) for p in profesionales]
        
        if form.validate_on_submit():
            try:
                cita = ServicioCita.crear_cita({
                    'paciente_id': form.paciente_id.data,
                    'profesional_id': form.profesional_id.data,
                    'fecha': form.fecha.data,
                    'hora': form.hora.data,
                    'tipo_cita': form.tipo_cita.data,
                    'motivo': form.motivo.data
                })
                
                flash('Cita creada exitosamente', 'success')
                return redirect(url_for('citas.lista'))
            except Exception as e:
                flash('Error al crear cita', 'danger')
        
        return render_template('citas/crear.html', form=form)
    
    @citas_bp.route('/<int:cita_id>')
    @requiere_login
    def detalle(cita_id):
        """Detalle de una cita"""
        cita = Cita.query.get_or_404(cita_id)
        
        # Verificar permisos
        if current_user.es_paciente() and cita.paciente.usuario_id != current_user.id:
            flash('No tiene permisos para ver esta cita', 'danger')
            return redirect(url_for('citas.lista'))
        elif current_user.es_profesional() and cita.profesional_id != current_user.id:
            flash('No tiene permisos para ver esta cita', 'danger')
            return redirect(url_for('citas.lista'))
        
        return render_template('citas/detalle.html', cita=cita)
    
    # Blueprint para consultas
    consultas_bp = Blueprint('consultas', __name__, url_prefix='/consultas')
    
    @consultas_bp.route('/')
    @requiere_login
    def lista():
        """Lista de consultas"""
        if current_user.es_administrador():
            consultas = ServicioConsulta.obtener_consultas()
        elif current_user.es_profesional():
            # Obtener consultas de citas del profesional
            consultas = Consulta.query.join(Cita).filter(Cita.profesional_id == current_user.id).all()
        else:  # Paciente
            if not current_user.paciente:
                flash('Complete su perfil de paciente primero', 'warning')
                return redirect(url_for('pacientes.completar_perfil'))
            consultas = ServicioConsulta.obtener_consultas_por_paciente(current_user.paciente.id)
        
        return render_template('consultas/lista.html', consultas=consultas)
    
    @consultas_bp.route('/crear/<int:cita_id>', methods=['GET', 'POST'])
    @requiere_profesional
    def crear(cita_id):
        """Crear consulta para una cita"""
        cita = Cita.query.get_or_404(cita_id)
        
        # Verificar que la cita pertenece al profesional
        if cita.profesional_id != current_user.id:
            flash('No tiene permisos para crear consulta en esta cita', 'danger')
            return redirect(url_for('citas.lista'))
        
        # Verificar que la cita no tenga consulta ya
        if cita.consulta:
            flash('Esta cita ya tiene una consulta registrada', 'warning')
            return redirect(url_for('citas.detalle', cita_id=cita_id))
        
        form = FormularioConsulta()
        if form.validate_on_submit():
            try:
                consulta = ServicioConsulta.crear_consulta(cita_id, {
                    'diagnostico': form.diagnostico.data,
                    'tratamiento': form.tratamiento.data,
                    'observaciones': form.observaciones.data,
                    'nivel_riesgo': form.nivel_riesgo.data
                })
                
                flash('Consulta registrada exitosamente', 'success')
                return redirect(url_for('citas.detalle', cita_id=cita_id))
            except Exception as e:
                flash('Error al registrar consulta', 'danger')
        
        return render_template('consultas/crear.html', form=form, cita=cita)
    
    # Blueprint para reportes y administración
    reportes_bp = Blueprint('reportes', __name__, url_prefix='/reportes')
    
    @reportes_bp.route('/dashboard')
    @requiere_administrador
    def dashboard_admin():
        """Dashboard administrativo principal con resumen general"""
        resumen = ServicioReporte.obtener_resumen_dashboard()
        return render_template('reportes/dashboard.html', resumen=resumen)
    
    @reportes_bp.route('/usuarios')
    @requiere_administrador
    def gestion_usuarios():
        """Gestión de usuarios del sistema"""
        usuarios = Usuario.query.all()
        return render_template('reportes/usuarios.html', usuarios=usuarios)
    
    @reportes_bp.route('/usuarios/<int:usuario_id>/toggle-activo')
    @requiere_administrador
    def toggle_usuario_activo(usuario_id):
        """Activar/Desactivar usuario"""
        usuario = Usuario.query.get_or_404(usuario_id)
        usuario.activo = not usuario.activo
        db.session.commit()
        
        estado = "activado" if usuario.activo else "desactivado"
        flash(f'Usuario {usuario.nombre} {estado} correctamente', 'success')
        return redirect(url_for('reportes.gestion_usuarios'))
    
    @reportes_bp.route('/usuarios/crear-directo', methods=['GET', 'POST'])
    @requiere_administrador
    def crear_usuario_directo():
        """Crear usuario directamente sin CSRF"""
        if request.method == 'POST':
            try:
                # Obtener datos del formulario
                nombre = request.form.get('nombre', '').strip()
                rol = request.form.get('rol', '').strip()
                dni = request.form.get('dni', '').strip()
                codigo_matricula = request.form.get('codigo_matricula', '').strip()
                password = request.form.get('password', '').strip()
                confirm_password = request.form.get('confirm_password', '').strip()
                
                # Campos adicionales para estudiantes
                carrera = request.form.get('carrera', '').strip()
                procedencia = request.form.get('procedencia', '').strip()
                
                # Validaciones básicas
                errores = []
                
                if not nombre:
                    errores.append('El nombre es obligatorio')
                if not rol:
                    errores.append('El rol es obligatorio')
                if not password:
                    errores.append('La contraseña es obligatoria')
                if password != confirm_password:
                    errores.append('Las contraseñas no coinciden')
                if len(password) < 6:
                    errores.append('La contraseña debe tener al menos 6 caracteres')
                
                # Validar campos específicos según rol
                if rol == 'PACIENTE':
                    if not codigo_matricula:
                        errores.append('Código de matrícula es obligatorio para estudiantes')
                    if not carrera:
                        errores.append('Carrera es obligatoria para estudiantes')
                if rol in ['PROFESIONAL', 'ADMINISTRADOR'] and not dni:
                    errores.append('DNI es obligatorio para profesionales y administradores')
                
                # Verificar unicidad
                if dni and Usuario.query.filter_by(dni=dni).first():
                    errores.append('DNI ya registrado en el sistema')
                if codigo_matricula and Usuario.query.filter_by(codigo_matricula=codigo_matricula).first():
                    errores.append('Código de matrícula ya registrado')
                
                if errores:
                    for error in errores:
                        flash(error, 'danger')
                    return render_template('reportes/crear_usuario_directo.html')
                
                # Crear usuario
                usuario = ServicioAutenticacion.crear_usuario({
                    'nombre': nombre,
                    'rol': rol,
                    'dni': dni if dni else None,
                    'codigo_matricula': codigo_matricula if codigo_matricula else None,
                    'password': password
                })
                
                # Si es estudiante, crear perfil de paciente con información académica
                if rol == 'PACIENTE':
                    from datetime import date
                    paciente = ServicioPaciente.crear_paciente(usuario.id, {
                        'carrera': carrera,
                        'procedencia': procedencia if procedencia else None,
                        'fecha_nacimiento': date(2000, 1, 1)  # Fecha placeholder, se puede actualizar después
                    })
                
                flash(f'Usuario {usuario.nombre} creado exitosamente y guardado en CSV', 'success')
                return redirect(url_for('reportes.gestion_usuarios'))
                
            except Exception as e:
                flash(f'Error al crear usuario: {str(e)}', 'danger')
                print(f"Error en creación de usuario: {e}")
                return render_template('reportes/crear_usuario_directo.html')
        
        return render_template('reportes/crear_usuario_directo.html')
    
    @reportes_bp.route('/estadisticas-detalladas')
    @requiere_administrador
    def estadisticas_detalladas():
        """Página de estadísticas detalladas"""
        estadisticas = {
            'citas_por_mes': ServicioReporte.obtener_tendencia_mensual_citas(),
            'consultas_por_carrera': ServicioReporte.obtener_estadisticas_consultas_por_carrera(),
            'niveles_riesgo': ServicioReporte.obtener_niveles_riesgo(),
            'profesionales_activos': ServicioReporte.obtener_estadisticas_profesionales(),
            'citas_por_tipo': ServicioReporte.obtener_estadisticas_citas_por_tipo(),
            'horarios_populares': ServicioReporte.obtener_horarios_populares()
        }
        return render_template('reportes/estadisticas.html', estadisticas=estadisticas)
    
    @reportes_bp.route('/reportes-exportar')
    @requiere_administrador
    def reportes_exportar():
        """Página para exportar reportes"""
        return render_template('reportes/exportar.html')
    
    @reportes_bp.route('/configuracion')
    @requiere_administrador
    def configuracion_sistema():
        """Configuración del sistema"""
        config = ServicioReporte.obtener_configuracion_sistema()
        return render_template('reportes/configuracion.html', config=config)
    
    # APIs para gráficos dinámicos
    @reportes_bp.route('/api/estadisticas-citas')
    @requiere_administrador
    def api_estadisticas_citas():
        """API para estadísticas de citas por estado"""
        estadisticas = ServicioReporte.obtener_estadisticas_citas()
        return jsonify(estadisticas)
    
    @reportes_bp.route('/api/estadisticas-carreras')
    @requiere_administrador
    def api_estadisticas_carreras():
        """API para estadísticas por carrera"""
        estadisticas = ServicioReporte.obtener_estadisticas_consultas_por_carrera()
        return jsonify(estadisticas)
    
    @reportes_bp.route('/api/tendencia-mensual')
    @requiere_administrador
    def api_tendencia_mensual():
        """API para tendencia mensual de citas"""
        tendencia = ServicioReporte.obtener_tendencia_mensual_citas()
        return jsonify(tendencia)
    
    @reportes_bp.route('/api/niveles-riesgo')
    @requiere_administrador
    def api_niveles_riesgo():
        """API para distribución de niveles de riesgo"""
        niveles = ServicioReporte.obtener_niveles_riesgo()
        return jsonify(niveles)
    
    @reportes_bp.route('/api/profesionales-rendimiento')
    @requiere_administrador
    def api_profesionales_rendimiento():
        """API para rendimiento de profesionales"""
        rendimiento = ServicioReporte.obtener_rendimiento_profesionales()
        return jsonify(rendimiento)
    
    @reportes_bp.route('/api/horarios-populares')
    @requiere_administrador
    def api_horarios_populares():
        """API para horarios más populares"""
        horarios = ServicioReporte.obtener_horarios_populares()
        return jsonify(horarios)
    
    @reportes_bp.route('/api/alertas-sistema')
    @requiere_administrador
    def api_alertas_sistema():
        """API para alertas del sistema"""
        alertas = ServicioReporte.obtener_alertas_sistema()
        return jsonify(alertas)
    
    # === RUTAS PARA GESTIÓN DE RESPALDO CSV ===
    
    @reportes_bp.route('/respaldo-csv')
    @requiere_administrador
    def gestion_respaldo_csv():
        """Página de gestión de respaldo CSV"""
        from respaldo_usuarios import ServicioRespaldoCSV
        estadisticas = ServicioRespaldoCSV.obtener_estadisticas_csv()
        return render_template('reportes/respaldo_csv.html', estadisticas=estadisticas)
    
    @reportes_bp.route('/respaldo-csv/exportar')
    @requiere_administrador
    def exportar_usuarios_csv():
        """Exportar todos los usuarios a CSV"""
        from respaldo_usuarios import ServicioRespaldoCSV
        resultado = ServicioRespaldoCSV.exportar_todos_usuarios_a_csv()
        
        if resultado['success']:
            flash(resultado['message'], 'success')
        else:
            flash(resultado['message'], 'danger')
        
        return redirect(url_for('reportes.gestion_respaldo_csv'))
    
    @reportes_bp.route('/respaldo-csv/importar')
    @requiere_administrador
    def importar_usuarios_csv():
        """Importar usuarios desde CSV"""
        from respaldo_usuarios import ServicioRespaldoCSV
        resultado = ServicioRespaldoCSV.cargar_usuarios_desde_csv()
        
        if resultado['success']:
            flash(resultado['message'], 'success')
        else:
            flash(resultado['message'], 'danger')
        
        return redirect(url_for('reportes.gestion_respaldo_csv'))
    
    @reportes_bp.route('/respaldo-csv/sincronizar')
    @requiere_administrador
    def sincronizar_csv():
        """Sincronizar CSV con base de datos"""
        from respaldo_usuarios import ServicioRespaldoCSV
        resultado = ServicioRespaldoCSV.sincronizar_csv_con_bd()
        
        if resultado['success']:
            flash(resultado['message'], 'success')
        else:
            flash(resultado['message'], 'danger')
        
        return redirect(url_for('reportes.gestion_respaldo_csv'))
    
    # === RUTAS PARA GRÁFICOS DE PLOTLY ===
    
    @reportes_bp.route('/graficos/citas-por-tipo')
    @requiere_administrador
    def grafico_citas_por_tipo():
        """Gráfico de citas por tipo de consulta"""
        datos = ServicioReporte.obtener_estadisticas_citas()
        
        # Crear gráfico de barras con Plotly
        fig = go.Figure(data=[
            go.Bar(
                x=list(datos.keys()),
                y=list(datos.values()),
                marker_color=['#28a745', '#17a2b8', '#dc3545'],
                text=list(datos.values()),
                textposition='auto',
            )
        ])
        
        fig.update_layout(
            title='Distribución de Citas por Tipo de Consulta',
            xaxis_title='Tipo de Consulta',
            yaxis_title='Número de Citas',
            template='plotly_white',
            height=400
        )
        
        grafico_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return render_template('reportes/grafico_plotly.html', 
                             grafico_json=grafico_json, 
                             titulo='Citas por Tipo')
    
    @reportes_bp.route('/graficos/consultas-por-carrera')
    @requiere_administrador
    def grafico_consultas_por_carrera():
        """Gráfico de consultas por carrera universitaria"""
        datos = ServicioReporte.obtener_estadisticas_consultas_por_carrera()
        
        if not datos:
            flash('No hay datos de consultas por carrera disponibles', 'warning')
            return redirect(url_for('reportes.dashboard_admin'))
        
        # Crear gráfico de torta con Plotly
        fig = go.Figure(data=[
            go.Pie(
                labels=list(datos.keys()),
                values=list(datos.values()),
                hole=0.3,
                textinfo='label+percent',
                textposition='outside'
            )
        ])
        
        fig.update_layout(
            title='Consultas Médicas por Carrera Universitaria',
            template='plotly_white',
            height=500
        )
        
        grafico_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return render_template('reportes/grafico_plotly.html', 
                             grafico_json=grafico_json, 
                             titulo='Consultas por Carrera')
    
    @reportes_bp.route('/graficos/tendencia-mensual')
    @requiere_administrador
    def grafico_tendencia_mensual():
        """Gráfico de tendencia mensual de citas"""
        datos = ServicioReporte.obtener_tendencia_mensual_citas()
        
        if not datos:
            flash('No hay datos de tendencia mensual disponibles', 'warning')
            return redirect(url_for('reportes.dashboard_admin'))
        
        # Crear gráfico de líneas con Plotly
        fig = go.Figure(data=[
            go.Scatter(
                x=datos.get('meses', []),
                y=datos.get('totales', []),
                mode='lines+markers',
                line=dict(color='#007bff', width=3),
                marker=dict(size=8),
                name='Citas por Mes'
            )
        ])
        
        fig.update_layout(
            title='Tendencia Mensual de Citas Médicas',
            xaxis_title='Mes',
            yaxis_title='Número de Citas',
            template='plotly_white',
            height=400
        )
        
        grafico_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return render_template('reportes/grafico_plotly.html', 
                             grafico_json=grafico_json, 
                             titulo='Tendencia Mensual')
    
    @reportes_bp.route('/graficos/dashboard-completo')
    @requiere_administrador
    def dashboard_graficos_completo():
        """Dashboard completo con múltiples gráficos"""
        # Obtener todos los datos
        citas_por_tipo = ServicioReporte.obtener_estadisticas_citas()
        consultas_por_carrera = ServicioReporte.obtener_estadisticas_consultas_por_carrera()
        tendencia_mensual = ServicioReporte.obtener_tendencia_mensual_citas()
        
        # Crear múltiples gráficos
        graficos = {}
        
        # Gráfico 1: Citas por tipo
        if citas_por_tipo:
            fig1 = go.Figure(data=[
                go.Bar(
                    x=list(citas_por_tipo.keys()),
                    y=list(citas_por_tipo.values()),
                    marker_color=['#28a745', '#17a2b8', '#dc3545'],
                    text=list(citas_por_tipo.values()),
                    textposition='auto',
                )
            ])
            fig1.update_layout(
                title='Citas por Tipo de Consulta',
                xaxis_title='Tipo',
                yaxis_title='Cantidad',
                template='plotly_white',
                height=300
            )
            graficos['citas_tipo'] = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
        
        # Gráfico 2: Consultas por carrera
        if consultas_por_carrera:
            fig2 = go.Figure(data=[
                go.Pie(
                    labels=list(consultas_por_carrera.keys()),
                    values=list(consultas_por_carrera.values()),
                    hole=0.3
                )
            ])
            fig2.update_layout(
                title='Consultas por Carrera',
                template='plotly_white',
                height=300
            )
            graficos['consultas_carrera'] = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
        
        # Gráfico 3: Tendencia mensual
        if tendencia_mensual:
            fig3 = go.Figure(data=[
                go.Scatter(
                    x=tendencia_mensual.get('meses', []),
                    y=tendencia_mensual.get('totales', []),
                    mode='lines+markers',
                    line=dict(color='#007bff', width=3),
                    marker=dict(size=6)
                )
            ])
            fig3.update_layout(
                title='Tendencia Mensual',
                xaxis_title='Mes',
                yaxis_title='Citas',
                template='plotly_white',
                height=300
            )
            graficos['tendencia_mensual'] = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
        
        return render_template('reportes/dashboard_graficos.html', graficos=graficos)
    
    # === RUTAS PARA ANÁLISIS AVANZADO ===
    
    @reportes_bp.route('/analisis/segmentacion')
    @requiere_administrador
    def analisis_segmentacion():
        """Análisis de segmentación de pacientes"""
        datos = ServicioReporte.obtener_datos_segmentacion()
        
        # Crear gráficos de segmentación
        graficos = {}
        
        # Gráfico 1: Segmentación por edad
        if datos.get('por_edad'):
            fig1 = go.Figure(data=[
                go.Pie(
                    labels=list(datos['por_edad'].keys()),
                    values=list(datos['por_edad'].values()),
                    hole=0.4,
                    marker=dict(colors=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A'])
                )
            ])
            fig1.update_layout(
                title='Segmentación por Edad',
                template='plotly_white',
                height=400
            )
            graficos['por_edad'] = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
        
        # Gráfico 2: Segmentación por tipo de consulta
        if datos.get('por_tipo_consulta'):
            fig2 = go.Figure(data=[
                go.Bar(
                    x=list(datos['por_tipo_consulta'].keys()),
                    y=list(datos['por_tipo_consulta'].values()),
                    marker_color=['#28a745', '#17a2b8', '#dc3545', '#ffc107']
                )
            ])
            fig2.update_layout(
                title='Segmentación por Tipo de Consulta',
                xaxis_title='Tipo de Consulta',
                yaxis_title='Número de Pacientes',
                template='plotly_white',
                height=400
            )
            graficos['por_tipo_consulta'] = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
        
        # Gráfico 3: Segmentación por nivel de riesgo
        if datos.get('por_riesgo'):
            fig3 = go.Figure(data=[
                go.Pie(
                    labels=list(datos['por_riesgo'].keys()),
                    values=list(datos['por_riesgo'].values()),
                    hole=0.3,
                    marker=dict(colors=['#28a745', '#ffc107', '#fd7e14', '#dc3545'])
                )
            ])
            fig3.update_layout(
                title='Segmentación por Nivel de Riesgo',
                template='plotly_white',
                height=400
            )
            graficos['por_riesgo'] = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
        
        # Gráfico 4: Segmentación por actividad
        if datos.get('por_actividad'):
            fig4 = go.Figure(data=[
                go.Bar(
                    x=list(datos['por_actividad'].keys()),
                    y=list(datos['por_actividad'].values()),
                    marker_color=['#28a745', '#6c757d']
                )
            ])
            fig4.update_layout(
                title='Segmentación por Actividad',
                xaxis_title='Tipo de Actividad',
                yaxis_title='Número de Pacientes',
                template='plotly_white',
                height=400
            )
            graficos['por_actividad'] = json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)
        
        return render_template('reportes/analisis_segmentacion.html', 
                             graficos=graficos, 
                             datos=datos)
    
    @reportes_bp.route('/analisis/prediccion')
    @requiere_administrador
    def analisis_prediccion():
        """Análisis predictivo de citas y consultas"""
        datos = ServicioReporte.obtener_datos_prediccion()
        
        # Crear gráficos predictivos
        graficos = {}
        
        # Gráfico 1: Tendencia de citas con predicción
        if datos.get('tendencia_citas'):
            tendencia = datos['tendencia_citas']
            
            # Agregar mes futuro para predicción
            meses_completos = tendencia['meses'] + ['Próximo mes']
            valores_completos = tendencia['valores'] + [tendencia['prediccion_proximo']]
            
            fig1 = go.Figure()
            
            # Línea de datos históricos
            fig1.add_trace(go.Scatter(
                x=tendencia['meses'],
                y=tendencia['valores'],
                mode='lines+markers',
                name='Datos Históricos',
                line=dict(color='#007bff', width=3),
                marker=dict(size=8)
            ))
            
            # Punto de predicción
            fig1.add_trace(go.Scatter(
                x=['Próximo mes'],
                y=[tendencia['prediccion_proximo']],
                mode='markers',
                name='Predicción',
                marker=dict(size=12, color='#dc3545', symbol='star')
            ))
            
            fig1.update_layout(
                title='Tendencia de Citas con Predicción',
                xaxis_title='Mes',
                yaxis_title='Número de Citas',
                template='plotly_white',
                height=400
            )
            graficos['tendencia_citas'] = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
        
        # Gráfico 2: Patrones semanales
        if datos.get('patrones_semanales'):
            fig2 = go.Figure(data=[
                go.Bar(
                    x=list(datos['patrones_semanales'].keys()),
                    y=list(datos['patrones_semanales'].values()),
                    marker_color=['#4ECDC4', '#45B7D1', '#FFA07A', '#FF6B6B', '#98D8C8', '#F7DC6F', '#BB8FCE']
                )
            ])
            fig2.update_layout(
                title='Patrones de Consulta por Día de la Semana',
                xaxis_title='Día de la Semana',
                yaxis_title='Número de Consultas',
                template='plotly_white',
                height=400
            )
            graficos['patrones_semanales'] = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
        
        # Gráfico 3: Demanda por tipo de consulta (actual vs predicción)
        if datos.get('demanda_por_tipo'):
            tipos = list(datos['demanda_por_tipo'].keys())
            valores_actuales = [datos['demanda_por_tipo'][t]['actual'] for t in tipos]
            valores_prediccion = [datos['demanda_por_tipo'][t]['prediccion'] for t in tipos]
            
            fig3 = go.Figure(data=[
                go.Bar(name='Actual', x=tipos, y=valores_actuales, marker_color='#17a2b8'),
                go.Bar(name='Predicción', x=tipos, y=valores_prediccion, marker_color='#28a745')
            ])
            fig3.update_layout(
                title='Demanda por Tipo de Consulta: Actual vs Predicción',
                xaxis_title='Tipo de Consulta',
                yaxis_title='Número de Consultas',
                template='plotly_white',
                height=400,
                barmode='group'
            )
            graficos['demanda_por_tipo'] = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
        
        return render_template('reportes/analisis_prediccion.html', 
                             graficos=graficos, 
                             datos=datos)
    
    @reportes_bp.route('/mapa/procedencia')
    @requiere_administrador
    def mapa_procedencia():
        """Mapa geográfico de procedencia de pacientes en Puno"""
        datos_geograficos = ServicioReporte.obtener_datos_geograficos()
        
        return render_template('reportes/mapa_procedencia.html', 
                             datos=datos_geograficos)
    
    @reportes_bp.route('/mapa/exportar-csv')
    @requiere_administrador
    def exportar_procedencia_csv():
        """Exportar datos de procedencia a CSV"""
        try:
            archivo = ServicioReporte.exportar_datos_procedencia_csv()
            
            # Enviar archivo como descarga
            from flask import send_file
            import os
            
            return send_file(
                archivo,
                as_attachment=True,
                download_name=f'procedencia_pacientes_{datetime.now().strftime("%Y%m%d")}.csv',
                mimetype='text/csv'
            )
        except Exception as e:
            flash(f'Error al exportar CSV: {str(e)}', 'error')
            return redirect(url_for('reportes.mapa_procedencia'))
    
    @reportes_bp.route('/mapa/importar-csv', methods=['GET', 'POST'])
    @requiere_administrador
    def importar_procedencia_csv():
        """Importar datos de procedencia desde CSV"""
        if request.method == 'POST':
            if 'archivo_csv' not in request.files:
                flash('No se seleccionó archivo', 'error')
                return redirect(url_for('reportes.mapa_procedencia'))
            
            archivo = request.files['archivo_csv']
            if archivo.filename == '':
                flash('No se seleccionó archivo', 'error')
                return redirect(url_for('reportes.mapa_procedencia'))
            
            if archivo and archivo.filename.endswith('.csv'):
                # Guardar archivo temporalmente
                import tempfile
                import os
                
                with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp:
                    archivo.save(tmp.name)
                    
                    # Importar datos
                    resultado = ServicioReporte.importar_datos_procedencia_csv(tmp.name)
                    
                    # Eliminar archivo temporal
                    os.unlink(tmp.name)
                    
                    if resultado['exitoso']:
                        flash(f'Importación exitosa: {resultado["registros_procesados"]} registros procesados', 'success')
                        if resultado['errores']:
                            flash(f'Advertencias: {len(resultado["errores"])} errores encontrados', 'warning')
                    else:
                        flash('Error en la importación', 'error')
                        for error in resultado['errores']:
                            flash(error, 'error')
            else:
                flash('El archivo debe ser formato CSV', 'error')
        
        return redirect(url_for('reportes.mapa_procedencia'))
    
    # Registrar blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(pacientes_bp)
    app.register_blueprint(citas_bp)
    app.register_blueprint(consultas_bp)
    app.register_blueprint(reportes_bp)
    
    return app
