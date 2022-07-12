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
reg_nummer = 'LJ48973'
reg_nummer = 'LJ48973222'
endpoint = f'https://www.vegvesen.no/ws/no/vegvesen/kjoretoy/felles/datautlevering/enkeltoppslag/kjoretoydata?kjennemerke={reg_nummer}'

r = requests.get(endpoint, headers=header)  # Issue an HTTP GET request
json_response = r.json()
#print(json_response)
#
# print(r)
# print(r.ok)


def valid_car_number(reg_nummer, endpoint, header):
    r = requests.get(endpoint, headers=header)  # Issue an HTTP GET request
    json_response = r.json()
    if r.ok:  # If the vehicle exists
        print('Kjøretøyet eksisterer')
        vehicle_id = json_response['kjoretoydataListe'][0]['godkjenning']['tekniskGodkjenning']["tekniskeData"]["generelt"]
        vehicle_weight = json_response['kjoretoydataListe'][0]['godkjenning']['tekniskGodkjenning']["tekniskeData"]["vekter"]
        vehicle_axle = json_response['kjoretoydataListe'][0]['godkjenning']['tekniskGodkjenning']["tekniskeData"]["akslinger"]
        vehicle_environmental_data = json_response['kjoretoydataListe'][0]['godkjenning']['tekniskGodkjenning']["tekniskeData"]['miljodata']
        vehicle_motor = json_response['kjoretoydataListe'][0]['godkjenning']['tekniskGodkjenning']["tekniskeData"]['motorOgDrivverk']['motor']
        vehicle_summary = {'vehicle_id': vehicle_id,
                           'vehicle_weight': vehicle_weight,
                           'vehicle_axle': vehicle_axle,
                           'vehicle_environmental_data': vehicle_environmental_data,
                           'motor': vehicle_motor}
        #print(vehicle_summary)
        vehicle_environmental_data = \
        vehicle_tillegg = json_response['kjoretoydataListe'][0]['godkjenning']['tilleggsgodkjenninger']
        print(vehicle_tillegg)

        try:
            vehicle_tillegg2 = json_response['kjoretoydataListe'][0]['godkjenning']['tilleggsgodkjenninger'][0]['godkjenningstype']['kodeVerdi']
            print(vehicle_tillegg2)
            if vehicle_tillegg2 == 'ADR':
                print(True)
                dangerous_goods = True
        except IndexError:  # Vehicle cannot transport dangerous goods
            print(False)
    else:
        print('Fant ikke kjøretøy')
        print('Feilmelding fra Vegvesenet:', json_response)

valid_car_number(reg_nummer, endpoint, header)