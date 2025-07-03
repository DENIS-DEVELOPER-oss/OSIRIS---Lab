# 📋 Instrucciones para Subir el Proyecto a GitHub

## 🎯 Repositorio Destino
**URL**: https://github.com/DENIS-DEVELOPER-oss/OSIRIS---Lab.git

## 📝 Pasos para Subir el Código

### 1. Preparar el Repositorio Local
Desde la terminal de Replit, ejecuta los siguientes comandos:

```bash
# Limpiar el repositorio git existente si hay problemas
rm -rf .git

# Inicializar nuevo repositorio
git init

# Configurar tu información (reemplaza con tus datos)
git config user.name "DENIS-DEVELOPER-oss"
git config user.email "tu-email@ejemplo.com"
```

### 2. Conectar con el Repositorio Remoto
```bash
# Agregar el repositorio remoto
git remote add origin https://github.com/DENIS-DEVELOPER-oss/OSIRIS---Lab.git

# Verificar la conexión
git remote -v
```

### 3. Preparar los Archivos
```bash
# Agregar todos los archivos importantes
git add app.py
git add main.py
git add modelos.py
git add servicios.py
git add rutas.py
git add formularios.py
git add decoradores.py
git add respaldo_usuarios.py
git add templates/
git add static/
git add README.md
git add .gitignore
git add dependencies.txt
git add replit.md

# Verificar qué archivos se van a subir
git status
```

### 4. Hacer el Commit
```bash
# Crear el commit con un mensaje descriptivo
git commit -m "Feat: Sistema de Gestión Médica Universitaria completo

- ✅ Sistema de autenticación por roles (estudiantes, profesionales, admins)
- ✅ Gestión completa de usuarios con validaciones específicas
- ✅ Sistema de citas médicas con calendario interactivo
- ✅ Registro detallado de consultas médicas
- ✅ Dashboard administrativo con estadísticas avanzadas
- ✅ Gráficos interactivos con Plotly:
  * Distribución de citas por tipo
  * Análisis de consultas por carrera
  * Tendencias mensuales de demanda
- ✅ Sistema de respaldo automático en CSV
- ✅ Interfaz responsiva con Bootstrap 5
- ✅ Base de datos PostgreSQL con SQLAlchemy
- ✅ Seguridad con Flask-Login y validaciones

Tecnologías: Flask, SQLAlchemy, Plotly, Bootstrap 5, PostgreSQL"
```

### 5. Subir al Repositorio
```bash
# Primera subida (puede requerir autenticación)
git push -u origin main

# Si hay conflictos o el repositorio ya tiene contenido:
git pull origin main --allow-unrelated-histories
git push origin main
```

## 🔐 Autenticación con GitHub

### Opción 1: Token Personal (Recomendado)
1. Ve a GitHub.com → Settings → Developer settings → Personal access tokens
2. Genera un nuevo token con permisos de "repo"
3. Usa el token como contraseña cuando Git te pida credenciales

### Opción 2: SSH (Avanzado)
```bash
# Generar clave SSH
ssh-keygen -t ed25519 -C "tu-email@ejemplo.com"

# Copiar la clave pública a GitHub
cat ~/.ssh/id_ed25519.pub

# Cambiar la URL remota a SSH
git remote set-url origin git@github.com:DENIS-DEVELOPER-oss/OSIRIS---Lab.git
```

## 📂 Estructura de Archivos que se Subirán

```
OSIRIS---Lab/
├── README.md                 # Documentación principal
├── .gitignore               # Archivos a ignorar
├── dependencies.txt         # Lista de dependencias
├── app.py                   # Configuración principal
├── main.py                  # Punto de entrada
├── modelos.py              # Modelos de base de datos
├── servicios.py            # Lógica de negocio
├── rutas.py                # Controladores y rutas
├── formularios.py          # Formularios WTF
├── decoradores.py          # Decoradores de seguridad
├── respaldo_usuarios.py    # Sistema de respaldo
├── templates/              # Plantillas HTML
│   ├── base.html
│   ├── reportes/
│   ├── pacientes/
│   └── citas/
├── static/                 # Archivos CSS/JS
└── replit.md              # Documentación técnica
```

## ⚠️ Archivos Excluidos por .gitignore
- `__pycache__/` - Cache de Python
- `.pythonlibs/` - Librerías de Replit
- `usuarios_respaldo.csv` - Datos sensibles
- `.replit` - Configuración específica de Replit
- `uv.lock` - Lock file específico de Replit

## 🚀 Verificación Post-Subida

1. **Revisar en GitHub**: Ve a https://github.com/DENIS-DEVELOPER-oss/OSIRIS---Lab
2. **Verificar archivos**: Confirma que todos los archivos importantes están presentes
3. **Probar clonado**: Clona el repositorio en otro lugar para verificar que funciona

## 🔄 Actualizaciones Futuras

Para futuras actualizaciones:
```bash
# Agregar cambios
git add .

# Commit con mensaje descriptivo
git commit -m "Update: descripción de los cambios"

# Subir cambios
git push origin main
```

## 📞 Soporte

Si encuentras problemas:
1. Verifica que tienes permisos en el repositorio
2. Asegúrate de que tu token de GitHub esté activo
3. Revisa que no hay conflictos de archivos
4. Usa `git status` para verificar el estado del repositorio

---

🎉 **¡Una vez completado, tu proyecto estará disponible públicamente en GitHub!**