# Import required libraries
import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Address, Member, Base
import pandas as pd
import time

# Database Setup
engine = create_engine('sqlite:///dbms.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Streamlit UI Setup
st.title('Address Management System')

# Utility Functions
def create_address(session, **address_data):
    address = Address(**address_data)
    session.add(address)
    try:
        session.commit()
        return True, "Address Created Successfully"
    except Exception as e:
        session.rollback()
        return False, str(e)

def get_address_by(session, **kwargs):
    filters = {k: v for k, v in kwargs.items() if v}
    return session.query(Address).filter_by(**filters).all()

def display_addresses(addresses):
    address_df = pd.DataFrame([{c.name: getattr(a, c.name) for c in Address.__table__.columns} for a in addresses])
    st.dataframe(address_df, hide_index=True)

# Address Creation Form
with st.form('address_form'):
    st.write('Create a New Address')
    # Address input fields
    address_data = {
        'member_user_id': st.selectbox('Member ID', [x[0] for x in session.query(Member.member_user_id).all()]),
        'house_number': st.text_input('House Number'),
        'street': st.text_input('Street'),
        'town': st.text_input('Town')
    }

    submitted = st.form_submit_button('Create Address')
    if submitted:
        success, message = create_address(session, **address_data)
        if success:
            st.success(message)
        else:
            st.error(message)

# Address Search Form
with st.form('address_search'):
    st.write('Search Addresses')
    search_params = {
        'member_user_id': st.text_input('By Member ID'),
        'house_number': st.text_input('By House Number'),
        'street': st.text_input('By Street'),
        'town': st.text_input('By Town')
    }

    searched = st.form_submit_button('Search')
    if searched:
        addresses = get_address_by(session, **search_params)
        display_addresses(addresses)

# Update Address Section
st.subheader('Update or Delete Address')
all_addresses = session.query(Address).all()
selected_address = st.selectbox('Select an address to update or delete', options=all_addresses, format_func=lambda x: f"{x.street}, {x.town} (ID: {x.member_user_id})")

if selected_address:
    if st.button('Edit This Address'):
        st.session_state['address_id_to_edit'] = selected_address.member_user_id

    # Address Update Form
    if 'address_id_to_edit' in st.session_state:
        with st.form("update_address_form"):
            st.write('Edit Address Details')
            update_data = {
                'house_number': st.text_input('New House Number', value=selected_address.house_number),
                'street': st.text_input('New Street', value=selected_address.street),
                'town': st.text_input('New Town', value=selected_address.town)
            }
            save_changes = st.form_submit_button('Save Changes')
            if save_changes:
                address_to_update = session.query(Address).filter_by(member_user_id=st.session_state['address_id_to_edit']).first()
                for key, value in update_data.items():
                    setattr(address_to_update, key, value)
                session.commit()
                st.success('Address Updated')
                del st.session_state['address_id_to_edit']
                time.sleep(1)
                st.rerun()

    # Address Deletion
    if st.button('Delete This Address'):
        address_to_delete = session.query(Address).filter_by(member_user_id=selected_address.member_user_id).first()
        session.delete(address_to_delete)
        session.commit()
        st.success('Address Deleted')
        time.sleep(1)
        st.rerun()
else:
    st.write("No address selected or address does not exist.")
