import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

from keras import layers
from keras.layers import LSTM, Dense
from keras.models import Sequential


# Load the CSV data into a DataFrame
df = pd.read_csv('../csv_files/aircraft_11_6.csv')

# Remove any rows with missing values (if present)
df.dropna(inplace=True)

# Convert timestamp to datetime object if it's in string format
# df['timestamp'] = pd.to_datetime(df['timestamp'])

# Drop irrelevant columns (if any) - 'timestamp' and 'takim_numarasi' in this case
df.drop(columns=['timestamp', 'takim_numarasi'], inplace=True)

# Normalize the features using Min-Max scaling to bring values within [0, 1] range
scaler = MinMaxScaler()
df_scaled = scaler.fit_transform(df)

# Define the number of previous time steps to use for prediction
n_steps = 30

# Initialize lists to store input sequences and corresponding outputs
X, y = [], []

# Create sequences and corresponding outputs
for i in range(n_steps, len(df_scaled)):
    X.append(df_scaled[i - n_steps:i])
    y.append(df_scaled[i])

# Convert lists to numpy arrays
X = np.array(X)
y = np.array(y)

# Assuming an 80-20 train-test split
split_ratio = 0.8
split_index = int(split_ratio * len(X))

X_train, X_test = X[:split_index], X[split_index:]
y_train, y_test = y[:split_index], y[split_index:]

model = Sequential()

# Add an LSTM layer with 50 units
model.add(LSTM(50, activation='relu', input_shape=(n_steps, df_scaled.shape[1])))

# Add a dense output layer
model.add(Dense(df_scaled.shape[1]))

# Compile the model
model.compile(optimizer='adam', loss='mse')

# Train the model
model.fit(X_train, y_train, epochs=1000, batch_size=64, verbose=1)

# Make predictions on the test data
y_pred = model.predict(X_test)

# Inverse transform the predictions and true values to their original scale
y_pred_original = scaler.inverse_transform(y_pred)
y_test_original = scaler.inverse_transform(y_test)

# Display the predicted and actual locations for the last time step in the test set
predicted_location = y_pred_original[-1, 2:4]  # Extract latitude and longitude
actual_location = y_test_original[-1, 2:4]

print("Predicted location:", predicted_location)
print("Actual location:", actual_location)
