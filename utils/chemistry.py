import re
from urllib.error import HTTPError
import pubchempy as pcp


def is_chemical_equation(equation):
    # Шаблон: коэффициенты (опц.) + Формула (Аа1) + (опц. + реагенты) + стрелка + ...
    pattern = r"^([0-9]*[A-Za-z0-9\(\)\[\]]+\s*\+*\s*)+\s*[\=\-\>]+\s*([0-9]*[A-Za-z0-9\(\)\[\]]+\s*\+*\s*)+$"
    return re.match(pattern, equation)


def get_name_from_formula(formula):
    # Поиск соединений по формуле
    name = 'unknown'
    try:
        compounds = pcp.get_compounds(formula, 'formula')
        if compounds:
            # Возвращаем наиболее релевантное название
            name = compounds[0].iupac_name
    except HTTPError:
        pass
    except pcp.BadRequestError:
        pass
    return name
