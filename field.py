from utils import extended_gcd


class Field:
    def __init__(self, p: int):
        self.modulus = p

    def __call__(self, n: int):
        return n % self.modulus

    def inverse(self, a: int) -> int:
        if a == 0:
            raise ZeroDivisionError

        if a < 0:
            return self.modulus - self.inverse(-a)

        gcd, x = extended_gcd(self.modulus, a)

        return self(x)
