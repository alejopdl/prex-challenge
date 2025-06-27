# Documentación de sender.py

## Descripción
`sender.py` es un módulo del agente recolector del sistema de monitoreo de servidores Prex Challenge. Se encarga de enviar la información del sistema recopilada al servidor API a través de solicitudes HTTP.

## Clase Principal

### `APISender`
Esta clase maneja el envío de datos al servidor API.

#### Métodos

##### `__init__(self, api_url: str)`
- **Descripción**: Inicializa el emisor con la URL de la API.
- **Parámetros**:
  - `api_url`: URL base del servidor API.
- **Detalles**: Asegura que la URL termine con un carácter "/".

##### `send_data(self, data: Dict[str, Any]) -> Dict[str, Any]`
- **Descripción**: Envía la información del sistema al servidor API.
- **Parámetros**:
  - `data`: Diccionario que contiene la información del sistema.
- **Retorno**: Diccionario con estado de respuesta y mensaje.
- **Excepciones**:
  - `ConnectionError`: Si no se puede conectar a la API.
- **Detalles**: 
  - Convierte los datos a formato JSON.
  - Envía una solicitud POST al endpoint de carga.
  - Verifica el estado de la respuesta y devuelve un diccionario con información del resultado.
  - Maneja diferentes tipos de errores que puedan surgir durante el proceso de envío.

## Uso
El módulo puede ejecutarse directamente para pruebas:

```python
python sender.py  # Recopila datos del sistema y los envía a la API local predeterminada
```

Este módulo es importado por `run_agent.py` para enviar los datos recopilados al servidor API. La clase `APISender` proporciona una interfaz limpia y robusta para la comunicación con la API, con manejo adecuado de errores y respuestas.

### Ejemplo de uso en el código:

```python
from sender import APISender
from collector import collect_all

# Crear instancia del emisor
sender = APISender("http://servidor-api:5000/")

# Recopilar datos del sistema
data = collect_all()

# Enviar a la API
try:
    result = sender.send_data(data)
    if result['success']:
        print("Datos enviados correctamente")
    else:
        print(f"Error: {result['message']}")
except ConnectionError as e:
    print(f"Error de conexión: {e}")
```
