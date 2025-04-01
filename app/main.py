from fastapi import FastAPI, HTTPException
from app.routes import users
from fastapi.responses import JSONResponse

app = FastAPI(title="Gestión de Eventos")

# Manejador de excepciones generales (errores internos)
@app.exception_handler(Exception)
async def general_exception_handler(request, exc: Exception):
    # Aquí puedes capturar más detalles del error, como el traceback
    return JSONResponse(
        status_code=500,
        content={
            "message": str(exc),  # Mensaje del error
        }
    )

# Registrar las rutas de usuarios
app.include_router(users.router, prefix="/users", tags=["users"])

@app.get("/")
def read_root():
    return {"message": "Hello, this is FastAPI!"}