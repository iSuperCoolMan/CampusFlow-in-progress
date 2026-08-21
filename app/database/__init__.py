from .base import BaseORM
from .models.auth import UserORM
from .models.people import StudentORM, InstructorORM
from .models.core import UniversityORM, CampusORM, DepartmentORM, ProgramORM
from .models.academic import CourseORM, CourseOfferingORM, SectionORM, EnrollmentsORM, GradeORM
from .models.facility import RoomORM, RoomBookingORM
from .models.finance import PaymentORM, ScholarshipORM
from .models.maintenance import MaintenanceRequestORM, VendorORM

__all__ = ["BaseORM"]