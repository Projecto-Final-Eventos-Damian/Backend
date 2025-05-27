from fastapi import FastAPI, HTTPException
from app.routes import users, categories, events, followers, ratings, reservations, tickets, ticketTypes, auth
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.auth.token_refresh import TokenRefreshMiddleware
import os

app = FastAPI(title="Gestión de Eventos")

app.add_middleware(TokenRefreshMiddleware)

# Habilitar CORS en FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["x-new-token"],
)

@app.exception_handler(Exception)
async def general_exception_handler(request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "message": str(exc),
        }
    )

@app.get("/")
def read_root():
    return {"message": "Hello, this is EventMix Api!"}

app.include_router(users.router)
app.include_router(categories.router)
app.include_router(events.router)
app.include_router(followers.router)
app.include_router(ratings.router)
app.include_router(reservations.router)
app.include_router(tickets.router)
app.include_router(ticketTypes.router)
app.include_router(auth.router)


app.mount("/public", StaticFiles(directory="public"), name="public")