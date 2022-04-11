from dataclasses import dataclass

from enum import Enum, auto


class OptionType(Enum):
    CALL = auto()
    PUT = auto()


@dataclass
class Option:
    type: OptionType
    option_index: int
    strike: float
    premium: float
