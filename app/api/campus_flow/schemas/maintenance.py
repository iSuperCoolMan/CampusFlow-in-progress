from datetime import datetime
from uuid import UUID

from app.api.campus_flow.schemas.base import BaseModelWithUUID


class MaintenanceRequest(BaseModelWithUUID):
    campus_uuid: UUID
    room_uuid: UUID
    description: str
    status: str
    requested_on: datetime
    resolved_on: datetime
    vendor_uuid: UUID


class Vendor(BaseModelWithUUID):
    name: str
    contact_email: str
    phone: str