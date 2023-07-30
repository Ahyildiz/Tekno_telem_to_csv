import os
import pandas as pd

def remove_constant_increase_from_end(filename):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(filename)
    # check if max value for the zaman_farki column is greater than 20000


    #do this until the last row is not the same as the row before it
    while df.tail(1)['iha_enlem'].values == df.iloc[-2]['iha_enlem'] and df.tail(1)['iha_boylam'].values == df.iloc[-2]['iha_boylam'] and df.tail(1)['iha_irtifa'].values == df.iloc[-2]['iha_irtifa'] and df.tail(1)['iha_dikilme'].values == df.iloc[-2]['iha_dikilme'] and df.tail(1)['iha_yonelme'].values == df.iloc[-2]['iha_yonelme'] and df.tail(1)['iha_yatis'].values == df.iloc[-2]['iha_yatis']:
        #drop the last row
        df.drop(df.tail(1).index, inplace=True)
        #save the new csv file
        df.to_csv(filename, index=False)
        print("Last row dropped")

    #do this from beginning to end
    while df.head(1)['iha_enlem'].values == df.iloc[1]['iha_enlem'] and df.head(1)['iha_boylam'].values == df.iloc[1]['iha_boylam'] and df.head(1)['iha_irtifa'].values == df.iloc[1]['iha_irtifa'] and df.head(1)['iha_dikilme'].values == df.iloc[1]['iha_dikilme'] and df.head(1)['iha_yonelme'].values == df.iloc[1]['iha_yonelme'] and df.head(1)['iha_yatis'].values == df.iloc[1]['iha_yatis']:
        #drop the first row
        df.drop(df.head(1).index, inplace=True)
        #save the new csv file
        df.to_csv(filename, index=False)
        print("First row dropped")

if __name__ == "__main__":

    file_path = "C:\\Users\\ahyil\\PycharmProjects\\Tekno_telem_to_csv"

    for root, _, files in os.walk(file_path):
        print(f"Processing {root}...")
        for filename in files:
            if filename.endswith(".csv"):
                file_path = os.path.join(root, filename)
                remove_constant_increase_from_end(file_path)


