from dataclasses import dataclass
from typing import Generic, Optional, TypeVar

from polynomial import Polynomial


T = TypeVar('T', int, Polynomial)


@dataclass
class Point(Generic[T]):
    x: Optional[T]
    y: Optional[T]

    def __str__(self):
        if self.is_infinity:
            return '0'
        
        return f'({str(self.x)}, {str(self.y)})'

    @staticmethod
    def infinity() -> 'Point':
        return Point(None, None)

    @property
    def is_infinity(self) -> bool:
        return self.x is self.y is None


PointP = Point[int]
Point2N = Point[Polynomial]
Point2S = Point[Polynomial]
