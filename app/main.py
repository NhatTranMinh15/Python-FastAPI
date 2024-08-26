from fastapi import FastAPI
from fastapi_pagination import add_pagination
from routers import user_router, company_router, task_router

app = FastAPI()

add_pagination(app)
app.include_router(user_router.router)
app.include_router(company_router.router)


@app.get("/")
async def main():
    return "Hello"
