class Polynomial:
    def __init__(self, bits: int):
        self.bits = bits

    def __add__(self, b: 'Polynomial') -> 'Polynomial':
        return Polynomial(self.bits ^ b.bits)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Polynomial):
            other = Polynomial(other)

        return self.bits == other.bits

    def __len__(self) -> int:
        return self.bits.bit_length()

    def __lshift__(self, other: int) -> 'Polynomial':
        return Polynomial(self.bits << other)

    def __mod__(self, b: 'Polynomial') -> 'Polynomial':
        a = self.clone()

        while len(a) >= len(b):
            a += b << (len(a) - len(b))

        return a

    def __mul__(self, b: 'Polynomial') -> 'Polynomial':
        addend, s = self.clone(), Polynomial(0)

        for c in b.as_string:
            if c == '1':
                s += addend

            addend <<= 1

        return s

    def __str__(self) -> str:
        return self.as_string

    def __sub__(self, b: 'Polynomial') -> 'Polynomial':
        return self + b

    @property
    def as_string(self) -> str:
        return bin(self.bits)[:1:-1]

    def clone(self) -> 'Polynomial':
        return Polynomial(self.bits)

    def inverse(self, b: 'Polynomial') -> 'Polynomial':
        p1, p2 = self.clone(), b.clone()
        x1, x2 = Polynomial(1), Polynomial(0)

        while p2 != 1:
            p1_len = len(p1)
            p2_len = len(p2)

            if p1_len == p2_len:
                p1, p2 = p2, p1 + p2
                x1, x2 = x2, x1 + x2
            elif p1_len < p2_len:
                p1, p2 = p2, (p1 << (p2_len - p1_len)) + p2
                x1, x2 = x2, (x1 << (p2_len - p1_len)) + x2
            else:
                p1, p2 = p2, (p2 << (p1_len - p2_len)) + p1
                x1, x2 = x2, (x2 << (p1_len - p2_len)) + x1

        return x2 % b
