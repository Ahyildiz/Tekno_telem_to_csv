from math import sqrt

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error

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
            ['iha_enlem_meters', 'iha_boylam_meters', 'iha_irtifa', 'iha_dikilme', 'iha_yonelme', 'iha_yatis',
             'time_diff']].values
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
predicted_irtifa = []
actual_enlem = []
actual_boylam = []
actual_irtifa = []

# Iterate through the data points and predict the next state
for i in range(len(X)):
    if i < len(X) - 1:
        last_data_point = X[i].reshape(1, -1)
        next_state = model.predict(last_data_point)  # Predict the next state
        predictions.append(next_state)
        # Append "enlem" and "boylam" values to the respective lists
        predicted_enlem.append(next_state[0, 0])
        predicted_boylam.append(next_state[0, 1])
        predicted_irtifa.append(next_state[0, 2])
        actual_enlem.append(y[i][0])
        actual_boylam.append(y[i][1])
        actual_irtifa.append(y[i][2])

# Convert the predictions list to a numpy array
predicted_states = np.vstack(predictions)

errors = []
for i in range(len(predicted_states)):
    errx = predicted_states[i][0] - y[i][0]
    erry = predicted_states[i][1] - y[i][1]
    errz = predicted_states[i][2] - y[i][2]
    errors.append(sqrt(errx ** 2 + erry ** 2 + errz ** 2))

# Display the predicted next states and the corresponding errors
for i in range(len(predicted_states)):
    print("predicted:", predicted_states[i])
    print("actual:", y[i])
    print("error: ", errors[i])

print("border for planes:")
print("width: ", np.max(actual_enlem) - np.min(actual_enlem))
print("height: ", np.max(actual_boylam) - np.min(actual_boylam))
print("depth: ", np.max(actual_irtifa) - np.min(actual_irtifa))
print("average error as a percentage of the border: ",
      (np.mean(errors) / 577.799394892) * 100, "%")
print("mean error: ", np.mean(errors), "meters")
print("std error: ", np.std(errors), "meters")
print("max error: ", np.max(errors), "meters")
print("min error: ", np.min(errors), "meters")
print("median error: ", np.median(errors), "meters")
print("variance error: ", np.var(errors))
print("mean squared error: ", mean_squared_error(predicted_states, y[0:len(predicted_states)]))

# Plot "enlem" and "boylam"  and "irtifa" for predicted and real values in a 3D plane

fig = plt.figure()
ax = plt.figure().add_subplot(projection='3d')
ax.plot(predicted_enlem, predicted_boylam, predicted_irtifa, label='predicted')
ax.plot(actual_enlem, actual_boylam, actual_irtifa, label='actual')

plt.show()
