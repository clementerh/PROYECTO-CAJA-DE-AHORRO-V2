"""
conexion_bd.py
Módulo de conexión a la base de datos MySQL
Sistema de Caja de Ahorro - UPTNM "Ludovico Silva"
"""

import mysql.connector
from mysql.connector import Error
import hashlib


# ============================================================
# CONFIGURACIÓN DE CONEXIÓN
# Modifica estos valores según tu instalación de MySQL
# ============================================================
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'clemente123',          # ← Pon tu contraseña de MySQL aquí
    'database': 'caja_ahorro',
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_spanish_ci',
    'autocommit': True,
    # En Windows evita crashes silenciosos del conector C y fuerza implementación Python.
    'use_pure': True,
    # Evita que el login se quede "colgado" mucho tiempo si MySQL no responde.
    'connection_timeout': 5,
}


def obtener_conexion():
    """
    Crea y retorna una conexión a la base de datos.
    Returns:
        mysql.connector.connection o None si falla
    """
    try:
        conexion = mysql.connector.connect(**DB_CONFIG)
        if conexion.is_connected():
            return conexion
    except Error as e:
        print(f"[ERROR BD] No se pudo conectar: {e}")
        return None
    except Exception as e:
        print(f"[ERROR BD] Falla inesperada en conexión: {e}")
        return None


def ejecutar_consulta(query, params=None, fetchone=False):
    """
    Ejecuta una consulta SELECT y retorna resultados.
    Args:
        query: Consulta SQL
        params: Tupla de parámetros (opcional)
        fetchone: Si True, retorna solo un registro
    Returns:
        Lista de diccionarios o un diccionario si fetchone=True
    """
    conexion = obtener_conexion()
    if not conexion:
        return None

    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute(query, params)
        if fetchone:
            resultado = cursor.fetchone()
        else:
            resultado = cursor.fetchall()
        return resultado
    except Error as e:
        print(f"[ERROR CONSULTA] {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conexion and conexion.is_connected():
            conexion.close()


def ejecutar_accion(query, params=None):
    """
    Ejecuta INSERT, UPDATE o DELETE.
    Args:
        query: Consulta SQL
        params: Tupla de parámetros (opcional)
    Returns:
        True si tuvo éxito, False si falló
    """
    conexion = obtener_conexion()
    if not conexion:
        return False

    try:
        cursor = conexion.cursor()
        cursor.execute(query, params)
        conexion.commit()
        return True
    except Error as e:
        print(f"[ERROR ACCIÓN] {e}")
        conexion.rollback()
        return False
    finally:
        if cursor:
            cursor.close()
        if conexion and conexion.is_connected():
            conexion.close()


def obtener_ultimo_id(query, params=None):
    """
    Ejecuta un INSERT y retorna el último ID generado.
    """
    conexion = obtener_conexion()
    if not conexion:
        return None

    try:
        cursor = conexion.cursor()
        cursor.execute(query, params)
        conexion.commit()
        return cursor.lastrowid
    except Error as e:
        print(f"[ERROR INSERT] {e}")
        conexion.rollback()
        return None
    finally:
        if cursor:
            cursor.close()
        if conexion and conexion.is_connected():
            conexion.close()


def hash_clave(clave):
    """
    Genera el hash SHA256 de una contraseña.
    Debe coincidir con SHA2() de MySQL.
    """
    return hashlib.sha256(clave.encode('utf-8')).hexdigest()


def validar_usuario(usuario_cedula, clave):
    """
    Valida las credenciales de un usuario contra la BD.
    Args:
        usuario_cedula: Cédula del usuario
        clave: Contraseña en texto plano
    Returns:
        Diccionario con datos del usuario si es válido, None si no
    """
    clave_hash = hash_clave(clave)
    query = """
        SELECT id_usuario, cedula, nombre, apellido, correo, rol
        FROM usuario
        WHERE cedula = %s AND clave_hash = %s AND activo = TRUE
    """
    return ejecutar_consulta(query, (usuario_cedula, clave_hash), fetchone=True)


def probar_conexion():
    """
    Prueba rápida de conexión a la BD.
    Returns:
        True si conecta, False si no
    """
    conexion = obtener_conexion()
    if conexion:
        conexion.close()
        return True
    return False


# ============================================================
# PRUEBA RÁPIDA
# ============================================================
if __name__ == "__main__":
    print("Probando conexión a la base de datos...")
    if probar_conexion():
        print("✅ Conexión exitosa a 'caja_ahorro'")

        # Probar login con admin
        usuario = validar_usuario("V-00.000.001", "admin123")
        if usuario:
            print(f"✅ Login exitoso: {usuario['nombre']} {usuario['apellido']} ({usuario['rol']})")
        else:
            print("❌ No se pudo validar el usuario admin")
    else:
        print("❌ No se pudo conectar a la base de datos")
        print("   Verifica que MySQL esté corriendo y que la BD 'caja_ahorro' exista")
        print("   Revisa la contraseña en DB_CONFIG")
