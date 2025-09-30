import pytest

def test_student_state(student_sample):
    assert student_sample.name == "Alice"
    assert student_sample.gpa == 3.8
    assert student_sample.year == "Sophomore"

def test_school_state(school_sample):
    assert school_sample.location == "Can Tho"
    assert len(school_sample.upcoming_events) == 2
    assert school_sample.upcoming_events[0].name == "Math Quiz"

def test_app_state(appstate_sample):
    assert appstate_sample.studentstate.name == "Alice"
    assert appstate_sample.schoolstate.location == "Can Tho"
    assert any(ev.name == "Science Fair" for ev in appstate_sample.schoolstate.upcoming_events)
