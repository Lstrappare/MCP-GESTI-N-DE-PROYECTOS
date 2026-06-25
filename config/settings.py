from pathlib import Path
from docx.shared import RGBColor

# ==============================================================================
# PALETA MERMAID — COLORES DE FASE Y BORDES
# ==============================================================================

MERMAID_COLORES_FASE = ["#d4edda", "#cce5ff", "#fff3cd", "#f8d7da", "#e2e3e5"]
MERMAID_BORDES_FASE = ["#28a745", "#007bff", "#ffc107", "#dc3545", "#6c757d"]

MERMAID_ESTILO_ROOT = "fill:#f8f9fa,stroke:#343a40,stroke-width:3px"
MERMAID_ESTILO_FASE_TEMPLATE = "fill:{fondo},stroke:{borde},stroke-width:2px"

# ==============================================================================
# PALETA WORD — COLORES CORPORATIVOS AZUL
# ==============================================================================

_COLOR_PRIMARIO = RGBColor(0x0D, 0x2B, 0x4E)       # Azul marino profundo
_COLOR_SECUNDARIO = RGBColor(0x1A, 0x5C, 0xA8)      # Azul medio
_COLOR_ACENTO = RGBColor(0x25, 0x80, 0xD0)           # Azul brillante
_COLOR_TEXTO = RGBColor(0x1A, 0x2A, 0x3A)            # Azul muy oscuro (texto)
_COLOR_GRIS_CLARO = RGBColor(0xE8, 0xEE, 0xF4)       # Gris azulado claro (fondos)
_COLOR_BLANCO = RGBColor(0xFF, 0xFF, 0xFF)

# Colores de fondo para cada etapa (hex sin #)
_COLORES_ETAPA = [
    "D6EAF8",  # Azul muy claro — Inicio
    "AED6F1",  # Azul claro — Planeación
    "85C1E9",  # Azul medio — Ejecución
    "5DADE2",  # Azul medio-fuerte — Control
    "3498DB",  # Azul fuerte — Cierre
]

# Colores de fondo para subtareas base (nivel 2)
_COLOR_SUBTAREA_BASE = "EBF5FB"

# ==============================================================================
# URLs EXTERNAS — RENDERIZADO MERMAID
# ==============================================================================

KROKI_MERMAID_PNG_URL = "https://kroki.io/mermaid/png"
MERMAID_INK_IMG_URL_TEMPLATE = "https://mermaid.ink/img/{encoded}?bgColor=white"

# ==============================================================================
# CONFIGURACIÓN DE SALIDA
# ==============================================================================

_PREFIJO_ARCHIVO = "EDT"
_CARPETA_DOWNLOADS = Path.home() / "Downloads"
