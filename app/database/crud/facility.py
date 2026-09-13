from app.database.models.facility import RoomORM, RoomBookingORM
from app.database.crud.base import BaseCRUD


roomCRUD = BaseCRUD(RoomORM)
room_bookingCRUD = BaseCRUD(RoomBookingORM)