import streamlit as st
import pandas as pd
import numpy as np
import joblib
import pymongo
import bcrypt
import sqlite3
from pymongo import MongoClient
from sklearn.preprocessing import LabelEncoder

# Load ML Model
rf_model = joblib.load("loan_risk_model.pkl")
label_encoders = joblib.load("label_encoders.pkl")
model_features = joblib.load("model_features.pkl")

# Database Connection
client = MongoClient("mongodb://localhost:27017/")  # Use your MongoDB URI
db = client["p2p_lending"]
users_collection = db["users"]
loans_collection = db["loans"]

# SQLite Connection
conn = sqlite3.connect("p2p_lending.db")
cursor = conn.cursor()

# Create Tables
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE,
                  password TEXT,
                  role TEXT)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS loans (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  borrower TEXT,
                  amount REAL,
                  duration TEXT,
                  purpose TEXT,
                  status TEXT)''')

conn.commit()

# User Authentication Functions
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def register_user(username, password, role):
    try:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                       (username, hash_password(password), role))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def login_user(username, password):
    cursor.execute("SELECT password, role FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    if user and check_password(password, user[0]):
        return user[1]
    return None

# Streamlit UI
st.title("Peer-to-Peer Lending Platform")

menu = st.sidebar.selectbox("Menu", ["Login", "Sign Up"])

if menu == "Sign Up":
    st.subheader("Create an Account")
    new_user = st.text_input("Username")
    new_password = st.text_input("Password", type="password")
    role = st.selectbox("Select Role", ["Borrower", "Lender", "Admin"])
    
    if st.button("Register"):
        if register_user(new_user, new_password, role):
            st.success("Account created successfully!")
        else:
            st.error("Username already exists!")

elif menu == "Login":
    st.subheader("Login to Your Account")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        role = login_user(username, password)
        if role:
            st.session_state["username"] = username
            st.session_state["role"] = role
        else:
            st.error("Invalid credentials!")

# After Login Dashboard
if "username" in st.session_state:
    st.sidebar.write(f"Logged in as: {st.session_state['username']} ({st.session_state['role']})")
    
    if st.session_state['role'] == "Borrower":
        st.subheader("Request a Loan")
        amount = st.number_input("Loan Amount", min_value=1000)
        duration = st.selectbox("Loan Duration", ['12 months', '24 months', '36 months'])
        purpose = st.text_area("Loan Purpose")
        
        if st.button("Request Loan"):
            cursor.execute("INSERT INTO loans (borrower, amount, duration, purpose, status) VALUES (?, ?, ?, ?, ?)", 
                           (st.session_state['username'], amount, duration, purpose, "Pending"))
            conn.commit()
            st.success("Loan request submitted!")
    
    elif st.session_state['role'] == "Lender":
        st.subheader("Loan Requests")
        cursor.execute("SELECT * FROM loans WHERE status = 'Pending'")
        loans = cursor.fetchall()
        for loan in loans:
            st.write(f"Borrower: {loan[1]}, Amount: {loan[2]}, Duration: {loan[3]}, Purpose: {loan[4]}")
            
            if st.button(f"Predict Risk for {loan[1]}"):
                borrower_data = pd.DataFrame([{  # Dummy Data - Replace with actual borrower info
                    "year": 2023, "state": "CA", "emp_duration": 5, "own_type": "Rent",
                    "income_type": "Job", "app_type": "Individual", "loan_purpose": loan[4],
                    "interest_payments": "Monthly", "grade": "B", "annual_pay": 50000,
                    "loan_amount": loan[2], "interest_rate": 12, "loan_duration": loan[3],
                    "dti": 20, "total_pymnt": 52000, "total_rec_prncp": 50000, "recoveries": 2000, "installment": 1000
                }])
                
                # Encode Categorical Features
                for col in ['state', 'own_type', 'income_type', 'app_type', 'loan_purpose', 'interest_payments', 'grade', 'loan_duration']:
                    borrower_data[col] = label_encoders[col].transform([borrower_data[col].iloc[0]])
                borrower_data = borrower_data.reindex(columns=model_features, fill_value=0)
                
                # Predict Risk
                prediction = rf_model.predict(borrower_data)
                probability = rf_model.predict_proba(borrower_data)[:, 1]
                risk_status = "High Risk" if prediction[0] == 1 else "Low Risk"
                
                st.write(f"Predicted Risk: {risk_status}")
                st.write(f"Probability of Default: {probability[0]:.4f}")
                
                if st.button(f"Approve Loan for {loan[1]}"):
                    cursor.execute("UPDATE loans SET status = 'Approved' WHERE id = ?", (loan[0],))
                    conn.commit()
                    st.success("Loan Approved!")
    
    elif st.session_state['role'] == "Admin":
        st.subheader("Admin Dashboard")
        cursor.execute("SELECT * FROM users")
        all_users = cursor.fetchall()
        for user in all_users:
            st.write(f"User: {user[1]}, Role: {user[2]}")
        
        cursor.execute("SELECT * FROM loans")
        all_loans = cursor.fetchall()
        for loan in all_loans:
            st.write(f"Borrower: {loan[1]}, Amount: {loan[2]}, Status: {loan[5]}")



import sqlite3

conn = sqlite3.connect("p2p_lending.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM users")
users = cursor.fetchall()

for user in users:
    print(user)

conn.close()
