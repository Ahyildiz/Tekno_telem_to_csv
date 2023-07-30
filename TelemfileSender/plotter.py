import os
import pandas as pd
import matplotlib.pyplot as plt

#csv_directory = "C:\\Users\\ahyil\\PycharmProjects\\Tekno_telem_to_csv\\TelemfileSender\\cleaned_files"
csv_directory = "C:\\Users\\ahyil\\PycharmProjects\\Tekno_telem_to_csv\\csv_files"
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
        plt.ylabel('Delay (ms)')
        plt.title(f'Airplane Delay Plot for {filename}')
        plt.grid(True)
        plt.savefig(f'{filename}_delay_plot.png')
        plt.close()  # Close the plot to avoid overlapping in the next iteration

print("Plots generated for all CSV files!")
