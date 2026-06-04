from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field
from typing import List

mcp = FastMCP("MCP-GestionProyectos")

# ==========================================
# TAREA IN-44 (MIGUEL): ESQUEMA JSON (PYDANTIC)
# ==========================================
# Miguel: Pydantic es la mejor forma de obligar a la IA a seguir una estructura.
# Modifica estas clases si necesitas más datos del documento.
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

# ==========================================
# TAREAS IN-45 (ROGELIO) e IN-46 (LEO)
# ==========================================
@mcp.tool()
def generar_edt(datos: EstructuraEDT) -> str:
    """
    Genera la estructura de desglose del trabajo (EDT) en formato Mermaid.js a partir de los datos del proyecto.
    """
    # IN-46 LEO: Validación estructural y manejo de excepciones
    try:
        if not datos.fases:
            raise ValueError("El JSON no contiene fases definidas. Revisa la extracción del PDF.")

        # IN-45 ROGELIO: Lógica de construcción del diagrama Mermaid
        mermaid_code = "```mermaid\ngraph TD;\n"
        mermaid_code += f"    Root[{datos.proyecto}]\n"
        
        for i, fase in enumerate(datos.fases):
            fase_id = f"F{i}"
            mermaid_code += f"    Root --> {fase_id}[{fase.nombre}]\n"
            
            if not fase.tareas:
                raise ValueError(f"La fase '{fase.nombre}' vino sin tareas asignadas.")
                
            for j, tarea in enumerate(fase.tareas):
                tarea_id = f"T{i}_{j}"
                mermaid_code += f"    {fase_id} --> {tarea_id}[{tarea.nombre} - {tarea.responsable}]\n"
        
        mermaid_code += "
```"
        return mermaid_code

    except Exception as e:
        # LEO: Este return es vital. Si falla, el Agente IA leerá este texto y corregirá su propio JSON.
        return f"Error de validación: {str(e)}. Corrige los parámetros y vuelve a ejecutar la herramienta."

if __name__ == "__main__":
    print("Iniciando Servidor MCP de Gestión de Proyectos...")
    mcp.run(transport='stdio')