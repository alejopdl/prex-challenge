# Presentación del Desafío Técnico Prex

**Candidato:** Alejo Ponce De Leon  
**Fecha:** 27 de junio de 2025  
**Repositorio:** [https://github.com/alejopdl/prex-challenge](https://github.com/alejopdl/prex-challenge)

---

## Hola equipo Prex!

Les dejo el repositorio donde subí todo lo referido al challenge de seguridad para la posición. 

## Descripción del Proyecto

He desarrollado un sistema de monitoreo de servidores que consta de dos componentes principales:

1. **Agente de Recolección:** Un programa en Python capaz de ejecutarse en Windows y Linux que recopila información del sistema (CPU, procesos, usuarios conectados, detalles del SO) y la envía a una API central.

2. **Servidor API:** Una aplicación Flask desplegada en AWS EC2 que recibe, almacena y permite consultar la información enviada por los agentes en formato JSON.

## Estructura del Proyecto

```
prex-challenge/
├── agent/                      # Código del agente de recolección
│   ├── collector.py            # Implementación principal del agente
│   └── utils.py                # Utilidades para la recolección de datos
│
├── api_server/                 # Servidor API
│   ├── app.py                  # Implementación de la API Flask
│   └── storage.py              # Gestión del almacenamiento de datos
│
├── data/                       # Directorio de almacenamiento de datos
├── docs/                       # Documentación técnica detallada
├── evidencia/                  # Capturas y documentación del despliegue
│   ├── api-health.png          # Verificación del endpoint /health
│   ├── api-list.png            # Listado de archivos almacenados
│   ├── api-query.png           # Consulta de datos específicos
│   ├── comandos.md             # Registro de comandos utilizados
│   ├── capturas.md             # Guía para capturas de pantalla
│   ├── ec2-instancia.png       # Panel de AWS mostrando EC2 running
│   └── server-logs.mov         # Video de los logs del servidor
│
├── tests/                      # Pruebas unitarias e integración
├── deploy.sh                   # Script de despliegue automatizado
├── Dockerfile                  # Configuración para Docker
└── README.md                   # Documentación principal
```

## Características Implementadas

- ✅ **Agente multiplataforma** compatible con Windows y Linux
- ✅ **API RESTful** con endpoints para subir y consultar datos
- ✅ **Almacenamiento en archivos JSON** con formato `<IP>_<YYYY-MM-DD>.json`
- ✅ **Despliegue en AWS EC2** con evidencia completa
- ✅ **Dockerización** para facilitar el despliegue
- ✅ **Documentación detallada** para instalación, uso y prueba

## Prueba del Sistema

El sistema está desplegado y funcional en AWS EC2 (15.228.201.242). Pueden probar los siguientes endpoints:

- `http://15.228.201.242:5000/health` - Estado del servidor
- `http://15.228.201.242:5000/list` - Listar archivos almacenados
- `http://15.228.201.242:5000/query?ip=192.168.100.212` - Consultar datos específicos

Para ejecutar el agente y enviar datos de su propio servidor, pueden seguir las instrucciones detalladas en el README.md del repositorio.

## Consideraciones de Seguridad

Se han identificado algunas consideraciones de seguridad importantes para un entorno de producción:

- Implementación de autenticación para la API
- Restricción de acceso por IP
- Cifrado de datos en reposo y en tránsito
- Protección contra ataques DoS
- Mejoras en la validación de entrada

El README.md incluye detalles y recomendaciones específicas para implementar estas mejoras.

## Herramientas Adicionales Utilizadas

Para el desarrollo de este proyecto, además de las tecnologías principales (Python, Flask, AWS), se utilizaron las siguientes herramientas de apoyo:

- **Windsurf**: Entorno de desarrollo inteligente, versión 2023.2 
- **Modelos de Lenguaje (LLMs)**:
  - Claude 3.7 Sonnet (Thinking) - Para asistencia en el desarrollo y diseño de sistemas
  - ChatGPT-4o - Para consultas técnicas y optimización de código

---

Agradezco la oportunidad de participar en este desafío técnico. Quedo a disposición para cualquier aclaración o pregunta adicional.

Saludos,

**Alejo Ponce De Leon**
