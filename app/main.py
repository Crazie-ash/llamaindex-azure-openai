from fastapi import FastAPI

from app.routers import router
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi import HTTPException

from app.services.azure_service import get_azure_embedding, get_azure_openai
from app.services.elasticsearch_service import get_elasticSearch

app = FastAPI()

get_azure_openai()
get_azure_embedding()
get_elasticSearch()

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"status": False, "message": exc.detail, "data": None},
    )

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
