# from https://github.com/icebound777/PMR-SeedGenerator/blob/main/rando_modules/random_partners.py

"""This module handles choosing random partners to start the seed with."""
import random

from ..data.partners_meta import all_partners as all_partners_imp


def get_rnd_starting_partners(min_partners, max_partners) -> list:
    """
    Returns a list of randomly chosen partners according to the parameters.
    """
    starting_partners = []
    all_partners = all_partners_imp.copy()

    non_guaranteed_partners = max_partners - min_partners
    randomly_added_partners = random.randint(0, non_guaranteed_partners)

    while len(starting_partners) < (min_partners + randomly_added_partners):
        new_partner = random.choice(all_partners)
        all_partners.remove(new_partner)
        starting_partners.append(new_partner)

    return starting_partners
