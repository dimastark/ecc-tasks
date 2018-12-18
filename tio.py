import os
import re

from os import path
from typing import List, Tuple

from point import Point
from polynomial import Polynomial


BASE_DIR = path.dirname(__file__)
INPUT_DIR = path.join(BASE_DIR, 'input')
OUTPUT_DIR = path.join(BASE_DIR, 'output')


def get_all_inputs() -> List[Tuple[str, dict]]:
    result = []

    for file in os.listdir(INPUT_DIR):
        if file.endswith('.txt'):
            file_path = path.join(INPUT_DIR, file)

            result.append((file, parse_input(file_path)))

    return result


def parse_input(from_file: str) -> dict:
    result = {}

    with open(from_file, encoding='utf-8') as input_file:
        result['kind'] = next_line(input_file)

        if result['kind'] in ('2s', '2n'):
            result['n'] = parse_int(next_line(input_file))
            result['polynomial'] = parse_polynomial(next_line(input_file))
        else:
            result['p'] = parse_int(result['kind'])

        result['a'] = parse_int(next_line(input_file))
        result['b'] = parse_int(next_line(input_file))

        if result['kind'] in ('2s', '2n'):
            result['c'] = parse_int(next_line(input_file))

        result['tasks'] = parse_tasks(result['kind'], read_lines(input_file))

    return result


def next_line(file) -> str:
    line = file.readline().strip().lower()

    while line.startswith('#'):
        line = file.readline().strip().lower()

    return line


def read_lines(file) -> List[str]:
    return [line.strip().lower() for line in file.readlines() if not line.startswith('#')]


def parse_polynomial(s: str) -> Polynomial:
    p = Polynomial(0)

    for x in re.findall(r'(x\^\d+|x|1)', s):
        if x == '1':
            p += Polynomial(1)
        elif x == 'x':
            p += Polynomial(2)
        else:
            p += Polynomial(1 << int(x[2:]))

    return p


def parse_tasks(curve_type: str, lines: List[str]) -> List[tuple]:
    result = []

    for line in lines:
        kind, *ops = line.strip().split()

        assert kind.lower() in ('у', 'с')

        ops_count = 3 if kind.lower() == 'у' else 4

        assert len(ops) == ops_count, f'Количество операндов != {ops_count}'

        args = [parse_int(o) for o in ops]

        if curve_type in ('2s', '2n'):
            args = [Polynomial(arg) for arg in args]

        result.append((kind.lower(), *args))

    return result


def parse_int(s: str) -> int:
    if s.lower().startswith('0b'):
        return int(s, 2)

    if s.lower().startswith('0x'):
        return int(s, 16)

    return int(s, 10)


def write_result(to_file: str, result: List[Point]):
    with open(path.join(OUTPUT_DIR, to_file), mode='w') as file:
        file.writelines([str(p) + os.linesep for p in result])
