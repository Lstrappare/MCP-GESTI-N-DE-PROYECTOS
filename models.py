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
        REGLA ESTRICTA PARA LA IA — DIAGRAMA 100% VERTICAL:
        1. Debes generar exactamente 5 etapas. Todas las tareas deben anidarse en UNA SOLA COLUMNA VERTICAL por etapa.
        2. Cada tarea padre debe tener máximo UNA (1) subtarea. ¡PROHIBIDO poner más de un hijo por nodo!
        3. Encadena las tareas en cascada perfecta hacia abajo (formato 1, 1.1, 1.1.1, 1.1.1.1...).
        4. No agrupes tareas horizontalmente. Usa UN solo hijo por nivel.
        5. El diagrama debe verse como 5 columnas verticales independientes, una por cada etapa.

        ESTRUCTURA OBLIGATORIA DE 5 ETAPAS:
        1. ETAPA 1 (Inicio) → todas sus tareas hijas en cascada vertical (1.1 → 1.1.1 → 1.1.1.1...)
        2. ETAPA 2 (Planeación) → todas sus tareas hijas en cascada vertical (2.1 → 2.1.1 → 2.1.1.1...)
        3. ETAPA 3 (Ejecución) → 5 sub-áreas, cada una con sus tareas en cascada vertical independiente:
           3.1 ÁREA TECNOLÓGICO → (3.1.1 → 3.1.1.1...)
           3.2 ÁREA OPERATIVO → (3.2.1 → 3.2.1.1...)
           3.3 ÁREA RECURSOS HUMANOS → (3.3.1 → 3.3.1.1...)
           3.4 ÁREA FINANZAS → (3.4.1 → 3.4.1.1...)
           3.5 ÁREA COMERCIAL → (3.5.1 → 3.5.1.1...)
        4. ETAPA 4 (Control) → 3 tareas:
           4.1 Checklist → subtarea única: Checklist de los 21 programas, que contiene 21 subtareas en cascada vertical
           4.2 Control de seguimiento (sin hijos)
           4.3 Control de cambios (sin hijos)
        5. ETAPA 5 (Cierre) → todas sus tareas hijas en cascada vertical (5.1 → 5.1.1 → 5.1.1.1...)
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
        ESTRUCTURA METODOLÓGICA FIJA — 5 ETAPAS OBLIGATORIAS (DIAGRAMA 100% VERTICAL):

        REGLA DE VERTICALIDAD: cada tarea padre debe tener máximo UNA (1) subtarea.
        Encadena las tareas en cascada: 1 → 1.1 → 1.1.1 → 1.1.1.1...
        ¡PROHIBIDO poner más de un hijo por nodo!

        1. ETAPA 1 (Inicio):
           Planeación Estratégica, Análisis del Entorno y Mercado, Estudio de Factibilidad,
           Definición de la Solución Tecnológica, Gestión Inicial del Proyecto.
           → Todas sus tareas en cascada vertical (1.1 → 1.1.1 → 1.1.1.1...)

        2. ETAPA 2 (Planeación):
           Integración del Proyecto, Gestión de Interesados, Gestión del Alcance,
           Gestión de Requisitos.
           → Todas sus tareas en cascada vertical (2.1 → 2.1.1 → 2.1.1.1...)

        3. ETAPA 3 (Ejecución) — 5 sub-áreas, cada una en cascada vertical independiente:
           3.1 ÁREA TECNOLÓGICO → (3.1.1 → 3.1.1.1...)
           3.2 ÁREA OPERATIVO → (3.2.1 → 3.2.1.1...)
           3.3 ÁREA RECURSOS HUMANOS → (3.3.1 → 3.3.1.1...)
           3.4 ÁREA FINANZAS → (3.4.1 → 3.4.1.1...)
           3.5 ÁREA COMERCIAL → (3.5.1 → 3.5.1.1...)

        4. ETAPA 4 (Control) — 3 tareas:
           4.1 Checklist → contiene subtarea única "Checklist de los 21 programas"
               con 21 subtareas hijas en cascada vertical.
           4.2 Control de seguimiento (sin hijos, sin subtareas).
           4.3 Control de cambios (sin hijos, sin subtareas).

        5. ETAPA 5 (Cierre):
           Plantilla de resultados, Acta de cierre.
           → Todas sus tareas en cascada vertical (5.1 → 5.1.1 → 5.1.1.1...)

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
