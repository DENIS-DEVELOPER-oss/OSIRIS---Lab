#!/bin/bash

# Script automatizado para subir el proyecto a GitHub
echo "🚀 Iniciando subida del proyecto a GitHub..."

# Configurar información del usuario
echo "📝 Configurando usuario Git..."
git config --global user.name "DENIS-DEVELOPER-oss"
git config --global user.email "denis.developer.oss@gmail.com"

# Limpiar repositorio existente si hay problemas
echo "🧹 Limpiando repositorio anterior..."
rm -rf .git

# Inicializar nuevo repositorio
echo "🎯 Inicializando nuevo repositorio..."
git init

# Conectar con el repositorio remoto
echo "🔗 Conectando con GitHub..."
git remote add origin https://github.com/DENIS-DEVELOPER-oss/OSIRIS---Lab.git

# Agregar archivos importantes
echo "📁 Agregando archivos al repositorio..."
git add README.md
git add .gitignore
git add dependencies.txt
git add INSTRUCCIONES_GITHUB.md
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
git add replit.md

# Verificar archivos agregados
echo "✅ Archivos preparados para subir:"
git status --short

# Hacer commit
echo "💾 Creando commit..."
git commit -m "Feat: Sistema de Gestión Médica Universitaria completo

✅ Sistema de autenticación por roles (estudiantes, profesionales, admins)
✅ Gestión completa de usuarios con validaciones específicas  
✅ Sistema de citas médicas con calendario interactivo
✅ Registro detallado de consultas médicas
✅ Dashboard administrativo con estadísticas avanzadas
✅ Gráficos interactivos con Plotly:
  - Distribución de citas por tipo
  - Análisis de consultas por carrera  
  - Tendencias mensuales de demanda
✅ Sistema de respaldo automático en CSV
✅ Interfaz responsiva con Bootstrap 5
✅ Base de datos PostgreSQL con SQLAlchemy
✅ Seguridad con Flask-Login y validaciones

Tecnologías: Flask, SQLAlchemy, Plotly, Bootstrap 5, PostgreSQL"

# Intentar subir a GitHub
echo "⬆️ Subiendo a GitHub..."
git push -u origin main

echo "🎉 ¡Subida completada! Verifica en: https://github.com/DENIS-DEVELOPER-oss/OSIRIS---Lab"