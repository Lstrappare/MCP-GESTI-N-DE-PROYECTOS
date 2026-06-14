from __future__ import annotations

import base64
import httpx
from datetime import datetime
from pathlib import Path

from mcp.server.fastmcp import FastMCP, Image
from pydantic import BaseModel, Field
from typing import List, Optional

mcp = FastMCP("MCP-GestionProyectos")

# ==========================================
# MODELOS PYDANTIC — ESTRUCTURA RECURSIVA
# Una Tarea puede contener subtareas del
# mismo tipo Tarea (profundidad ilimitada).
# ==========================================

class Tarea(BaseModel):
    nombre: str = Field(..., min_length=1)
    subtareas: Optional[List[Tarea]] = []

# Necesario para que Pydantic resuelva la
# auto-referencia después de la definición.
Tarea.model_rebuild()


class Fase(BaseModel):
    nombre: str = Field(..., min_length=1)
    tareas: List[Tarea] = []


class EDTInput(BaseModel):
    nombre_proyecto: str = Field(..., min_length=1, description="El nombre oficial del proyecto.")
    fases: List[Fase] = Field(
        ...,
        description="""
        REGLA ESTRICTA PARA LA IA:
        1. Debes generar exactamente las etapas principales indicadas en los documentos fuente (ej. Inicio, Planeación, Ejecución, Control, Cierre).
        2. El anidamiento dentro de cada etapa debe ser COMPLETAMENTE VERTICAL Y LINEAL.
        3. Cada tarea padre debe tener un máximo de UNA (1) subtarea.
        4. Crea una cadena en cascada perfecta hacia abajo. ¡PROHIBIDO agrupar elementos horizontalmente!
        """
    )


# ==========================================
# FUNCIÓN AUXILIAR RECURSIVA
# Genera las conexiones Mermaid para un nodo
# y todos sus descendientes sin límite de
# profundidad. Usa un prefijo de ID único
# heredado por cada nivel de la llamada.
# ==========================================

def _agregar_nodos(
    tarea: Tarea,
    parent_id: str,
    node_id: str,
    lines: list[str],
) -> None:
    """Añade la arista parent→nodo y desciende recursivamente."""
    lines.append(f'    {parent_id} --> {node_id}["{tarea.nombre}"]')

    if tarea.subtareas:
        for idx, subtarea in enumerate(tarea.subtareas):
            child_id = f"{node_id}_{idx}"
            _agregar_nodos(subtarea, node_id, child_id, lines)


# ==========================================
# HELPER COMPARTIDO — CONSTRUCCIÓN MERMAID
# Separado para que ambas herramientas lo
# reutilicen sin duplicar lógica.
# ==========================================

def _construir_mermaid(datos: EDTInput) -> str:
    """Construye y retorna el código Mermaid completo del EDT."""
    if not datos.fases:
        raise ValueError(
            "El JSON no contiene fases definidas. "
            "Revisa la extracción de los datos."
        )

    lines: list[str] = [
        "graph TD",
        f'    Root["{datos.nombre_proyecto}"]',
    ]

    for i, fase in enumerate(datos.fases):
        fase_id = f"F{i}"
        lines.append(f'    Root --> {fase_id}["{fase.nombre}"]')

        if not fase.tareas:
            raise ValueError(
                f"La fase '{fase.nombre}' vino sin tareas asignadas."
            )

        for j, tarea in enumerate(fase.tareas):
            tarea_id = f"T{i}_{j}"
            _agregar_nodos(tarea, fase_id, tarea_id, lines)

    # Estilos de color automáticos de MINTRANET
    lines.append("\n    %% Estilos automáticos de MINTRANET")
    lines.append("    style Root fill:#f8f9fa,stroke:#343a40,stroke-width:3px")

    colores = ["#d4edda", "#cce5ff", "#fff3cd", "#f8d7da", "#e2e3e5"]
    bordes  = ["#28a745", "#007bff", "#ffc107", "#dc3545", "#6c757d"]

    for i in range(len(datos.fases)):
        color_fondo = colores[i % len(colores)]
        color_borde = bordes[i % len(bordes)]
        lines.append(
            f"    style F{i} fill:{color_fondo},stroke:{color_borde},stroke-width:2px"
        )

    return "\n".join(lines)


# ==========================================
# HERRAMIENTAS MCP
# ==========================================

@mcp.tool()
def generar_edt(datos: EDTInput) -> str:
    """
    Transforma la estructura de un proyecto en un diagrama de Mermaid.

    INSTRUCCIONES CRÍTICAS PARA EL LLM ANTES DE INVOCAR ESTA HERRAMIENTA:
    - Lee todos los archivos .txt proporcionados por el usuario.
    - Extrae la información y fuérzala a una estructura de árbol de
      profundidad máxima pero de anchura mínima.
    - Para que el diagrama no se expanda hacia los lados, encadena cada
      tarea como hija única de la tarea anterior.
    - Solo invoca esta herramienta cuando hayas estructurado mentalmente
      el JSON cumpliendo la regla de 1 solo hijo por nodo.
    - Soporta profundidad de tareas ilimitada mediante recursividad.
    """
    try:
        return _construir_mermaid(datos)
    except Exception as e:
        # Retorno vital para que el Agente IA lea el error y corrija su JSON.
        return (
            f"Error de validación: {str(e)}. "
            "Corrige los parámetros y vuelve a ejecutar la herramienta."
        )


@mcp.tool()
def exportar_imagen_edt(datos: EDTInput) -> Image:
    """
    Genera el EDT en Mermaid, lo renderiza como imagen PNG y lo muestra
    directamente en el chat. También guarda el archivo en ~/Downloads/.

    Usa la API pública mermaid.ink para renderizar sin dependencias locales.
    Devuelve la imagen para que Claude la muestre inline en la conversación.

    CUÁNDO USAR ESTA HERRAMIENTA:
    - Cuando el usuario pida la imagen, el PNG, ver el diagrama o descargarlo.
    - Aplica las mismas reglas de estructura que generar_edt.
    """
    # 1. Construir el código Mermaid
    mermaid_code = _construir_mermaid(datos)

    # 2. Codificar en base64 para la API de mermaid.ink
    encoded = base64.urlsafe_b64encode(
        mermaid_code.encode("utf-8")
    ).decode("utf-8")
    url_imagen = f"https://mermaid.ink/img/{encoded}?bgColor=white"

    # 3. Descargar los bytes PNG
    response = httpx.get(url_imagen, timeout=20, follow_redirects=True)
    response.raise_for_status()
    image_bytes = response.content

    # 4. Guardar también en ~/Downloads como respaldo
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_seguro = datos.nombre_proyecto.replace(" ", "_").replace("/", "-")
    nombre_archivo = f"EDT_{nombre_seguro}_{timestamp}.png"
    ruta = Path.home() / "Downloads" / nombre_archivo
    ruta.write_bytes(image_bytes)

    # 5. Devolver objeto Image → Claude Desktop lo muestra inline en el chat
    return Image(data=image_bytes, format="png")


if __name__ == "__main__":
    print("Iniciando Servidor MCP de Gestión de Proyectos...")
    mcp.run(transport='stdio')