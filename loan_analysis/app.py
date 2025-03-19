import pandas as pd
import numpy as np
import os
import joblib
import gradio as gr
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# Define dataset path
dataset_path = r"C:\Users\ASUS\Desktop\RISK_ANALYSIS\loan_analysis\corrected_loan_dataset.csv"

# Load dataset
try:
    df = pd.read_csv(dataset_path)
    print("✅ Dataset loaded successfully!")
except FileNotFoundError:
    print(f"❌ Error: Dataset not found at {dataset_path}")
    exit()

df.columns = df.columns.str.lower()

# Check if 'loan_status' column exists, if not, rename 'defaulted'
if "loan_status" not in df.columns and "defaulted" in df.columns:
    df.rename(columns={"defaulted": "loan_status"}, inplace=True)
elif "loan_status" not in df.columns:
    print("❌ Error: No suitable target column found!")
    exit()

X = df.drop(columns=["loan_status"])
y = df["loan_status"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Identify numeric & categorical features
numeric_features = X_train.select_dtypes(include=np.number).columns.tolist()
categorical_features = X_train.select_dtypes(exclude=np.number).columns.tolist()

# Define preprocessing pipelines
numeric_transformer = Pipeline([
    ('imputer', SimpleImputer(strategy='mean')),  # Handle missing values
    ('scaler', StandardScaler())  # Scale numeric data
])

categorical_transformer = Pipeline([
    ('imputer', SimpleImputer(strategy='most_frequent')),  # Handle missing values
    ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))  # Encode categorical data
])

preprocessor = ColumnTransformer([
    ('num', numeric_transformer, numeric_features),
    ('cat', categorical_transformer, categorical_features)
])

# Build model pipeline
model = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(
        n_estimators=200,
        class_weight='balanced',
        random_state=42,
        n_jobs=-1
    ))
])

# Train model
model.fit(X_train, y_train)

# Save model
model_path = "loan_risk/loan_risk_model.pkl"
os.makedirs(os.path.dirname(model_path), exist_ok=True)
joblib.dump(model, model_path)
print(f"✅ Model saved at {model_path}")

# Load model for Gradio
model = joblib.load(model_path)

# Prediction function
def predict_loan_status(monthly_income, employment_status, existing_loans, 
                        credit_score, loan_purpose, loan_amount_requested,
                        debt_to_income_ratio, repayment_history):
    try:
        # Create input DataFrame
        input_data = pd.DataFrame({
            "monthly_income": [monthly_income],
            "employment_status": [employment_status],
            "existing_loans": [existing_loans],
            "credit_score": [credit_score],
            "loan_purpose": [loan_purpose],
            "loan_amount_requested": [loan_amount_requested],
            "debt_to_income_ratio": [debt_to_income_ratio],
            "repayment_history": [repayment_history]
        })
        
        # Ensure numeric conversion for numerical columns
        for col in ["monthly_income", "existing_loans", "credit_score", "loan_amount_requested", "debt_to_income_ratio"]:
            input_data[col] = pd.to_numeric(input_data[col], errors='coerce')

        # Fill missing values
        input_data.fillna(0, inplace=True)

        # Preprocess input
        input_transformed = model.named_steps['preprocessor'].transform(input_data)

        # Make prediction
        prediction = model.named_steps['classifier'].predict(input_transformed)[0]

        return "✅ Low Risk (Not Default)" if prediction == 0 else "⚠️ High Risk (Default)"

    except Exception as e:
        return f"❌ Prediction Error: {str(e)}"

# Gradio UI
inputs = [
    gr.Number(label="Monthly Income ($)"),
    gr.Dropdown(["Employed", "Unemployed", "Self-Employed"], label="Employment Status"),
    gr.Number(label="Existing Loans Count"),
    gr.Slider(300, 850, label="Credit Score"),
    gr.Dropdown(["Home Improvement", "Debt Consolidation", "Business", "Education"], label="Loan Purpose"),
    gr.Number(label="Loan Amount ($)"),
    gr.Slider(0, 100, label="Debt-to-Income Ratio (%)"),
    gr.Dropdown(["Good", "Fair", "Poor"], label="Repayment History")
]

interface = gr.Interface(
    fn=predict_loan_status,
    inputs=inputs,
    outputs=gr.Textbox(label="Risk Assessment"),
    title="💰 Loan Default Risk Predictor",
    description="Enter applicant details to assess the risk of loan default.",
    theme="default"
)

# Launch Gradio
if __name__ == "__main__":
    interface.launch(share=True)
