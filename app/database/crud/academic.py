from app.database.models.academic import CourseORM, CourseOfferingORM, SectionORM, EnrollmentORM, GradeORM
from app.database.crud.base import BaseCRUD


courseCRUD = BaseCRUD[CourseORM]()
course_offeringCRUD = BaseCRUD[CourseOfferingORM]()
sectionCRUD = BaseCRUD[SectionORM]()
enrollmentCRUD = BaseCRUD[EnrollmentORM]()
gradeCRUD = BaseCRUD[GradeORM]()







