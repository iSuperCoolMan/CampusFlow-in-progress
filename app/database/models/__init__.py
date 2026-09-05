from .academic import CourseORM, CourseOfferingORM, SectionORM, EnrollmentORM, GradeORM
from .auth import UserORM
from .base import BaseORM
from .core import UniversityORM, CampusORM, DepartmentORM, ProgramORM
from .facility import RoomORM, RoomBookingORM
from .finance import PaymentORM, ScholarshipORM
from .maintenance import MaintenanceRequestORM, VendorORM
from .people import PeopleORM, StudentORM, InstructorORM, AdminORM, RegistrarORM, FacilityManagerORM, FinanceManagerORM