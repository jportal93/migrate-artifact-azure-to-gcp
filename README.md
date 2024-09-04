
# Azure to Google Artifact Registry Image Migration Script

Este script tiene como objetivo extraer imágenes de contenedores de un registro de contenedores de Azure, procesarlas y subirlas a Google Artifact Registry.

## Requisitos previos

### Dependencias

- **Python 3.x**
- **Azure SDK para Python**
- **Google Cloud SDK**
- **Docker**

Instalar las dependencias necesarias con:

```bash
pip install azure-identity azure-mgmt-containerregistry google-cloud-storage google-auth google-cloud
```

### Credenciales

- **Azure:** Necesitarás la información del registro de contenedores de Azure, incluyendo el usuario y la contraseña.
- **Google:** El script utiliza un archivo de cuenta de servicio de Google Cloud para autenticarse en Google Artifact Registry. Debes proporcionar la ruta a tu archivo de credenciales JSON (`prod.json`).

## Configuración

Asegúrate de configurar las siguientes variables en el script:

```python
azure_registry = 'containers.azurecr.io'
azure_user = 'userContainers'
azure_password = '********'

google_region = 'us-central1'
google_project_id = 'project_id'
google_repository = 'name_of_repository_in_artifact'
```

## Estructura del Script

### Funciones principales

1. **`find_images_with_prefix(directory, prefix)`**: Busca las imágenes de contenedores con un prefijo específico dentro de los archivos YAML del directorio de GitOps.

2. **`setup_auth()`**: Realiza la autenticación en Azure Container Registry y Google Cloud para interactuar con los registros de contenedores.

3. **Ciclo principal**: Itera sobre las imágenes encontradas, las descarga desde Azure, las etiqueta y las sube a Google Artifact Registry.

### Directorios

- **`directory_path`**: Ruta al directorio que contiene los archivos de GitOps.
- **`key_path`**: Ruta al archivo de credenciales JSON para la autenticación en Google Cloud.

### Uso del script

1. **Buscar imágenes en archivos YAML**:

   El script buscará en los archivos del directorio especificado imágenes que comiencen con un prefijo dado, como las imágenes del registro de contenedores de Azure.

2. **Autenticación**:

   Autentica primero en Azure y luego en Google Artifact Registry para permitir la transferencia de imágenes entre ambos registros.

3. **Transferencia de imágenes**:

   El script descarga las imágenes del registro de Azure, las etiqueta para Google Artifact Registry y las sube.

4. **Limpieza**:

   Elimina las imágenes locales después de subirlas a Google Artifact Registry para liberar espacio.

## Ejecución

Ejecuta el script con:

```bash
python3 migrate_images.py
```

## Notas adicionales

- El archivo de credenciales de Google debe ser un archivo JSON válido descargado desde la consola de Google Cloud.
- Asegúrate de que Docker esté instalado y configurado correctamente para poder usar el comando `docker` desde la línea de comandos.
- La autenticación en Google Cloud puede ser configurada con `gcloud` antes de ejecutar el script.
  
## Contacto

Para más detalles o problemas al ejecutar el script, contacta a [jorgearmandoportaldiaz@gmail.com].
