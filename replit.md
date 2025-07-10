# Plataforma de Gestión Médica Universitaria

## Overview

This is a web application built with Flask for managing medical consultations in a university setting. The platform enables students, medical professionals, and administrators to interact within a comprehensive healthcare management system. The application provides role-based access control, appointment scheduling, medical consultations recording, and administrative reporting capabilities.

## System Architecture

### Backend Architecture
- **Framework**: Flask with SQLAlchemy ORM
- **Architecture Pattern**: Factory Pattern for app creation
- **Database ORM**: SQLAlchemy with declarative base
- **Authentication**: Flask-Login with role-based access control
- **Form Handling**: WTForms with Flask-WTF for CSRF protection
- **Security**: CSRF protection, password hashing with Werkzeug

### Frontend Architecture
- **Template Engine**: Jinja2 templates
- **CSS Framework**: Bootstrap 5 for responsive design
- **JavaScript**: Chart.js for dashboard visualizations
- **Icons**: Font Awesome
- **Typography**: Google Fonts (Roboto)

### Data Storage
- **Primary Database**: SQLite (development) / PostgreSQL (production ready)
- **ORM**: SQLAlchemy with declarative base
- **Migration Support**: Built-in SQLAlchemy schema management

### Authentication & Authorization
- **User Management**: Custom user model with multiple identification methods
- **Role System**: Enum-based roles (PACIENTE, PROFESIONAL, ADMINISTRADOR)
- **Login Methods**: 
  - Students: Matricula code + password
  - Professionals/Admins: DNI + password
- **Session Management**: Flask-Login for user sessions

## Key Components

### Models (`modelos.py`)
- **Usuario**: Base user model with role-based authentication
- **Paciente**: Student profile with academic information
- **Cita**: Medical appointment scheduling
- **Consulta**: Medical consultation records
- **Enums**: Role, appointment types, and risk levels

### Services (`servicios.py`)
- **ServicioAutenticacion**: User authentication and creation
- **ServicioPaciente**: Patient management operations
- **ServicioCita**: Appointment scheduling logic
- **ServicioConsulta**: Medical consultation handling
- **ServicioReporte**: Statistical reporting and analytics

### Security (`decoradores.py`)
- **@requiere_login**: Authentication requirement decorator
- **@requiere_rol**: Role-specific access control
- **@requiere_administrador**: Admin-only access
- **@requiere_profesional**: Professional-only access

### Forms (`formularios.py`)
- **FormularioLogin**: Role-aware login form
- **FormularioRegistro**: User registration with validation
- **FormularioPaciente**: Patient profile management
- **FormularioCita**: Appointment scheduling
- **FormularioConsulta**: Medical consultation recording

## Data Flow

1. **User Authentication**: 
   - Users login with role-specific identifiers
   - System validates credentials and establishes session
   - Role-based redirection to appropriate dashboard

2. **Patient Management**:
   - Students register with matricula codes
   - Profile completion with academic information
   - Medical history tracking

3. **Appointment Scheduling**:
   - Admins create appointments between patients and professionals
   - Calendar-based scheduling with time slots
   - Appointment type categorization (Medicine, Psychology, Emergency)

4. **Medical Consultations**:
   - Professionals record consultation details
   - Diagnosis and treatment documentation
   - Risk level assessment for psychological cases

5. **Reporting & Analytics**:
   - Administrative dashboard with statistics
   - Chart-based visualizations
   - Trend analysis for medical services

## External Dependencies

### Python Packages
- **Flask**: Web framework
- **Flask-SQLAlchemy**: ORM integration
- **Flask-Login**: User session management
- **Flask-WTF**: Form handling and CSRF protection
- **WTForms**: Form validation
- **Werkzeug**: Password hashing and security utilities

### Frontend Libraries
- **Bootstrap 5**: UI framework
- **Chart.js**: Data visualization
- **Font Awesome**: Icon library
- **Google Fonts**: Typography

### Development Tools
- **SQLAlchemy**: Database ORM
- **Jinja2**: Template engine
- **ProxyFix**: Production deployment support

## Deployment Strategy

### Configuration
- **Environment Variables**: 
  - `SESSION_SECRET`: Flask session security
  - `DATABASE_URL`: Database connection string
- **Database**: SQLite for development, PostgreSQL production-ready
- **WSGI**: ProxyFix middleware for reverse proxy deployment

### Production Considerations
- Database connection pooling configured
- CSRF protection enabled
- Session security with environment-based secrets
- Responsive design for mobile compatibility

## GitHub Repository

**URL**: https://github.com/DENIS-DEVELOPER-oss/OSIRIS---Lab.git

El proyecto está preparado para ser subido a GitHub con:
- README.md completo con documentación
- .gitignore configurado para Flask/Python
- dependencies.txt con todas las dependencias
- INSTRUCCIONES_GITHUB.md con pasos detallados para la subida

## Recent Changes

### July 10, 2025 - Nuevo Panel de Administración con Sidebar Azul
- ✅ **Implementación completa del nuevo diseño de administración:**
  - Creación de `static/css/admin-dashboard.css` - Sistema de estilos exclusivo para administradores
  - Implementación de `templates/admin_base.html` - Template base para panel administrativo
  - Sidebar lateral azul con navegación completa (basado en referencia visual del usuario)
  - Paleta de colores profesional con azul primario (#4f46e5) y gradientes
  - Diseño moderno con tarjetas de estadísticas, gráficos y efectos visuales
  
- ✅ **Dashboard administrativo modernizado:**
  - Tarjetas de estadísticas con iconos y colores temáticos
  - Gráficos integrados con Chart.js (líneas y dona)
  - Sidebar fijo con navegación completa
  - Header con barra de búsqueda y avatar de usuario
  - Animaciones y efectos hover profesionales
  
- ✅ **Templates administrativos actualizados:**
  - `templates/dashboard.html` - Dashboard dual (admin con nuevo diseño, otros roles con diseño anterior)
  - `templates/reportes/usuarios.html` - Gestión de usuarios con nuevo diseño
  - `templates/reportes/crear_usuario_directo.html` - Creación de usuarios modernizada
  - `templates/reportes/estadisticas.html` - Estadísticas con nuevo layout
  - `templates/reportes/respaldo_csv.html` - Gestión de respaldos modernizada
  - `templates/reportes/configuracion.html` - Configuración del sistema modernizada
  
- ✅ **Características del nuevo diseño administrativo:**
  - Sidebar lateral con logo OSIRIS y navegación completa
  - Tarjetas de estadísticas con colores diferenciados (éxito, información, advertencia, peligro)
  - Área de gráficos con Chart.js para visualización de datos
  - Diseño responsivo para dispositivos móviles
  - Efectos de hover y animaciones suaves
  - Iconos Boxicons integrados consistentemente
  
- ✅ **Correcciones técnicas:**
  - Solución de errores de rutas en la navegación administrativa
  - Corrección de `url_for` para todas las rutas de reportes
  - Integración exitosa del sistema dual de templates (admin vs usuarios generales)

### July 10, 2025 - Sistema Completo con Tema Moderno OSIRIS
- ✅ **Rediseño completo del sistema con tema moderno profesional:**
  - Creación de `static/css/modern-theme.css` - Sistema unificado de estilos
  - Implementación de `templates/modern_base.html` - Base template moderna
  - Paleta de colores médica con gradientes cyan y efectos visuales
  - Diseño dark mode profesional con efectos de backdrop blur
  - Iconos Boxicons integrados en toda la aplicación

### July 10, 2025 - Mapa Geográfico de Procedencia en Puno
- ✅ **Implementación completa del sistema de mapeo geográfico:**
  - Agregado campo `procedencia` al modelo Paciente con 22 localidades de Puno
  - Nuevo servicio `ServicioReporte.obtener_datos_geograficos()` con coordenadas reales
  - Template `mapa_procedencia.html` con mapa interactivo usando Leaflet
  - Integración en formulario de pacientes con selector de procedencia
  - Migración de base de datos con nueva columna procedencia

- ✅ **Características del mapa interactivo:**
  - Mapa centrado en la región de Puno con coordenadas reales
  - Marcadores circulares con tamaños y colores según cantidad de pacientes
  - Tooltips y popups informativos para cada localidad
  - Leyenda visual con rangos de colores (1-5, 6-10, 11-20, 21+ pacientes)
  - Tabla de detalles con estadísticas por localidad
  
- ✅ **Localidades incluidas en el sistema:**
  - 22 distritos y provincias principales de Puno
  - Coordenadas geográficas precisas para cada localidad
  - Opción "Otro lugar" para casos especiales
  - Estadísticas automáticas de distribución geográfica

- ✅ **Navegación y accesibilidad:**
  - Nueva opción "Mapa Puno" en sidebar administrativo
  - Acceso directo desde panel de estadísticas  
  - Integración con análisis de segmentación y predicción
  - Diseño responsivo compatible con dispositivos móviles

- ✅ **Gestión de datos CSV:**
  - Coordenadas geográficas cargadas desde `datos_procedencia.csv`
  - Exportación de datos de procedencia a CSV con estadísticas
  - Importación masiva de datos desde archivos CSV
  - Archivo de ejemplo `ejemplo_importacion_procedencia.csv`
  - Interfaz web para carga/descarga de archivos CSV

### July 10, 2025 - Rediseño Completo de Vistas de Citas
- ✅ **Mejora integral del diseño de las vistas de citas:**
  - `templates/citas/lista.html` - Lista moderna con diseño adaptativo por rol de usuario
  - `templates/citas/crear.html` - Formulario estructurado en secciones con validación visual
  - `templates/citas/detalle.html` - Vista detallada con información organizada y acciones contextuales
  - Integración con templates base según rol (admin_base.html vs modern_base.html)

- ✅ **Características del nuevo diseño:**
  - Headers con gradientes temáticos y descripciones contextuales
  - Badges de estado con colores y iconos profesionales (Programada, Completada, Cancelada)
  - Badges de tipo de consulta diferenciados (Medicina, Psicología, Emergencia)
  - Formularios organizados en secciones lógicas (Participantes, Programación, Detalles)
  - Vista de detalle con información de procedencia del paciente integrada
  - Estados vacíos informativos con call-to-action apropiados

- ✅ **Mejoras en experiencia de usuario:**
  - Navegación coherente entre vistas de citas
  - Acciones contextuales según rol del usuario (admin, profesional, paciente)
  - Información de consulta médica integrada en vista de detalle
  - Diseño responsivo para dispositivos móviles
  - Iconos Boxicons consistentes en toda la interfaz

### July 10, 2025 - Limpieza y Optimización Completa del Sistema
- ✅ **Eliminación de código duplicado y archivos innecesarios:**
  - Eliminación de archivos CSS redundantes (estilos.css, login.css, modern-home.css, modern-login.css)
  - Consolidación a solo 2 archivos CSS: modern-theme.css y admin-dashboard.css
  - Actualización de referencias CSS en todos los templates
  - Eliminación de carpeta attached_assets no utilizada
  - Limpieza de archivos temporales y cache

- ✅ **Resolución de errores JavaScript:**
  - Actualización de versiones de Plotly.js de "latest" a versión específica 2.33.0
  - Eliminación completa de dependencias jQuery ($)
  - Reemplazo de jQuery con JavaScript vanilla y Bootstrap 5
  - Corrección del error "$ is not defined" en todas las vistas
  - Modernización de tooltips y modales con Bootstrap 5

- ✅ **Optimización de estructura de archivos:**
  - Reducción de 6 archivos CSS a 2 archivos optimizados
  - Unificación de estilos en modern-theme.css para todos los usuarios
  - Mantenimiento de admin-dashboard.css específico para administradores
  - Eliminación de imports innecesarios y comentarios redundantes
  - Sistema más limpio y mantenible

- ✅ **Rediseño completo del dashboard para consistencia:**
  - Actualización del dashboard para profesionales y pacientes con diseño moderno
  - Headers con gradientes y animaciones consistentes con el tema OSIRIS
  - Tarjetas de estadísticas con gradientes y efectos hover profesionales
  - Botones de acción modernos con colores temáticos diferenciados
  - Diseño responsivo optimizado para todos los dispositivos
  - Eliminación de elementos obsoletos y mejora de la navegación

### July 10, 2025 - Implementación de Sidebar Izquierdo con Logo de Imagen
- ✅ **Migración completa de navegación superior a sidebar izquierdo:**
  - Reemplazo del header horizontal por sidebar fijo lateral de 280px
  - Integración del logo OSIRIS como imagen (osiris.png) en lugar de texto
  - Navegación organizada por secciones según rol del usuario
  - Botón toggle para colapsar/expandir sidebar (70px colapsado)
  - Información del usuario y botón de logout en parte inferior del sidebar
  
- ✅ **Características del nuevo sidebar:**
  - Logo de imagen profesional con texto "OSIRIS" en gradiente
  - Navegación por secciones: Principal, Administración, Profesional, Estudiante, Reportes
  - Efectos hover con gradientes y animaciones suaves
  - Elemento activo destacado automáticamente según la página actual
  - Diseño responsivo que se oculta en dispositivos móviles
  
- ✅ **Estructura de contenido actualizada:**
  - Header superior minimalista con botón toggle y título de página
  - Área de contenido principal con padding optimizado
  - Footer simple en parte inferior
  - Transiciones suaves entre estados colapsado/expandido
  - Compatibilidad total con el diseño existente del dashboard

### July 10, 2025 - Eliminación de Opción de Respaldo CSV
- ✅ **Limpieza de navegación administrativa:**
  - Eliminación de opción "Respaldo CSV" del sidebar de administradores
  - Actualización de templates modern_base.html y admin_base.html
  - Simplificación del menú de reportes manteniendo solo Estadísticas y Configuración
  - Navegación más limpia y enfocada en funciones principales

### July 10, 2025 - Rediseño Completo del Footer
- ✅ **Footer moderno y profesional implementado:**
  - Diseño completamente renovado con gradiente oscuro profesional
  - Logo OSIRIS integrado como imagen en el footer
  - Estructura organizada en 4 secciones: Logo/Descripción, Sistema, Soporte, Información
  - Enlaces de navegación rápida a funciones principales del sistema
  - Información de versión y derechos de autor profesional
  
- ✅ **Características del nuevo footer:**
  - Gradiente de fondo oscuro (2c3e50 a 34495e) para contraste elegante
  - Iconos sociales con efectos hover y animaciones suaves
  - Sección inferior con información técnica y enlaces sociales
  - Elementos con gradientes cyan temáticos del sistema OSIRIS
  - Diseño completamente responsivo para dispositivos móviles
  - Enlaces organizados con efectos de transformación al hover

### July 10, 2025 - Análisis Avanzado: Segmentación y Predicción
- ✅ **Implementación completa de análisis avanzados:**
  - Nuevo servicio `ServicioReporte.obtener_datos_segmentacion()` - Análisis de segmentación de pacientes
  - Nuevo servicio `ServicioReporte.obtener_datos_prediccion()` - Análisis predictivo con tendencias
  - Corrección del error SQLAlchemy en `obtener_rendimiento_profesionales()`
  - Optimización de consultas SQL para PostgreSQL

- ✅ **Gráficos de segmentación implementados:**
  - Segmentación por edad (18-22, 23-27, 28+)
  - Segmentación por tipo de consulta (Medicina, Psicología, Emergencia)
  - Segmentación por nivel de riesgo (Bajo, Medio, Alto, Crítico)
  - Segmentación por actividad (Activos últimos 30 días vs Inactivos)

- ✅ **Análisis predictivo con visualizaciones:**
  - Tendencia de citas con predicción del próximo mes
  - Patrones de consulta por día de la semana
  - Predicción de demanda por tipo de consulta (15% crecimiento estimado)
  - Recomendaciones estratégicas automáticas

- ✅ **Nuevas rutas y templates:**
  - `/reportes/analisis/segmentacion` - Dashboard de segmentación con 4 gráficos
  - `/reportes/analisis/prediccion` - Dashboard predictivo con tendencias
  - Templates con diseño profesional usando Plotly para gráficos interactivos
  - Navegación integrada en sidebar administrativo

- ✅ **Mejoras en la experiencia de usuario:**
  - Acceso directo desde estadísticas a análisis avanzados
  - Tarjetas de insights con métricas clave
  - Recomendaciones estratégicas basadas en datos
  - Botones de navegación entre diferentes análisis

### July 10, 2025 - Limpieza y Optimización del Proyecto
- ✅ Eliminación de archivos innecesarios:
  - Archivos temporales: cookies.txt, comandos_git.txt
  - Archivos de assets no utilizados: attached_assets/
  - Archivos comprimidos duplicados: *.tar.gz
  - Archivos de documentación redundantes: INSTRUCCIONES_GITHUB.md, SUBIDA_SIMPLE_GITHUB.md
  - Scripts de subida temporales: subir_a_github.sh
  - Archivos de ejemplo: usuarios_ejemplo.csv
- ✅ Limpieza de código:
  - Eliminación de imports no utilizados (CSRFProtect)
  - Actualización de dependencies.txt con versiones flexibles
  - Limpieza de carpetas __pycache__ temporales
- ✅ Optimización del .gitignore:
  - Configuración completa para Python/Flask
  - Exclusión de archivos temporales y de desarrollo
  - Preparación para producción
- ✅ Estructura del proyecto simplificada y optimizada

### July 03, 2025 - Sistema Completo con Gráficos Plotly
- ✅ Problemas de CSRF resueltos completamente
- ✅ Gráficos estadísticos interactivos implementados con Plotly:
  - Citas por tipo de consulta (barras)
  - Consultas por carrera universitaria (torta)
  - Tendencia mensual de citas (líneas)
  - Dashboard completo con múltiples visualizaciones
- ✅ Enlaces integrados en dashboard administrativo
- ✅ Sistema de creación de usuarios/pacientes funcional
- ✅ Preparación completa para GitHub

### Funcionalidades Completadas
- Sistema de autenticación por roles
- Gestión completa de usuarios con respaldo CSV
- Sistema de citas médicas
- Registro de consultas médicas
- Dashboard administrativo avanzado
- Estadísticas interactivas con Plotly
- Documentación completa para GitHub

## Changelog

- July 03, 2025. Sistema completo implementado con gráficos Plotly y preparado para GitHub

## User Preferences

Preferred communication style: Simple, everyday language.