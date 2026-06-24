# ==============================================================================
# Archivo: main.py
# Autores:
#- Cisneros Valero José Manuel -
#- García Vázquez Rogelio -
#- Gonzales Velázquez Josué - 
#- Flores Jasso Miguel Angel -
#- Martínez Nicolas Francisco Leonardo -
#- Parra Mendoza Ernesto Zuriel –
#
#
# Descripción:
#   Este programa implementa un servidor robusto bajo el estándar Model Context 
#   Protocol (MCP) utilizando el framework FastMCP. Su objetivo principal es actuar 
#   como un puente inteligente para que Modelos de Lenguaje (LLMs) procesen, 
#   autoricen y sistematicen información de proyectos a través de tres componentes:
#     1. Generación de diagramas jerárquicos EDT empleando sintaxis Mermaid.
#     2. Renderizado remoto y exportación automática de diagramas visuales en PNG.
#     3. Creación automatizada de documentación corporativa en formato Word (.docx),
#        incluyendo esquemas visuales, tablas de codificación y minutas de validación.
#
#   Diseñado con un enfoque de recursividad ilimitada para estructuras de tareas anidadas.
#
# ==============================================================================

from mcp.server.fastmcp import FastMCP, Image

from models import EDTInput, DocumentoEDTInput
from services.mermaid_service import (
    construir_mermaid,
    renderizar_mermaid_png,
    guardar_png_edt,
)
from services.docx_service import generar_documento_word
from services.validator_service import validar_datos_proyecto as _validar_datos_proyecto

mcp = FastMCP("MCP-GestionProyectos")


# ==============================================================================
# HERRAMIENTAS MCP
# ==============================================================================

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
        return construir_mermaid(datos)
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

    Usa la API pública kroki.io (POST) para renderizar sin límite de URL,
    con fallback a mermaid.ink (GET) si kroki falla.

    CUÁNDO USAR ESTA HERRAMIENTA:
    - Cuando el usuario pida la imagen, el PNG, ver el diagrama o descargarlo.
    - Aplica las mismas reglas de estructura que generar_edt.

    ESTRUCTURA METODOLÓGICA FIJA — 5 ETAPAS OBLIGATORIAS:
    1. Etapa 0 (Inicio): Planeación Estratégica, Análisis del Entorno y Mercado,
       Estudio de Factibilidad, Definición de la Solución Tecnológica, Gestión Inicial del Proyecto.
    2. Etapa 1 (Planeación): Integración del Proyecto, Gestión de Interesados,
       Gestión del Alcance, Gestión de Requisitos.
    3. Etapa 2 (Ejecución): Tecnológica, Operativa, Recursos Humanos, Finanzas, Comercial.
    4. Etapa 3 (Control): Checklist (con hija 'Checklist de los 21 programas'),
       Control y seguimiento, Control de cambios.
    5. Etapa 4 (Cierre): Plantilla de resultados, Acta de cierre.

    Las tareas del proyecto deben anidarse como subtareas de nivel 3 o inferior
    dentro de esta estructura fija.

    REQUISITO DE NODOS:
    - Para garantizar una imagen legible y sin errores, se recomienda que el
      diagrama tenga exactamente 90 nodos (5 fases + 85 tareas).
    - El JSON debe estructurarse en 5 fases, cada una con una cadena vertical
      de 17 tareas anidadas secuencialmente (una subtarea por nodo).
    - Ejemplo: 5 fases × 17 tareas = 85 tareas + 5 fases = 90 nodos.
    """
    # 1. Construir el código Mermaid
    mermaid_code = construir_mermaid(datos)

    # 2. Renderizar PNG (Kroki → fallback a mermaid.ink)
    image_bytes = renderizar_mermaid_png(mermaid_code)

    # 3. Guardar en ~/Downloads/
    guardar_png_edt(datos, image_bytes)

    # 4. Devolver objeto Image
    return Image(data=image_bytes, format="png")


@mcp.tool()
def generar_documento_proyecto_word(datos: DocumentoEDTInput) -> str:
    """
    Genera un documento corporativo .docx con la EDT completa del proyecto.

    El documento incluye tres secciones:
    1. DIAGRAMA EDT — Imagen PNG del diagrama visual generada vía mermaid.ink.
    2. TABLA BASE DE LA EDT — Tabla jerárquica con Código EDT, Nombre, Descripción
       Operativa e Hito para cada tarea.
    3. MINUTA DE VALIDACIÓN — Datos del proyecto y campos de firma para validación.

    INSTRUCCIONES PARA EL LLM:
    - Lee todos los archivos .txt del usuario y extrae: nombre del proyecto,
      ID del proyecto, presupuesto total, y todas las tareas/actividades.
    - Clasifica TODAS las tareas dentro de la Estructura Metodológica Fija de 5 etapas.
    - Para cada tarea, proporciona: descripcion_operativa (breve descripción) y
      hito (ej. "Hito 1", "N/A").
    - Las tareas del proyecto deben anidarse en nivel 3 o inferior.
    - El archivo .docx se guarda automáticamente en ~/Downloads/.

    REGLAS ESTRICTAS PARA EL LLM:
    - NUNCA inventes datos. Si el usuario no proporcionó un campo, déjalo vacío.
    - NUNCA asumas presupuestos, responsables, tiempos ni actividades.
    - Antes de invocar esta herramienta, usa validar_datos_proyecto para verificar
      que todos los datos requeridos están completos.
    - Si validar_datos_proyecto reporta campos faltantes, solicítaselos al usuario
      ANTES de llamar a esta herramienta.
    """
    resultado = _validar_datos_proyecto(datos)
    if not resultado.es_valido:
        return resultado.sugerencia

    return generar_documento_word(datos)


@mcp.tool()
def validar_datos_proyecto(datos: DocumentoEDTInput) -> str:
    """
    Verifica que todos los datos requeridos para generar el documento Word estén
    completos. Devuelve un resumen claro de qué campos están listos y cuáles faltan.

    USA ESTA HERRAMIENTA ANTES de llamar a generar_documento_proyecto_word.

    CAMPOS OBLIGATORIOS QUE VERIFICA:
    1. Información General: nombre del proyecto, ID del proyecto.
    2. Información Financiera: presupuesto de la fase, presupuesto total del proyecto.
    3. EDT: fases con al menos una tarea cada una.
    4. Minuta de Validación: mínimo 3 actividades, cada una con nombre, tiempo,
       recursos y responsable.
    5. Conclusión personalizada sobre la alineación del proyecto.

    Si hay campos faltantes, la herramienta los lista agrupados para que el LLM
    se los solicite al usuario de forma clara.
    """
    resultado = _validar_datos_proyecto(datos)

    if resultado.es_valido:
        return (
            "✅ Validación exitosa. Todos los datos requeridos están completos.\n\n"
            + "Puede proceder con generar_documento_proyecto_word."
        )

    lineas = [resultado.sugerencia, ""]
    if resultado.campos_completos:
        lineas.append("📋 Campos ya completos:")
        for campo in resultado.campos_completos:
            lineas.append(f"  ✅ {campo}")

    return "\n".join(lineas)


if __name__ == "__main__":
    print("Iniciando Servidor MCP de Gestión de Proyectos...")
    mcp.run(transport='stdio')
