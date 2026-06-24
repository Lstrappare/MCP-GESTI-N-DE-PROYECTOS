from __future__ import annotations

from pydantic import BaseModel, Field
from typing import List, Optional


# ==============================================================================
# MODELOS PYDANTIC UNIFICADOS — ESTRUCTURA RECURSIVA
# ==============================================================================

class TareaBase(BaseModel):
    nombre: str = Field(..., min_length=1)
    descripcion_operativa: Optional[str] = "N/A"
    hito: Optional[str] = "N/A"
    subtareas: Optional[List[TareaBase]] = []


# Necesario para que Pydantic resuelva la auto-referencia después de la definición.
TareaBase.model_rebuild()


class FaseBase(BaseModel):
    nombre: str = Field(..., min_length=1)
    tareas: List[TareaBase] = []


class EDTInput(BaseModel):
    nombre_proyecto: str = Field(..., min_length=1, description="El nombre oficial del proyecto.")
    fases: List[FaseBase] = Field(
        ...,
        description="""
        REGLA ESTRICTA PARA LA IA:
        1. Debes generar exactamente las etapas principales indicadas en los documentos fuente (ej. Inicio, Planeación, Ejecución, Control, Cierre).
        2. El anidamiento dentro de cada etapa debe ser COMPLETAMENTE VERTICAL Y LINEAL.
        3. Cada tarea padre debe tener un máximo de UNA (1) subtarea.
        4. Crea una cadena en cascada perfecta hacia abajo. ¡PROHIBIDO agrupar elementos horizontalmente!
        """
    )


class ActividadMinuta(BaseModel):
    actividad: str = Field(..., min_length=1, description="Nombre de la actividad de la minuta.")
    tiempo: str = Field(..., min_length=1, description="Tiempo estimado para la actividad.")
    recursos: str = Field(..., min_length=1, description="Recursos necesarios para la actividad.")
    responsable: str = Field(..., min_length=1, description="Responsable de la actividad.")


class DocumentoEDTInput(EDTInput):
    id_proyecto: Optional[str] = Field("N/A", description="Identificador único del proyecto.")
    nombre_empresa: Optional[str] = Field("MINTRANET", description="Nombre de la empresa.")
    presupuesto_fase: Optional[str] = Field("N/A", description="Presupuesto asignado a la fase.")
    presupuesto_proyecto: Optional[str] = Field("N/A", description="Presupuesto total del proyecto.")
    presupuesto_total: Optional[str] = Field("N/A", description="Presupuesto total del proyecto.")
    fecha_generacion: Optional[str] = Field(
        None,
        description="Fecha de generación del documento. Se auto-genera si no se proporciona.",
    )
    actividades_minuta: List[ActividadMinuta] = []
    conclusion_minuta: Optional[str] = Field(
        "La estructura de desglose del trabajo queda validada por los responsables del proyecto, "
        "conforme a los criterios técnicos, financieros y metodológicos establecidos.",
        description="Conclusión de la minuta de validación.",
    )
    fases: List[FaseBase] = Field(
        ...,
        description="""
        ESTRUCTURA METODOLÓGICA FIJA — 5 ETAPAS OBLIGATORIAS:
        1. Etapa 0 (Inicio): Planeación Estratégica, Análisis del Entorno y Mercado,
           Estudio de Factibilidad, Definición de la Solución Tecnológica, Gestión Inicial del Proyecto.
        2. Etapa 1 (Planeación): Integración del Proyecto, Gestión de Interesados,
           Gestión del Alcance, Gestión de Requisitos.
        3. Etapa 2 (Ejecución): Tecnológica, Operativa, Recursos Humanos, Finanzas, Comercial.
        4. Etapa 3 (Control): Checklist (con hija 'Checklist de los 21 programas'),
           Control y seguimiento, Control de cambios.
        5. Etapa 4 (Cierre): Plantilla de resultados, Acta de cierre.

        Las tareas del proyecto deben anidarse en nivel 3 o inferior dentro de esta estructura.
        """,
    )


# ==============================================================================
# ALIAS SEMÁNTICOS — Compatibilidad con nombres originales
# ==============================================================================

Tarea = TareaBase
TareaEDT = TareaBase
Fase = FaseBase
FaseEDT = FaseBase
