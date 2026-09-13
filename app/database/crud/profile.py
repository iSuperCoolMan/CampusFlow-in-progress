from app.database.models.profile import (
    StudentORM, InstructorORM, AdminORM, RegistrarORM, FinanceManagerORM, FacilityManagerORM
)

from app.database.crud.base import BaseCRUD
from app.utils.enums import RoleStr


studentCRUD = BaseCRUD(StudentORM)
instructorCRUD = BaseCRUD(InstructorORM)
adminCRUD = BaseCRUD(AdminORM)
registrarCRUD = BaseCRUD(RegistrarORM)
finance_managerCRUD = BaseCRUD(FinanceManagerORM)
facility_managerCRUD = BaseCRUD(FacilityManagerORM)


profileCRUD_map = {
    RoleStr.student: studentCRUD,
    RoleStr.instructor: instructorCRUD,
    RoleStr.admin: adminCRUD,
    RoleStr.registrar: registrarCRUD,
    RoleStr.finance_manager: finance_managerCRUD,
    RoleStr.facility_manager: facility_managerCRUD,
}