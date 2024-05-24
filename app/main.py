from fastapi import FastAPI

from app.routers import router
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi import HTTPException
import signal
import sys
from multiprocessing import Process, current_process
import time

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

def handle_sigint(signum, frame):
    print(f"Signal handler called with signal {signum}")
    print("Cleaning up...")
    # Perform cleanup here
    sys.exit(0)  # Exit gracefully

def worker():
    try:
        while True:
            print(f"Working in process {current_process().name}")
            time.sleep(1)
    except KeyboardInterrupt:
        print("KeyboardInterrupt caught in worker")
    finally:
        print(f"Cleaning up the worker process {current_process().name}")

if __name__ == "__main__":
        # Set up signal handling
    signal.signal(signal.SIGINT, handle_sigint)

    # Create and start child processes
    processes = [Process(target=worker, name=f"Worker-{i}") for i in range(2)]
    for p in processes:
        p.start()

    try:
        for p in processes:
            p.join()
    except KeyboardInterrupt:
        print("KeyboardInterrupt caught in main process")
    finally:
        # Ensure all child processes are terminated before main process exits
        for p in processes:
            p.terminate()
            p.join()
        print("Cleaned up main process")

    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
