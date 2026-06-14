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
    nombre_proyecto: str = Field(..., min_length=1)
    fases: List[Fase]


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
    Genera la Estructura de Desglose del Trabajo (EDT) en formato
    Mermaid.js a partir de los datos del proyecto.
    Soporta profundidad de tareas ilimitada mediante recursividad.
    """
    try:
        if not datos.fases:
            raise ValueError(
                "El JSON no contiene fases definidas. "
                "Revisa la extracción de los datos."
            )

        lines: list[str] = [
            "```mermaid",
            "graph TD;",
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

        lines.append("```")
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