# Documentación de run_agent.py

## Descripción
`run_agent.py` es el punto de entrada principal para el agente de monitoreo del sistema Prex Challenge. Se encarga de coordinar la recolección de información del sistema y el envío de estos datos al servidor API, ya sea de forma única o programada a intervalos regulares.

## Configuración de Registro (Logging)
El módulo configura un sistema de registro que guarda los mensajes tanto en la consola como en un archivo llamado `agent.log`. Esto permite un seguimiento detallado de la actividad del agente y facilita la depuración de problemas.

## Funciones Principales

### `run_once(api_url: str) -> Dict[str, Any]`
- **Descripción**: Ejecuta el agente una sola vez, recopilando y enviando datos.
- **Parámetros**:
  - `api_url`: URL del servidor API.
- **Retorno**: Diccionario con el estado del resultado.
- **Detalles**: 
  - Recopila la información del sistema utilizando `collect_all()` del módulo `collector`.
  - Crea una instancia de `APISender` y envía los datos al API.
  - Registra el resultado de la operación (éxito o error).
  - Maneja excepciones para asegurar que el agente no falle abruptamente.

### `run_scheduled(api_url: str, interval: int) -> None`
- **Descripción**: Ejecuta el agente en un horario programado.
- **Parámetros**:
  - `api_url`: URL del servidor API.
  - `interval`: Intervalo en segundos entre ejecuciones.
- **Detalles**:
  - Crea un bucle infinito que llama a `run_once()` periódicamente.
  - Espera el intervalo especificado entre cada ejecución.
  - Maneja excepciones para asegurar la ejecución continua incluso si hay errores.

### `parse_arguments()`
- **Descripción**: Analiza los argumentos de la línea de comandos.
- **Retorno**: Objeto con los argumentos analizados.
- **Detalles**:
  - Define los argumentos aceptados por el script:
    - `--url`: URL del servidor API (predeterminado: http://localhost:5000/).
    - `--interval`: Intervalo en segundos para ejecuciones programadas (predeterminado: 300, que son 5 minutos).
    - `--once`: Ejecutar una vez y salir (predeterminado: false).

## Bloque Principal
El bloque principal del script:
1. Analiza los argumentos de la línea de comandos.
2. Determina el modo de ejecución (única o programada) basado en el argumento `--once`.
3. En modo único:
   - Llama a `run_once()` y muestra el resultado en formato JSON.
4. En modo programado:
   - Llama a `run_scheduled()` que ejecuta el agente periódicamente hasta que se detenga con Ctrl+C.
   - Maneja la interrupción del teclado (Ctrl+C) para salir limpiamente.

## Uso
El script puede ejecutarse con varios parámetros para adaptarse a diferentes escenarios:

```bash
# Ejecución única
python agent/run_agent.py --url http://servidor-api:5000 --once

# Ejecución programada cada 5 minutos (predeterminado)
python agent/run_agent.py --url http://servidor-api:5000

# Ejecución programada con intervalo personalizado (ej. cada 60 segundos)
python agent/run_agent.py --url http://servidor-api:5000 --interval 60
```
