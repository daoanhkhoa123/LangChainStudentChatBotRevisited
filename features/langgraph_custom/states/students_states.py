from dataclasses import dataclass
from states.decorator import include_in_appstate

@include_in_appstate
@dataclass
class StudentState:
    name: str
    age: int
    year: str
    major: str
    gpa: float
    rating: float
