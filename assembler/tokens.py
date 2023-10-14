from dataclasses import dataclass
from enum import Enum


class TokenType(Enum):
    LABEL = 1
    LABEL_REFERENCE = 2
    INSTRUCTION = 3
    REGISTER = 4
    IMMEDIATE = 5


@dataclass
class Token:
    type: TokenType
    content: str
