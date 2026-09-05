from app.database.models.maintenance import MaintenanceRequestORM, VendorORM
from app.database.crud.base import BaseCRUD


maintenance_requestCRUD = BaseCRUD[MaintenanceRequestORM]()
vendorCRUD = BaseCRUD[VendorORM]()