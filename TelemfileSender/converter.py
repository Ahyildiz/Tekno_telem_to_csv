import os
import json
import csv
global total_team_number

total_team_number = 0
json_directory = "C:\\Users\\ahyil\\PycharmProjects\\Tekno_telem_to_csv"
def process_json_files(directory_path):
    global total_team_number
    total_team_number += 1
    aircraft_data = {}  # Reset the aircraft_data dictionary for each competition
    for root, _, files in os.walk(directory_path):
        for filename in files:
            if filename.endswith(".json"):
                file_path = os.path.join(root, filename)
                with open(file_path, "r") as json_file:
                    print(f"Processing {file_path}...")
                    # Load JSON content into a dictionary
                    json_data = json.load(json_file)

                    # Extract relevant data from the JSON
                    timestamp = json_data["sunucusaati"]
                    aircraft_stats = json_data["konumBilgileri"]

                    # Process aircraft stats and store in the aircraft_data dictionary
                    if aircraft_stats:
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
        csv_file_path = os.path.join(json_directory, f"aircraft_{takim_numarasi}_{total_team_number}.csv")
        with open(csv_file_path, "w", newline="") as csv_file:
            fieldnames = ["timestamp", "takim_numarasi", "iha_enlem", "iha_boylam", "iha_irtifa",
                          "iha_dikilme", "iha_yonelme", "iha_yatis", "zaman_farki"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            # Write the header
            writer.writeheader()

            # Write the data rows
            writer.writerows(data_list)

def main():
    # Directory containing the JSON files (and subdirectories)


    # Search through all folders and convert JSON files to CSV files
    for root, dirs, _ in os.walk(json_directory):
        print(f"Processing {root}...")
        if "TeknoTelem" in dirs:
            tekno_telem_path = os.path.join(root, "TeknoTelem")
            print("calling process_json_files with path: ", tekno_telem_path)
            process_json_files(tekno_telem_path)
        if "Tekno" in dirs:
            tekno_telem_path = os.path.join(root, "Tekno")
            print("calling process_json_files with path: ", tekno_telem_path)
            process_json_files(tekno_telem_path)

    print("CSV files creation completed!")

if __name__ == "__main__":
    main()
