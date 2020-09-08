from Mapbox import Directions, Geocoder
from mavsdk import System

# Creates array of mapbox mission items to feed to drone, given starting and ending addresses of desired path 
def parse_coordinates(start, dest):
    geocoder = Geocoder()
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
    
   response = service.directions([origin, destination], 'mapbox.walking')
  
