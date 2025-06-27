# Evidencia de Despliegue en AWS EC2

Este directorio contiene la evidencia que demuestra que el servidor API está funcionando correctamente en una instancia EC2 de AWS para el desafío técnico de Prex.

## Contenidos de la Evidencia

1. `ec2-instancia.png` - Captura del panel AWS mostrando la instancia EC2 en funcionamiento
2. `api-health.png` - Respuesta del endpoint `/health` confirmando que la API está funcionando
3. `api-list.png` - Listado de archivos JSON almacenados en el servidor
4. `api-query.png` - Datos consultados a través del endpoint `/query`
5. `server-logs.mov` - Video mostrando los logs del servidor en tiempo real
6. `comandos.md` - Documentación de los comandos utilizados para la implementación y pruebas
7. `capturas.md` - Guía para recolectar y organizar las capturas de pantalla

## Detalles de la Implementación

- **Instancia**: t2.micro (nivel gratuito de AWS)
- **Sistema Operativo**: Ubuntu Server 22.04 LTS
- **IP Pública**: 15.228.201.242
- **Método de Implementación**: Script de despliegue automatizado (`deploy.sh`)
- **Puerto**: 5000
- **Fecha de Implementación**: 27 de junio de 2025

## Pasos para Verificar el Funcionamiento

1. **Verificar estado del servidor**:
   ```
   curl http://15.228.201.242:5000/health
   ```
   Respuesta esperada: `{"message":"API server is running","status":"ok"}`

2. **Listar archivos almacenados**:
   ```
   curl http://15.228.201.242:5000/list
   ```

3. **Consultar datos específicos**:
   ```
   curl "http://15.228.201.242:5000/query?ip=192.168.100.212"
   ```

## Consideraciones de Seguridad

El despliegue actual es una prueba de concepto que cumple con los requisitos del desafío. Para un entorno de producción, se recomienda implementar las siguientes mejoras de seguridad:

1. **Autenticación API**: Actualmente la API no requiere autenticación, lo que permitiría a cualquier persona con conocimiento de la IP acceder a los datos.

2. **Restricción del puerto 5000**: El puerto está abierto públicamente, lo que aumenta la superficie de ataque.

3. **Cifrado de datos**: Los datos sensibles del sistema se almacenan en archivos JSON sin cifrar.

4. **Protección contra DoS**: No hay límites de tasa implementados para prevenir ataques de denegación de servicio.

Consulte la sección "Consideraciones de Seguridad" en el README.md principal para obtener detalles y ejemplos de cómo implementar estas mejoras.
