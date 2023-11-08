import time
from math import sqrt

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime
import matplotlib.pyplot as plt
from threading import Thread
import tkinter as tk
from tkinter import filedialog
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk,
)

import matplotlib

matplotlib.use('TkAgg')
# Load the CSV data into a Pandas DataFrame
data = pd.read_csv('C:\\Users\\ahyil\\PycharmProjects\\Tekno_telem_to_csv\\new2.csv')

# Convert the 'sent_time' column to datetime objects
data['sent_time'] = data['sent_time'].apply(lambda x: datetime.strptime(x, '%H:%M:%S.%f'))

# Calculate the time difference between data points
data['time_diff'] = (data['sent_time'] - data['sent_time'].shift()).dt.total_seconds()
data['time_diff'].fillna(0, inplace=True)


def twoDistance(x1, y1, x2, y2):
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


# Function to create a rolling window of the last 5 data points
def create_rolling_window(data, window_size=10):
    features = []
    targets = []
    for i in range(len(data) - window_size):
        feature_window = data.iloc[i:i + window_size][
            ['iha_enlem_meters', 'iha_boylam_meters', 'iha_irtifa', 'iha_dikilme', 'iha_yonelme',
             'iha_yatis', 'time_diff']].values
        target = data.iloc[i + window_size][
            ['iha_enlem_meters', 'iha_boylam_meters', 'iha_irtifa', 'iha_dikilme', 'iha_yonelme',
             'iha_yatis']].values
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
    print("error: ", sqrt(errx ** 2 + erry ** 2))
    print()


def drawThread(ax):
    # Plot "enlem" and "boylam" for predicted and real values in a 2D plane
    time.sleep(2)
    predctArr = []
    actualArr = []
    maxDistance = 0
    for i in range(len(predicted_enlem)):
        if (len(predctArr) < 30):
            predctArr.append([predicted_enlem[i], predicted_boylam[i]])
            actualArr.append([actual_enlem[i], actual_boylam[i]])
        else:
            predctArr.pop(0)
            actualArr.pop(0)
            predctArr.append([predicted_enlem[i], predicted_boylam[i]])
            actualArr.append([actual_enlem[i], actual_boylam[i]])

        ax.clear()
        ax.plot([x[0] for x in predctArr], [x[1] for x in predctArr], 'r', label="predicted")
        ax.plot([x[0] for x in actualArr], [x[1] for x in actualArr], 'b', label="actual")

        distance = twoDistance(predicted_enlem[i], predicted_boylam[i], actual_enlem[i], actual_boylam[i])
        distancestr = float('{0:.2f}'.format(distance))
        ax.text(1400, 1600, "distance: " + str(distancestr))
        if (distance > maxDistance):
            maxDistance = distance

        time.sleep(0.04)
        ax.legend()
        ax.set_xlim(1000, 1800)
        ax.set_ylim(1500, 1800)
        canvas.draw()

    print("maxDistance: ", maxDistance)

    ax.arrow(1380, 1650, 1, 1, width=1, color='r',
             head_starts_at_zero=True,
             length_includes_head=True, clip_on=False)


if __name__ == '__main__':
    root = tk.Tk()
    root.configure(background="white")
    root.geometry("1500x1050")
    root.resizable(0, 0)
    fig = Figure(figsize=(6, 4), dpi=100)
    canvas = FigureCanvasTkAgg(fig, master=root)

    canvas.get_tk_widget().place(x=0, y=50, width=1400, height=900)
    canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

    imagecanvas = tk.Canvas(root, width=50, height=50, bg="white")

    toolbarFrame = tk.Frame(master=root)
    toolbarFrame.place(x=0, y=0, width=370, height=42)
    toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)

    ax = fig.subplots()
    ax.set_xlim(1300, 1800)
    ax.set_ylim(1000, 1500)
    Thread(target=drawThread, args=(ax,)).start()

    root.mainloop()
