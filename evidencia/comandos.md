# Comandos de Despliegue y Prueba

## Despliegue en AWS EC2

```bash
# Configurar permisos de la llave SSH
chmod 400 prex-challenge-key.pem

# Ejecutar script de despliegue automatizado
bash deploy.sh
```

## Verificación del Servidor API

```bash
# Verificar que el servidor API está funcionando
curl -v http://15.228.201.242:5000/health
```

Respuesta:
```json
{"message":"API server is running","status":"ok"}
```

## Prueba del Agente de Recopilación

```bash
# Activar entorno virtual e instalar dependencias
source venv/bin/activate
pip install -r requirements.txt

# Ejecutar el agente para enviar datos al servidor API
python3 agent/run_agent.py --url http://15.228.201.242:5000/ --once
```

Respuesta:
```
2025-06-27 15:23:10,405 - agent - INFO - Running agent in single-run mode
2025-06-27 15:23:10,405 - agent - INFO - Starting data collection...
2025-06-27 15:23:12,551 - agent - INFO - Data collected for Alejos-MacBook-Pro-2.local (192.168.100.212)
2025-06-27 15:23:12,728 - agent - INFO - Data sent successfully to API
{
  "success": true,
  "message": "Data sent successfully",
  "response": {
    "file_path": "data/192.168.100.212_2025-06-27.json",
    "message": "Data received and stored successfully",
    "success": true
  }
}
```

## Verificación de Archivos Almacenados

```bash
# Listar archivos de datos disponibles en el servidor
curl -v http://15.228.201.242:5000/list
```

Respuesta:
```json
{"available_data":[{"date":"2025-06-27","filename":"192.168.100.212_2025-06-27.json","ip_address":"192.168.100.212"}],"message":"Found 1 data files","success":true}
```

## Consulta de Datos

```bash
# Consultar datos para una dirección IP específica
curl "http://15.228.201.242:5000/query?ip=192.168.100.212"
```

La respuesta es un JSON completo con todos los datos del sistema recolectados, incluyendo:
- Información de CPU
- Lista de procesos en ejecución
- Usuarios conectados
- Detalles del sistema operativo

## Conclusión

El despliegue ha sido exitoso, con todos los componentes funcionando de acuerdo a los requisitos del desafío Prex:
- Servidor API desplegado en AWS EC2
- Almacenamiento en formato JSON
- Comunicación correcta entre el agente y el servidor
- Funcionalidad completa de subida y consulta de datos
