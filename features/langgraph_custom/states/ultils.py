from typing import Any, Iterable
from langgraph.graph import add_messages

class AddMessageList(list):
    def append(self, object: Any) -> None:
        merged = add_messages(self, object)
        super().clear()
        super().extend(merged)

    def extend(self, items: Iterable[Any]) -> None:
        merged = add_messages(self, items) # type: ignore
        super().clear()
        super().extend(merged)