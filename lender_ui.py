import streamlit as st
import pandas as pd

st.title("💰 Become a Lender")

# Sidebar Navigation
menu = st.sidebar.radio("Navigation", ["Register as Lender", "View Lenders"])

# Initialize session state for storing lender data
if "lenders" not in st.session_state:
    st.session_state.lenders = []

# 📝 Lender Registration Form
if menu == "Register as Lender":
    st.header("📋 Register as a Lender")

    with st.form(key="lender_form"):
        name = st.text_input("Full Name", placeholder="Enter your name")
        company_name = st.text_input("Company Name (Optional)", placeholder="Enter company name if applicable")
        email = st.text_input("Email", placeholder="Enter your email")
        phone = st.text_input("Phone", placeholder="Enter your phone number")
        loan_amount = st.number_input("Loan Amount (₹)", min_value=1000.0, step=500.0)
        interest_rate = st.number_input("Interest Rate (%)", min_value=1.0, max_value=50.0, step=0.1)
        lending_period = st.number_input("Lending Period (Months)", min_value=1, max_value=60, step=1)

        submit_button = st.form_submit_button("✅ Register")

    if submit_button:
        if not name or not email or not phone:
            st.warning("⚠️ Name, Email, and Phone are required fields!")
        else:
            lender_data = {
                "Name": name,
                "Company Name": company_name,
                "Email": email,
                "Phone": phone,
                "Loan Amount (₹)": loan_amount,
                "Interest Rate (%)": interest_rate,
                "Lending Period (Months)": lending_period,
            }

            # Store lender data in session state
            st.session_state.lenders.append(lender_data)
            st.success("🎉 Successfully registered as a lender!")

# 📊 View All Lenders
elif menu == "View Lenders":
    st.header("📊 Registered Lenders")

    if st.session_state.lenders:
        df = pd.DataFrame(st.session_state.lenders)
        st.dataframe(df)
    else:
        st.info("⚠️ No lenders registered yet.")
