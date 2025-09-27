from dataclasses import dataclass
from typing import List

from states.decorator import include_in_appstate

@dataclass
class EventState:
    name: str
    description: str
    time: str
    place: str

@include_in_appstate
@dataclass
class SchoolState:
    location: str
    upcoming_events: List[EventState]

    @property
    def name(self) -> str:
        return "FPT University"
