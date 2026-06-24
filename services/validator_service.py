from __future__ import annotations

from typing import List, Optional
from pydantic import BaseModel, Field

from models import DocumentoEDTInput


# ==============================================================================
# MODELO DE RESULTADO DE VALIDACIÓN
# ==============================================================================

class ResultadoValidacion(BaseModel):
    es_valido: bool = False
    campos_faltantes: List[str] = []
    campos_completos: List[str] = []
    sugerencia: str = ""


# ==============================================================================
# VALIDADOR CENTRAL
# ==============================================================================

def validar_datos_proyecto(datos: DocumentoEDTInput) -> ResultadoValidacion:
    """
    Valida que todos los campos requeridos estén presentes y completos.
    
    Verifica:
    - Información general (nombre_proyecto, id_proyecto).
    - Información financiera (presupuesto_fase, presupuesto_proyecto).
    - EDT (fases con tareas).
    - Minuta de validación (mínimo 3 actividades con todos sus campos).
    - Conclusión personalizada.
    """
    faltantes: list[str] = []
    completos: list[str] = []

    # ── Información General ──
    if not datos.nombre_proyecto or datos.nombre_proyecto.strip() in ("",):
        faltantes.append("Nombre del proyecto")
    else:
        completos.append("Nombre del proyecto")

    if not datos.id_proyecto or datos.id_proyecto.strip() in ("", "N/A"):
        faltantes.append("ID del proyecto")
    else:
        completos.append("ID del proyecto")

    # ── Información Financiera ──
    if not datos.presupuesto_fase or datos.presupuesto_fase.strip() in ("", "N/A"):
        faltantes.append("Presupuesto de la fase")
    else:
        completos.append("Presupuesto de la fase")

    if not datos.presupuesto_proyecto or datos.presupuesto_proyecto.strip() in ("", "N/A"):
        faltantes.append("Presupuesto total del proyecto")
    else:
        completos.append("Presupuesto total del proyecto")

    # ── EDT — al menos una fase con al menos una tarea ──
    tiene_fases = bool(datos.fases)
    tiene_tareas = False
    if tiene_fases:
        for fase in datos.fases:
            if fase.tareas:
                tiene_tareas = True
                break

    if not tiene_fases or not tiene_tareas:
        faltantes.append("Actividades de la EDT (fases con tareas)")
    else:
        completos.append("Actividades de la EDT")

    # ── Minuta de Validación ──
    num_actividades = len(datos.actividades_minuta)
    if num_actividades < 3:
        faltantes.append(
            f"Actividades de validación (mínimo 3 requeridas, actual: {num_actividades})"
        )
    else:
        act_ok = True
        for i, act in enumerate(datos.actividades_minuta):
            prefijo = f"Actividad de validación #{i + 1}"
            if not act.actividad or act.actividad.strip() in ("", "N/A"):
                faltantes.append(f"{prefijo}: nombre/descripción")
                act_ok = False
            if not act.tiempo or act.tiempo.strip() in ("", "N/A"):
                faltantes.append(f"{prefijo}: tiempo estimado")
                act_ok = False
            if not act.recursos or act.recursos.strip() in ("", "N/A"):
                faltantes.append(f"{prefijo}: recursos necesarios")
                act_ok = False
            if not act.responsable or act.responsable.strip() in ("", "N/A"):
                faltantes.append(f"{prefijo}: responsable")
                act_ok = False
        if act_ok:
            completos.append("Actividades de validación (completas)")

    # ── Conclusión ──
    conclusion_default = (
        "La estructura de desglose del trabajo queda validada por los responsables "
        "del proyecto, conforme a los criterios técnicos, financieros y metodológicos "
        "establecidos."
    )
    if not datos.conclusion_minuta or datos.conclusion_minuta.strip() == conclusion_default.strip():
        faltantes.append("Conclusión personalizada sobre la alineación del proyecto")
    else:
        completos.append("Conclusión sobre la alineación del proyecto")

    es_valido = len(faltantes) == 0

    sugerencia = formatear_faltantes(faltantes) if not es_valido else (
        "Todos los datos requeridos están completos. Puede proceder con la generación del documento."
    )

    return ResultadoValidacion(
        es_valido=es_valido,
        campos_faltantes=faltantes,
        campos_completos=completos,
        sugerencia=sugerencia,
    )


# ==============================================================================
# FORMATEO DE MENSAJE PARA EL USUARIO
# ==============================================================================

def formatear_faltantes(faltantes: list[str]) -> str:
    """Formatea la lista de campos faltantes en un mensaje claro y agrupado."""
    if not faltantes:
        return ""

    lineas = [
        "⚠️  DATOS INCOMPLETOS — No se puede generar el documento aún.",
        "",
        "Antes de continuar necesito la siguiente información:",
        "",
    ]
    for i, campo in enumerate(faltantes, start=1):
        lineas.append(f"  {i}. {campo}")

    lineas.append("")
    lineas.append("Cuando me proporciones esta información podré continuar con la generación.")
    return "\n".join(lineas)
