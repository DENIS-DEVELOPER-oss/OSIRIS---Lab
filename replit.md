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

### July 10, 2025 - Interfaz Moderna OSIRIS Implementada
- ✅ Diseño de login completamente renovado con estilo moderno basado en imagen proporcionada:
  - Formulario de login con dos secciones (formulario + bienvenida)
  - Fondo oscuro con efectos de gradiente y partículas
  - Campos con iconos de usuario y contraseña
  - Botón de login con gradiente azul cian
  - Sección "WELCOME BACK!" con logo OSIRIS
  - Efectos visuales y animaciones suaves
- ✅ Página de inicio rediseñada con estilo médico profesional:
  - Header con logo médico y navegación moderna
  - Sección principal con texto "TECNOLOGÍA INTELIGENTE"
  - Ilustración médica con cerebro, estetoscopio y cruz médica (SVG)
  - Iconos sociales y botón de llamada a la acción
  - Animaciones de partículas flotantes
  - Diseño totalmente responsivo
- ✅ Nuevos archivos CSS creados:
  - `static/css/modern-login.css` - Estilos para login moderno
  - `static/css/modern-home.css` - Estilos para página de inicio
- ✅ Imágenes integradas correctamente en `static/images/`
- ✅ Navegación fluida entre inicio y login

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