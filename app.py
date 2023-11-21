import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, Base
from populate import populate

# Setting up the page configuration for a more appealing look
st.set_page_config(
    page_title="Caregivers Online Platform",
    page_icon=":family:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Database Setup
engine = create_engine('sqlite:///dbms.db')
Base.metadata.create_all(engine)

# Main Header and Introduction
st.title('Welcome to Caregivers Online Platform')
st.markdown("""
This platform is designed to connect families with trustworthy caregivers. 
Whether you're looking for a babysitter, elderly care, or any other caregiving service, 
we've got you covered. Easily find, contact, and schedule appointments with caregivers 
tailored to your needs.
""")

# Sidebar for Additional Navigation
with st.sidebar:
    st.header("Navigate")
    st.info("Use the sidebar to navigate through the platform, manage your profile, or search for caregivers and jobs.")

    # Additional navigation or account management options
    st.button("Your Profile")
    st.button("Search Caregivers")
    st.button("Post a Job")
    st.button("View Appointments")

# Populate Database Button
st.header("Get Started")
st.write("New to the platform? Populate your database to see sample data.")
if st.button('Populate Database'):
    try:
        populate()
        st.success("Database populated successfully!")
    except Exception as e:
        st.error(str(e))

# Main Features Section
st.header("What We Offer")
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Find Caregivers")
    st.write("Browse through profiles of qualified caregivers and find the perfect match for your family's needs.")

with col2:
    st.subheader("Post Jobs")
    st.write("Looking for specific caregiving services? Post a job and let caregivers apply to you.")

with col3:
    st.subheader("Schedule Appointments")
    st.write("Easily schedule and manage appointments with your preferred caregivers.")
