#!/usr/bin/env python3
"""
API REST para FixCellGt - Serverless en Vercel
Versión compatible con Vercel Serverless Functions
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor
import os
import sys

app = Flask(__name__)
CORS(app)

# Configuración de base de datos desde variables de entorno
DB_HOST = os.getenv('SUPABASE_DB_HOST')
DB_PORT = os.getenv('SUPABASE_DB_PORT', '5432')
DB_NAME = os.getenv('SUPABASE_DB_NAME', 'postgres')
DB_USER = os.getenv('SUPABASE_DB_USER')
DB_PASSWORD = os.getenv('SUPABASE_DB_PASSWORD')

def conectar_db():
    """Conecta a Supabase"""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            sslmode='require'
        )
        return conn
    except Exception as e:
        print(f"Error conectando a DB: {e}")
        return None

# ==================== ENDPOINTS ====================

@app.route('/', methods=['GET'])
def index():
    """Endpoint raíz"""
    return jsonify({
        'status': 'ok',
        'message': 'FixCellGt API v1.0',
        'endpoints': {
            'GET /api/marcas': 'Obtener todas las marcas',
            'GET /api/repuestos': 'Obtener todos los repuestos',
            'GET /api/calidades': 'Obtener todas las calidades',
            'GET /api/inventario/buscar': 'Buscar en inventario',
            'GET /api/estadisticas': 'Estadísticas generales'
        }
    })

@app.route('/api/marcas', methods=['GET'])
def obtener_marcas():
    """Obtiene todas las marcas"""
    conn = conectar_db()
    if not conn:
        return jsonify({'error': 'Error de conexión'}), 500
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT nombre_marca FROM marcas ORDER BY nombre_marca")
        marcas = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return jsonify(marcas)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/repuestos', methods=['GET'])
def obtener_repuestos():
    """Obtiene todos los tipos de repuestos"""
    conn = conectar_db()
    if not conn:
        return jsonify({'error': 'Error de conexión'}), 500
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT nombre_repuesto FROM tipo_repuestos ORDER BY nombre_repuesto")
        repuestos = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return jsonify(repuestos)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/calidades', methods=['GET'])
def obtener_calidades():
    """Obtiene todas las calidades"""
    conn = conectar_db()
    if not conn:
        return jsonify({'error': 'Error de conexión'}), 500
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT nombre_calidad FROM calidades ORDER BY nombre_calidad")
        calidades = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return jsonify(calidades)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/inventario/buscar', methods=['GET'])
def buscar_inventario():
    """Busca en inventario con filtros"""
    conn = conectar_db()
    if not conn:
        return jsonify({'error': 'Error de conexión'}), 500
    try:
        # Parámetros de búsqueda
        marca = request.args.get('marca', '')
        modelo = request.args.get('modelo', '')
        repuesto = request.args.get('repuesto', '')
        calidad = request.args.get('calidad', '')
        precio_min = request.args.get('precio_min', 0)
        precio_max = request.args.get('precio_max', 999999)

        # Construir consulta SQL dinámicamente
        sql = """
            SELECT
                ma.nombre_marca as marca,
                m.nombre_modelo as modelo,
                tr.nombre_repuesto as repuesto,
                c.nombre_calidad as calidad,
                col.nombre_color as color,
                inv.precio_base_mayorista as precio_base,
                inv.precio_reparacion as precio_reparacion,
                inv.margen_reparacion as margen,
                inv.cantidad as cantidad
            FROM inventario inv
            JOIN marcas ma ON inv.id_marca = ma.id_marca
            JOIN modelos m ON inv.id_modelo = m.id_modelo
            JOIN tipo_repuestos tr ON inv.id_repuesto = tr.id_repuesto
            JOIN calidades c ON inv.id_calidad = c.id_calidad
            JOIN colores col ON inv.id_color = col.id_color
            WHERE 1=1
        """
        params = []

        if marca:
            sql += " AND ma.nombre_marca = %s"
            params.append(marca)
        if modelo:
            sql += " AND m.nombre_modelo ILIKE %s"
            params.append(f"%{modelo}%")
        if repuesto:
            sql += " AND tr.nombre_repuesto = %s"
            params.append(repuesto)
        if calidad:
            sql += " AND c.nombre_calidad = %s"
            params.append(calidad)
        if precio_min:
            sql += " AND inv.precio_reparacion >= %s"
            params.append(float(precio_min))
        if precio_max:
            sql += " AND inv.precio_reparacion <= %s"
            params.append(float(precio_max))

        sql += " ORDER BY ma.nombre_marca, m.nombre_modelo LIMIT 1000"

        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute(sql, params)
        resultados = cursor.fetchall()

        # Convertir a diccionarios
        datos = []
        for row in resultados:
            datos.append({
                'marca': row['marca'],
                'modelo': row['modelo'],
                'repuesto': row['repuesto'],
                'calidad': row['calidad'],
                'color': row['color'],
                'precio_base': float(row['precio_base']),
                'precio_reparacion': float(row['precio_reparacion']),
                'margen': float(row['margen']),
                'cantidad': row['cantidad']
            })

        cursor.close()
        conn.close()
        return jsonify(datos)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/estadisticas', methods=['GET'])
def obtener_estadisticas():
    """Obtiene estadísticas generales"""
    conn = conectar_db()
    if not conn:
        return jsonify({'error': 'Error de conexión'}), 500
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        cursor.execute("""
            SELECT
                COUNT(DISTINCT inv.id_modelo) as total_modelos,
                COUNT(DISTINCT ma.id_marca) as total_marcas,
                COUNT(DISTINCT tr.id_repuesto) as total_repuestos,
                ROUND(AVG(inv.precio_reparacion)::numeric, 2) as precio_promedio,
                ROUND(MAX(inv.precio_reparacion)::numeric, 2) as precio_maximo,
                ROUND(MIN(inv.precio_reparacion)::numeric, 2) as precio_minimo,
                ROUND(SUM(inv.margen_reparacion)::numeric, 2) as margen_total
            FROM inventario inv
            JOIN marcas ma ON inv.id_marca = ma.id_marca
            JOIN tipo_repuestos tr ON inv.id_repuesto = tr.id_repuesto
        """)
        stats = cursor.fetchone()
        cursor.close()
        conn.close()

        return jsonify({
            'total_modelos': stats['total_modelos'],
            'total_marcas': stats['total_marcas'],
            'total_repuestos': stats['total_repuestos'],
            'precio_promedio': float(stats['precio_promedio']),
            'precio_maximo': float(stats['precio_maximo']),
            'precio_minimo': float(stats['precio_minimo']),
            'margen_total': float(stats['margen_total'])
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint no encontrado'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Error interno del servidor'}), 500

# Para Vercel
if __name__ != '__main__':
    # Esto permite que Vercel importe 'app' directamente
    pass
