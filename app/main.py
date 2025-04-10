from fastapi import FastAPI, HTTPException
from app.routes import users, categories, events, followers, ratings, reservations, tickets, auth
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Gestión de Eventos")

# Habilitar CORS en FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Manejador de excepciones generales (errores internos)
@app.exception_handler(Exception)
async def general_exception_handler(request, exc: Exception):
    # Aquí puedes capturar más detalles del error
    return JSONResponse(
        status_code=500,
        content={
            "message": str(exc),  # Mensaje del error
        }
    )

@app.get("/")
def read_root():
    return {"message": "Hello, this is EventMix Api!"}

# Registrar las rutas de usuarios
app.include_router(users.router)
app.include_router(categories.router)
app.include_router(events.router)
app.include_router(followers.router)
app.include_router(ratings.router)
app.include_router(reservations.router)
app.include_router(tickets.router)
app.include_router(auth.router)