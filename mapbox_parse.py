from Mapbox import Directions, Geocoder
from mavsdk import System
import json

# Creates array of mapbox mission items to feed to drone, given starting and ending addresses of desired path 
def parse_coordinates(start, dest):
    geocoder = Geocoder(access_token='sk.eyJ1IjoiaGtpbTgwOCIsImEiOiJja2V1bXA5NTAxY2cxMnBzYW14NGp3MXhmIn0.NmL-zgIUGxcN034JdVpsAg')
    starting_location = geocoder.forward(start)
    first = starting_location.geojson()['features'][0]
    starting_coords = [round(coord, 5) for coord in first['geometry']['coordinates']]
    
    destination = geocoder.forward(dest)
    last = starting_location.geojson()['features'][0]
    destination_coords = [round(coord, 5) for coord in last['geometry']['coordinates']]

    service = Directions() 
    origin = {
        'type': 'Feature',
        'properties': {'name': start},
        'geometry': {
            'type': 'Point',
            'coordinates': [starting_coords[0], starting_coords[1]]}}

    destination = {
        'type': 'Feature', 
        'properties': {'name': dest},
        'geometry': {
            'type': 'Point', 
            'coordinates': [destination_coords[0], destination_coords[1]]}}

    service = Directions(access_token='sk.eyJ1IjoiaGtpbTgwOCIsImEiOiJja2V1bXA5NTAxY2cxMnBzYW14NGp3MXhmIn0.NmL-zgIUGxcN034JdVpsAg')
    response = service.directions([origin, destination], 
                                    'mapbox.cycling', 
                                    steps=True, 
                                    access_token='sk.eyJ1IjoiaGtpbTgwOCIsImEiOiJja2V1bXA5NTAxY2cxMnBzYW14NGp3MXhmIn0.NmL-zgIUGxcN034JdVpsAg')


    directions = json.loads(response)
    coords_filter = {key: val for key, value in directions['routes']['legs']['steps'][0] if key = "intersections"} 
    coords_list = # Final list 
    mission_items = []
    for coord_pair in coords_list:
        mission_items.append(MissionItem(coord_pair[0],
                                     coord_pair[1],
                                     25,
                                     10,
                                     True,
                                     float('nan'),
                                     float('nan'),
                                     MissionItem.CameraAction.START_PHOTO_INTERVAL,
                                     float('nan'),
                                     float('nan')))
    
    return mission_items 





    



