#!/usr/bin/env python3
"""
Уравнивание химической реакции
"""
# NH4NO3 + Cu = Cu(NO3)2 + H2O + NH3 + NH4NO3
# C2H4O2 + NaOH = C2H3NaO2 + H2O + C2H4O2
import argparse
from chempy import Substance
from chempy import mass_fractions
from chempy import balance_stoichiometry
from chempy.units import default_units as u
# from pprint import pprint

from .solving_system_equations import solution_system


def reaction_calculator(chemical_reaction):
    # chemical_reaction = "Mg(OH)2 + KNO3 = MgN2O6 + KOH"
    left, right = chemical_reaction.split('=')
    left = [Substance.from_formula(x.strip()) for x in left.split('+')]
    right = [Substance.from_formula(x.strip()) for x in right.split('+')]

    # print([x.composition for x in left])
    # print([x.composition for x in right])

    # print(f'\n{chemical_reaction}\n')

    substance_count = len(left) + len(right)

    chem_elements = Substance.composition_keys(left + right)
    # print(chem_elements)

    matrix = []
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
        # print(element, equation)
        matrix.append(equation)

    # pprint(matrix)

    solutions = solution_system(matrix)

    print(solutions)

    list_solutions = []
    for solution in solutions:
        left_part = ' + '.join(
            [f"{k if k > 1 else ''}{substance.unicode_name}"
             for substance, k
             in zip(left, solution[:len(left)])])
        right_part = ' + '.join(
            [f"{k if k > 1 else ''}{substance.unicode_name}"
             for substance, k
             in zip(right, solution[len(left):])])
        list_solutions.append(f"{left_part} = {right_part}")

    return list_solutions


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "reaction", nargs="?",
        default="Mg(OH)2 + KNO3 = MgN2O6 + KOH",
        help="Chemical reaction",
        type=str)
    args = parser.parse_args()
    # print(args)
    chemical_reaction = args.reaction

    list_solutions = reaction_calculator(chemical_reaction)
    for solution in list_solutions:
        print(solution)



