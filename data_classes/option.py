from dataclasses import dataclass
from enum import Enum, auto


class OptionType(Enum):
    CALL = auto()
    PUT = auto()


@dataclass
class Option:
    type: OptionType
    strike: float
    premium: float
