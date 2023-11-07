import numpy as np
import pandas as pd
from filterpy.kalman import KalmanFilter
from filterpy.common import Q_discrete_white_noise

# Load your UAV data from the CSV file
data = pd.read_csv('C:\\Users\\ahyil\\PycharmProjects\\Tekno_telem_to_csv\\new.csv')

# Create a Kalman Filter for your specific application with 3 dimensions
kf = KalmanFilter(dim_x=3, dim_z=3)

# Define the state transition matrix (A)
dt = 1.0  # Time step
kf.F = np.array([[1, dt, 0],
                [0, 1, 0],
                [0, 0, 1]])

# Define the measurement function (H)
kf.H = np.array([[1, 0, 0],
                [0, 0, 1],
                [0, 1, 0]])

# Initialize the state estimate (x) and covariance matrix (P)
kf.x = np.array(data.iloc[0][1:4])  # Initial state based on the first row of data
kf.P *= 0.1  # Initial covariance matrix

# Define the process noise covariance matrix (Q)
q = Q_discrete_white_noise(dim=3, dt=dt, var=0.01)
kf.Q[0:3, 0:3] = q

# Define the measurement noise covariance matrix (R)
kf.R = np.eye(3) * 0.1  # You can adjust the measurement noise covariance

# Iterate over the data and predict the next state
for index, row in data.iterrows():
    measurement = np.array(row[1:4])
    kf.predict()
    kf.update(measurement)

# Extract the estimated state (latitude, longitude, and altitude) of the UAV
estimated_state = kf.x

# Print the estimated state
print("Estimated State (Enlem, Boylam, İrtifa):", estimated_state)
