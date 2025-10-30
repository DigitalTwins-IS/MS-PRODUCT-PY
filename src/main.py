"""
MS-PRODUCT-PY - Microservicio de Gestión de Productos
FastAPI Application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from src.routers import products_router
from .config import settings

# Crear aplicación FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="""
    Microservicio de gestión de productos para el Sistema Digital Twins.

    ## Funcionalidades

    * **Productos**: Registro, actualización, desactivación (soft delete)
    * **Filtrado por categoría**: Listar productos por categoría específica
    * **Health Check**: Verificación del estado de la base de datos y servicio

    ## Historias de Usuario Implementadas
    * **HU23**: Como administrador, quiero gestionar productos (crear, listar, actualizar y desactivar)
    """,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(
    products_router,
    prefix=settings.API_PREFIX,
    tags=["products"]
)


@app.get("/", include_in_schema=False)
async def root():
    """Redireccionar a la documentación"""
    return RedirectResponse(url="/docs")


@app.get("/health", tags=["Health"])
async def root_health():
    """Health check raíz"""
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION
    }


# Event handlers
@app.on_event("startup")
async def startup_event():
    """Evento de inicio de la aplicación"""
    print(f"🚀 {settings.APP_NAME} v{settings.APP_VERSION} iniciado")
    print(f"📚 Documentación: http://{settings.SERVICE_HOST}:{settings.SERVICE_PORT}/docs")
    print(f"🗂️ Prefijo API: {settings.API_PREFIX}")


@app.on_event("shutdown")
async def shutdown_event():
    """Evento de cierre de la aplicación"""
    print(f"🛑 {settings.APP_NAME} detenido")


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "src.main:app",
        host=settings.SERVICE_HOST,
        port=settings.SERVICE_PORT,
        reload=settings.DEBUG
    )

