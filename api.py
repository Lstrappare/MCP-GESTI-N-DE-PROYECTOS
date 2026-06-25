# api.py
# Servidor HTTP que expone las funcionalidades del MCP a través de una API REST
# y sirve una interfaz web para uso humano.

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import base64
from io import BytesIO
from pathlib import Path
import re

# Importamos los modelos y servicios del MCP
from models import EDTInput, DocumentoEDTInput
from services.mermaid_service import construir_mermaid, renderizar_mermaid_png
from services.docx_service import generar_documento_word
from services.validator_service import validar_datos_proyecto

app = FastAPI(title="API EDT - Gestión de Proyectos", version="1.0")

# Servir archivos estáticos (frontend)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Modelo de respuesta para imagen en base64
class ImagenResponse(BaseModel):
    imagen_base64: str
    mensaje: str

# ------------------- ENDPOINTS -------------------

@app.post("/api/edt/mermaid")
def get_mermaid(datos: EDTInput):
    """
    Genera el código Mermaid del EDT.
    """
    try:
        codigo = construir_mermaid(datos)
        return {"mermaid": codigo}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/edt/imagen", response_model=ImagenResponse)
def get_imagen(datos: EDTInput):
    """
    Genera la imagen PNG del diagrama y la devuelve en base64.
    """
    try:
        mermaid_code = construir_mermaid(datos)
        image_bytes = renderizar_mermaid_png(mermaid_code)
        b64 = base64.b64encode(image_bytes).decode("utf-8")
        return ImagenResponse(imagen_base64=b64, mensaje="Imagen generada correctamente")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/edt/validar")
def validar(datos: DocumentoEDTInput):
    """
    Valida los datos del proyecto antes de generar el documento Word.
    """
    try:
        resultado = validar_datos_proyecto(datos)
        return {
            "es_valido": resultado.es_valido,
            "mensaje": resultado.sugerencia,
            "faltantes": resultado.campos_faltantes,
            "completos": resultado.campos_completos,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/edt/documento")
def get_documento(datos: DocumentoEDTInput):
    """
    Genera el documento Word y lo devuelve como archivo descargable.
    """
    try:
        # La función generar_documento_word guarda en ~/Downloads y devuelve mensaje con ruta
        mensaje = generar_documento_word(datos)
        # Extraemos la ruta del mensaje
        match = re.search(r"📁 Ruta: (.*?)(?:\n|$)", mensaje)
        if not match:
            raise HTTPException(status_code=500, detail="No se pudo obtener la ruta del archivo")
        ruta = Path(match.group(1))
        if not ruta.exists():
            raise HTTPException(status_code=404, detail="El archivo no se generó correctamente")
        # Leer el archivo y devolverlo
        with open(ruta, "rb") as f:
            contenido = f.read()
        # (Opcional) Borrar el archivo después de enviarlo
        # ruta.unlink()
        return StreamingResponse(
            BytesIO(contenido),
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={"Content-Disposition": f"attachment; filename={ruta.name}"}
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/")
def root():
    """Redirige al frontend."""
    return RedirectResponse(url="/static/index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)