import os
import pandas as pd
import matplotlib.pyplot as plt

csv_directory = "C:\\Users\\ahyil\\PycharmProjects\\Tekno_telem_to_csv"

# Iterate through each file in the directory
for filename in os.listdir(csv_directory):
    if filename.endswith(".csv"):
        file_path = os.path.join(csv_directory, filename)

        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(file_path)

        # Plotting a time-series of the aircraft's latitude
        plt.figure(figsize=(10, 5))
        plt.plot(df['timestamp'], df['zaman_farki'])
        plt.xlabel('Timestamp')
        plt.ylabel('Aircraft Latitude')
        plt.title(f'Aircraft Latitude Over Time - {filename}')
        plt.grid(True)
        plt.savefig(f'aircraft_latitude_plot_{filename}.png')  # Save the plot as an image file
        plt.close()  # Close the plot to avoid overlapping in the next iteration

print("Plots generated for all CSV files!")
