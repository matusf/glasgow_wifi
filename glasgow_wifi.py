#!/usr/bin/env python3

from collections import namedtuple
from threading import Thread
from folium import Map, Circle, FeatureGroup, LayerControl


def load_data(file):
    data = []
    with open(file, 'r') as f:
        f.readline()
        for line in f:
            Wifi = namedtuple('wifi', ['bssid', 'lat', 'long', 'protection'])
            data.append(Wifi(*line.strip().split(',')))
    return data


glasgow = Map(location=[55.873543, -4.289058],
              tiles='OpenStreetMap',
              zoom_start=13
              )

colours = {
    'None': '#3186cc',
    'WPA': '#169316',
    'WPA2': '#862D43',
    'WEP': '#B9BF40'
}

protections = {
    'None': FeatureGroup(name='Free'),
    'WPA': FeatureGroup(name='WPA'),
    'WPA2': FeatureGroup(name='WPA2'),
    'WEP': FeatureGroup(name='WEP')
}

wifi_connections = load_data('glasgow-dl.csv')

for connection in wifi_connections:
    Circle(
        location=[float(connection.lat), float(connection.long)],
        radius=20,
        color=colours[connection.protection],
        fill=True,
        fill_color=colours[connection.protection],
        weight=1
    ).add_to(protections[connection.protection])

for key, group in protections.items():
    group.add_to(glasgow)

LayerControl().add_to(glasgow)
glasgow.save('glasgow.html')
#  https://data.glasgow.gov.uk/dataset/wi-fi-access-point-locations
