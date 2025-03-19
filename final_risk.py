import gradio as gr
import pandas as pd
import numpy as np
import shap
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import LabelEncoder
import xgboost as xgb

# Load dataset
df = pd.read_csv(r'C:\Users\ASUS\Desktop\RISK_ANALYSIS\final_corrected_loan_dataset_realistic.csv')

# Store serial numbers separately
serial_numbers = df['serial_number']
df = df.drop(columns=['serial_number'])

# Encode categorical features
label_encoders = {}
categorical_columns = ['employment_status', 'loan_purpose', 'repayment_history']

for col in categorical_columns:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# Handle missing values
df.fillna(df.median(numeric_only=True), inplace=True)

# Split data into features and target
X = df.drop(columns=['defaulted'])
y = df['defaulted']

# Split into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Handle class imbalance with SMOTE
smote = SMOTE(random_state=42)
X_train, y_train = smote.fit_resample(X_train, y_train)

# XGBoost Classifier
xgb_model = xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss')

# Hyperparameter Grid Search
param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [3, 5, 7],
    'learning_rate': [0.01, 0.1, 0.2],
    'subsample': [0.8, 1.0],
    'colsample_bytree': [0.8, 1.0],
    'gamma': [0, 0.1, 0.2]
}

grid_search = GridSearchCV(estimator=xgb_model, param_grid=param_grid, cv=3, scoring='accuracy', verbose=3, n_jobs=-1)
grid_search.fit(X_train, y_train)

# Best Model
best_model = grid_search.best_estimator_

# SHAP Explainer
explainer = shap.Explainer(best_model, X_train)

# Function for prediction with explanation
def predict_risk(serial_number):
    if serial_number not in serial_numbers.values:
        return "Serial Number not found"
    
    record = df.iloc[serial_numbers[serial_numbers == serial_number].index]
    X_input = record.drop(columns=['defaulted'])
    prediction = best_model.predict(X_input)
    risk_label = "High Risk" if prediction[0] == 1 else "Low Risk"
    
    # SHAP explanation
    shap_values = explainer(X_input)
    feature_importances = np.abs(shap_values.values).mean(axis=0)
    most_important_feature = X.columns[np.argmax(feature_importances)]
    reason = f"{most_important_feature} is the most influential factor."
    
    return f"{risk_label}. Reason: {reason}"

# Gradio Interface
demo = gr.Interface(
    fn=predict_risk,
    inputs=[gr.Number(label="Serial Number")],
    outputs=gr.Textbox(label="Risk Analysis Result"),
    title="P2P Lending Risk Analysis",
    description="Enter serial number to predict default risk using XGBoost model. The output also provides a reason based on feature importance."
)

demo.launch()
