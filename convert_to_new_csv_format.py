import pandas as pd
import math

# Reference point in degrees
ref_latitude = 41.5
ref_longitude = 36.0

# Radius of the Earth in meters
earth_radius = 6371000

def haversine(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = earth_radius * c

    return distance



# Read the input CSV file
df = pd.read_csv('C:\\Users\\ahyil\\PycharmProjects\\Tekno_telem_to_csv\\csv_files\\aircraft_11_1.csv')

# Convert timestamp to datetime format
df['timestamp'] = pd.to_datetime(df['timestamp'], format='%H:%M:%S')

# Calculate sent_time using zaman_farki
df['sent_time'] = (df['timestamp'] - pd.to_timedelta(df['zaman_farki'], unit='ms')).dt.strftime('%H:%M:%S.%f')

# Drop the 'zaman_farki' column
df = df.drop(columns=['zaman_farki'])
df = df.drop(columns=['takim_numarasi'])

# Reorder the columns to take the 'sent_time' column to the front


# Convert "enlem" and "boylam" to meters
df['iha_enlem_meters'] = df.apply(lambda row: haversine(ref_latitude, ref_longitude, row['iha_enlem'], ref_longitude), axis=1)
df['iha_boylam_meters'] = df.apply(lambda row: haversine(ref_latitude, ref_longitude, ref_latitude, row['iha_boylam']), axis=1)
df = df.drop(columns=['iha_enlem', 'iha_boylam'])
df['timestamp'] = df['timestamp'].dt.strftime('%H:%M:%S.%f')
#remove miliseconds from timestamp
df['timestamp'] = df['timestamp'].str[:-7]


#reorder the columns to take the 'iha_enlem_meters' and 'iha_boylam_meters' columns to the front
cols = df.columns.tolist()
cols = cols[-3:] + cols[:-3]
df = df[cols]
# Print the updated DataFrame
print(df)
# Save the output to a new CSV file in the same directory
df.to_csv('C:\\Users\\ahyil\\PycharmProjects\\Tekno_telem_to_csv\\new2.csv', index=False)