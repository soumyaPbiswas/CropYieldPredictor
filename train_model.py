import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import joblib
import os

# Load CSVs
rainfall_df = pd.read_csv('data/rainfall.csv')
temp_df = pd.read_csv('data/temp.csv')
pesticide_df = pd.read_csv('data/pesticides.csv')
yield_df = pd.read_csv('data/yield.csv')

print("✅ CSVs Loaded")


# Replace '..' with NaN
for df in [rainfall_df, temp_df, pesticide_df, yield_df]:
    df.replace('..', pd.NA, inplace=True)

# Convert relevant columns to numeric
rainfall_df['average_rain_fall_mm_per_year'] = pd.to_numeric(rainfall_df['average_rain_fall_mm_per_year'], errors='coerce')
temp_df['avg_temp'] = pd.to_numeric(temp_df['avg_temp'], errors='coerce')
pesticide_df['Value'] = pd.to_numeric(pesticide_df['Value'], errors='coerce')
yield_df['Value'] = pd.to_numeric(yield_df['Value'], errors='coerce')


# Clean column names (strip whitespaces)
rainfall_df.columns = rainfall_df.columns.str.strip()
temp_df.columns = temp_df.columns.str.strip()
pesticide_df.columns = pesticide_df.columns.str.strip()
yield_df.columns = yield_df.columns.str.strip()

# Rename columns for consistency
rainfall_df = rainfall_df.rename(columns={
    'Area': 'Country',
    'average_rain_fall_mm_per_year': 'Rainfall'
})[['Country', 'Year', 'Rainfall']]

temp_df = temp_df.rename(columns={
    'country': 'Country',
    'avg_temp': 'Temperature'
})[['Country', 'Year', 'Temperature']]

pesticide_df = pesticide_df.rename(columns={
    'Area': 'Country',
    'Value': 'Pesticide'
})[['Country', 'Year', 'Pesticide']]

yield_df = yield_df.rename(columns={
    'Area': 'Country',
    'Item': 'Crop',
    'Value': 'Yield'
})[['Country', 'Year', 'Crop', 'Yield']]

# Merge datasets
data = yield_df.merge(rainfall_df, on=['Country', 'Year'], how='left')
data = data.merge(temp_df, on=['Country', 'Year'], how='left')
data = data.merge(pesticide_df, on=['Country', 'Year'], how='left')

# Drop rows with missing values
data = data.dropna()

# Encode categorical variables
data = pd.get_dummies(data, columns=['Country', 'Crop'], drop_first=True)

# Split into features and target
X = data.drop(columns=['Yield'])
y = data['Yield']

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
rmse = mean_squared_error(y_test, y_pred, squared=False)
print(f"✅ Model trained successfully. RMSE on test set: {rmse:.2f}")



# Save model and feature names
joblib.dump((model, X.columns.tolist()), 'crop_yield_model.pkl')

print("✅ Model saved as 'crop_yield_model.pkl'")
