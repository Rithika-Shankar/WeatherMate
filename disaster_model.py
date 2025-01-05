import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import LabelEncoder
import joblib

# Load the dataset (assuming it's in the same directory)
data = pd.read_csv('disasters.csv')

# Preprocessing the data
# Convert categorical features to numerical using LabelEncoder
label_encoder = LabelEncoder()

# Columns that might need encoding (just examples, you can extend this)
categorical_columns = ['Disaster Group', 'Disaster Type', 'Country', 'Region', 'Continent', 'Disaster Subgroup']

# Apply label encoding
for column in categorical_columns:
    data[column] = label_encoder.fit_transform(data[column].astype(str))

# Fill or remove missing values (depends on your use case)
data.fillna(0, inplace=True)

# Define the target and features
# You can choose what to predict (e.g., Total Deaths, Total Affected, etc.)
# Example: We want to predict 'Total Deaths' as a binary outcome (e.g., 0 or 1)
data['High Impact'] = data['Total Deaths'].apply(lambda x: 1 if x > 1000 else 0)

# Features (drop the target variable and some irrelevant columns)
features = data.drop(columns=['Total Deaths', 'High Impact', 'Event Name', 'Geo Locations', 'Latitude', 'Longitude'])

# Define the target variable
target = data['High Impact']

# Split data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

# Model training using Random Forest
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Evaluate the model
print(f"Accuracy: {accuracy_score(y_test, y_pred)}")
print(classification_report(y_test, y_pred))

# Save the model for future use
joblib.dump(model, 'disaster_predictor_model.pkl')

print("Model saved as disaster_predictor_model.pkl")
