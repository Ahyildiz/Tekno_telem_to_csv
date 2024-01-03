from math import sqrt

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime
import matplotlib.pyplot as plt

# Load the CSV data into a Pandas DataFrame
data = pd.read_csv('C:\\Users\\ahyil\\PycharmProjects\\Tekno_telem_to_csv\\new2.csv')

# Convert the 'sent_time' column to datetime objects
data['sent_time'] = data['sent_time'].apply(lambda x: datetime.strptime(x, '%H:%M:%S.%f'))

# Calculate the time difference between data points
data['time_diff'] = (data['sent_time'] - data['sent_time'].shift()).dt.total_seconds()
data['time_diff'].fillna(0, inplace=True)

# Function to create a rolling window of the last 5 data points
def create_rolling_window(data, window_size=10):
    features = []
    targets = []
    for i in range(len(data) - window_size):
        feature_window = data.iloc[i:i + window_size][
            ['iha_enlem_meters', 'iha_boylam_meters', 'iha_irtifa', 'iha_dikilme', 'iha_yonelme', 'iha_yatis', 'time_diff']].values
        target = data.iloc[i + window_size][
            ['iha_enlem_meters', 'iha_boylam_meters', 'iha_irtifa', 'iha_dikilme', 'iha_yonelme', 'iha_yatis']].values
        features.append(feature_window)
        targets.append(target)
    return np.array(features), np.array(targets)

# Create features and targets using the rolling window
X, y = create_rolling_window(data, window_size=10)

# Create a model (not linear regression)
model = LinearRegression()

# Create an empty list to store predictions
predictions = []

# Reshape the input data to be 2D
X = X.reshape(X.shape[0], -1)

# Fit the model on the entire dataset
model.fit(X, y)

# Create lists to store predicted and actual "enlem" and "boylam" values
predicted_enlem = []
predicted_boylam = []
actual_enlem = []
actual_boylam = []

# Iterate through the data points and predict the next state
for i in range(len(X)):
    if i < len(X) - 1:
        last_data_point = X[i].reshape(1, -1)
        next_state = model.predict(last_data_point)  # Predict the next state
        predictions.append(next_state)
        # Append "enlem" and "boylam" values to the respective lists
        predicted_enlem.append(next_state[0, 0])
        predicted_boylam.append(next_state[0, 1])
        actual_enlem.append(y[i][0])
        actual_boylam.append(y[i][1])

# Convert the predictions list to a numpy array
predicted_states = np.vstack(predictions)

# Display the predicted next states and the corresponding errors
for i in range(len(predicted_states)):
    print(f"Predicted Next State {i + 1}:")
    print(predicted_states[i])
    print(f"Actual Next State {i + 1}:")
    print(y[i])
    errx = predicted_states[i][0] - y[i][0]
    erry = predicted_states[i][1] - y[i][1]
    print("error: ", sqrt(errx**2+erry**2))
    print()

# Plot "enlem" and "boylam" for predicted and real values in a 2D plane with small plots
plt.figure(figsize=(8, 6))
plt.scatter(predicted_enlem, predicted_boylam, label='Predicted')
plt.scatter(actual_enlem, actual_boylam, label='Actual')

plt.xlabel('Enlem')
plt.ylabel('Boylam')
plt.title('Linear Regression')
plt.legend()
plt.grid(True)
plt.show()
