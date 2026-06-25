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

def _agregar_nodos(tarea, parent_id: str, node_id: str, lines: list[str], max_chars: int = 65) -> None:
    """Añade la arista parent→nodo y desciende recursivamente."""
    nombre = tarea.nombre
    if len(nombre) > max_chars:
        nombre = nombre[:max_chars].rsplit(" ", 1)[0] + "…"
    lines.append(f'    {parent_id} --> {node_id}["{nombre}"]')

    if tarea.subtareas:
        for idx, subtarea in enumerate(tarea.subtareas):
            child_id = f"{node_id}_{idx}"
            _agregar_nodos(subtarea, node_id, child_id, lines, max_chars)


# ==============================================================================
# CONSTRUCCIÓN MERMAID
# ==============================================================================

def _truncar(texto: str, max_chars: int = 70) -> str:
    """Trunca texto a max_chars, cortando en espacio."""
    if len(texto) <= max_chars:
        return texto
    return texto[:max_chars].rsplit(" ", 1)[0] + "…"


def construir_mermaid(datos: EDTInput) -> str:
    """Construye y retorna el código Mermaid completo del EDT."""
    if not datos.fases:
        raise ValueError(
            "El JSON no contiene fases definidas. "
            "Revisa la extracción de los datos."
        )

    root_name = _truncar(datos.nombre_proyecto, 60)
    lines: list[str] = [
        "graph TD",
        f'    Root["{root_name}"]',
    ]

    for i, fase in enumerate(datos.fases):
        fase_id = f"F{i}"
        fase_name = _truncar(fase.nombre, 50)
        lines.append(f'    Root --> {fase_id}["{fase_name}"]')

        if not fase.tareas:
            raise ValueError(
                f"La fase '{fase.nombre}' vino sin tareas asignadas."
            )

        for j, tarea in enumerate(fase.tareas):
            tarea_id = f"T{i}_{j}"
            _agregar_nodos(tarea, fase_id, tarea_id, lines)

    # Estilos de color automáticos 
    lines.append("\n    %% Estilos automáticos")
    lines.append(f"    style Root {MERMAID_ESTILO_ROOT}")

    for i in range(len(datos.fases)):
        color_fondo = MERMAID_COLORES_FASE[i % len(MERMAID_COLORES_FASE)]
        color_borde = MERMAID_BORDES_FASE[i % len(MERMAID_BORDES_FASE)]
        lines.append(
            f"    style F{i} {MERMAID_ESTILO_FASE_TEMPLATE.format(fondo=color_fondo, borde=color_borde)}"
        )

    return "\n".join(lines)


# ==============================================================================
# CONSTRUCCIÓN MERMAID POR FASES (CHUNKED)
# ==============================================================================

def construir_mermaid_fase(datos: EDTInput, fase_idx: int) -> str:
    """Construye el código Mermaid para una sola fase (con nodo raíz)."""
    if fase_idx < 0 or fase_idx >= len(datos.fases):
        raise ValueError(f"Índice de fase fuera de rango: {fase_idx}")
    fase = datos.fases[fase_idx]

    lines: list[str] = [
        "graph TD",
        f'    Root["{datos.nombre_proyecto}"]',
    ]

    fase_id = "F0"
    lines.append(f'    Root --> {fase_id}["{fase.nombre}"]')

    if not fase.tareas:
        raise ValueError(f"La fase '{fase.nombre}' vino sin tareas asignadas.")

    for j, tarea in enumerate(fase.tareas):
        tarea_id = f"T0_{j}"
        _agregar_nodos(tarea, fase_id, tarea_id, lines)

    # Estilo root + fase
    lines.append("\n    %% Estilos automáticos")
    lines.append(f"    style Root {MERMAID_ESTILO_ROOT}")
    color_fondo = MERMAID_COLORES_FASE[0]
    color_borde = MERMAID_BORDES_FASE[0]
    lines.append(
        f"    style F0 {MERMAID_ESTILO_FASE_TEMPLATE.format(fondo=color_fondo, borde=color_borde)}"
    )

    return "\n".join(lines)


def construir_mermaid_tarea(datos: EDTInput, fase_idx: int, tarea_idx: int) -> str:
    """Construye el código Mermaid para una sola tarea de una fase (con nodo raíz y fase)."""
    if fase_idx < 0 or fase_idx >= len(datos.fases):
        raise ValueError(f"Índice de fase fuera de rango: {fase_idx}")
    fase = datos.fases[fase_idx]
    if tarea_idx < 0 or tarea_idx >= len(fase.tareas):
        raise ValueError(f"Índice de tarea fuera de rango: {tarea_idx}")
    tarea = fase.tareas[tarea_idx]

    lines: list[str] = [
        "graph TD",
        f'    Root["{datos.nombre_proyecto}"]',
    ]
    lines.append(f'    Root --> F0["{fase.nombre}"]')

    tarea_id = "T0_0"
    _agregar_nodos(tarea, "F0", tarea_id, lines)

    lines.append("\n    %% Estilos automáticos")
    lines.append(f"    style Root {MERMAID_ESTILO_ROOT}")
    color_fondo = MERMAID_COLORES_FASE[0]
    color_borde = MERMAID_BORDES_FASE[0]
    lines.append(
        f"    style F0 {MERMAID_ESTILO_FASE_TEMPLATE.format(fondo=color_fondo, borde=color_borde)}"
    )

    return "\n".join(lines)


def _renderizar_una_imagen(mermaid_code: str) -> bytes | None:
    """Intenta renderizar un código Mermaid a PNG. Retorna None si falla."""
    # Kroki: POST con el código como texto plano
    try:
        response = httpx.post(
            KROKI_MERMAID_PNG_URL,
            content=mermaid_code.encode("utf-8"),
            headers={"Content-Type": "text/plain"},
            timeout=30,
            follow_redirects=True,
        )
        response.raise_for_status()
        return response.content
    except Exception:
        pass
    # Fallback: mermaid.ink (GET con base64 en URL)
    try:
        encoded = base64.urlsafe_b64encode(mermaid_code.encode("utf-8")).decode("utf-8")
        url_imagen = MERMAID_INK_IMG_URL_TEMPLATE.format(encoded=encoded)
        response = httpx.get(url_imagen, timeout=30, follow_redirects=True)
        response.raise_for_status()
        return response.content
    except Exception:
        return None


def construir_mermaid_chunked(datos: EDTInput) -> list[str]:
    """Devuelve una lista de códigos Mermaid, uno por cada fase."""
    return [construir_mermaid_fase(datos, i) for i in range(len(datos.fases))]


# ==============================================================================
# RENDERIZADO DE PNG
# ==============================================================================

def renderizar_mermaid_png(mermaid_code: str) -> bytes:
    """Renderiza código Mermaid como PNG usando Kroki, con fallback a mermaid.ink."""
    img = _renderizar_una_imagen(mermaid_code)
    if img:
        return img
    raise RuntimeError("No se pudo renderizar el diagrama Mermaid.")


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
    """Genera la imagen PNG del diagrama EDT usando Kroki, con fallback a mermaid.ink."""
    mermaid_code = construir_mermaid(datos)

    # Intentar primero con Kroki (POST, sin límite de URL)
    img = _renderizar_una_imagen(mermaid_code)
    if img:
        return img

    raise RuntimeError("No se pudo generar la imagen del diagrama EDT.")
