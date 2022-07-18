#!python
# -*- coding: utf-8 -*-

"""
...information about the code...
"""

__author__ = 'Astrid Moum'
__email__ = 'astridmo@nmbu.no'

import requests


user_key = "AIzaSyBndJoKpNsClohAzxDAKP0Px3Lcbtkg3f4"
#endpoint = f"https://maps.googleapis.com/maps/api/directions/json?origin=Disneyland&destination=Universal+Studios+Hollywood&key={user_key}"

#endpoint = f"https://maps.googleapis.com/maps/api/directions/json?origin=place_id:ChIJa147K9HX3IAR-lwiGIQv9i4&destination=place_id:ChIJzzgyJU--woARcZqceSdQ3dM&key={user_key}"
endpoint = f"https://maps.googleapis.com/maps/api/directions/json?origin=place_id:ChIJ45z55u4SREYRn7yzbSC-Ibc&" \
           f"destination=place_id:ChIJSzH2LNMmR0YRouNJCQtiZaI&waypoints=via:place_id:ChIJfU4GSloHQUYRctPAyVvm1zI&key={user_key}"

r = requests.get(endpoint)  # Issue an HTTP GET request
json_response = r.json()
print(json_response)