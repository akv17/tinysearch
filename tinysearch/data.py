from dataclasses import dataclass
from typing import Any


@dataclass
class Document:
    key: str
    text: str


@dataclass
class MatrixEncoding:
    keys: Any
    matrix: Any
    vector: Any
    texts: Any


@dataclass
class Score:
    key: str
    score: float
    text: str
