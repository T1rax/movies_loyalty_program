import uvicorn
from api.endpoints.adminsite import site
from fastapi import FastAPI
from settings import logger, settings


app = FastAPI()

# Mount the background management system
site.mount_app(app)

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host=settings.app.host,
        port=settings.app.port,
        log_config=logger.LOGGING,
        reload=True,
    )
