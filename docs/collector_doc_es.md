# Documentación de collector.py

## Descripción
`collector.py` es un módulo del agente recolector del sistema de monitoreo de servidores Prex Challenge. Se encarga de recopilar información del sistema utilizando las bibliotecas psutil, platform y socket.

## Funciones Principales

### `get_cpu_info()`
- **Descripción**: Recopila información de la CPU.
- **Detalles**: Obtiene el número de núcleos físicos y lógicos, el porcentaje de uso de la CPU y el modelo de la CPU.
- **Retorno**: Diccionario con detalles de la CPU incluyendo recuento, porcentaje de uso e información del modelo.
- **Compatibilidad**: Detecta automáticamente si el sistema operativo es Linux o Windows para obtener la información correcta del modelo de CPU.

### `get_process_list()`
- **Descripción**: Obtiene la lista de procesos en ejecución.
- **Detalles**: Para cada proceso, recopila el ID del proceso (PID), nombre, usuario, porcentaje de memoria y porcentaje de CPU.
- **Retorno**: Lista de diccionarios con detalles de procesos.
- **Manejo de Errores**: Gestiona excepciones como NoSuchProcess, AccessDenied y ZombieProcess para una ejecución robusta.

### `get_logged_users()`
- **Descripción**: Obtiene la lista de usuarios conectados.
- **Detalles**: Para cada usuario, recopila el nombre, terminal, host y tiempo de inicio de sesión.
- **Retorno**: Lista de diccionarios con detalles de usuario.
- **Formato**: Las marcas de tiempo se convierten a formato legible "YYYY-MM-DD HH:MM:SS".

### `get_os_info()`
- **Descripción**: Obtiene información del sistema operativo.
- **Detalles**: Recopila el nombre, versión, release, arquitectura y tipo de procesador del sistema operativo.
- **Retorno**: Diccionario con información del sistema operativo.
- **Características Especiales**: Para sistemas Linux, intenta obtener información adicional de la distribución.

### `collect_all()`
- **Descripción**: Función principal que recopila toda la información del sistema.
- **Detalles**: Obtiene el hostname e IP, y reúne toda la información del sistema llamando a las funciones anteriores.
- **Retorno**: Diccionario con toda la información recopilada.
- **Características Especiales**: Intenta obtener una IP más precisa realizando una conexión de prueba a un servidor externo (8.8.8.8).

## Uso
El módulo puede ejecutarse directamente para pruebas:

```python
python collector.py  # Muestra en formato JSON toda la información recolectada
```

En contexto del proyecto, este módulo es importado por `run_agent.py` para recolectar datos que luego serán enviados al servidor API.
