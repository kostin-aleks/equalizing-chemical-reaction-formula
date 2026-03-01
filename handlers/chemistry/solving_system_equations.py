"""
Решение системы линейных однородных уравнений
в натуральных числах
"""

import math
from functools import reduce


def list_without_doubles(lst: list):
    lst = list(set([tuple(x) for x in lst]))
    return [list(x) for x in lst]


def find_list_gcd(numbers: list):
    """получить наибольший общий делитель для списка чисел"""
    # Применяет math.gcd последовательно к элементам списка
    return reduce(math.gcd, numbers)


def scalar_product(first, second):
    """скалярное произведение двух векторов"""
    return sum(x * y for x, y in zip(first, second))


def sum_vectors(first, second):
    """сумма векторов равная вектору где координаты - это попарные суммы координат векторов"""
    return [x + y for x, y in zip(first, second)]


def xfactor(vector, factor):
    """произведение вектора на число"""
    return [factor * x for x in vector]


def combination(plus_vector, minus_vector):
    """линейная комбинация двух векторов"""
    return {
        "r": 0,
        "vector": sum_vectors(
            xfactor(plus_vector["vector"], abs(minus_vector["r"])),
            xfactor(minus_vector["vector"], abs(plus_vector["r"])),
        ),
    }


def get_solution(equation, basis):
    """получить набор решений для уравнения для базового набора векторов basis"""
    M_zero = []
    M_plus = []
    M_minus = []

    for vector in basis:
        mlt = scalar_product(equation, vector)
        if mlt > 0:
            M_plus.append({"r": mlt, "vector": vector})
        if mlt < 0:
            M_minus.append({"r": mlt, "vector": vector})
        if mlt == 0:
            M_zero.append({"r": mlt, "vector": vector})

    if M_plus and M_minus:
        for plus_vector in M_plus:
            for minus_vector in M_minus:
                M_zero.append(combination(plus_vector, minus_vector))

    return M_zero


def solutions_without_zero(solutions):
    result = []
    for vector in solutions:
        if 0 not in vector:
            result.append(vector)
        else:
            k = 0
            for item in solutions:
                combination = sum_vectors(vector, item)
                if 0 not in combination:
                    result.append(combination)
                    break

    return result


def solution_system(matrix):
    # print("=============== решение ==========================")
    solution_details = ''

    N = len(matrix[0])

    # начальный предбазис
    basis = []
    for k in range(N):
        basis.append([0 for x in range(N)])

    i = 0
    for item in basis:
        item[i] = 1
        i += 1

    # цикл по уравнениям системы

    k = 0
    while k < len(matrix):
        row = matrix[k]
        solutions = get_solution(row, basis)
        basis = [x["vector"] for x in solutions]

        k += 1

    solutions = basis

    # попробовать найти общий делитель для каждого вектора решения
    # разделить, если есть общий делитель
    for i in range(len(solutions)):
        vector = solutions[i]
        nod = find_list_gcd(vector)
        # print(nod, vector)
        if nod > 1:
            solutions[i] = [x // nod for x in vector]

    solutions = list_without_doubles(solutions)
    print(solutions)
    if solutions:
        solution_details += '\nРешения системы\n'
        for solution in solutions:
            solution_details += f"{str(solution)}\n"

    solutions = solutions_without_zero(solutions)
    solutions = list_without_doubles(solutions)

    solutions = sorted(solutions, key=lambda x: sum(x))

    return solutions, solution_details

