# 🦆 Servidor MCP de Gestión de Proyectos

Servidor de herramientas basado en el **Model Context Protocol (MCP)** para automatizar la generación de Estructuras de Desglose del Trabajo (EDT) en formato Mermaid.js para el proyecto MINTRANET.

---

## ✅ Requisitos previos

Asegúrate de tener instalado lo siguiente:

| Herramienta | Versión mínima | Enlace |
|---|---|---|
| Python | 3.10+ | [python.org](https://www.python.org/downloads/) |
| Node.js | 18+ | [nodejs.org](https://nodejs.org/) |
| Git | cualquiera | [git-scm.com](https://git-scm.com/) |

> **Windows**: usa **PowerShell** o **Git Bash** para todos los comandos.  
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

Esto instala `mcp[cli]` y todas sus dependencias automáticamente.

---

## 🔌 4. Iniciar el servidor MCP (Inspector visual)

El método más sencillo para probar es con el **MCP Inspector**, que abre una UI en el navegador:

### macOS / Linux
```bash
mcp dev server.py
```

### Windows (PowerShell o CMD)
```powershell
mcp dev server.py
```

Luego abre tu navegador en **`http://localhost:5173`**.

> Si `mcp` no se reconoce, usa: `python -m mcp dev server.py`

---

## ▶️ 5. Iniciar el servidor en modo producción (stdio)

Para conectarlo directamente a un agente IA o cliente MCP:

### macOS / Linux
```bash
python server.py
```

### Windows
```powershell
python server.py
```

---

## 🧪 6. Prueba rápida desde la terminal

Puedes verificar que todo funciona sin levantar el inspector:

### macOS / Linux
```bash
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
python -c "
from server import generar_edt, EDTInput, Fase, Tarea
datos = EDTInput(nombre_proyecto='Proyecto de Prueba', fases=[Fase(nombre='Inicio', tareas=[Tarea(nombre='Acta de constitucion', subtareas=[Tarea(nombre='Firma del patrocinador')])])])
print(generar_edt(datos))
"
```

> En Windows evita acentos y caracteres especiales en el one-liner de PowerShell; el Inspector visual no tiene esa limitación.

---

## 🧪 7. JSON de prueba en el Inspector

Cuando uses `mcp dev server.py`, selecciona la herramienta **`generar_edt`** y pega este JSON:

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
            "subtareas": [
              {
                "nombre": "Aprobación del patrocinador",
                "subtareas": []
              }
            ]
          }
        ]
      },
      {
        "nombre": "Planeación",
        "tareas": [
          {
            "nombre": "Cronograma",
            "subtareas": [
              {
                "nombre": "Definición de hitos",
                "subtareas": []
              }
            ]
          }
        ]
      },
      {
        "nombre": "Ejecución",
        "tareas": [
          {
            "nombre": "Desarrollo del módulo principal",
            "subtareas": [
              {
                "nombre": "Integración con base de datos",
                "subtareas": []
              }
            ]
          }
        ]
      }
    ]
  }
}
```

El resultado será un bloque ` ```mermaid ``` ` listo para pegar en cualquier Markdown, Notion o GitHub.

---

## 🛑 Detener el servidor

Presiona `Ctrl + C` en la terminal.

Para desactivar el entorno virtual:

```bash
deactivate
```

---

## ❓ Solución de problemas

| Problema | Solución |
|---|---|
| `mcp: command not found` | Usa `python -m mcp dev server.py` |
| `python: command not found` (macOS/Linux) | Usa `python3` en lugar de `python` |
| Error de permisos en Windows (`Activate.ps1`) | Ejecuta `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` en PowerShell como administrador |
| Puerto 5173 ocupado | Cierra otras instancias del inspector o reinicia la terminal |
| `ModuleNotFoundError: mcp` | Verifica que el `venv` esté activo (`(venv)` visible) y ejecuta `pip install -r requirements.txt` |

---

## 📝 Notas

- La herramienta `generar_edt` soporta **profundidad ilimitada** de tareas y subtareas mediante recursividad.
- Los diagramas generados incluyen **estilos de color automáticos** para cada fase (hasta 5 colores rotativos).
- Si tienes dudas, contacta a **José Manuel**.