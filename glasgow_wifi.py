#!/usr/bin/env python3

from collections import defaultdict, namedtuple
from threading import Thread
from folium import Map, Circle, FeatureGroup, LayerControl


def load_data(file):
    protection_group = defaultdict(list)
    with open(file, 'r') as f:
        f.readline()
        for line in f:
            Wifi = namedtuple('wifi', ['lat', 'long', 'protection'])
            _, lat, long, prot = line.strip().split(',')
            protection_group[prot].append(Wifi(float(lat), float(long), prot))
    return protection_group


def add_markers(wifi_connections, protections):
    for connection in wifi_connections:
        Circle(
            location=[connection.lat, connection.long],
            radius=20,
            color=colours[connection.protection],
            fill=True,
            fill_color=colours[connection.protection],
            weight=1
        ).add_to(protections[connection.protection])


def add_feature_groups(groups, map):
    for key, group in groups.items():
        group.add_to(map)


glasgow = Map(location=[55.873543, -4.289058],
              tiles='OpenStreetMap',
              zoom_start=13
              )

colours = {
    'None': '#3186cc',
    'WPA': '#169316',
    'WPA2': '#963D53',
    'WEP': '#A9AF30'
}

protections = {
    'None': FeatureGroup(name='Free'),
    'WPA': FeatureGroup(name='WPA'),
    'WPA2': FeatureGroup(name='WPA2'),
    'WEP': FeatureGroup(name='WEP')
}

wifi_connections = load_data('test.csv')
threads = [Thread(target=add_markers, args=[wifi_connections[conn_type], protections])
                for conn_type in wifi_connections]

[t.start() for t in threads]
[t.join() for t in threads]

add_feature_groups(protections, glasgow)
LayerControl().add_to(glasgow)

glasgow.save('glasgow2.html')

# SOURCE OF DATASET
# https://data.glasgow.gov.uk/dataset/wi-fi-access-point-locations
# LICENCE OF DATASET
# http://open.glasgow.gov.uk/ckansupport/open.glasgow.gov.uk_Licence_version 1.0.htm