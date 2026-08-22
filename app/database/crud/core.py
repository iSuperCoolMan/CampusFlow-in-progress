from app.database.models.core import UniversityORM, CampusORM, DepartmentORM, ProgramORM
from app.database.crud.base import BaseCRUD


universityCRUD = BaseCRUD(UniversityORM)
campusCRUD = BaseCRUD(CampusORM)
departmentCRUD = BaseCRUD(DepartmentORM)
programCRUD = BaseCRUD(ProgramORM)