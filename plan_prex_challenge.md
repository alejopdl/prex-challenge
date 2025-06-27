# Plan de Desarrollo - Desafío Técnico Prex: Relevamiento de Servidores

## 🔎 Objetivo del Desafío

Crear un sistema compuesto por un **agente** que recolecte información de instancias Windows y Linux, y una **API** que reciba y almacene estos datos. Este sistema debe correr en una instancia EC2 de AWS y facilitar la consulta de los datos recolectados.

---

## 📊 Requisitos y Cómo Serán Cumplidos

### 1. **Agente de Recolección**

**Debe:**

- Recolectar:
  - Información del procesador
  - Listado de procesos
  - Usuarios con sesión abierta
  - Nombre del sistema operativo
  - Versión del sistema operativo
- Enviar la información a una API
- Funcionar en Windows y Linux

**Solución:**

- Lenguaje: Python 3
- Librerías: `psutil`, `platform`, `socket`, `os`, `json`, `requests`
- Enviar información en formato JSON mediante `requests.post()`

### 2. **API de Recepción y Consulta**

**Debe:**

- Tener un endpoint para recibir datos (POST `/upload`)
- Almacenar la info en archivos `IP_YYYY-MM-DD.json`
- Tener un endpoint de consulta (GET `/query?ip=...`)

**Solución:**

- Framework: Flask (o FastAPI)
- Almacenamiento: archivos JSON en disco (con opción futura de pasar a DB)
- Archivo `storage.py` para manejo de guardado y lectura

### 3. **Entrega del Proyecto**

**Debe incluir:**

- Código fuente en repositorio (GitHub o Bitbucket)
- Instrucciones de ejecución (README con requisitos y pasos)
- Descripción técnica
- Evidencia de servidor corriendo en EC2

**Solución:**

- Se incluye archivo `README.md` detallado
- Capturas o grabaciones mostrando servidor activo
- Instrucciones para correr localmente o con Docker

### 4. **Extras Deseables**

| Requisito         | Acción                                           |
| ----------------- | ------------------------------------------------ |
| Dockerizar la API | Crear `Dockerfile` que ejecute el servidor       |
| Almacenar en DB   | Opcional: SQLite o PostgreSQL en futuro refactor |

---

## 📚 Estructura del Proyecto

```
prex-challenge/
│
├── agent/                       # Agente recolector
│   ├── collector.py             # Obtención de datos
│   ├── sender.py                # Enío de datos a la API
│   └── run_agent.py             # Script principal
│
├── api_server/                  # API
│   ├── app.py                   # Endpoints Flask
│   ├── storage.py               # Guardado/carga de datos
│   └── run_api.py               # Servidor
│
├── Dockerfile                   # Contenedor para la API
├── requirements.txt             # Dependencias
├── README.md                    # Documentación
└── .gitignore
```

---

## ☁️ Despliegue en AWS EC2

**Pasos:**

1. Crear cuenta AWS y lanzar instancia EC2 Ubuntu (free-tier)
2. Instalar Python, Git, pip
3. Clonar repositorio y ejecutar `run_api.py`
4. Configurar reglas de seguridad para exponer puerto (ej: 5000)
5. Verificar acceso desde agente local

---

## 🚀 Tecnologías Seleccionadas

| Componente     | Tecnología                     | Justificación                       |
| -------------- | ------------------------------ | ----------------------------------- |
| Lenguaje       | Python 3                       | Multiplataforma, sencillo, robusto  |
| API            | Flask                          | Liviano, rápido de implementar      |
| Recolección    | psutil, platform               | Alta compatibilidad                 |
| Transporte     | requests                       | Estándar HTTP client                |
| Almacenamiento | Archivos JSON                  | Sencillo, cumple requisitos mínimos |
| Despliegue     | EC2 Ubuntu + Docker (opcional) | Flexible y gratuito                 |

---

## 🚪 Seguridad y Consideraciones Finales

- Una vez entregado el ejercicio, eliminar la instancia EC2 y la cuenta para evitar costos.
- No almacenar información sensible en los logs o archivos JSON.
- Documentar cada módulo para facilitar la evaluación.

---

Este plan cubre todos los requerimientos del ejercicio de Prex y deja espacio para mejoras futuras como el uso de bases de datos o dashboards de monitoreo.

