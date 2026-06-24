import base64
import httpx
from datetime import datetime
from pathlib import Path

from models import EDTInput
from config.settings import (
    MERMAID_COLORES_FASE,
    MERMAID_BORDES_FASE,
    MERMAID_ESTILO_ROOT,
    MERMAID_ESTILO_FASE_TEMPLATE,
    KROKI_MERMAID_PNG_URL,
    MERMAID_INK_IMG_URL_TEMPLATE,
    _PREFIJO_ARCHIVO,
    _CARPETA_DOWNLOADS,
)


# ==============================================================================
# FUNCIÓN AUXILIAR RECURSIVA
# ==============================================================================

def _agregar_nodos(tarea, parent_id: str, node_id: str, lines: list[str]) -> None:
    """Añade la arista parent→nodo y desciende recursivamente."""
    lines.append(f'    {parent_id} --> {node_id}["{tarea.nombre}"]')

    if tarea.subtareas:
        for idx, subtarea in enumerate(tarea.subtareas):
            child_id = f"{node_id}_{idx}"
            _agregar_nodos(subtarea, node_id, child_id, lines)


# ==============================================================================
# CONSTRUCCIÓN MERMAID
# ==============================================================================

def construir_mermaid(datos: EDTInput) -> str:
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
    lines.append(f"    style Root {MERMAID_ESTILO_ROOT}")

    for i in range(len(datos.fases)):
        color_fondo = MERMAID_COLORES_FASE[i % len(MERMAID_COLORES_FASE)]
        color_borde = MERMAID_BORDES_FASE[i % len(MERMAID_BORDES_FASE)]
        lines.append(
            f"    style F{i} {MERMAID_ESTILO_FASE_TEMPLATE.format(fondo=color_fondo, borde=color_borde)}"
        )

    return "\n".join(lines)


# ==============================================================================
# RENDERIZADO DE PNG
# ==============================================================================

def renderizar_mermaid_png(mermaid_code: str) -> bytes:
    """Renderiza código Mermaid como PNG usando Kroki, con fallback a mermaid.ink."""
    payload = {"diagram": mermaid_code}
    try:
        response = httpx.post(KROKI_MERMAID_PNG_URL, json=payload, timeout=30, follow_redirects=True)
        response.raise_for_status()
        return response.content
    except Exception:
        encoded = base64.urlsafe_b64encode(mermaid_code.encode("utf-8")).decode("utf-8")
        url_mermaid = MERMAID_INK_IMG_URL_TEMPLATE.format(encoded=encoded)
        response = httpx.get(url_mermaid, timeout=30, follow_redirects=True)
        response.raise_for_status()
        return response.content


def exportar_edt_png(datos: EDTInput) -> bytes:
    """Construye Mermaid y renderiza a PNG."""
    mermaid_code = construir_mermaid(datos)
    return renderizar_mermaid_png(mermaid_code)


def guardar_png_edt(datos: EDTInput, image_bytes: bytes) -> Path:
    """Guarda la imagen PNG del EDT en ~/Downloads/."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_seguro = datos.nombre_proyecto.replace(" ", "_").replace("/", "-")
    nombre_archivo = f"{_PREFIJO_ARCHIVO}_{nombre_seguro}_{timestamp}.png"
    ruta = _CARPETA_DOWNLOADS / nombre_archivo
    ruta.write_bytes(image_bytes)
    return ruta


def generar_imagen_mermaid_para_docx(datos: EDTInput) -> bytes:
    """Genera la imagen PNG del diagrama EDT usando mermaid.ink (sin Kroki)."""
    mermaid_code = construir_mermaid(datos)
    encoded = base64.urlsafe_b64encode(mermaid_code.encode("utf-8")).decode("utf-8")
    url_imagen = MERMAID_INK_IMG_URL_TEMPLATE.format(encoded=encoded)
    response = httpx.get(url_imagen, timeout=30, follow_redirects=True)
    response.raise_for_status()
    return response.content
