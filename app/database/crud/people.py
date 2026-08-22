from app.database.models.people import (
    StudentORM, InstructorORM, AdminORM, RegistrarORM, FinanceManagerORM, FacilityManagerORM
)

from app.database.crud.base import BaseCRUD


studentCRUD = BaseCRUD(StudentORM)
instructorCRUD = BaseCRUD(InstructorORM)
adminCRUD = BaseCRUD(AdminORM)
registrarCRUD = BaseCRUD(RegistrarORM)
finance_managerCRUD = BaseCRUD(FinanceManagerORM)
facility_managerCRUD = BaseCRUD(FacilityManagerORM)