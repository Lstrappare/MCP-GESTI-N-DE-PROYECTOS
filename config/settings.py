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
# PALETA WORD — COLORES CORPORATIVOS
# ==============================================================================

_COLOR_PRIMARIO = RGBColor(0x1B, 0x3A, 0x5C)       # Azul oscuro corporativo
_COLOR_SECUNDARIO = RGBColor(0x2E, 0x86, 0xC1)      # Azul medio
_COLOR_ACENTO = RGBColor(0x17, 0xA5, 0x89)           # Verde-azul
_COLOR_TEXTO = RGBColor(0x2C, 0x3E, 0x50)            # Gris oscuro
_COLOR_GRIS_CLARO = RGBColor(0xEC, 0xF0, 0xF1)       # Fondo gris claro
_COLOR_BLANCO = RGBColor(0xFF, 0xFF, 0xFF)

# Colores de fondo para cada etapa (hex sin #)
_COLORES_ETAPA = [
    "D4EDDA",  # Verde claro — Inicio
    "CCE5FF",  # Azul claro — Planeación
    "FFF3CD",  # Amarillo claro — Ejecución
    "F8D7DA",  # Rojo claro — Control
    "E2E3E5",  # Gris claro — Cierre
]

# Colores de fondo para subtareas base (nivel 2)
_COLOR_SUBTAREA_BASE = "F0F4F8"

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
