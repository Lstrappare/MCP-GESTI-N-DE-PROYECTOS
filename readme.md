# 🦆 Servidor MCP de Gestión de Proyectos

Servidor de herramientas basado en el **Model Context Protocol (MCP)** para automatizar la generación de Estructuras de Desglose del Trabajo (EDT) en formato Mermaid.js, imagen PNG y documento Word corporativo (.docx) para el proyecto MINTRANET.

### 🔧 Herramientas disponibles

| Herramienta | Descripción |
|---|---|
| `generar_edt` | Genera el código Mermaid del EDT en texto |
| `exportar_imagen_edt` | Renderiza el EDT como PNG y lo guarda en `~/Downloads/` |
| `generar_documento_proyecto_word` | Genera un documento corporativo `.docx` con diagrama EDT, tabla base jerarquizada y minuta de validación |

---

## ✅ Requisitos previos

| Herramienta | Versión mínima | Enlace |
|---|---|---|
| Python | 3.10+ | [python.org](https://www.python.org/downloads/) |
| Node.js | 18+ | [nodejs.org](https://nodejs.org/) |
| Git | cualquiera | [git-scm.com](https://git-scm.com/) |
| Claude Desktop | última | [claude.ai/download](https://claude.ai/download) |

> **Windows**: usa **PowerShell** o **Git Bash**.  
> **macOS/Linux**: usa la **Terminal** estándar.

---

## 📦 1. Clonar el repositorio

```bash
git clone https://github.com/JosaSeCisneros/MCP-GESTI-N-DE-PROYECTOS.git
cd MCP-GESTI-N-DE-PROYECTOS
```

---

## 🐍 2. Crear y activar el entorno virtual

### macOS / Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows (PowerShell)
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

### Windows (CMD)
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

> Sabrás que está activo cuando veas `(venv)` al inicio de tu línea de comandos.

---

## 📥 3. Instalar dependencias

Con el entorno virtual activo, ejecuta:

```bash
pip install -r requirements.txt
```

---

## 🖥️ 4. Integrar con Claude Desktop

### 4.1 Localizar el archivo de configuración

| Sistema operativo | Ruta |
|---|---|
| macOS | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Windows | `%APPDATA%\Claude\claude_desktop_config.json` |
| Linux | `~/.config/Claude/claude_desktop_config.json` |

### 4.2 Encontrar la ruta del Python del venv

Necesitas la ruta **absoluta** al intérprete Python dentro del venv.

#### macOS / Linux
```bash
# Ejecuta esto estando en la carpeta del proyecto con el venv activo:
which python
# Ejemplo de salida: /Users/tuUsuario/Downloads/Tareas/MCP-GESTI-N-DE-PROYECTOS/venv/bin/python
```

#### Windows (PowerShell)
```powershell
# Ejecuta esto con el venv activo:
where.exe python
# Ejemplo de salida: C:\Users\tuUsuario\...\MCP-GESTI-N-DE-PROYECTOS\venv\Scripts\python.exe
```

### 4.3 Editar el archivo de configuración

Abre `claude_desktop_config.json` y agrega la sección `gestion-proyectos` dentro de `mcpServers`:

#### macOS / Linux
```json
{
  "mcpServers": {
    "gestion-proyectos": {
      "command": "/RUTA_ABSOLUTA/MCP-GESTI-N-DE-PROYECTOS/venv/bin/python",
      "args": [
        "/RUTA_ABSOLUTA/MCP-GESTI-N-DE-PROYECTOS/server.py"
      ]
    }
  }
}
```

#### Windows
```json
{
  "mcpServers": {
    "gestion-proyectos": {
      "command": "C:\\RUTA_ABSOLUTA\\MCP-GESTI-N-DE-PROYECTOS\\venv\\Scripts\\python.exe",
      "args": [
        "C:\\RUTA_ABSOLUTA\\MCP-GESTI-N-DE-PROYECTOS\\server.py"
      ]
    }
  }
}
```

> ⚠️ Reemplaza `RUTA_ABSOLUTA` con la ruta real obtenida en el paso 4.2.  
> En Windows usa doble barra invertida `\\` dentro del JSON.

### 4.4 Reiniciar Claude Desktop

```
Menú → Claude → Quit Claude
```
Luego vuelve a abrirlo. Haz clic en el ícono de **martillo 🔨** en el chat para verificar que aparezcan las herramientas:

```
gestion-proyectos
  ├── generar_edt
  ├── exportar_imagen_edt
  └── generar_documento_proyecto_word
```

---

## 🧪 5. Pruebas con el Inspector MCP (sin Claude Desktop)

El inspector abre una UI web para invocar las herramientas manualmente.

### macOS / Linux
```bash
source venv/bin/activate
mcp dev server.py
```

### Windows
```powershell
venv\Scripts\Activate.ps1
mcp dev server.py
```

Luego abre **`http://localhost:5173`** en tu navegador.

> Si `mcp` no se reconoce: `python -m mcp dev server.py`

---

## 🧪 6. Prueba rápida desde la terminal

Verifica que todo funciona sin levantar el inspector ni Claude:

### macOS / Linux
```bash
source venv/bin/activate
python -c "
from server import generar_edt, EDTInput, Fase, Tarea

datos = EDTInput(
    nombre_proyecto='Proyecto de Prueba',
    fases=[
        Fase(nombre='Inicio', tareas=[
            Tarea(nombre='Acta de constitución', subtareas=[
                Tarea(nombre='Firma del patrocinador')
            ])
        ]),
        Fase(nombre='Planeación', tareas=[
            Tarea(nombre='Cronograma', subtareas=[
                Tarea(nombre='Definición de hitos')
            ])
        ]),
    ]
)
print(generar_edt(datos))
"
```

### Windows (PowerShell)
```powershell
venv\Scripts\Activate.ps1
python -c "from server import generar_edt, EDTInput, Fase, Tarea; datos = EDTInput(nombre_proyecto='Proyecto Test', fases=[Fase(nombre='Inicio', tareas=[Tarea(nombre='Acta', subtareas=[Tarea(nombre='Firma')])])]); print(generar_edt(datos))"
```

---

## 🗂️ 7. JSON de prueba en el Inspector

Cuando uses `mcp dev server.py`, selecciona la herramienta y pega este JSON:

### `generar_edt` — devuelve código Mermaid

```json
{
  "datos": {
    "nombre_proyecto": "Proyecto MINTRANET",
    "fases": [
      {
        "nombre": "Inicio",
        "tareas": [
          {
            "nombre": "Acta de constitución",
            "subtareas": [{ "nombre": "Firma del patrocinador", "subtareas": [] }]
          }
        ]
      },
      {
        "nombre": "Planeación",
        "tareas": [
          {
            "nombre": "Cronograma",
            "subtareas": [{ "nombre": "Definición de hitos", "subtareas": [] }]
          }
        ]
      },
      {
        "nombre": "Ejecución",
        "tareas": [
          {
            "nombre": "Desarrollo del módulo",
            "subtareas": [{ "nombre": "Integración con base de datos", "subtareas": [] }]
          }
        ]
      },
      {
        "nombre": "Control",
        "tareas": [
          {
            "nombre": "Seguimiento de avances",
            "subtareas": [{ "nombre": "Informe semanal", "subtareas": [] }]
          }
        ]
      },
      {
        "nombre": "Cierre",
        "tareas": [
          {
            "nombre": "Entrega final",
            "subtareas": [{ "nombre": "Acta de cierre", "subtareas": [] }]
          }
        ]
      }
    ]
  }
}
```

### `exportar_imagen_edt` — guarda PNG en `~/Downloads/`

Usa el mismo JSON de arriba. La herramienta responderá con:
```
✅ Imagen generada y guardada exitosamente.
📁 Ruta: /Users/tuUsuario/Downloads/EDT_Proyecto_MINTRANET_20260613_200622.png
🖼️  Archivo: EDT_Proyecto_MINTRANET_20260613_200622.png
```

---

## 💬 8. Cómo pedírselo a Claude Desktop

El servidor tiene **tres herramientas distintas**. Claude elige automáticamente la correcta según lo que le pidas:

### Herramienta `generar_edt` → devuelve código Mermaid en texto

> *"Genera el EDT del proyecto MINTRANET con las fases Inicio, Planeación, Ejecución, Control y Cierre en cascada vertical."*

Claude devolverá el código Mermaid como texto. Claude Desktop puede renderizarlo como diagrama interactivo, pero **solo permite descargarlo como `.html`**, no como imagen.

---

### Herramienta `exportar_imagen_edt` → muestra la imagen en el chat y guarda el PNG

> *"Genera el EDT del proyecto MINTRANET y **muéstrame la imagen**."*

> *"Exporta el diagrama como **imagen PNG**."*

> *"Usa la herramienta `exportar_imagen_edt` para generar el EDT."*

Con esta herramienta Claude Desktop:
1. **Muestra la imagen inline** directamente en el chat (sin `.html`)
2. **Guarda automáticamente** el archivo PNG en `~/Downloads/EDT_Proyecto_MINTRANET_YYYYMMDD_HHMMSS.png`

---

### Herramienta `generar_documento_proyecto_word` → genera documento corporativo .docx

> *"Genera el documento Word de la EDT del proyecto MINTRANET con la estructura metodológica completa."*

> *"Usa la herramienta `generar_documento_proyecto_word` para crear el documento corporativo."*

> *"Lee los archivos .txt del proyecto y genera el documento Word con el diagrama, la tabla base y la minuta de validación."*

Con esta herramienta Claude Desktop:
1. **Lee archivos de contexto** `.txt` proporcionados por el usuario
2. **Clasifica las tareas** dentro de la Estructura Metodológica Fija de 5 etapas
3. **Genera un `.docx` corporativo** que incluye:
   - Portada con datos del proyecto
   - Diagrama EDT visual (imagen embebida)
   - Tabla Base de la EDT jerarquizada (Código EDT, Nombre, Descripción Operativa, Hito)
   - Minuta de Validación con campos de firma
4. **Guarda automáticamente** el archivo en `~/Downloads/EDT_NombreProyecto_YYYYMMDD_HHMMSS.docx`

> ⚠️ **Recuerda reiniciar Claude Desktop** después de cualquier cambio en `server.py` para que cargue la versión actualizada.

---

## 🛑 Detener el servidor (Inspector)

Presiona `Ctrl + C` en la terminal.

Para desactivar el entorno virtual:
```bash
deactivate
```

---

## ❓ Solución de problemas

| Problema | Solución |
|---|---|
| No aparece el 🔨 en Claude Desktop | Verifica las rutas en `claude_desktop_config.json` y reinicia Claude |
| Claude solo descarga `.html` al pedir el diagrama | Pídele explícitamente usar `exportar_imagen_edt`: *"Muéstrame la imagen"* |
| `string_too_short` en el Inspector | El campo `nombre_proyecto` quedó vacío — escribe un nombre real antes de ejecutar |
| `mcp: command not found` | Usa `python -m mcp dev server.py` |
| `python: command not found` (macOS/Linux) | Usa `python3` en lugar de `python` |
| Error de permisos en Windows (`Activate.ps1`) | Ejecuta `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` como administrador |
| Puerto 5173 ocupado | Cierra otras instancias del inspector o reinicia la terminal |
| `ModuleNotFoundError: mcp` | Verifica que el `(venv)` esté activo y ejecuta `pip install -r requirements.txt` |
| Error al exportar imagen | Verifica conexión a internet (usa la API de `mermaid.ink`) |
| Rutas con espacios en Windows | Encierra las rutas entre comillas dobles en el JSON |

---

## 📝 Notas

- La herramienta `generar_edt` soporta **profundidad ilimitada** de tareas y subtareas mediante recursividad.
- La herramienta `exportar_imagen_edt` requiere **conexión a internet** para usar la API de `mermaid.ink`.
- Los diagramas incluyen **estilos de color automáticos** para cada fase (5 colores rotativos).
- Si tienes dudas, contacta a **José Manuel**.