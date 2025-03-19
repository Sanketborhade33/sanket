



import streamlit as st
import pandas as pd

st.title("💰 Get a Loan")

# Sidebar Navigation
menu = st.sidebar.radio("Navigation", ["Apply for Loan", "View Loan Applications"])

# Initialize session state for storing loan applications
if "loan_applications" not in st.session_state:
    st.session_state.loan_applications = []

# 📝 Loan Application Form
if menu == "Apply for Loan":
    st.header("📋 Apply for a Loan")

    with st.form(key="loan_form"):
        name = st.text_input("Full Name", placeholder="Enter your name")
        email = st.text_input("Email", placeholder="Enter your email")
        phone = st.text_input("Phone", placeholder="Enter your phone number")
        loan_amount = st.number_input("Loan Amount (₹)", min_value=1000.0, step=500.0)
        purpose = st.text_area("Purpose of Loan", placeholder="Explain why you need the loan")
        duration = st.number_input("Loan Duration (Months)", min_value=1, max_value=60, step=1)

        submit_button = st.form_submit_button("✅ Apply for Loan")

    if submit_button:
        if not name or not email or not phone or not purpose:
            st.warning("⚠️ Name, Email, Phone, and Purpose are required fields!")
        else:
            loan_data = {
                "Name": name,
                "Email": email,
                "Phone": phone,
                "Loan Amount (₹)": loan_amount,
                "Purpose": purpose,
                "Duration (Months)": duration,
            }

            # Store loan application in session state
            st.session_state.loan_applications.append(loan_data)
            st.success("🎉 Your loan application has been submitted successfully!")

# 📊 View All Loan Applications
elif menu == "View Loan Applications":
    st.header("📊 Loan Applications")

    if st.session_state.loan_applications:
        df = pd.DataFrame(st.session_state.loan_applications)
        st.dataframe(df)
    else:
        st.info("⚠️ No loan applications submitted yet.")


