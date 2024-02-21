import pandas as pd
import math
import numpy as np
import json
from threading import Thread
import os
import socket
import zlib
import keyboard

from sklearn.linear_model import LinearRegression

def listenTCP(IP='', Port=0, PacketSize=65536):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # soketi oluştur ve server olarak ata
    server.bind((IP, Port))  # soketi bağla
    server.listen(1)  # dinlemeye başla
    conn, addr = server.accept()  # bağlantıyı kabul et
    a = conn.recv(PacketSize)
    return a.decode("utf-8")


# Reference point in degrees
ref_latitude = 41.5
ref_longitude = 36.0

# Radius of the Earth in meters
earth_radius = 6371000

lastMessages = []

def calculate_cartesian_distance(point1, point2):
    return np.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)

def predict_new_position(current_position, heading, speed, time_interval=1):
    heading_radians = math.radians(heading)
    dx = speed * math.cos(heading_radians) * time_interval
    dy = speed * math.sin(heading_radians) * time_interval
    return current_position[0] + dx, current_position[1] + dy

def haversine(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = earth_radius * c

    return distance


def haversine(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = earth_radius * c

    return distance


def readMessageUDP(IP='', Port=0, PacketSize=65536):
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # soketi oluştur ve client olarak ata
    client.settimeout(0.8)
    client.connect((IP, Port))  # soketi bağla
    a = client.recv(PacketSize)
    return a.decode("utf-8")

aircraft_data = {}

def predict_new_position_based_on_last_n_points(data, n=5):
    features = []
    targets = []
    for i in range(len(data) - n):
        feature_window = data.iloc[i:i + n][
            ['iha_enlem_meters', 'iha_boylam_meters', 'iha_irtifa', 'iha_dikilme', 'iha_yonelme', 'iha_yatis',
             'zaman_farki']].values
        target = data.iloc[i + n][
            ['iha_enlem_meters', 'iha_boylam_meters', 'iha_irtifa', 'iha_dikilme', 'iha_yonelme', 'iha_yatis']].values
        features.append(feature_window)
        targets.append(target)
    return np.array(features), np.array(targets)

takim_numaralari = []
while True:
    # Take input from tcp server that is running on the other side msg[0], "127.0.0.1", 2589, receive=False, compress=False
    data = listenTCP("127.0.0.1", 2589)

    # example data {"sunucusaati":{"saat":14,"dakika":9,"saniye":59,"milisaniye":903},"konumBilgileri":[{"takim_numarasi":3,"iha_enlem":41.5132,"iha_boylam":36.1189,"iha_irtifa":-0.5,"iha_dikilme":6.2706,"iha_yonelme":100.3472,"iha_yatis":2.5268,"zaman_farki":1667.0},{"takim_numarasi":8,"iha_enlem":41.51321,"iha_boylam":36.11896,"iha_irtifa":0.007,"iha_dikilme":0.0,"iha_yonelme":103.0,"iha_yatis":0.0,"zaman_farki":1132.0},{"takim_numarasi":11,"iha_enlem":41.5130959,"iha_boylam":36.119297,"iha_irtifa":-1.226,"iha_dikilme":-1.32590342,"iha_yonelme":44.0,"iha_yatis":1.31732583,"zaman_farki":1817.0},{"takim_numarasi":12,"iha_enlem":41.51314,"iha_boylam":36.1190643,"iha_irtifa":0.001,"iha_dikilme":-0.184152573,"iha_yonelme":96.1219,"iha_yatis":0.7862835,"zaman_farki":1258.0},{"takim_numarasi":15,"iha_enlem":41.5130959,"iha_boylam":36.11897,"iha_irtifa":-3.89,"iha_dikilme":-5.0,"iha_yonelme":82.0,"iha_yatis":0.0,"zaman_farki":413.0},{"takim_numarasi":16,"iha_enlem":41.513176,"iha_boylam":36.1189651,"iha_irtifa":-7.816,"iha_dikilme":-1.2220856,"iha_yonelme":79.9404755,"iha_yatis":2.89447761,"zaman_farki":1246.0},{"takim_numarasi":22,"iha_enlem":41.51314,"iha_boylam":36.1191368,"iha_irtifa":0.001,"iha_dikilme":2.09852314,"iha_yonelme":82.16577,"iha_yatis":1.5617739,"zaman_farki":1488.0}]}

    json_data = json.loads(data)
    # Extract relevant data from the JSON
    timestamp = json_data["sunucusaati"]
    aircraft_stats = json_data["konumBilgileri"]

    # if user wants to stop the program
    if keyboard.is_pressed('q'):
        break

    # Process aircraft stats and store in the aircraft_data dictionary
    if aircraft_stats:
        for aircraft in aircraft_stats:
            takim_numarasi = aircraft["takim_numarasi"]

            if takim_numarasi not in aircraft_data:
                aircraft_data[takim_numarasi] = []
                takim_numaralari.append(takim_numarasi)

            data_row = {
                "timestamp": pd.to_datetime(f"{timestamp['saat']}:{timestamp['dakika']}:"
                                            f"{timestamp['saniye']}:{timestamp['milisaniye']}", format='%H:%M:%S:%f'),
                "takim_numarasi": takim_numarasi,
                "iha_enlem": aircraft["iha_enlem"],
                "iha_boylam": aircraft["iha_boylam"],
                "iha_irtifa": aircraft["iha_irtifa"],
                "iha_dikilme": aircraft["iha_dikilme"],
                "iha_yonelme": aircraft["iha_yonelme"],
                "iha_yatis": aircraft["iha_yatis"],
                "zaman_farki": aircraft["zaman_farki"]
                # Add other aircraft statistics as needed
            }

            # add sent_time to data_row
            data_row['sent_time'] = (data_row['timestamp'] - pd.to_timedelta(data_row['zaman_farki'], unit='ms'))

            # Convert "enlem" and "boylam" to meters
            data_row['iha_enlem_meters'] = haversine(ref_latitude, ref_longitude, data_row['iha_enlem'], ref_longitude)
            data_row['iha_boylam_meters'] = haversine(ref_latitude, ref_longitude, ref_latitude, data_row['iha_boylam'])

            aircraft_data[takim_numarasi].append(data_row)

    for takim_numarasi in takim_numaralari:
        airdata = []
        for data in aircraft_data[takim_numarasi]:
            airdata.append(data)
        window = airdata[-5:]
        print(window)
        coords = window[['iha_enlem_meters', 'iha_boylam_meters']].values
        timestamps = window['sent_time']
        speeds = []
        for i in range(1, len(coords)):
            time_diff = (timestamps.iloc[i] - timestamps.iloc[i - 1]).total_seconds()
            distance = calculate_cartesian_distance(coords[i - 1], coords[i])
            speeds.append(distance / time_diff if time_diff != 0 else 0)
        average_speed = sum(speeds) / len(speeds) if speeds else 0
        current_position = coords[-1]
        current_heading = window.iloc[-1]['iha_yonelme']
        new_position = predict_new_position(current_position, current_heading, average_speed)
        print(new_position)
        print(current_position)

#print all data in aircraft_data for aircraft with takim_numarasi = 3

