from .academic_session import AcademicSession
from .program_course import ProgramCourse
from .course import Course
# from .department import Department
# from .faculty import Faculty
from .grade_point import GradePoint
from .grading_scheme import GradingScheme
from .program import Program
from .enums import RepeatPolicy, Grade
from .university import University
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator