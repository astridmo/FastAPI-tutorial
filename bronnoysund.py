#!python
# -*- coding: utf-8 -*-

"""
Code to check if company exists from Brønnøysundregisteret
"""

__author__ = 'Astrid Moum'
__email__ = 'astridmo@nmbu.no'

import requests

#curl 'https://data.brreg.no/enhetsregisteret/api/enheter' -i -X GET

# endpoint = 'https://data.brreg.no/enhetsregisteret/api/enheter'

org_1 = '922924368'
org_2 = '916627939'
org_3 = '911963582'
org_nei = '432'
org_meg = '927773880'

# r = requests.get(endpoint)  # Issue an HTTP GET request
# json_response = r.json()

# print(json_response)

endpoint = f'https://data.brreg.no/enhetsregisteret/api/enheter?organisasjonsnummer={org_1}'
r = requests.get(endpoint)  # Issue an HTTP GET request
print(r.ok)
json_response = r.json()
print(json_response)

print(json_response['_embedded']['enheter'])


def existing_company(organization_num):
    """
    Function to check if organization exists in Norway.
    The information is gathered from Enhetsregisteret in Brønnøysundsregisteret

    Parameters
    ----------
    organization_num : str
        organization number of the company

    Returns
    -------
    boolean
        True if the company exists. False if not.
    """
    endpoint = f'https://data.brreg.no/enhetsregisteret/api/enheter?organisasjonsnummer={organization_num}'
    r = requests.get(endpoint)  # Issue an HTTP GET request
    json_response = r.json()
    try:  # Check if this key exists in the json response
        json_response['_embedded']['enheter']
        return True
    except KeyError:  # The company does not exist (either it has never existed or it is shut down)
        return False


print(existing_company(org_nei))