from secret import PETFINDER_API_KEY
import requests
from random import randint

BASE_URL = 'http://api.petfinder.com/pet.getRandom'


def get_random_pet():
    """Send get request to Petfinder API for random pet name, age, and image"""

    species_types = ['cat', 'dog']
    animal = species_types[randint(0, 1)]

    raw_resp = requests.get(
        BASE_URL,
        params={
            'format': 'json',
            'key': PETFINDER_API_KEY,
            'output': 'basic',
            'animal': animal
        })

    resp = raw_resp.json()
    name = resp['petfinder']['pet']['name']['$t']
    age = resp['petfinder']['pet']['age']['$t']
    if 'photos' in (resp['petfinder']['pet']['media']):
        photo_url = resp['petfinder']['pet']['media']['photos']['photo'][2][
            '$t']
    else:
        photo_url = None
    species = resp['petfinder']['pet']['animal']['$t']
    if 'breeds' in (resp['petfinder']['pet']):
        notes = resp['petfinder']['pet']['breeds']['breed']['$t']
    else:
        notes = None

    age = convert_age_to_int(age)

    return {
        'name': name,
        'age': age,
        'photo_url': photo_url,
        'species': species,
        'notes': notes
    }


def convert_age_to_int(age_string):
    """Converting the Petfinder age string to an integer"""

    age_conversions = {'baby': 0, 'young': 3, 'adult': 6, 'senior': 10}
    age = age_conversions[age_string.lower()]

    return age
