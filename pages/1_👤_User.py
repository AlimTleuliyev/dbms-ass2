# Import required libraries
import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from models import User, Base
import pandas as pd
import time

# Database Setup
engine = create_engine('sqlite:///dbms.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Streamlit UI Setup
st.title('User Management System')

# Utility Functions
def create_user(session, **user_data):
    user = User(**user_data)
    session.add(user)
    try:
        session.commit()
        return True, "User Created Successfully"
    except Exception as e:
        session.rollback()
        return False, str(e)

def get_user_by(session, **kwargs):
    filters = {k: v for k, v in kwargs.items() if v}
    return session.query(User).filter_by(**filters).all()

def display_users(users):
    user_df = pd.DataFrame([{c.name: getattr(u, c.name) for c in User.__table__.columns} for u in users])
    st.dataframe(user_df, hide_index=True)

# User Creation Form
with st.form('user_form'):
    st.write('Create a New User')
    # User input fields
    user_data = {
        'email': st.text_input('Email'),
        'given_name': st.text_input('Given Name'),
        'surname': st.text_input('Surname'),
        'city': st.text_input('City'),
        'phone_number': st.text_input('Phone Number'),
        'profile_description': st.text_area('Profile Description'),
        'password': st.text_input('Password', type='password')
    }

    submitted = st.form_submit_button('Create User')
    if submitted:
        success, message = create_user(session, **user_data)
        if success:
            st.success(message)
        else:
            st.error(message)


# User Search Form
with st.form('user_search'):
    st.write('Search Users')
    search_params = {
        'user_id': st.text_input('By User ID'),
        'email': st.text_input('By Email'),
        'given_name': st.text_input('By Given Name'),
        'surname': st.text_input('By Surname'),
        'city': st.text_input('By City')
    }

    searched = st.form_submit_button('Search')
    if searched:
        users = get_user_by(session, **search_params)
        display_users(users)

# Update User Section
st.subheader('Update or Delete User')
all_users = session.query(User).all()
selected_user = st.selectbox('Select a user to update or delete', options=all_users, format_func=lambda x: f"{x.given_name + ' ' + x.surname} ({x.email}) ID:{x.user_id}")

if selected_user:
    if st.button('Edit This User'):
        st.session_state['user_id_to_edit'] = selected_user.user_id

    # User Update Form
    if 'user_id_to_edit' in st.session_state:
        with st.form("update_user_form"):
            st.write('Edit User Details')
            update_data = {
                'email': st.text_input('New Email', value=selected_user.email),
                'given_name': st.text_input('New Given Name', value=selected_user.given_name),
                'surname': st.text_input('New Surname', value=selected_user.surname),
                'city': st.text_input('New City', value=selected_user.city),
                'phone_number': st.text_input('New Phone Number', value=selected_user.phone_number),
                'profile_description': st.text_area('New Profile Description', value=selected_user.profile_description),
                'password': st.text_input('New Password', value=selected_user.password, type='password')
            }
            save_changes = st.form_submit_button('Save Changes')
            if save_changes:
                user_to_update = session.query(User).filter_by(user_id=st.session_state['user_id_to_edit']).first()
                for key, value in update_data.items():
                    setattr(user_to_update, key, value)
                session.commit()
                st.success('User Updated')
                del st.session_state['user_id_to_edit']
                time.sleep(1)
                st.rerun()

    # User Deletion
    if st.button('Delete This User'):
        user_to_delete = session.query(User).filter_by(user_id=selected_user.user_id).first()
        session.delete(user_to_delete)
        session.commit()
        st.success('User Deleted')
        time.sleep(1)
        st.rerun()
else:
    st.write("No user selected or user does not exist.")

