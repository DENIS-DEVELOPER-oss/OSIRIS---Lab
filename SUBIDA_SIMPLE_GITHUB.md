# 🚀 Guía Súper Simple para Subir a GitHub

## Opción 1: Usando el Script Automatizado (MÁS FÁCIL)

### Paso 1: Abre la Terminal
- Busca el botón **"Shell"** en la parte inferior de Replit
- Haz clic y se abrirá una pantalla negra

### Paso 2: Ejecuta el Script
Copia y pega este comando en la terminal:
```bash
./subir_a_github.sh
```

Si te pide usuario y contraseña:
- **Usuario**: `DENIS-DEVELOPER-oss`
- **Contraseña**: Tu Personal Access Token de GitHub

---

## Opción 2: Comandos Paso a Paso (MANUAL)

En la terminal, ejecuta uno por uno:

```bash
# 1. Configurar Git
git config --global user.name "DENIS-DEVELOPER-oss"
git config --global user.email "tu-email@ejemplo.com"

# 2. Inicializar repositorio
git init

# 3. Conectar con GitHub
git remote add origin https://github.com/DENIS-DEVELOPER-oss/OSIRIS---Lab.git

# 4. Agregar archivos
git add .

# 5. Hacer commit
git commit -m "Sistema médico universitario completo"

# 6. Subir a GitHub
git push -u origin main
```

---

## Opción 3: Subida Manual (SIN TERMINAL)

### Si no funciona la terminal:

1. **Ve a tu repositorio**: https://github.com/DENIS-DEVELOPER-oss/OSIRIS---Lab
2. **Haz clic en "uploading an existing file"**
3. **Arrastra estos archivos desde Replit**:
   - `README.md`
   - `app.py`
   - `main.py`
   - `modelos.py`
   - `servicios.py`
   - `rutas.py`
   - `formularios.py`
   - `decoradores.py`
   - `respaldo_usuarios.py`
   - `dependencies.txt`
   - `.gitignore`
   - Carpeta `templates/` completa
   - Carpeta `static/` completa

4. **Escribe un mensaje**: "Sistema médico universitario completo"
5. **Haz clic en "Commit changes"**

---

## 🔑 Si Te Pide Autenticación:

### Crear Personal Access Token:
1. Ve a GitHub.com → Settings → Developer settings
2. Personal access tokens → Tokens (classic)
3. Generate new token → Classic
4. Selecciona "repo" permission
5. Copia el token generado
6. Úsalo como contraseña cuando Git te lo pida

---

## ✅ ¿Qué Método Prefieres?

- **Opción 1**: Más automático (recomendado)
- **Opción 2**: Control manual paso a paso  
- **Opción 3**: Sin usar terminal (arrastar archivos)

¡Escoge el que te parezca más fácil!