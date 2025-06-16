# EventMix - Backend

EventMix es una aplicación diseñada para la gestión de eventos, facilitando la organización, seguimiento y administración de eventos.

Este documento explica cómo poner en marcha el backend de EventMix, desarrollado con **FastAPI**, para que puedas ejecutarlo localmente usando Docker.

---

## Guía para iniciar el backend

### Paso 1: Clonar el repositorio

```bash
git clone https://github.com/Projecto-Final-Eventos-Damian/Backend.git
```

### Paso 2: Acceder al directorio del proyecto

```bash
cd Backend
```

### Paso 3: añadir el .envDev a un .env

```bash
cp .envDev .env
```

### Paso 4: Construir y levantar los contenedores con Docker Compose

```bash
docker-compose up --build
```

---

## Solución a posibles errores

Si al ejecutar el paso 3 aparece un error similar a:

```vbnet
KeyError: 'ContainerConfig'
```

Sigue estos pasos para solucionarlo:

1.  Detén y elimina los contenedores y volúmenes actuales:
    

```bash
docker-compose down --volumes
```

2.  Vuelve a construir y levantar los contenedores:
    

```bash
docker-compose up --build
```

---

## Verificación del funcionamiento

Una vez levantado el backend, accede a la siguiente URL desde tu navegador o herramienta de API:

```arduino
http://localhost:8000
```

Deberías ver un mensaje de bienvenida o información sobre la API, indicando que el backend está funcionando correctamente.
