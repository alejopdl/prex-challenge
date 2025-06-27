# Capturas de Pantalla - Evidencia de Despliegue

## Capturas Necesarias

Para completar la evidencia requerida por el desafío Prex, se recomienda incluir las siguientes capturas de pantalla:

1. **Panel de Control de AWS EC2**
   - Mostrar la instancia EC2 en ejecución con la IP 15.228.201.242
   - Confirmar que está utilizando el grupo de seguridad adecuado con los puertos abiertos

2. **Respuesta del Servidor API**
   - Una captura del navegador o terminal mostrando la respuesta del endpoint `/health`
   - Una captura del navegador o terminal mostrando la respuesta del endpoint `/list`

3. **Datos Almacenados**
   - Una captura del navegador o terminal mostrando parte de los datos consultados a través del endpoint `/query`

4. **Registro en el Servidor**
   - Opcional: capturas de pantalla de los logs del servidor en EC2 mostrando las solicitudes recibidas

## Pasos para Capturar la Evidencia

1. Para el panel de AWS EC2:
   - Iniciar sesión en la consola de AWS
   - Navegar a EC2 > Instancias
   - Buscar la instancia "prex-challenge-server"
   - Tomar una captura de pantalla que muestre el estado "running" y la IP pública

2. Para las respuestas de la API:
   - Abrir un navegador y visitar:
     - `http://15.228.201.242:5000/health`
     - `http://15.228.201.242:5000/list` 
     - `http://15.228.201.242:5000/query?ip=192.168.100.212`
   - Alternativamente, usar los comandos curl como se documentó anteriormente

3. Para los logs del servidor:
   - Conectarse a la instancia EC2 mediante SSH
   - Revisar los logs con el siguiente comando:
     ```bash
     ssh -i "prex-challenge-key.pem" ubuntu@15.228.201.242
     cd prex-challenge
     tail -f logs/api_server.log
     ```
   - Tomar una captura de pantalla mostrando las solicitudes procesadas

## Organización de la Evidencia

Guardar todas las capturas de pantalla en la carpeta `evidencia` con nombres descriptivos:
- `ec2-instancia.png`: Panel de AWS mostrando la instancia
- `api-health.png`: Respuesta del endpoint health
- `api-list.png`: Listado de archivos JSON almacenados
- `api-query.png`: Datos consultados de un sistema
- `server-logs.png`: Logs del servidor mostrando peticiones

Esta documentación visual, junto con el archivo `comandos.md`, proporciona evidencia completa del correcto funcionamiento del sistema en AWS EC2, cumpliendo con los requisitos del desafío Prex.
