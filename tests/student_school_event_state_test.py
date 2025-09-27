from states.students_states import StudentState
from states.school_state import EventState, SchoolState
from states import AppState

student_sample = StudentState(
    name="Alice",
    age=20,
    year="Sophomore",
    major="Computer Science",
    gpa=3.8,
    rating=4.5
)

event1 = EventState(
    name="Math Quiz",
    description="Math competition for first-year students",
    time="2025-10-01 10:00",
    place="Room 101"
)

event2 = EventState(
    name="Science Fair",
    description="Annual science exhibition",
    time="2025-10-15 14:00",
    place="Auditorium"
)

school_sample = SchoolState(
    location="Can Tho",
    upcoming_events=[event1, event2]
)

app_state = AppState(
    studentstate=student_sample,
    schoolstate=school_sample
)

print(app_state)