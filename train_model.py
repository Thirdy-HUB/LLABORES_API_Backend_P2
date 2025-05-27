import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report
import joblib
import os

# Make sure folder for saving models exists
os.makedirs("trained_data", exist_ok=True)

# Load your dataset here
# For example: columns could be Internet_Access_at_Home, Parent_Education_Level, Stress_Level, Sleep_Hours_per_Night_Entier, Estimated_Grade
df = pd.read_csv('csv/student_data.csv')  # Replace with your dataset path

# For this example, let's create a binary target: Passed or Failed based on Estimated_Grade
# Let's assume Grades A,B,C,D = Passed; F = Failed
df['Passed'] = df['Estimated_Grade'].apply(lambda x: 0 if x == 'F' else 1)

# Features and target
X = df[['Internet_Access_at_Home', 'Parent_Education_Level', 'Stress_Level', 'Sleep_Hours_per_Night_Entier']]
y = df['Passed']

# Define categorical and numerical features
categorical_features = ['Internet_Access_at_Home', 'Parent_Education_Level']
numerical_features = ['Stress_Level', 'Sleep_Hours_per_Night_Entier']

# Preprocessing pipeline
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features),
        ('num', 'passthrough', numerical_features)
    ])

# Create a pipeline with preprocessing and classifier
model_pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', MLPClassifier(hidden_layer_sizes=(64,), activation='relu', max_iter=1000, random_state=42, early_stopping=True))
])

# Split data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model_pipeline.fit(X_train, y_train)

# Evaluate on test data
y_pred = model_pipeline.predict(X_test)
print("Classification Report:\n", classification_report(y_test, y_pred))

# Save the trained model pipeline
joblib.dump(model_pipeline, 'trained_data/grade_pass_model.pkl')

print("Model training complete and saved to 'trained_data/grade_pass_model.pkl'")
