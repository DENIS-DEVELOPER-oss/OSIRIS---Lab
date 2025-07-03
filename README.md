# 🏥 Sistema de Gestión Médica Universitaria

Una plataforma web completa desarrollada con Flask para la gestión de consultas médicas en un entorno universitario. El sistema permite a estudiantes, profesionales médicos y administradores interactuar de manera eficiente a través de un sistema integral de gestión de atención médica.

## 🌟 Características Principales

### 🔐 Sistema de Autenticación Basado en Roles
- **Estudiantes**: Acceso con código de matrícula
- **Profesionales**: Acceso con DNI para médicos y psicólogos  
- **Administradores**: Acceso con DNI para personal administrativo
- Gestión segura de sesiones con Flask-Login

### 👥 Gestión de Usuarios
- Registro diferenciado por rol
- Perfiles completos para estudiantes con información académica
- Sistema de respaldo automático en CSV
- Validaciones específicas por tipo de usuario

### 📅 Sistema de Citas Médicas
- Programación de citas por tipo: Medicina, Psicología, Emergencia
- Calendario interactivo para profesionales
- Seguimiento de estado de citas
- Notificaciones automáticas

### 🩺 Registro de Consultas Médicas
- Documentación detallada de diagnósticos
- Sistema de evaluación de niveles de riesgo
- Historial médico completo
- Tratamientos y observaciones

### 📊 Dashboard Administrativo con Estadísticas Avanzadas
- **Gráficos Interactivos con Plotly**:
  - Distribución de citas por tipo de consulta
  - Análisis de consultas por carrera universitaria  
  - Tendencias mensuales de demanda médica
  - Niveles de riesgo de pacientes
- Reportes exportables
- Métricas en tiempo real

### 💾 Sistema de Respaldo
- Exportación automática a CSV
- Importación masiva de usuarios
- Sincronización de datos
- Historial de cambios

## 🛠️ Tecnologías Utilizadas

### Backend
- **Flask** - Framework web principal
- **SQLAlchemy** - ORM para base de datos
- **Flask-Login** - Gestión de autenticación
- **Flask-WTF** - Formularios y protección CSRF
- **PostgreSQL** - Base de datos (producción)
- **Werkzeug** - Utilidades de seguridad

### Frontend
- **Bootstrap 5** - Framework CSS responsivo
- **Plotly.js** - Visualizaciones de datos interactivas
- **Chart.js** - Gráficos adicionales
- **Font Awesome** - Iconografía
- **Google Fonts** - Tipografía profesional

### Análisis de Datos
- **Plotly** - Generación de gráficos estadísticos
- **Numpy** - Procesamiento de datos numéricos

## 🚀 Instalación y Configuración

### Prerrequisitos
- Python 3.11+
- PostgreSQL (para producción)
- Git

### Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/DENIS-DEVELOPER-oss/OSIRIS---Lab.git
cd OSIRIS---Lab
```

2. **Crear entorno virtual**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**
```bash
export SESSION_SECRET="tu-clave-secreta-aqui"
export DATABASE_URL="postgresql://usuario:password@localhost/nombre_bd"
```

5. **Inicializar base de datos**
```bash
python app.py
```

6. **Ejecutar aplicación**
```bash
python main.py
```

## 📋 Uso del Sistema

### Acceso Inicial
- **Administrador por defecto**: 
  - DNI: `12345678`
  - Contraseña: `admin123`

### Flujo de Trabajo
1. **Registro de Usuarios**: Crear estudiantes, profesionales y administradores
2. **Completar Perfiles**: Los estudiantes completan información académica
3. **Programar Citas**: Los administradores coordinan citas médicas
4. **Realizar Consultas**: Los profesionales documentan las consultas
5. **Generar Reportes**: Los administradores analizan estadísticas

## 📊 Características de Reportes

### Gráficos Disponibles
- **Citas por Tipo**: Distribución de consultas médicas vs psicológicas vs emergencias
- **Consultas por Carrera**: Análisis de demanda por programa académico
- **Tendencias Mensuales**: Evolución temporal de la demanda de servicios
- **Dashboard Completo**: Vista integrada con múltiples visualizaciones

### Funcionalidades de Análisis
- Filtros por fecha y tipo
- Exportación de gráficos
- Datos en tiempo real
- Interfaz interactiva con Plotly

## 🔧 Estructura del Proyecto

```
sistema-medico-universitario/
├── app.py                 # Configuración principal de Flask
├── main.py               # Punto de entrada de la aplicación
├── modelos.py            # Modelos de base de datos
├── servicios.py          # Lógica de negocio
├── rutas.py              # Rutas y controladores
├── formularios.py        # Formularios WTF
├── decoradores.py        # Decoradores de seguridad
├── respaldo_usuarios.py  # Sistema de respaldo CSV
├── templates/            # Plantillas HTML
│   ├── base.html
│   ├── reportes/
│   ├── pacientes/
│   └── citas/
├── static/              # Archivos estáticos
└── requirements.txt     # Dependencias
```

## 🛡️ Seguridad

- Autenticación basada en roles
- Protección CSRF en formularios
- Validación de datos en servidor
- Sesiones seguras
- Sanitización de entradas

## 🤝 Contribución

1. Haz fork del proyecto
2. Crea una rama para tu característica (`git checkout -b feature/nueva-caracteristica`)
3. Commit tus cambios (`git commit -am 'Agregar nueva característica'`)
4. Push a la rama (`git push origin feature/nueva-caracteristica`)
5. Crea un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👨‍💻 Autor

Desarrollado para la gestión médica universitaria con enfoque en usabilidad y análisis de datos.

## 🆘 Soporte

Para reportar problemas o solicitar características:
- Abre un issue en GitHub
- Incluye detalles del error y pasos para reproducir
- Especifica tu entorno (SO, versión de Python, etc.)

---

⭐ ¡Si este proyecto te resulta útil, no olvides darle una estrella en GitHub!