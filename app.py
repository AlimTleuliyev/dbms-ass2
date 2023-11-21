import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, Base  # Import your SQLAlchemy models here

# Database setup
engine = create_engine('sqlite:///your_database.db')
Session = sessionmaker(bind=engine)
session = Session()

# Streamlit UI
st.title('User Management')

# Add User Function
def add_user(email, given_name, surname, city, phone_number, profile_description, password):
    new_user = User(
        email=email, 
        given_name=given_name, 
        surname=surname, 
        city=city, 
        phone_number=phone_number, 
        profile_description=profile_description, 
        password=password
    )
    session.add(new_user)
    session.commit()

# View Users Function
def view_users():
    users = session.query(User).all()
    for user in users:
        st.write(f"ID: {user.user_id}, Email: {user.email}, Name: {user.given_name} {user.surname}")

# Update User Function
def update_user(user_id, email, given_name, surname, city, phone_number, profile_description, password):
    user = session.query(User).filter(User.user_id == user_id).first()
    user.email = email
    user.given_name = given_name
    user.surname = surname
    user.city = city
    user.phone_number = phone_number
    user.profile_description = profile_description
    user.password = password
    session.commit()

# Delete User Function
def delete_user(user_id):
    user = session.query(User).filter(User.user_id == user_id).first()
    session.delete(user)
    session.commit()

# UI for Adding a New User
with st.form("Add User"):
    st.subheader("Add New User")
    new_email = st.text_input("Email")
    new_given_name = st.text_input("Given Name")
    new_surname = st.text_input("Surname")
    new_city = st.text_input("City")
    new_phone_number = st.text_input("Phone Number")
    new_profile_description = st.text_area("Profile Description")
    new_password = st.text_input("Password", type="password")
    
    if st.form_submit_button("Add User"):
        add_user(new_email, new_given_name, new_surname, new_city, new_phone_number, new_profile_description, new_password)
        st.success("User added successfully!")

# UI for Updating an Existing User
with st.form("Update User"):
    st.subheader("Update Existing User")
    user_id = st.number_input("User ID", step=1, min_value=0)
    updated_email = st.text_input("Updated Email")
    updated_given_name = st.text_input("Updated Given Name")
    updated_surname = st.text_input("Updated Surname")
    updated_city = st.text_input("Updated City")
    updated_phone_number = st.text_input("Updated Phone Number")
    updated_profile_description = st.text_area("Updated Profile Description")
    updated_password = st.text_input("Updated Password", type="password")
    
    if st.form_submit_button("Update User"):
        update_user(user_id, updated_email, updated_given_name, updated_surname, updated_city, updated_phone_number, updated_profile_description, updated_password)
        st.success("User updated successfully!")

# UI for Deleting a User
delete_user_id = st.number_input("Delete User ID", step=1, min_value=0)
if st.button('Delete User'):
    delete_user(delete_user_id)
    st.success(f"User with ID {delete_user_id} deleted successfully!")

# Button to View All Users
if st.button('Show All Users'):
    view_users()
