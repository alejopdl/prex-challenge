# Documentación del Proyecto Prex Challenge

## Descripción General del Proyecto
Este proyecto implementa un sistema de monitoreo de servidores compuesto por un agente de recolección y un servidor API. El agente recolecta información del sistema de máquinas Windows y Linux y la envía a la API, que almacena los datos en archivos JSON para su posterior consulta.

## Objetivos del Proyecto
- Crear un sistema de monitoreo de servidores para el desafío técnico de Prex.
- Implementar un agente que recolecte información del sistema de máquinas Windows y Linux.
- Desarrollar una API que reciba y almacene los datos en archivos JSON.
- Desplegar el sistema en una instancia EC2 de AWS.

## Estructura del Proyecto

```
prex-challenge/
│
├── agent/                       # Agente recolector
│   ├── collector.py             # Recolección de datos del sistema
│   ├── sender.py                # Envío de datos a la API
│   └── run_agent.py             # Script principal del agente
│
├── api_server/                  # API
│   ├── app.py                   # Endpoints de Flask
│   ├── storage.py               # Almacenamiento/recuperación de datos
│   └── run_api.py               # Servidor API
│
├── data/                        # Directorio de almacenamiento de datos
├── docs/                        # Documentación en español
├── evidencia/                   # Evidencia del despliegue en AWS EC2
├── tests/                       # Directorio de pruebas
├── Dockerfile                   # Configuración Docker para la API
├── requirements.txt             # Dependencias del proyecto
└── README.md                    # Documentación
```

## Documentación Detallada de los Componentes

### Agente de Recolección

1. [**collector.py**](docs/collector_doc_es.md) - Módulo encargado de recopilar información del sistema utilizando las bibliotecas psutil, platform y socket. Incluye funciones para obtener información de CPU, procesos, usuarios conectados y detalles del sistema operativo.

2. [**sender.py**](docs/sender_doc_es.md) - Módulo que maneja el envío de la información recopilada al servidor API a través de solicitudes HTTP POST. Implementa la clase `APISender` para manejar la comunicación con la API.

3. [**run_agent.py**](docs/run_agent_doc_es.md) - Script principal del agente que coordina la recolección y el envío de datos. Puede ejecutarse en modo único o programado a intervalos regulares.

### Servidor API

1. [**app.py**](docs/app_doc_es.md) - Aplicación Flask que implementa los endpoints para recibir y consultar datos. Incluye rutas para subir datos, consultar por IP y fecha, listar archivos disponibles y verificar el estado del servidor.

2. [**storage.py**](docs/storage_doc_es.md) - Módulo que maneja el almacenamiento y recuperación de datos en archivos JSON. Implementa la clase `JSONStorage` para gestionar operaciones de archivo.

3. **run_api.py** - Script para iniciar el servidor API con opciones configurables como host y puerto.

## Requisitos del Sistema

- Python 3.7 o superior
- Bibliotecas:
  - psutil - Para recolectar información del sistema
  - requests - Para enviar datos a la API
  - flask - Para implementar el servidor API
  - python-dateutil - Para manipulación de fechas
- Docker (opcional, para containerización de la API)

## Instalación y Uso

### Instalación

1. Clonar el repositorio:
   ```
   git clone <repository-url>
   cd prex-challenge
   ```

2. Instalar dependencias:
   ```
   pip install -r requirements.txt
   ```

### Uso del Agente

El agente puede ejecutarse en dos modos:
- Ejecución única (recolecta y envía datos una vez)
- Programado (se ejecuta periódicamente a intervalos especificados)

#### Modo de ejecución única:
```bash
python agent/run_agent.py --url http://your-api-server:5000 --once
```

#### Modo programado (por defecto: cada 5 minutos):
```bash
python agent/run_agent.py --url http://your-api-server:5000 --interval 300
```

### Uso del Servidor API

#### Ejecución directa:
```bash
python api_server/run_api.py --host 0.0.0.0 --port 5000
```

#### Ejecución con Docker:
```bash
docker build -t prex-challenge-api .
docker run -p 5000:5000 -v $(pwd)/data:/app/data prex-challenge-api
```

## Despliegue en AWS EC2

1. Lanzar una instancia EC2 (nivel gratuito de Ubuntu)
2. Instalar dependencias:
   ```bash
   sudo apt update
   sudo apt install -y python3 python3-pip git
   ```

3. Clonar el repositorio e instalar dependencias:
   ```bash
   git clone <repository-url>
   cd prex-challenge
   pip3 install -r requirements.txt
   ```

4. Ejecutar el servidor API:
   ```bash
   python3 api_server/run_api.py
   ```

5. Configurar grupo de seguridad para permitir tráfico entrante en el puerto 5000

## Consideraciones de Seguridad

### Riesgos Identificados

1. **Autenticación**: La API actualmente no implementa ningún mecanismo de autenticación o autorización, lo que permite que cualquier cliente con conocimiento de la IP del servidor pueda subir o consultar datos.

2. **Superficie de Exposición**: El puerto 5000 está abierto públicamente en la configuración del grupo de seguridad de AWS EC2, lo que aumenta la superficie de ataque potencial.

3. **Almacenamiento sin Cifrado**: Los datos se almacenan en archivos JSON de texto plano sin cifrar, lo que podría comprometer información sensible si se accede al sistema de archivos.

4. **Protección contra DoS**: No hay implementados límites de tasa para las solicitudes, lo que podría hacer al sistema vulnerable a ataques de denegación de servicio.

5. **Validación de Entrada**: La validación básica de entrada podría ser mejorada para prevenir inyecciones o desbordamientos de búfer.

### Mejoras Recomendadas para Entornos de Producción

1. **Implementar Autenticación**:
   ```python
   # Ejemplo de middleware para autenticación con token API
   @app.before_request
   def authenticate():
       if request.endpoint not in ['health', 'index']:
           api_key = request.headers.get('X-Api-Key')
           if not api_key or api_key != config.API_KEY:
               return jsonify({'error': 'Unauthorized'}), 401
   ```

2. **Restricción de Acceso por IP**:
   - Modificar el grupo de seguridad para permitir conexiones solo desde IPs conocidas
   - Implementar listas blancas de IPs en la aplicación

3. **Implementar HTTPS** para cifrar datos en tránsito

4. **Cifrado de Datos en Reposo**:
   - Cifrar los archivos JSON o utilizar una base de datos con capacidades de cifrado

5. **Limitar Tamaño de Carga y Tasa de Solicitudes**:
   ```python
   # Configurar límites de tasa con Flask-Limiter
   from flask_limiter import Limiter
   limiter = Limiter(app, key_func=get_remote_address)
   
   @app.route('/upload', methods=['POST'])
   @limiter.limit("10 per minute")
   def upload():
       # existing code
   ```

6. **Registro y Monitoreo**:
   - Implementar logging detallado de seguridad
   - Configurar alertas para actividades sospechosas

## Notas de Implementación

- Este proyecto está diseñado como una prueba de concepto y puede requerir las mejoras de seguridad mencionadas para un despliegue en producción.
- Cierre el puerto 5000 cuando no sea necesario para minimizar la exposición.

## Mejoras Futuras Potenciales

1. **Seguridad**: Implementar autenticación y autorización para la API.
2. **Almacenamiento**: Migrar a una base de datos relacional o NoSQL para mejorar la escalabilidad.
3. **Interfaz de Usuario**: Desarrollar un panel de control web para visualizar los datos recopilados.
4. **Alertas**: Añadir un sistema de alertas basado en umbrales para notificar sobre valores anormales.
5. **Optimización**: Mejorar el rendimiento y la eficiencia del agente para sistemas con recursos limitados.

## Licencia

Este proyecto es parte de un desafío técnico para Prex.
