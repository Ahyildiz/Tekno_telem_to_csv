import os
import json
import csv

# Directory containing the JSON files
json_directory = "19-08-2022/TeknoTelem"

# Dictionary to store data for each aircraft
aircraft_data = {}

# Loop through each JSON file in the directory
for filename in os.listdir(json_directory):
    if filename.endswith(".json"):
        file_path = os.path.join(json_directory, filename)
        with open(file_path, "r") as json_file:
            # Load JSON content into a dictionary
            json_data = json.load(json_file)

            # Extract relevant data from the JSON
            timestamp = json_data["sunucusaati"]
            aircraft_stats = json_data["konumBilgileri"]

            # Process aircraft stats and store in the aircraft_data dictionary
            for aircraft in aircraft_stats:
                takim_numarasi = aircraft["takim_numarasi"]

                if takim_numarasi not in aircraft_data:
                    aircraft_data[takim_numarasi] = []

                data_row = {
                    "timestamp": f"{timestamp['saat']}:{timestamp['dakika']}:{timestamp['saniye']}",
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

                aircraft_data[takim_numarasi].append(data_row)

# Write data for each aircraft to separate CSV files
for takim_numarasi, data_list in aircraft_data.items():
    csv_file_path = f"aircraft_{takim_numarasi}.csv"
    with open(csv_file_path, "w", newline="") as csv_file:
        fieldnames = ["timestamp", "takim_numarasi", "iha_enlem", "iha_boylam", "iha_irtifa",
                      "iha_dikilme", "iha_yonelme", "iha_yatis", "zaman_farki"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        # Write the header
        writer.writeheader()

        # Write the data rows
        writer.writerows(data_list)

print("CSV files creation completed!")