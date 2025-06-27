#!/usr/bin/env python3
"""
Módulo emisor para el agente de Prex Challenge.
Maneja el envío de la información recopilada del sistema al servidor API.
"""

import json
import requests
from typing import Dict, Any


class APISender:
    """
    Clase para manejar el envío de datos al servidor API.
    """
    
    def __init__(self, api_url: str):
        """
        Inicializa el emisor con la URL de la API.
        
        Args:
            api_url: URL base del servidor API
        """
        self.api_url = api_url
        if not self.api_url.endswith('/'):
            self.api_url += '/'
    
    def send_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Envía información del sistema al servidor API.
        
        Args:
            data: Diccionario que contiene información del sistema
        
        Returns:
            Diccionario con estado de respuesta y mensaje
        
        Raises:
            ConnectionError: Si no es posible conectar con la API
        """
        upload_endpoint = f"{self.api_url}upload"
        
        try:
            # Convertir datos a JSON
            json_data = json.dumps(data)
            
            # Enviar solicitud POST
            headers = {'Content-Type': 'application/json'}
            response = requests.post(upload_endpoint, data=json_data, headers=headers)
            
            # Verificar estado de la respuesta
            if response.status_code == 200:
                return {
                    "success": True,
                    "message": "Data sent successfully",
                    "response": response.json()
                }
            else:
                return {
                    "success": False,
                    "message": f"Error sending data: HTTP {response.status_code}",
                    "response": response.text
                }
                
        except requests.exceptions.ConnectionError:
            raise ConnectionError(f"Could not connect to API at {upload_endpoint}")
        except Exception as e:
            return {
                "success": False,
                "message": f"Error sending data: {str(e)}",
                "response": None
            }


if __name__ == "__main__":
    # Ejemplo de uso
    from collector import collect_all
    
    # Reemplazar con la URL real de la API
    sender = APISender("http://localhost:5000/")
    
    # Obtener información del sistema
    data = collect_all()
    
    # Enviar a la API
    try:
        result = sender.send_data(data)
        print(json.dumps(result, indent=2))
    except ConnectionError as e:
        print(f"Connection error: {e}")
