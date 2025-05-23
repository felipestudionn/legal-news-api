from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any
from .scraper import NewsScraper
import logging

# Configuración del logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicialización de la app
app = FastAPI(
    title="Telecom News API",
    description="API para obtener noticias de tecnología y telecomunicaciones",
    version="1.0.0"
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todas las origins en desarrollo
    allow_credentials=False,  # Importante: debe ser False cuando allow_origins=["*"]
    allow_methods=["GET"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600
)

# Instancia del scraper
scraper = NewsScraper()

@app.get("/")
async def read_root():
    """
    Endpoint raíz que proporciona información básica sobre la API
    """
    return {
        "message": "Bienvenido a la API de Noticias de Tecnología y Telecomunicaciones",
        "version": "1.0.0",
        "endpoints": {
            "/news": "Obtener todas las noticias",
            "/news/sources": "Listar fuentes disponibles"
        }
    }

@app.get("/news")
async def get_news(date: str = None) -> Dict[str, Any]:
    """
    Endpoint principal que devuelve noticias de todas las fuentes
    """
    try:
        news = await scraper.get_all_news(date)
        return {
            "status": "success",
            "count": len(news),
            "news": news
        }
    except Exception as e:
        logger.error(f"Error obteniendo noticias: {str(e)}")
        raise HTTPException(status_code=500, detail="Error obteniendo noticias")

@app.get("/news/sources")
async def get_sources() -> Dict[str, List[str]]:
    """
    Endpoint que lista las fuentes de noticias disponibles
    """
    return {
        "sources": ["El Español", "Expansión", "El Economista"]
    }

@app.get("/news/dates")
async def get_available_dates() -> Dict[str, List[str]]:
    """
    Endpoint que lista las fechas disponibles en el histórico
    """
    dates = scraper.list_available_dates()
    return {
        "dates": dates
    }
