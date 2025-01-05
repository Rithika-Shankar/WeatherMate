import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor

# Load the dataset
data = pd.read_csv('disaster.csv')

# Preprocess the data
features = ['Year', 'Disaster Group', 'Disaster Type', 'Total Deaths', 'No Injured', 'No Affected']
X = data[features]
y = data["Total Damages ('000 US$)"]

# Handle missing values
data.fillna(method='ffill', inplace=True)
y = y.fillna(y.mean())

# Identify categorical and numerical features
categorical_features = ['Disaster Group', 'Disaster Type']
numeric_features = ['Year', 'Total Deaths', 'No Injured', 'No Affected']

# Create transformers for preprocessing
numeric_transformer = StandardScaler()
categorical_transformer = OneHotEncoder(handle_unknown='ignore')

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ])

# Create a pipeline with the preprocessor and model
pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('model', RandomForestRegressor())
])

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
pipeline.fit(X_train, y_train)

# Predict
y_pred = pipeline.predict(X_test)

print("Resource optimization model trained and predictions made!")
