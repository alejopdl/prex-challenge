#!/usr/bin/env python3
"""
Punto de entrada principal para el agente de monitoreo de sistemas Prex Challenge.
Recopila información del sistema y la envía al servidor API.
"""

import os
import sys
import time
import json
import argparse
import logging
from typing import Dict, Any, Optional

# Añadir directorio padre a la ruta para importar módulos correctamente si se ejecuta desde un subdirectorio
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from agent.collector import collect_all
from agent.sender import APISender


# Configurar registro de logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('agent.log')
    ]
)
logger = logging.getLogger('agent')


def run_once(api_url: str) -> Dict[str, Any]:
    """
    Ejecuta el agente una vez, recopilando y enviando datos.
    
    Args:
        api_url: URL del servidor API
    
    Returns:
        Diccionario con el estado del resultado
    """
    logger.info(f"Starting data collection...")
    try:
        # Recopilar información del sistema
        data = collect_all()
        logger.info(f"Data collected for {data['hostname']} ({data['ip_address']})")
        
        # Enviar datos a la API
        sender = APISender(api_url)
        result = sender.send_data(data)
        
        if result['success']:
            logger.info("Data sent successfully to API")
        else:
            logger.error(f"Failed to send data: {result['message']}")
            
        return result
    
    except Exception as e:
        logger.error(f"Error in agent execution: {str(e)}")
        return {
            "success": False,
            "message": f"Agent error: {str(e)}"
        }


def run_scheduled(api_url: str, interval: int) -> None:
    """
    Ejecuta el agente según un cronograma.
    
    Args:
        api_url: URL del servidor API
        interval: Intervalo en segundos entre ejecuciones
    """
    logger.info(f"Starting scheduled monitoring every {interval} seconds")
    
    while True:
        try:
            run_once(api_url)
        except Exception as e:
            logger.error(f"Unhandled error in scheduled run: {str(e)}")
            
        logger.info(f"Sleeping for {interval} seconds...")
        time.sleep(interval)


def parse_arguments():
    """Analiza los argumentos de línea de comandos."""
    parser = argparse.ArgumentParser(description='System Monitoring Agent for Prex Challenge')
    
    parser.add_argument(
        '--url', 
        type=str, 
        default='http://localhost:5000/', 
        help='URL del servidor API (predeterminado: http://localhost:5000/)'
    )
    
    parser.add_argument(
        '--interval', 
        type=int, 
        default=300,  # 5 minutos
        help='Intervalo en segundos para ejecuciones programadas (predeterminado: 300)'
    )
    
    parser.add_argument(
        '--once',
        action='store_true',
        help='Ejecutar una vez y salir (predeterminado: false)'
    )
    
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    
    if args.once:
        # Ejecutar una vez y salir
        logger.info("Running agent in single-run mode")
        result = run_once(args.url)
        print(json.dumps(result, indent=2))
    else:
        # Ejecutar según cronograma hasta que se detenga
        try:
            run_scheduled(args.url, args.interval)
        except KeyboardInterrupt:
            logger.info("Agent stopped by user")
            sys.exit(0)
