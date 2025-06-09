from pydantic import BaseModel, Field
from typing import Optional
from typing import List


class Coordinates(BaseModel):
    latitude: float
    longitude: float


class DateSchema(BaseModel):
    year: int
    month: int
    dayOfMonth: int
    hourOfDay: int
    minute: int
    second: int


class GatewaySchema(BaseModel):
    mac: str
    ip: str
    manufacturer: str
    hostName: str
    status: bool
    date: DateSchema
    solution: str
    coordinates: Coordinates


class GatewayResponseSchema(BaseModel):
    message: str


class GatewayMacListResponse(BaseModel):
    mac_addresses: list[str]
    message: str

class DeviceResponseSchema(BaseModel):
    message: str


class DeviceIdListResponse(BaseModel):
    device_ids: List[str]
    message: str