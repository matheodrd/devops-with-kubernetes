from fastapi import FastAPI

app = FastAPI(title="Todo app", version="0.1.0")


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Hello from Todo app :)"}
