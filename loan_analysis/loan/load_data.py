import pandas as pd
from loan.models import LoanApplication

# Load the CSV file
df = pd.read_csv("expanded_loan_dataset.csv")

# Insert data into the database
for _, row in df.iterrows():
    LoanApplication.objects.create(
        employment_status=row["employment_status"],
        monthly_income=row["monthly_income"],
        existing_loans=row["existing_loans"],
        credit_score=row["credit_score"],
        loan_amount_requested=row["loan_amount_requested"],
        debt_to_income_ratio=row["debt_to_income_ratio"],
        loan_purpose=row["loan_purpose"],
        repayment_history=row["repayment_history"],
        defaulted=row["defaulted"],
    )

print("Data Loaded Successfully!")
