#!/usr/bin/env python3
"""
Punto de entrada para ejecutar el servidor API de Prex Challenge.
"""

import os
import sys
import argparse
import logging

# Añadir directorio padre a la ruta para importar módulos correctamente si se ejecuta desde un subdirectorio
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from api_server.app import app

# Configurar registro de logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('api_server.log')
    ]
)
logger = logging.getLogger('api_server')


def parse_arguments():
    """Analiza los argumentos de línea de comandos."""
    parser = argparse.ArgumentParser(description='Prex Challenge API Server')
    
    parser.add_argument(
        '--host',
        type=str,
        default='0.0.0.0',
        help='Host al que vincular el servidor (predeterminado: 0.0.0.0)'
    )
    
    parser.add_argument(
        '--port',
        type=int,
        default=5000,
        help='Puerto al que vincular el servidor (predeterminado: 5000)'
    )
    
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Ejecutar en modo de depuración (predeterminado: false)'
    )
    
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    
    # Asegurar que el directorio de datos existe
    data_dir = os.path.join(parent_dir, "data")
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        logger.info(f"Created data directory: {data_dir}")
    
    # Registrar información de inicio
    logger.info(f"Starting API server on {args.host}:{args.port}")
    
    # Ejecutar aplicación Flask
    app.run(
        host=args.host,
        port=args.port,
        debug=args.debug
    )
