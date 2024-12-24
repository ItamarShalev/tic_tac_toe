from __future__ import annotations
from enum import Enum

class Piece(Enum):
    X = 'X'
    O = 'O'
    EMPTY = ' '

    @classmethod
    def from_str(cls, value: str | Piece):
        if isinstance(value, Piece):
            return value
        return cls(value.upper())

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return self.value

    def __eq__(self, other):
        if isinstance(other, str):
            return self.value == other
        if not isinstance(other, Piece):
            return False
        return self.value == other.value

    def __hash__(self):
        return hash(self.value)
