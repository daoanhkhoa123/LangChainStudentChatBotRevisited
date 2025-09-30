from typing import Iterable, Dict
from dataclasses import asdict
import json

from states.school_state import SchoolState, EventState
from states.students_states import StudentState
from .ultils import retry

from llms.gemini import gemini

def greeting_with_events(student:StudentState, school:SchoolState, top_k_event:int=3) -> str:
    res = f"Greeting {student.name}."

    events = school.upcoming_events[:top_k_event]
    if events:
        res += " Upcoming events:\n"
        for e in events:
            res+=f"-{e.name}\n"

        res += "Which one do you want to join the most?"
    else:
        res += " How are you today?"

    return  res

@retry(default={"events_chosen": []})
def choose_events(events:Iterable[EventState], prompt:str):
    system_msg = """You are an assistant that identifies which events a user is referring to.
    You will be given a user query and a list of upcoming events. 
    Return ONLY the event names that are most relevant, as a JSON list of strings."""
    
    events_dict = [asdict(e) for e in events]

    user_msg = f"""
    User query: {prompt}

    Events:
    {json.dumps(events_dict, indent=2)}
    """

    resp = gemini.invoke([
        {"role": "system", "content": system_msg},
        {"role": "user", "content": user_msg},
    ])

    chosen_names = resp.content
    chosen_events = [e for e in events if e.name in chosen_names]

    return chosen_events


def tell_events(event_str: str, user_query: str):
    system_msg = """You are an assistant that explains upcoming school events.
    The user has already chosen or been matched with some events.
    Your job is to describe these events in clear, friendly language,
    including their purpose, time, and why they might be relevant."""

    user_msg = f"""
    User query: {user_query}

    Selected events:
    {event_str}

    Please explain these events to the user.
    """

    resp = gemini.invoke([
        {"role": "system", "content": system_msg},
        {"role": "user", "content": user_msg},
    ])

    return resp.content
