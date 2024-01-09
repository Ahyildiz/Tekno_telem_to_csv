
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from datetime import datetime

# Function to create a rolling window of the last N data points
def create_rolling_window(data, window_size=10):
    features = []
    targets = []
    for i in range(len(data) - window_size):
        feature_window = data.iloc[i:i + window_size].drop(columns=['sent_time', 'timestamp'])
        target = data.iloc[i + window_size][['iha_enlem_meters', 'iha_boylam_meters', 'iha_irtifa', 'iha_dikilme', 'iha_yonelme', 'iha_yatis']]
        features.append(feature_window.values.flatten())
        targets.append(target.values)
    return np.array(features), np.array(targets)

# Load the dataset
data = pd.read_csv('new2.csv')

# Convert 'sent_time' and 'timestamp' to datetime
data['sent_time'] = data['sent_time'].apply(lambda x: datetime.strptime(x, '%H:%M:%S.%f'))
data['timestamp'] = pd.to_datetime(data['timestamp'], format='%H:%M:%S')

# Create rolling windows
window_size = 10
X, y = create_rolling_window(data, window_size)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Random Forest model
rf_model = RandomForestRegressor(n_estimators=100, random_state=42) # n_estimators is the number of trees
rf_model.fit(X_train, y_train)
rf_predictions = rf_model.predict(X_test)
rf_mse = mean_squared_error(y_test, rf_predictions)
print('Random Forest MSE:', rf_mse)


predicted_enlem = []
predicted_boylam = []
predicted_irtifa = []
actual_enlem = []
actual_boylam = []
actual_irtifa = []
errors = []
for i in range(len(rf_predictions)):
    predicted_enlem.append(rf_predictions[i][0])
    predicted_boylam.append(rf_predictions[i][1])
    predicted_irtifa.append(rf_predictions[i][2])
    actual_enlem.append(y_test[i][0])
    actual_boylam.append(y_test[i][1])
    actual_irtifa.append(y_test[i][2])
    errors.append(np.linalg.norm(rf_predictions[i] - y_test[i]))


print("average error as a percentage of the border: ",
      (np.mean(errors) / 577.799394892) * 100, "%")
print("mean error: ", np.mean(errors), "meters")
print("std error: ", np.std(errors), "meters")
print("max error: ", np.max(errors), "meters")
print("min error: ", np.min(errors), "meters")
print("median error: ", np.median(errors), "meters")
print("variance error: ", np.var(errors))
print("mean squared error: ", np.mean(np.square(errors)))

plt.figure(figsize=(8, 6))
plt.scatter(predicted_enlem, predicted_boylam, label='predicted')
plt.scatter(actual_enlem, actual_boylam, label='actual')

plt.xlabel('Enlem')
plt.ylabel('Boylam')
plt.title('Random Forest')
plt.legend()
plt.grid(True)
plt.show()
