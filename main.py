import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from elastic_search.index_manager import create_all_indices
from events import Receive
from api.router import api_router  # Asegúrate de importar tu router

# Configurar logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')

# Crear indices para Elasticsearch
create_all_indices()

# Inicializar FastAPI
app = FastAPI()

@app.on_event("startup")
async def startup_event():
    import threading
    threading.Thread(target=Receive, daemon=True).start()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_origin_regex=r"https://.*\.ngrok-free\.app",
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"]
)

# Incluir routers
app.include_router(api_router, prefix="/api")