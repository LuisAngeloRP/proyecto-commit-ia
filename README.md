
# Git Commit Assistant

Este proyecto es un script automatizado para realizar commits en Git con mensajes generados automáticamente o utilizando IA para una descripción detallada.

## Requisitos

- Python 3.10.x
- Repositorio Git válido
- [OpenAI API Key](https://platform.openai.com/signup) (opcional para generar mensajes con IA)
- Archivo `.env` con tu clave de API de OpenAI:

```bash
OPENAI_API_KEY=tu_clave_api_aqui
```

## Instalación

1. Clona este repositorio y navega a la carpeta del proyecto.
2. Instala las dependencias:

```bash
pip install -r requirements.txt
```

3. Asegúrate de que tu entorno tiene acceso a la API de OpenAI cargando el archivo `.env`.

## Uso

> **Nota:** En algunos casos, puede ser necesario ejecutar `git add .` manualmente para agregar cambios al área de staging antes de utilizar el script.

### Modo 1: Commit de todos los cambios

Para realizar un commit de todos los archivos cambiados:

```bash
python git_commit_assistant.py --mode all
```

- Agrega `--use-ai` para generar el mensaje de commit utilizando IA:

```bash
python git_commit_assistant.py --mode all --use-ai
```

### Modo 2: Commit por archivo

Para hacer commits individuales por archivo:

```bash
python git_commit_assistant.py --mode per-file
```

- También puedes usar IA para generar mensajes en este modo:

```bash
python git_commit_assistant.py --mode per-file --use-ai
```

## Ejemplo

```bash
git add .
python git_commit_assistant.py --mode all --use-ai
```

- El script muestra un mensaje de commit sugerido y te pide confirmación antes de proceder.

## Notas

- El script maneja automáticamente archivos eliminados y cambios en los archivos existentes.
- Si no deseas usar IA, el mensaje de commit se generará utilizando un formato estándar basado en el tipo de cambio.

## Contribuciones

¡Las contribuciones son bienvenidas! Si encuentras errores o tienes sugerencias, siéntete libre de abrir un issue o enviar un pull request.
