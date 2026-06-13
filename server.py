from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field
from typing import List

mcp = FastMCP("MCP-GestionProyectos")

# ==========================================
# TAREA IN-44 (MIGUEL): ESQUEMA JSON (PYDANTIC)
# ==========================================
class Subtarea(BaseModel):
    nombre: str = Field(..., min_length=1)

class Tarea(BaseModel):
    nombre: str = Field(..., min_length=1)
    subtareas: List[Subtarea] = []

class Fase(BaseModel):
    nombre: str = Field(..., min_length=1)
    tareas: List[Tarea] = []

class EDTInput(BaseModel):
    nombre_proyecto: str = Field(..., min_length=1)
    fases: List[Fase]


@mcp.tool()
def generar_edt(datos: EDTInput) -> str:
    """
    Genera la estructura de desglose del trabajo (EDT) en formato Mermaid.js a partir de los datos del proyecto.
    """
    # Validación estructural y manejo de excepciones
    try:
        if not datos.fases:
            raise ValueError("El JSON no contiene fases definidas. Revisa la extracción de los datos.")

        # Lógica de construcción del diagrama Mermaid
        mermaid_code = "```mermaid\ngraph TD;\n"
        mermaid_code += f"    Root[{datos.nombre_proyecto}]\n"
        
        for i, fase in enumerate(datos.fases):
            fase_id = f"F{i}"
            mermaid_code += f"    Root --> {fase_id}[{fase.nombre}]\n"
            
            if not fase.tareas:
                raise ValueError(f"La fase '{fase.nombre}' vino sin tareas asignadas.")
                
            for j, tarea in enumerate(fase.tareas):
                tarea_id = f"T{i}_{j}"
                mermaid_code += f"    {fase_id} --> {tarea_id}[{tarea.nombre}]\n"
                
                # Integración del nivel de subtareas
                if tarea.subtareas:
                    for k, subtarea in enumerate(tarea.subtareas):
                        subtarea_id = f"ST{i}_{j}_{k}"
                        mermaid_code += f"    {tarea_id} --> {subtarea_id}[{subtarea.nombre}]\n"
        
        mermaid_code += "```"
        return mermaid_code

    except Exception as e:
        # Retorno vital para que el Agente IA lea el error y corrija su propio JSON.
        return f"Error de validación: {str(e)}. Corrige los parámetros y vuelve a ejecutar la herramienta."

if __name__ == "__main__":
    print("Iniciando Servidor MCP de Gestión de Proyectos...")
    mcp.run(transport='stdio')