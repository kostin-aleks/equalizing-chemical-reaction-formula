#!/usr/bin/env python3
"""
Уравнивание химической реакции
"""
# NH4NO3 + Cu = Cu(NO3)2 + H2O + NH3 + NH4NO3
# C2H4O2 + NaOH = C2H3NaO2 + H2O + C2H4O2
import argparse
from pprint import pprint

import mendeleev
from chemformula import ChemFormula
from chempy import Substance, balance_stoichiometry, mass_fractions
from chempy.units import default_units as u
from chempy.util import periodic

from utils.chemistry import is_chemical_equation

from .solving_system_equations import solution_system


def to_equation_text(equation: list) -> str:
    equation_str = f"{equation[0]}z1" if equation[0] else ""
    k = 1
    while k < len(equation):
        sign = "-" if equation[k] < 0 else "+" if equation[k] else ""
        if equation[k]:
            if equation_str:
                sign_str = f" {sign} "
            elif sign == "-":
                sign_str = f"{sign} "
            else:
                sign_str = ""
            equation_str += f"{sign_str}{abs(equation[k])}z{k+1}"
        k += 1
    equation_str += " = 0"
    return equation_str


def reaction_calculator(chemical_reaction):
    result = {
        "list_solutions": [],
        "substances": [],
        "solution_details": [],
        "error": "",
    }
    chemical_reaction = chemical_reaction.strip()
    if not is_chemical_equation(chemical_reaction):
        result["error"] = (
            f'Получена реакция "{chemical_reaction}"\n Проверьте, не получается обработать.'
        )
        return result

    solution_details = ["Решение:\n"]
    splitter = "="
    if "=" not in chemical_reaction:
        splitter = "->"
    left, right = chemical_reaction.split(splitter)
    left = [Substance.from_formula(x.strip()) for x in left.split("+")]
    right = [Substance.from_formula(x.strip()) for x in right.split("+")]

    # print([x.composition for x in left])
    # print([x.composition for x in right])

    print(f"\n{chemical_reaction}\n")

    substances = [{"formula": x.name, "name": x.unicode_name} for x in left + right]

    substance_count = len(left) + len(right)
    solution_details.append(f"Соединений: {substance_count} = количество неизвестных\n")

    chem_elements = Substance.composition_keys(left + right)
    elements_count = len(chem_elements)
    print(chem_elements)
    solution_details.append(f"\nЭлементов: {elements_count} = количество уравнений\n")
    for num in chem_elements:
        chem_element = mendeleev.element(num)
        solution_details.append(
            f"{chem_element.atomic_number:>3} {chem_element.symbol:<2} is {chem_element.name}\n"
        )

    matrix = []
    solution_details.append("\nУравнения системы:\n")
    for element in chem_elements:
        equation = [0 for i in range(substance_count)]
        # print(equation)
        k = 0
        for item in left:
            equation[k] = item.composition.get(element) or 0
            k += 1
        for item in right:
            equation[k] = -(item.composition.get(element) or 0)
            k += 1
        # print(element, periodic.symbols[element], equation)
        chem_element = mendeleev.element(element)
        solution_details.append(
            f"{chem_element.symbol} -> {to_equation_text(equation)}\n"
        )
        matrix.append(equation)

    # pprint(matrix)

    solutions, details = solution_system(matrix)
    print(solutions)
    if not solutions:
        result["error"] = (
            "Система уравнений не имеет решений. Не получается уравнять реакцию."
        )
        return result

    solution_details += details

    solution_details += "\nРешения системы после оптимизации\n"
    for solution in solutions:
        solution_details += f"{str(solution)}\n"

    list_solutions = []
    for solution in solutions:
        left_part = " + ".join(
            [
                f"{k if k > 1 else ''}{substance.unicode_name}"
                for substance, k in zip(left, solution[: len(left)])
            ]
        )
        right_part = " + ".join(
            [
                f"{k if k > 1 else ''}{substance.unicode_name}"
                for substance, k in zip(right, solution[len(left) :])
            ]
        )
        list_solutions.append(f"{left_part} = {right_part}")

    solution_details = "".join(solution_details)
    result["list_solutions"] = list_solutions
    result["substances"] = substances
    result["solution_details"] = solution_details

    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "reaction",
        nargs="?",
        default="Mg(OH)2 + KNO3 = MgN2O6 + KOH",
        help="Chemical reaction",
        type=str,
    )
    args = parser.parse_args()
    # print(args)
    chemical_reaction = args.reaction

    list_solutions = reaction_calculator(chemical_reaction)
    for solution in list_solutions:
        print(solution)
