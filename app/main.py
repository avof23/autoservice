"""
FastAPI module for execute function fastapi and connect routers
"""
from fastapi import FastAPI
from app.routers import parts, works, masters, clients, orders
app = FastAPI()

app.include_router(orders.router, prefix="/orders", tags=["orders"])
app.include_router(clients.router, prefix="/clients", tags=["clients"])
app.include_router(works.router, prefix="/works", tags=["works"])
app.include_router(parts.router, prefix="/parts", tags=["parts"])
app.include_router(masters.router, prefix="/masters", tags=["masters"])


@app.get("/")
async def root() -> dict:
    """
    Function return API name
    :return: dict include API name
    """
    return {"message": "API AutoService"}
