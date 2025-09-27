import os
import importlib
import inspect
from dataclasses import make_dataclass, is_dataclass, field
from typing import List, Type, TypeAlias

from .ultils import AddMessageList

folder_path = "states"  
dataclass_types: List[Type] = []

for file in os.listdir(folder_path):
    if file.endswith(".py") and file != "__init__.py":
        module_name = f"{folder_path}.{file[:-3]}"  # e.g., states.student
        module = importlib.import_module(module_name)
        for _, obj in inspect.getmembers(module, inspect.isclass):
            if is_dataclass(obj) and getattr(obj, "_include_in_appstate", None):
                dataclass_types.append(obj)
                
fields_list = [(cls.__name__.lower(), cls) for cls in dataclass_types]
fields_list += [("messages", list, field(default_factory=list))] 
fields_list += [("user_input", str|None, field(default=None))]
fields_list += [("cache", list, field(default_factory=list))]

AppState:TypeAlias = make_dataclass("GraphState", fields_list) # type: ignore