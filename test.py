import pandas as pd

# Read the input CSV file
df = pd.read_csv('C:\\Users\\ahyil\\PycharmProjects\\Tekno_telem_to_csv\\csv_files\\aircraft_11_1.csv')

# Convert timestamp to datetime format
df['timestamp'] = pd.to_datetime(df['timestamp'], format='%H:%M:%S')

# Calculate sent_time using zaman_farki
df['sent_time'] = (df['timestamp'] - pd.to_timedelta(df['zaman_farki'], unit='ms')).dt.strftime('%H:%M:%S.%f')

# Drop the 'zaman_farki' column
df = df.drop(columns=['zaman_farki'])
df = df.drop(columns=['timestamp'])
df = df.drop(columns=['takim_numarasi'])

# Reorder the columns to take the 'sent_time' column to the front
cols = df.columns.tolist()
cols = cols[-1:] + cols[:-1]
df = df[cols]

# Save the output to a new CSV file in the same directory
df.to_csv('C:\\Users\\ahyil\\PycharmProjects\\Tekno_telem_to_csv\\new.csv', index=False)