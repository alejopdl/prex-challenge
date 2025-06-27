# Documentación de app.py

## Descripción
`app.py` es la aplicación principal del servidor API para el sistema de monitoreo Prex Challenge. Implementa los endpoints para recibir datos de los agentes de monitoreo y proporcionar acceso a los datos almacenados a través de consultas. Está desarrollado utilizando el framework Flask.

## Componentes Principales

### Inicialización de la Aplicación
- Inicializa la aplicación Flask.
- Configura el sistema de almacenamiento utilizando la clase `JSONStorage` del módulo `storage`.
- Asegura que las rutas de importación sean correctas, incluso cuando se ejecuta desde un subdirectorio.

### Endpoint `/upload` (POST)
- **Descripción**: Recibe información del sistema desde los agentes.
- **Método HTTP**: POST
- **Datos esperados**: Carga JSON con información del sistema.
- **Validación**:
  - Verifica que la solicitud sea JSON.
  - Comprueba que los campos requeridos ('hostname', 'ip_address', 'timestamp') estén presentes.
- **Respuesta**:
  - Éxito: Mensaje de confirmación y ruta del archivo donde se guardaron los datos.
  - Error: Mensaje de error detallando el problema (400 para solicitudes mal formadas, 500 para errores internos).

### Endpoint `/query` (GET)
- **Descripción**: Consulta información del sistema por dirección IP y fecha.
- **Método HTTP**: GET
- **Parámetros de consulta**:
  - `ip`: Dirección IP a consultar (obligatorio).
  - `date`: Fecha en formato YYYY-MM-DD (opcional, predeterminado: hoy).
- **Respuesta**:
  - Éxito: Datos solicitados en formato JSON.
  - Error: Mensaje indicando que no se encontraron datos o detallando el problema.

### Endpoint `/list` (GET)
- **Descripción**: Lista todos los archivos de datos disponibles.
- **Método HTTP**: GET
- **Respuesta**:
  - Éxito: Lista de archivos de datos disponibles con IP y fecha.
  - Error: Mensaje detallando el problema.

### Endpoint `/health` (GET)
- **Descripción**: Verifica el estado del servidor API.
- **Método HTTP**: GET
- **Respuesta**: Mensaje indicando que el servidor API está funcionando.

### Endpoint `/` (GET)
- **Descripción**: Raíz del API, proporciona información general del API.
- **Método HTTP**: GET
- **Respuesta**: Información sobre el API incluyendo nombre, versión y lista de endpoints disponibles.

## Ejecución
Si el script se ejecuta directamente (no importado como módulo), la aplicación se inicia en modo de depuración, escuchando en todas las interfaces ('0.0.0.0'). Sin embargo, para despliegue adecuado, se recomienda usar `run_api.py` que proporciona opciones adicionales de configuración.

## Uso
El archivo no está diseñado para ser ejecutado directamente en producción. En su lugar:

```bash
# Para desarrollo/pruebas
python api_server/app.py

# Para producción (recomendado)
python api_server/run_api.py --host 0.0.0.0 --port 5000
```

## Consideraciones de Seguridad
- El API no implementa autenticación, lo que podría ser un riesgo de seguridad en entornos de producción.
- No se realiza una validación exhaustiva de los datos entrantes más allá de verificar los campos requeridos.
- En un entorno de producción, se recomienda agregar autenticación y validación adicional de datos.
