#!/usr/bin/env python3
"""
Módulo de almacenamiento para el servidor API de Prex Challenge.
Maneja el almacenamiento y recuperación de información del sistema en archivos JSON.
"""

import os
import json
import datetime
from typing import Dict, List, Any, Optional


class JSONStorage:
    """
    Clase para manejar el almacenamiento y recuperación de información del sistema en archivos JSON.
    Los archivos se nombran basándose en la dirección IP y la fecha: IP_YYYY-MM-DD.json
    """
    
    def __init__(self, data_dir: str = "data"):
        """
        Inicializa el manejador de almacenamiento.
        
        Args:
            data_dir: Directorio para almacenar los archivos JSON (predeterminado: "data")
        """
        self.data_dir = data_dir
        
        # Crear directorio de datos si no existe
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def store_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Almacena información del sistema en un archivo JSON.
        
        Args:
            data: Diccionario que contiene información del sistema
        
        Returns:
            Diccionario con estado y ruta del archivo
        """
        try:
            # Extraer dirección IP de los datos
            ip_address = data.get('ip_address', 'unknown')
            
            # Obtener fecha actual para el nombre del archivo
            date_str = datetime.datetime.now().strftime("%Y-%m-%d")
            
            # Create filename
            filename = f"{ip_address}_{date_str}.json"
            file_path = os.path.join(self.data_dir, filename)
            
            # Verificar si el archivo existe y cargar datos existentes
            existing_data = []
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    existing_data = json.load(f)
                    
                    # Asegurar que sea una lista
                    if not isinstance(existing_data, list):
                        existing_data = [existing_data]
            
            # Añadir nuevos datos a los datos existentes
            existing_data.append(data)
            
            # Escribir datos en el archivo
            with open(file_path, 'w') as f:
                json.dump(existing_data, f, indent=2)
            
            return {
                "success": True,
                "message": "Data stored successfully",
                "file_path": file_path
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error storing data: {str(e)}",
                "file_path": None
            }
    
    def query_data(self, ip_address: str, date: Optional[str] = None) -> Dict[str, Any]:
        """
        Consulta información del sistema para una dirección IP específica.
        
        Args:
            ip_address: Dirección IP a consultar
            date: Fecha opcional en formato YYYY-MM-DD. Si es None, devuelve datos de hoy.
        
        Returns:
            Diccionario con estado y datos recuperados
        """
        try:
            # Obtener fecha del parámetro o usar la fecha de hoy
            if date is None:
                date_str = datetime.datetime.now().strftime("%Y-%m-%d")
            else:
                # Validar formato de fecha
                try:
                    datetime.datetime.strptime(date, "%Y-%m-%d")
                    date_str = date
                except ValueError:
                    return {
                        "success": False,
                        "message": f"Invalid date format: {date}. Use YYYY-MM-DD.",
                        "data": None
                    }
            
            # Create filename
            filename = f"{ip_address}_{date_str}.json"
            file_path = os.path.join(self.data_dir, filename)
            
            # Check if file exists
            if not os.path.exists(file_path):
                return {
                    "success": False,
                    "message": f"No data found for IP {ip_address} on {date_str}",
                    "data": None
                }
            
            # Leer datos del archivo
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            return {
                "success": True,
                "message": f"Data retrieved for IP {ip_address} on {date_str}",
                "data": data
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error querying data: {str(e)}",
                "data": None
            }
    
    def list_available_data(self) -> Dict[str, Any]:
        """
        Lista todos los archivos de datos disponibles.
        
        Returns:
            Diccionario con estado y lista de archivos de datos disponibles
        """
        try:
            available_data = []
            
            for filename in os.listdir(self.data_dir):
                if filename.endswith('.json'):
                    # Extraer IP y fecha del nombre del archivo
                    parts = filename.replace('.json', '').split('_')
                    if len(parts) == 2:
                        ip_address, date_str = parts
                        available_data.append({
                            "ip_address": ip_address,
                            "date": date_str,
                            "filename": filename
                        })
            
            return {
                "success": True,
                "message": f"Found {len(available_data)} data files",
                "available_data": available_data
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error listing data: {str(e)}",
                "available_data": []
            }


if __name__ == "__main__":
    # Prueba del almacenamiento
    storage = JSONStorage()
    
    # Datos de ejemplo
    test_data = {
        "ip_address": "127.0.0.1",
        "hostname": "test-host",
        "timestamp": "2023-01-01 12:00:00",
        "cpu_info": {"cores": 4},
        "os_info": {"name": "Linux", "version": "5.10.0"}
    }
    
    # Almacenar datos
    result = storage.store_data(test_data)
    print(json.dumps(result, indent=2))
    
    # Consultar datos
    result = storage.query_data("127.0.0.1")
    print(json.dumps(result, indent=2))
    
    # Listar datos disponibles
    result = storage.list_available_data()
    print(json.dumps(result, indent=2))
