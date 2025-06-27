# Evidencia de Despliegue en AWS EC2

Este directorio contiene la evidencia que demuestra que el servidor API está funcionando correctamente en una instancia EC2 de AWS.

## Contenidos

1. `ec2_instance.png` - Captura de pantalla del panel AWS mostrando la instancia EC2 en funcionamiento
2. `api_test.png` - Captura de pantalla que muestra una prueba exitosa de la API
3. `api_logs.txt` - Logs del servidor API mostrando peticiones procesadas

## Detalles de la Implementación

- **Instancia**: t2.micro (nivel gratuito de AWS)
- **Sistema Operativo**: Ubuntu Server 22.04 LTS
- **IP Pública**: [TU-IP-EC2]
- **Método de Implementación**: Docker
- **Puerto**: 5000
- **Fecha de Implementación**: [FECHA]

## Pasos para Verificar

Para verificar que el servidor está funcionando, puede realizar una solicitud a:

```
http://[TU-IP-EC2]:5000/status
```

También puede consultar datos almacenados con:

```
http://[TU-IP-EC2]:5000/query?ip=[DIRECCIÓN-IP]&date=[YYYY-MM-DD]
```
