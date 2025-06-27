#!/usr/bin/env python3
"""
Aplicación Flask para el servidor API de Prex Challenge.
Proporciona endpoints para subir y consultar información del sistema.
"""

import os
import sys
import json
from flask import Flask, request, jsonify, abort

# Añadir directorio padre a la ruta para importar módulos correctamente si se ejecuta desde un subdirectorio
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from api_server.storage import JSONStorage

# Inicializar aplicación Flask
app = Flask(__name__)

# Inicializar manejador de almacenamiento
storage = JSONStorage(data_dir="data")


@app.route('/upload', methods=['POST'])
def upload():
    """
    Endpoint para recibir información del sistema desde los agentes.
    
    Espera un payload JSON con información del sistema.
    Devuelve una respuesta JSON con el estado.
    """
    if not request.is_json:
        return jsonify({
            "success": False,
            "message": "Request must be JSON"
        }), 400
    
    data = request.get_json()
    
    # Validar campos requeridos
    required_fields = ['hostname', 'ip_address', 'timestamp']
    if not all(field in data for field in required_fields):
        return jsonify({
            "success": False,
            "message": f"Missing required fields: {', '.join(required_fields)}"
        }), 400
    
    # Almacenar datos
    result = storage.store_data(data)
    
    if result['success']:
        return jsonify({
            "success": True,
            "message": "Data received and stored successfully",
            "file_path": result['file_path']
        })
    else:
        return jsonify({
            "success": False,
            "message": result['message']
        }), 500


@app.route('/query', methods=['GET'])
def query():
    """
    Endpoint para consultar información del sistema por dirección IP y fecha.
    
    Parámetros de consulta:
    - ip: Dirección IP a consultar (requerido)
    - date: Fecha en formato YYYY-MM-DD (opcional, por defecto es hoy)
    
    Devuelve una respuesta JSON con los datos consultados.
    """
    ip_address = request.args.get('ip')
    date = request.args.get('date')
    
    if not ip_address:
        return jsonify({
            "success": False,
            "message": "IP address is required"
        }), 400
    
    # Consultar datos
    result = storage.query_data(ip_address, date)
    
    if result['success']:
        return jsonify({
            "success": True,
            "message": result['message'],
            "data": result['data']
        })
    else:
        return jsonify({
            "success": False,
            "message": result['message']
        }), 404


@app.route('/list', methods=['GET'])
def list_data():
    """
    Endpoint para listar todos los archivos de datos disponibles.
    
    Devuelve una respuesta JSON con una lista de archivos de datos disponibles.
    """
    result = storage.list_available_data()
    
    if result['success']:
        return jsonify({
            "success": True,
            "message": result['message'],
            "available_data": result['available_data']
        })
    else:
        return jsonify({
            "success": False,
            "message": result['message']
        }), 500


@app.route('/health', methods=['GET'])
def health_check():
    """
    Endpoint de verificación de salud.
    
    Devuelve una respuesta JSON con el estado.
    """
    return jsonify({
        "status": "ok",
        "message": "API server is running"
    })


@app.route('/', methods=['GET'])
def index():
    """
    Endpoint raíz.
    
    Devuelve una respuesta JSON con información de la API.
    """
    return jsonify({
        "name": "Prex Challenge API Server",
        "version": "1.0.0",
        "endpoints": [
            {"method": "POST", "path": "/upload", "description": "Subir información del sistema"},
            {"method": "GET", "path": "/query?ip=<IP>&date=<YYYY-MM-DD>", "description": "Consultar información del sistema"},
            {"method": "GET", "path": "/list", "description": "Listar archivos de datos disponibles"},
            {"method": "GET", "path": "/health", "description": "Verificación de salud"}
        ]
    })


if __name__ == "__main__":
    # Esto es solo para pruebas directas, utilice run_api.py para un despliegue adecuado
    app.run(debug=True, host='0.0.0.0')
