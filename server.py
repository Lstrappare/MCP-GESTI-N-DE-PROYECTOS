from __future__ import annotations

from mcp.server.fastmcp import FastMCP
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
# HERRAMIENTA MCP
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
                # La función recursiva se encarga de este nodo
                # y de toda su descendencia (subtareas de subtareas…)
                _agregar_nodos(tarea, fase_id, tarea_id, lines)

        # Agregar estilos de color antes de cerrar el bloque de Mermaid
        lines.append("\n    %% Estilos automáticos de MINTRANET")
        lines.append("    style Root fill:#f8f9fa,stroke:#343a40,stroke-width:3px")

        # Lista de colores predefinidos para las 5 etapas
        colores = ["#d4edda", "#cce5ff", "#fff3cd", "#f8d7da", "#e2e3e5"]
        bordes  = ["#28a745", "#007bff", "#ffc107", "#dc3545", "#6c757d"]

        for i in range(len(datos.fases)):
            color_fondo = colores[i % len(colores)]
            color_borde = bordes[i % len(bordes)]
            lines.append(
                f"    style F{i} fill:{color_fondo},stroke:{color_borde},stroke-width:2px"
            )


        return "\n".join(lines)

    except Exception as e:
        # Retorno vital para que el Agente IA lea el error y corrija su JSON.
        return (
            f"Error de validación: {str(e)}. "
            "Corrige los parámetros y vuelve a ejecutar la herramienta."
        )


if __name__ == "__main__":
    print("Iniciando Servidor MCP de Gestión de Proyectos...")
    mcp.run(transport='stdio')