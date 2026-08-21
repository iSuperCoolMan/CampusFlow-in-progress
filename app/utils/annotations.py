from datetime import datetime
from typing import Annotated

from annotated_types import Interval


days_of_week_annotation = Annotated[int, Interval(ge=1, le=7)]
grade_value = Annotated[int, Interval(ge=1, le=5)]
established_year_annotation = Annotated[int, Interval(ge=0, le=datetime.now().year)]