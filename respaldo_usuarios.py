# -*- coding: utf-8 -*-
"""
Módulo de respaldo y carga de usuarios mediante archivos CSV.

Este módulo proporciona funcionalidades para:
- Guardar usuarios en archivo CSV como respaldo
- Cargar usuarios desde archivo CSV
- Sincronizar datos entre base de datos y archivo CSV
- Mantener integridad de datos

Autor: Sistema Médico Universitario
Fecha: Julio 2025
"""

import csv
import os
from datetime import datetime
from werkzeug.security import generate_password_hash
from app import db
from modelos import Usuario, RolUsuario

# Configuración del archivo CSV
CSV_FILE_PATH = 'usuarios_respaldo.csv'
CSV_HEADERS = [
    'id', 'nombre', 'dni', 'codigo_matricula', 'rol', 
    'password_hash', 'fecha_creacion', 'activo'
]

class ServicioRespaldoCSV:
    """
    Servicio para gestionar respaldos de usuarios en formato CSV.
    
    Este servicio permite mantener sincronizados los datos de usuarios
    entre la base de datos PostgreSQL y un archivo CSV de respaldo.
    """
    
    @staticmethod
    def crear_archivo_csv_si_no_existe():
        """
        Crea el archivo CSV con headers si no existe.
        
        Verifica si el archivo de respaldo existe y lo crea con los
        headers apropiados si es necesario.
        """
        if not os.path.exists(CSV_FILE_PATH):
            with open(CSV_FILE_PATH, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=CSV_HEADERS)
                writer.writeheader()
            print(f"Archivo CSV creado: {CSV_FILE_PATH}")
    
    @staticmethod
    def guardar_usuario_en_csv(usuario):
        """
        Guarda un usuario en el archivo CSV de respaldo.
        
        Args:
            usuario (Usuario): Instancia del usuario a guardar
            
        Returns:
            bool: True si se guardó exitosamente, False en caso contrario
        """
        try:
            # Crear archivo si no existe
            ServicioRespaldoCSV.crear_archivo_csv_si_no_existe()
            
            # Preparar datos del usuario para CSV
            datos_usuario = {
                'id': usuario.id,
                'nombre': usuario.nombre,
                'dni': usuario.dni or '',
                'codigo_matricula': usuario.codigo_matricula or '',
                'rol': usuario.rol.name,
                'password_hash': usuario.password_hash,
                'fecha_creacion': usuario.fecha_creacion.isoformat() if usuario.fecha_creacion else '',
                'activo': str(usuario.activo)
            }
            
            # Escribir en el archivo CSV
            with open(CSV_FILE_PATH, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=CSV_HEADERS)
                writer.writerow(datos_usuario)
            
            print(f"Usuario {usuario.nombre} guardado en CSV correctamente")
            return True
            
        except Exception as e:
            print(f"Error al guardar usuario en CSV: {e}")
            return False
    
    @staticmethod
    def cargar_usuarios_desde_csv():
        """
        Carga usuarios desde el archivo CSV a la base de datos.
        
        Lee el archivo CSV y crea usuarios en la base de datos
        que no existan previamente.
        
        Returns:
            dict: Resumen de la operación con estadísticas
        """
        if not os.path.exists(CSV_FILE_PATH):
            return {
                'success': False,
                'message': 'Archivo CSV no encontrado',
                'usuarios_cargados': 0,
                'usuarios_existentes': 0,
                'errores': 0
            }
        
        usuarios_cargados = 0
        usuarios_existentes = 0
        errores = 0
        
        try:
            with open(CSV_FILE_PATH, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                
                for row in reader:
                    try:
                        # Verificar si el usuario ya existe
                        usuario_existente = None
                        if row['dni']:
                            usuario_existente = Usuario.query.filter_by(dni=row['dni']).first()
                        elif row['codigo_matricula']:
                            usuario_existente = Usuario.query.filter_by(codigo_matricula=row['codigo_matricula']).first()
                        
                        if usuario_existente:
                            usuarios_existentes += 1
                            continue
                        
                        # Crear nuevo usuario
                        usuario = Usuario()
                        usuario.nombre = row['nombre']
                        usuario.dni = row['dni'] if row['dni'] else None
                        usuario.codigo_matricula = row['codigo_matricula'] if row['codigo_matricula'] else None
                        usuario.rol = RolUsuario[row['rol']]
                        usuario.password_hash = row['password_hash']
                        usuario.activo = row['activo'].lower() == 'true'
                        
                        # Guardar en base de datos
                        db.session.add(usuario)
                        db.session.commit()
                        usuarios_cargados += 1
                        
                        print(f"Usuario {usuario.nombre} cargado desde CSV")
                        
                    except Exception as e:
                        errores += 1
                        print(f"Error al procesar fila: {e}")
                        db.session.rollback()
            
            return {
                'success': True,
                'message': f'Proceso completado: {usuarios_cargados} usuarios cargados, {usuarios_existentes} existentes, {errores} errores',
                'usuarios_cargados': usuarios_cargados,
                'usuarios_existentes': usuarios_existentes,
                'errores': errores
            }
            
        except Exception as e:
            print(f"Error al leer archivo CSV: {e}")
            return {
                'success': False,
                'message': f'Error al leer archivo CSV: {e}',
                'usuarios_cargados': 0,
                'usuarios_existentes': 0,
                'errores': 1
            }
    
    @staticmethod
    def exportar_todos_usuarios_a_csv():
        """
        Exporta todos los usuarios de la base de datos al archivo CSV.
        
        Sobrescribe el archivo CSV existente con todos los usuarios
        actuales de la base de datos.
        
        Returns:
            dict: Resultado de la operación
        """
        try:
            usuarios = Usuario.query.all()
            
            # Crear archivo CSV con todos los usuarios
            with open(CSV_FILE_PATH, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=CSV_HEADERS)
                writer.writeheader()
                
                for usuario in usuarios:
                    datos_usuario = {
                        'id': usuario.id,
                        'nombre': usuario.nombre,
                        'dni': usuario.dni or '',
                        'codigo_matricula': usuario.codigo_matricula or '',
                        'rol': usuario.rol.name,
                        'password_hash': usuario.password_hash,
                        'fecha_creacion': usuario.fecha_creacion.isoformat() if usuario.fecha_creacion else '',
                        'activo': str(usuario.activo)
                    }
                    writer.writerow(datos_usuario)
            
            return {
                'success': True,
                'message': f'Exportados {len(usuarios)} usuarios al archivo CSV',
                'total_usuarios': len(usuarios)
            }
            
        except Exception as e:
            print(f"Error al exportar usuarios: {e}")
            return {
                'success': False,
                'message': f'Error al exportar usuarios: {e}',
                'total_usuarios': 0
            }
    
    @staticmethod
    def sincronizar_csv_con_bd():
        """
        Sincroniza el archivo CSV con la base de datos.
        
        Compara los usuarios en CSV con los de la BD y actualiza
        según sea necesario.
        
        Returns:
            dict: Resultado de la sincronización
        """
        try:
            # Primero exportar todos los usuarios actuales
            resultado_exportar = ServicioRespaldoCSV.exportar_todos_usuarios_a_csv()
            
            if resultado_exportar['success']:
                return {
                    'success': True,
                    'message': f'Sincronización completada. {resultado_exportar["total_usuarios"]} usuarios en CSV',
                    'usuarios_sincronizados': resultado_exportar['total_usuarios']
                }
            else:
                return resultado_exportar
                
        except Exception as e:
            return {
                'success': False,
                'message': f'Error en sincronización: {e}',
                'usuarios_sincronizados': 0
            }
    
    @staticmethod
    def obtener_estadisticas_csv():
        """
        Obtiene estadísticas del archivo CSV.
        
        Returns:
            dict: Estadísticas del archivo CSV
        """
        if not os.path.exists(CSV_FILE_PATH):
            return {
                'existe_archivo': False,
                'total_registros': 0,
                'fecha_modificacion': None,
                'tamaño_archivo': 0
            }
        
        try:
            # Contar registros en CSV
            with open(CSV_FILE_PATH, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                total_registros = sum(1 for row in reader)
            
            # Obtener información del archivo
            stat_info = os.stat(CSV_FILE_PATH)
            fecha_modificacion = datetime.fromtimestamp(stat_info.st_mtime)
            tamaño_archivo = stat_info.st_size
            
            return {
                'existe_archivo': True,
                'total_registros': total_registros,
                'fecha_modificacion': fecha_modificacion,
                'tamaño_archivo': tamaño_archivo
            }
            
        except Exception as e:
            print(f"Error al obtener estadísticas CSV: {e}")
            return {
                'existe_archivo': True,
                'total_registros': 0,
                'fecha_modificacion': None,
                'tamaño_archivo': 0,
                'error': str(e)
            }