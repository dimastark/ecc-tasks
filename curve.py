from typing import Union

from field import Field
from point import Point, PointP, Point2N, Point2S
from polynomial import Polynomial
from utils import fast_multiply


class CurveP:
    def __init__(self, p: int, a: int, b: int):
        self.field = Field(p)

        self.a = a
        self.b = b

    def add(self, a: PointP, b: PointP) -> PointP:
        if a.is_infinity:
            return b

        if b.is_infinity:
            return a

        if a.x == b.x and a.y != b.y:
            return Point.infinity()

        if a.x == b.x:
            k = (3 * a.x * b.x + self.a) * self.field.inverse(2 * a.y)
        else:
            k = (a.y - b.y) * self.field.inverse(a.x - b.x)

        x3 = k * k - a.x - b.x
        y3 = a.y + k * (x3 - a.x)

        return Point(self.field(x3), self.field(-y3))

    def multiply(self, k: int, p: PointP) -> PointP:
        if p.is_infinity:
            return p

        if k < 0:
            return self.multiply(-k, self.negate(p))

        return fast_multiply(k, Point.infinity(), p, self.add)

    def negate(self, p: PointP) -> PointP:
        if p.is_infinity:
            return p

        return Point(p.x, self.field(-p.y))


class Curve2N:
    def __init__(self, p: Polynomial, a: Polynomial, b: Polynomial, c: Polynomial):
        self.p = p
        self.a = a
        self.b = b
        self.c = c

    def add(self, a: Point2N, b: Point2N) -> Point2N:
        if a.is_infinity:
            return b

        if b.is_infinity:
            return a

        if a.x == b.x and (a.y != b.y or a.x == 0):
            return Point.infinity()

        if a.x != b.x:
            k = ((a.y + b.y) * (a.x + b.x).inverse(self.p)) % self.p
            x3 = (k * k + a.x + b.x + self.a * k + self.b) % self.p
        else:
            k = ((a.x * a.x + self.a * a.y) * (a.x * self.a).inverse(self.p)) % self.p
            x3 = (k * k + k * self.a + self.b) % self.p

        y3 = (a.y + k * (a.x + x3) + self.a * x3) % self.p

        return Point(x3, y3)

    def multiply(self, k: Polynomial, p: Point2N) -> Point2N:
        if p.is_infinity:
            return p

        if k.bits < 0:
            return self.multiply(Polynomial(-k.bits), self.negate(p))

        if k == 0:
            return Point.infinity()

        return fast_multiply(k.bits, Point.infinity(), p, self.add)

    def negate(self, p: Point2N) -> Point2N:
        if p.is_infinity:
            return p

        return Point(p.x, (p.x * self.a + p.y) % self.p)


class Curve2S:
    def __init__(self, p: Polynomial, a: Polynomial, b: Polynomial, c: Polynomial):
        self.p = p
        self.a = a
        self.b = b
        self.c = c

    def add(self, a: Point2S, b: Point2S) -> Point2S:
        if a.is_infinity:
            return b

        if b.is_infinity:
            return a

        if a.x == b.x and a.y != b.y:
            return Point.infinity()

        if a.x != b.x:
            k = ((a.y + b.y) * (a.x + b.x).inverse(self.p)) % self.p
            x3 = (k * k + a.x + b.x) % self.p
        else:
            k = ((a.x * b.x + self.b) * self.a.inverse(self.p)) % self.p
            x3 = (k * k) % self.p

        y3 = (k * (a.x + x3) + a.y + self.a) % self.p

        return Point(x3, y3)

    def multiply(self, k: Polynomial, p: Point2S) -> Point2S:
        if p.is_infinity:
            return p

        if k.bits < 0:
            return self.multiply(Polynomial(-k.bits), self.negate(p))

        if k == 0:
            return Point.infinity()

        return fast_multiply(k.bits, Point.infinity(), p, self.add)

    def negate(self, p: Point2S) -> Point2S:
        if p.is_infinity:
            return p

        return Point(p.x, p.y + self.a)


def create_curve(kind: str, **kwargs) -> Union[CurveP, Curve2N, Curve2S]:
    if kind == '2s':
        return Curve2S(
            p=kwargs['polynomial'],
            a=Polynomial(kwargs['a']),
            b=Polynomial(kwargs['b']),
            c=Polynomial(kwargs['c']),
        )

    if kind == '2n':
        return Curve2N(
            p=kwargs['polynomial'],
            a=Polynomial(kwargs['a']),
            b=Polynomial(kwargs['b']),
            c=Polynomial(kwargs['c']),
        )

    return CurveP(p=kwargs['p'], a=kwargs['a'], b=kwargs['b'])
