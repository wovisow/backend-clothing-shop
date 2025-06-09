from pydantic import BaseModel


class MonitoringSchema(BaseModel):
    health: bool
