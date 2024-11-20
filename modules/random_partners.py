# from https://github.com/icebound777/PMR-SeedGenerator/blob/main/rando_modules/random_partners.py

"""This module handles choosing random partners to start the seed with."""
from ..data.partners_meta import all_partners as all_partners_imp


def get_rnd_starting_partners(partners: int, random) -> list:
    """
    Returns a list of randomly chosen partners.
    """
    starting_partners = []
    all_partners = all_partners_imp.copy()

    while len(starting_partners) < partners:
        new_partner = random.choice(all_partners)
        all_partners.remove(new_partner)
        starting_partners.append(new_partner)

    return starting_partners
