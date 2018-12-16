import tio

from curve import create_curve, Point


def main():
    for input_name, input_dict in tio.get_all_inputs():
        result = []

        curve = create_curve(**input_dict)

        for task_type, *task_args in input_dict['tasks']:
            if task_type == 'у':
                x, y, k = task_args

                result.append(curve.multiply(k, Point(x, y)))
            if task_type == 'с':
                x1, y1, x2, y2 = task_args

                result.append(curve.add(Point(x1, y1), Point(x2, y2)))

        tio.write_result(input_name, result)


if __name__ == '__main__':
    main()
