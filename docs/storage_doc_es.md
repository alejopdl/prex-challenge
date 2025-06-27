# Documentación de storage.py

## Descripción
`storage.py` es el módulo encargado del almacenamiento y recuperación de la información del sistema en el servidor API del sistema de monitoreo Prex Challenge. Implementa una solución de almacenamiento basada en archivos JSON, donde cada archivo se nombra según la dirección IP y la fecha: `IP_YYYY-MM-DD.json`.

## Clase Principal

### `JSONStorage`
Esta clase maneja el almacenamiento y recuperación de información del sistema en archivos JSON.

#### Métodos

##### `__init__(self, data_dir: str = "data")`
- **Descripción**: Inicializa el manejador de almacenamiento.
- **Parámetros**:
  - `data_dir`: Directorio para almacenar los archivos JSON (predeterminado: "data").
- **Detalles**: Crea el directorio de datos si no existe.

##### `store_data(self, data: Dict[str, Any]) -> Dict[str, Any]`
- **Descripción**: Almacena la información del sistema en un archivo JSON.
- **Parámetros**:
  - `data`: Diccionario con la información del sistema.
- **Retorno**: Diccionario con estado y ruta del archivo.
- **Detalles**:
  - Extrae la dirección IP de los datos.
  - Obtiene la fecha actual para el nombre del archivo.
  - Verifica si el archivo ya existe y carga datos existentes.
  - Añade los nuevos datos a los existentes.
  - Escribe los datos en el archivo.

##### `query_data(self, ip_address: str, date: Optional[str] = None) -> Dict[str, Any]`
- **Descripción**: Consulta información del sistema para una dirección IP específica.
- **Parámetros**:
  - `ip_address`: Dirección IP a consultar.
  - `date`: Fecha opcional en formato YYYY-MM-DD. Si es None, devuelve datos de hoy.
- **Retorno**: Diccionario con estado y datos recuperados.
- **Detalles**:
  - Valida el formato de fecha si se proporciona.
  - Construye el nombre del archivo basado en IP y fecha.
  - Verifica si existe el archivo.
  - Lee y devuelve los datos del archivo.

##### `list_available_data(self) -> Dict[str, Any]`
- **Descripción**: Lista todos los archivos de datos disponibles.
- **Retorno**: Diccionario con estado y lista de archivos de datos disponibles.
- **Detalles**:
  - Recorre el directorio de datos buscando archivos JSON.
  - Extrae IP y fecha del nombre de cada archivo.
  - Construye una lista de datos disponibles con información sobre cada archivo.

## Uso
El módulo puede ejecutarse directamente para pruebas:

```python
python storage.py
```

Esto ejecutará un conjunto de pruebas que:
1. Crea una instancia de `JSONStorage`
2. Almacena datos de ejemplo
3. Consulta los datos almacenados
4. Lista los datos disponibles

En el contexto del proyecto, este módulo es utilizado por `app.py` para manejar el almacenamiento y recuperación de datos cuando se reciben solicitudes a los endpoints de la API.

## Estructura de Archivos
Los datos se almacenan en archivos JSON con la siguiente estructura de nombres:
```
IP_YYYY-MM-DD.json
```

Por ejemplo:
```
192.168.1.1_2023-01-01.json
```

## Consideraciones
- Los datos se almacenan en formato JSON, lo que facilita la lectura humana pero puede no ser óptimo para grandes volúmenes de datos.
- La implementación actual admite la acumulación de múltiples entradas para una misma IP en el mismo día.
- Para entornos de producción con requisitos de escalabilidad, se podría considerar migrar a una base de datos relacional o NoSQL.
