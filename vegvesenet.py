#!python
# -*- coding: utf-8 -*-

"""
...information about the code...
"""

__author__ = 'Astrid Moum'
__email__ = 'astridmo@nmbu.no'

import requests

# Dette er Astrid sin personlige nøkkel. Dere må opprette en egen nøkkel i deres navn.
# Siden dere er selskap så kreves det videre at dere har de riktige rettigheten i Altinn
# For mer informasjon : https://www.vegvesen.no/om-oss/om-organisasjonen/apne-data/et-utvalg-apne-data/api-for-tekniske-kjoretoyopplysninger/
user_key = "428ef288-2da1-4c0d-847e-d34217db7af6"
header = {'SVV-Authorization': "428ef288-2da1-4c0d-847e-d34217db7af6"}
#endpoint = 'https://www.vegvesen.no/ws/no/vegvesen/kjoretoy/felles/datautlevering/enkeltoppslag/kjoretoydata?kjennemerke=AS15000'
reg_nummer = 'AS15000'
endpoint = f'https://www.vegvesen.no/ws/no/vegvesen/kjoretoy/felles/datautlevering/enkeltoppslag/kjoretoydata?kjennemerke={reg_nummer}'

r = requests.get(endpoint, headers=header)  # Issue an HTTP GET request
json_response = r.json()
print(json_response)

print(r)
print(r.ok)


def valid_car_number(reg_nummer, endpoint, header):
    r = requests.get(endpoint, headers=header)  # Issue an HTTP GET request
    json_response = r.json()
    if r.ok:
        print('Kjøretøyet eksisterer')
    else:
        print('Fant ikke kjøretøy')
        print('Feilmelding fra Vegvesenet:', json_response)

valid_car_number(reg_nummer, endpoint, header)