import pandas as pd
import numpy as np
import math

from matplotlib import pyplot as plt
from sklearn.metrics import mean_squared_error

# Function to calculate Euclidean distance between two points
def calculate_cartesian_distance(point1, point2):
    return np.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)

# Function to predict new position based on current position, heading, and speed
def predict_new_position(current_position, heading, speed, time_interval=1):
    heading_radians = math.radians(heading)
    dx = speed * math.cos(heading_radians) * time_interval
    dy = speed * math.sin(heading_radians) * time_interval
    return current_position[0] + dx, current_position[1] + dy

# Function to create a rolling window for the last 3 data points
def create_rolling_window(data):
    window_size = 3
    rolling_windows = []
    for i in range(len(data) - window_size + 1):
        window = data.iloc[i:i + window_size]
        rolling_windows.append(window)
    return rolling_windows

# Load the CSV file
df = pd.read_csv('C:\\Users\\ahyil\\PycharmProjects\\Tekno_telem_to_csv\\new2.csv')


# Convert 'sent_time' to datetime
df['sent_time'] = pd.to_datetime(df['sent_time'])

# Create rolling windows
windows = create_rolling_window(df)

# For loop to predict all next points
predicted_positions = []
actual_positions = []
for window in windows:
    coords = window[['iha_enlem_meters', 'iha_boylam_meters']].values
    timestamps = window['sent_time']
    speeds = []
    for i in range(1, len(coords)):
        time_diff = (timestamps.iloc[i] - timestamps.iloc[i - 1]).total_seconds()
        distance = calculate_cartesian_distance(coords[i - 1], coords[i])
        speeds.append(distance / time_diff if time_diff != 0 else 0)
    average_speed = sum(speeds) / len(speeds) if speeds else 0
    current_position = coords[-1]
    current_heading = window.iloc[-1]['iha_yonelme']
    new_position = predict_new_position(current_position, current_heading, average_speed)
    predicted_positions.append(new_position)
    actual_positions.append(coords[-1])

for i in range(len(predicted_positions)):
    print('Predicted position:', predicted_positions[i])
    print('Actual position:', actual_positions[i])
    print('Distance between predicted and actual:', calculate_cartesian_distance(predicted_positions[i], actual_positions[i]))
    print('-------------------------------------')


predicted_enlem = []
predicted_boylam = []
actual_enlem = []
actual_boylam = []
errors = []
for i in range(len(predicted_positions)):
    predicted_enlem.append(predicted_positions[i][0])
    predicted_boylam.append(predicted_positions[i][1])
    actual_enlem.append(actual_positions[i][0])
    actual_boylam.append(actual_positions[i][1])
    errors.append(calculate_cartesian_distance(predicted_positions[i], actual_positions[i]))

print("average error as a percentage of the border: ",
      (np.mean(errors) / 577.799394892) * 100, "%")
print("mean error: ", np.mean(errors), "meters")
print("std error: ", np.std(errors), "meters")
print("max error: ", np.max(errors), "meters")
print("min error: ", np.min(errors), "meters")
print("median error: ", np.median(errors), "meters")
print("variance error: ", np.var(errors))
print("mean squared error: ", mean_squared_error(predicted_positions, actual_positions))


plt.figure(figsize=(8, 6))
plt.scatter(predicted_enlem, predicted_boylam, label='Predicted')
plt.scatter(actual_enlem, actual_boylam, label='Actual')

plt.xlabel('Enlem')
plt.ylabel('Boylam')
plt.title('Mathematical Model')
plt.legend()
plt.grid(True)
plt.show()

