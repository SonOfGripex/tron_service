from pydantic import BaseModel
from datetime import datetime

class AddressRequest(BaseModel):
    address: str

class AddressResponse(BaseModel):
    address: str
    balance_trx: float
    bandwidth: int
    energy: int

class LogResponse(BaseModel):
    id: int
    address: str
    timestamp: datetime
