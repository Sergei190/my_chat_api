from fastapi import FastAPI
from app.api.v1.router import v1_router

# ВКЛЮЧАЕМ DEBUG
app = FastAPI(title="Chat API", version="1.0.0", debug=True)

app.include_router(v1_router, prefix="/v1")

@app.get("/")
async def root():
    return {"message": "Welcome to Chat API"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}