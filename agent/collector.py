#!/usr/bin/env python3
"""
Módulo recolector para el agente de Prex Challenge.
Recopila información del sistema utilizando las bibliotecas psutil, platform y socket.
"""

import os
import psutil
import platform
import socket
import datetime
from typing import Dict, List, Any


def get_cpu_info() -> Dict[str, Any]:
    """
    Recopila información de la CPU.
    
    Returns:
        Diccionario con detalles de la CPU incluyendo conteo, porcentaje de uso e información del modelo.
    """
    cpu_info = {
        "physical_cores": psutil.cpu_count(logical=False),
        "logical_cores": psutil.cpu_count(logical=True),
        "usage_percent": psutil.cpu_percent(interval=1, percpu=True),
        "avg_usage": psutil.cpu_percent(interval=1),
    }
    
    # Añadir información del modelo de CPU si está disponible (depende del sistema)
    if platform.system() == "Linux":
        try:
            with open("/proc/cpuinfo", "r") as f:
                for line in f:
                    if "model name" in line:
                        cpu_info["model"] = line.split(":")[1].strip()
                        break
        except:
            cpu_info["model"] = "Unknown"
    elif platform.system() == "Windows":
        cpu_info["model"] = platform.processor()
    else:
        cpu_info["model"] = platform.processor()
        
    return cpu_info


def get_process_list() -> List[Dict[str, Any]]:
    """
    Obtiene la lista de procesos en ejecución.
    
    Returns:
        Lista de diccionarios con detalles de los procesos.
    """
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'username', 'memory_percent', 'cpu_percent']):
        try:
            pinfo = proc.as_dict()
            # Manejar valores que podrían ser None
            memory_percent = pinfo.get('memory_percent')
            memory_percent = round(memory_percent, 2) if memory_percent is not None else 0
            
            cpu_percent = pinfo.get('cpu_percent')
            cpu_percent = round(cpu_percent, 2) if cpu_percent is not None else 0
            
            processes.append({
                "pid": pinfo['pid'],
                "name": pinfo['name'],
                "username": pinfo['username'] or "Unknown",
                "memory_percent": memory_percent,
                "cpu_percent": cpu_percent
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return processes


def get_logged_users() -> List[Dict[str, str]]:
    """
    Obtiene la lista de usuarios conectados.
    
    Returns:
        Lista de diccionarios con detalles de los usuarios.
    """
    users = []
    for user in psutil.users():
        users.append({
            "name": user.name,
            "terminal": user.terminal,
            "host": user.host,
            "started": datetime.datetime.fromtimestamp(user.started).strftime("%Y-%m-%d %H:%M:%S")
        })
    return users


def get_os_info() -> Dict[str, str]:
    """
    Obtiene información del sistema operativo.
    
    Returns:
        Diccionario con el nombre y versión del SO.
    """
    os_info = {
        "name": platform.system(),
        "version": platform.version(),
        "release": platform.release(),
        "machine": platform.machine(),
        "processor": platform.processor()
    }
    
    # Añadir información de distribución para Linux
    if platform.system() == "Linux":
        try:
            distro_info = platform.freedesktop_os_release()
            os_info["distribution"] = distro_info.get("NAME", "Unknown")
            os_info["distribution_version"] = distro_info.get("VERSION_ID", "Unknown")
        except:
            # Alternativa para versiones antiguas de Python
            try:
                import distro
                os_info["distribution"] = distro.name()
                os_info["distribution_version"] = distro.version()
            except ImportError:
                os_info["distribution"] = "Unknown"
                os_info["distribution_version"] = "Unknown"
    
    return os_info


def collect_all() -> Dict[str, Any]:
    """
    Recopila toda la información del sistema.
    
    Returns:
        Diccionario con toda la información recopilada.
    """
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    
    # Para máquinas con múltiples interfaces de red, intentar obtener una IP más precisa
    try:
        # Crear una conexión de socket a un servidor externo y obtener la IP local
        temp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        temp_socket.connect(("8.8.8.8", 80))
        ip_address = temp_socket.getsockname()[0]
        temp_socket.close()
    except:
        pass
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    system_info = {
        "hostname": hostname,
        "ip_address": ip_address,
        "timestamp": timestamp,
        "cpu_info": get_cpu_info(),
        "processes": get_process_list(),
        "logged_users": get_logged_users(),
        "os_info": get_os_info()
    }
    
    return system_info


if __name__ == "__main__":
    # Solo para probar el recolector directamente
    import json
    info = collect_all()
    print(json.dumps(info, indent=2))
