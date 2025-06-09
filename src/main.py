from src.app.service import RestService
from src.app.config import settings


app = RestService(config=settings).create_application()
