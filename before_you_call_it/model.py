"""Explicit observation states; missing data never becomes a measurement."""
from dataclasses import dataclass
from enum import Enum


class State(str, Enum):
    OBSERVED = "OBSERVED"
    UNAVAILABLE = "UNAVAILABLE"
    NOT_CHECKED = "NOT_CHECKED"


@dataclass(frozen=True)
class Observation:
    key: str
    value: str | int | float | bool | None = None
    unit: str = ""
    method: str = ""
    timestamp: str = ""
    state: State = State.NOT_CHECKED
    reason: str = ""

    def __post_init__(self):
        if self.state == State.OBSERVED and self.value is None:
            raise ValueError("An observed measurement needs a value")
        if self.state != State.OBSERVED and self.value is not None:
            raise ValueError("Missing observations cannot have a value")
