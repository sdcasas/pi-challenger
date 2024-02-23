# API de Characters

Esta API permite interactuar con 

## Requisitos

- Python 3.12
- Docker (opcional)

## Configuración del entorno de desarrollo

1. Clona este repositorio:

```bash
git clone https://github.com/sdcasas/pi-challenger.git
```

2. Accede al directorio del proyecto:

```bash
cd pi-challenger
```

3. Crea un entorno virtual e instala las dependencias:

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Ejecución

### Con Docker (recomendado)

```bash
docker-compose up -d --build
```

La API estará disponible en `http://localhost:8000`.

### Sin Docker

```bash
uvicorn app.main:app --reload
```

La API estará disponible en `http://localhost:8000`.

