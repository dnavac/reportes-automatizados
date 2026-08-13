import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from scripts.generar_reporte import generar_reporte
from scripts.generar_datos import generar_datos_supabase, generar_datos_sqlite, SUPABASE_URL, SUPABASE_KEY

app = FastAPI(
    title="Servicio de Reportes Inmobiliarios",
    description="API REST para la generación automatizada de reportes PDF inmobiliarios",
    version="1.0.0"
)

@app.get("/")
def home():
    return {
        "service": "Reportes Inmobiliarios API",
        "status": "online",
        "endpoints": {
            "health": "/health",
            "generar_reporte": "POST /generar-reporte",
            "generar_datos": "POST /generar-datos"
        }
    }

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/generar-reporte")
def api_generar_reporte():
    try:
        generar_reporte()
        pdf_path = os.path.join(os.path.dirname(__file__), 'examples', 'reporte_ejemplo.pdf')
        
        if not os.path.exists(pdf_path):
            raise HTTPException(status_code=500, detail="El archivo PDF no fue generado correctamente.")
            
        return FileResponse(
            path=pdf_path,
            filename="reporte_inmobiliario.pdf",
            media_type="application/pdf"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generar-datos")
def api_generar_datos():
    try:
        if SUPABASE_URL and SUPABASE_KEY:
            generar_datos_supabase()
            mode = "Supabase"
        else:
            generar_datos_sqlite()
            mode = "SQLite local"
        return {"status": "success", "message": f"Datos de prueba generados exitosamente en {mode}."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
