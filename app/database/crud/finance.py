from app.database.models.finance import PaymentORM, ScholarshipORM
from app.database.crud.base import BaseCRUD


paymentCRUD = BaseCRUD[PaymentORM]()
scholarshipCRUD = BaseCRUD[ScholarshipORM]()