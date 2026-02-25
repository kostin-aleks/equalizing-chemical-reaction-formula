from urllib.error import HTTPError
import pubchempy as pcp


def get_name_from_formula(formula):
    # Поиск соединений по формуле
    try:
        compounds = pcp.get_compounds(formula, 'formula')
        if compounds:
            # Возвращаем наиболее релевантное название
            # pprint(compounds[0].to_dict())
            name = compounds[0].iupac_name
    except HTTPError:
        name = 'Unknown'
    except pcp.BadRequestError:
        name = 'Unknown'
    return name
