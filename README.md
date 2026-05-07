# Automation Task Script

Proyecto de automatización en Python para organizar archivos dentro de una carpeta saturada usando reglas simples por extensión. El objetivo es dejar un entregable listo para producción básica, demostrable en portafolio y fácil de extender.

## Funcionalidad principal

- `.pdf` se mueve a `Documentos`
- `.jpg`, `.jpeg`, `.png` se mueven a `Imágenes`
- `.xlsx`, `.csv` se mueven a `Datos`
- Cualquier otra extensión se mueve a `Otros`
- Las carpetas de destino se crean automáticamente si no existen
- Si ya existe un archivo con el mismo nombre, el script genera un sufijo incremental para evitar sobrescrituras

## Estructura del proyecto

```text
automation-task-script/
|-- src/
|   `-- automation_task_script/
|       |-- __init__.py
|       |-- cli.py
|       `-- organizer.py
|-- tests/
|   |-- test_cli.py
|   |-- test_organizer.py
|   `-- _bootstrap.py
|-- .gitignore
|-- LICENSE
|-- pyproject.toml
`-- README.md
```

## Tecnologías utilizadas

- Python 3.10+
- `pathlib` para manejo de rutas
- `shutil` para mover archivos
- `unittest` para validación automatizada sin dependencias externas
- Buenas prácticas PEP 8 y diseño modular

## Instalación

1. Clona el repositorio:

```powershell
git clone <TU-REPOSITORIO>
cd automation-task-script
```

2. Crea y activa un entorno virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Instala el proyecto en modo editable:

```powershell
pip install -e .
```

## Uso paso a paso

1. Coloca archivos mezclados dentro de una carpeta, por ejemplo `C:\temp\entrada`.
2. Ejecuta el script con la ruta objetivo:

```powershell
automation-task-script C:\temp\entrada
```

3. El sistema analizará los archivos y los moverá a las carpetas correctas.
4. Revisa dentro de la carpeta objetivo las subcarpetas `Documentos`, `Imágenes`, `Datos` y `Otros`.

También puedes ejecutarlo sin instalar el comando global:

```powershell
python -m automation_task_script.cli C:\temp\entrada
```

## Ejemplo de ejecución

Supongamos esta carpeta inicial:

```text
C:\temp\entrada
|-- contrato.pdf
|-- foto.png
|-- ventas.csv
`-- ideas.txt
```

Comando:

```powershell
automation-task-script C:\temp\entrada
```

Salida esperada:

```text
Organizacion completada.
Archivos detectados: 4
Archivos movidos: 4
Elementos omitidos: 4
- Documentos: 1
- Imágenes: 1
- Datos: 1
- Otros: 1
```

Resultado:

```text
C:\temp\entrada
|-- Datos/
|   `-- ventas.csv
|-- Documentos/
|   `-- contrato.pdf
|-- Imágenes/
|   `-- foto.png
`-- Otros/
    `-- ideas.txt
```

## Testing y validación

Ejecuta la suite automatizada:

```powershell
python -m unittest discover -s tests -v
```

Cobertura validada por pruebas:

- Clasificación correcta por extensión
- Omisión de carpetas existentes
- Resolución de colisiones de nombres
- Error al apuntar a una ruta inexistente

## Configurar Selenium con Microsoft Edge

Si más adelante quieres extender este proyecto para automatización web:

1. Instala Selenium:

```powershell
pip install selenium
```

2. Verifica que Microsoft Edge esté instalado.
3. Descarga la versión compatible de `msedgedriver` o usa Selenium Manager con Selenium reciente.
4. Agrega `msedgedriver` al `PATH` si trabajas con driver manual.
5. Usa una configuración mínima como esta:

```python
from selenium import webdriver
from selenium.webdriver.edge.options import Options

options = Options()
options.add_argument("--start-maximized")

driver = webdriver.Edge(options=options)
driver.get("https://www.example.com")
```

Recomendación profesional:

- Usa Selenium 4.6+ para aprovechar Selenium Manager y evitar gestionar drivers manualmente.
- Fija versiones en un `requirements.txt` o lockfile cuando el proyecto pase a un entorno corporativo.

## Automatizar GitHub de forma segura

Nunca hardcodees usuario, contraseña o tokens en el código.

Buenas prácticas:

1. Usa variables de entorno para credenciales o tokens:

```powershell
$env:GITHUB_TOKEN="tu_token_temporal"
```

2. Consume el token desde Python:

```python
import os

github_token = os.getenv("GITHUB_TOKEN")
```

3. Usa GitHub CLI o tokens personales con permisos mínimos.
4. Agrega `.env` al `.gitignore` si usas archivos locales de configuración.
5. Rota credenciales si sospechas exposición.

Ejemplo con GitHub CLI:

```powershell
gh auth login
git remote add origin https://github.com/USUARIO/automation-task-script.git
git push -u origin main
```

## Posibles mejoras futuras

- Soporte para más tipos de archivo mediante configuración externa
- Modo simulación (`--dry-run`) para previsualizar cambios
- Logging estructurado a archivo
- Integración con watchdog para organización en tiempo real
- Empaquetado con Docker para entornos consistentes
- Pipeline CI con GitHub Actions

## Licencia

MIT
