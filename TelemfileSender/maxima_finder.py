import pandas as pd
import os


def has_multiple_local_maxima(df, threshold, window_size=3):
    # Create a rolling window to find local maxima
    rolling_max = df['zaman_farki'].rolling(window=window_size, center=True).max()

    # Check if there are multiple local maxima above the threshold
    local_maxima = (df['zaman_farki'] == rolling_max) & (rolling_max > threshold)

    return local_maxima.sum()


# Load the CSV file into a DataFrame
folder_path = 'C:\\Users\\ahyil\\PycharmProjects\\Tekno_telem_to_csv\\csv_files'  # Replace with the actual file path
only_one_maxima_files = []

#check every file in the folder
for root, _, files in os.walk(folder_path):
    print(f"Processing {root}...")
    for filename in files:
        if filename.endswith(".csv"):
            file_path = os.path.join(root, filename)
            df = pd.read_csv(file_path)
            threshold_value = 10000
            result = has_multiple_local_maxima(df, threshold_value)
            print(f"{filename} has {result} local maxima above {threshold_value}")
            if result == 1:
                only_one_maxima_files.append(filename)


for file in only_one_maxima_files:
    print(file)
    #split the file into two parts and save them
    file_path = os.path.join(folder_path, file)
    df = pd.read_csv(file_path)
    #from beginnig to the maxima
    df1 = df.iloc[:df['zaman_farki'].idxmax()]
    df1.to_csv(os.path.join(folder_path, file[:-4] + "_1.csv"), index=False)
    #from maxima to the end
    df2 = df.iloc[df['zaman_farki'].idxmax():]
    df2.to_csv(os.path.join(folder_path, file[:-4] + "_2.csv"), index=False)

