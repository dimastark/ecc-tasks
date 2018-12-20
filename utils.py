# from typing import Callable, Tuple, TypeVar


# T = TypeVar('T')


# def extended_gcd(a: int, b: int) -> Tuple[int, int]:
def extended_gcd(a: int, b: int):
    s, old_s = 0, 1
    r, old_r = a, b

    while r != 0:
        quotient = old_r // r

        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s

    gcd, x = old_r, old_s

    return gcd, x


# def fast_multiply(k: int, start: T, element: T, add: Callable[[T, T], T]) -> T:
def fast_multiply(k: int, start, element, add):
    result = start
    addend = element

    while k:
        if k & 1:
            result = add(result, addend)

        addend = add(addend, addend)

        k >>= 1

    return result
