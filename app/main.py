from fastapi import FastAPI
from routers import properties,search, user

app = FastAPI()
app.include_router(properties.router, prefix="/api/v1", tags=["Properties"])
app.include_router(search.router, prefix="/api/v1", tags=["Search"])
app.include_router(user.router, prefix="/api/v1", tags=["User"])