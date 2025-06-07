from src.application.service import RestService
from src.application.config import settings


app = RestService(config=settings).create_application()
