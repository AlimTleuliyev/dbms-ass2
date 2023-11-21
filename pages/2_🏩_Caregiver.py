# caregiver_page.py
# Import required libraries
import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from models import Caregiver, Base, GenderEnum, CaregivingTypeEnum
import pandas as pd
import time

# Database Setup
engine = create_engine('sqlite:///dbms.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Streamlit UI Setup
st.title('Caregiver Management System')

# Utility Functions
def create_caregiver(session, **caregiver_data):
    caregiver = Caregiver(**caregiver_data)
    session.add(caregiver)
    try:
        session.commit()
        return True, "Caregiver Created Successfully"
    except Exception as e:
        session.rollback()
        return False, str(e)

def get_caregiver_by(session, **kwargs):
    filters = {k: v for k, v in kwargs.items() if v}
    return session.query(Caregiver).filter_by(**filters).all()

def display_caregivers(caregivers):
    caregiver_df = pd.DataFrame([{c.name: getattr(cg, c.name) for c in Caregiver.__table__.columns} for cg in caregivers])
    st.dataframe(caregiver_df, hide_index=True)

# Caregiver Creation Form
with st.form('caregiver_form'):
    st.write('Create a New Caregiver')
    # Caregiver input fields
    caregiver_data = {
        'caregiver_user_id': st.number_input('User ID', step=1, format='%d'),
        'photo': st.text_input('Photo URL'),
        'gender': st.selectbox('Gender', [e.value for e in GenderEnum]),
        'caregiving_type': st.selectbox('Caregiving Type', [e.value for e in CaregivingTypeEnum]),
        'hourly_rate': st.number_input('Hourly Rate', min_value=0.00, step=0.01, format='%f')
    }

    submitted = st.form_submit_button('Create Caregiver')
    if submitted:
        success, message = create_caregiver(session, **caregiver_data)
        if success:
            st.success(message)
        else:
            st.error(message)

# Caregiver Search Form
with st.form('caregiver_search'):
    st.write('Search Caregivers')
    search_params = {
        'caregiver_user_id': st.text_input('By Caregiver User ID'),
        'gender': st.selectbox('By Gender', ['', ] + [e.value for e in GenderEnum], index=0),
        'caregiving_type': st.selectbox('By Caregiving Type', ['', ] + [e.value for e in CaregivingTypeEnum], index=0)
    }

    searched = st.form_submit_button('Search')
    if searched:
        # If the fields are left empty, remove them from the search query
        search_params = {k: v for k, v in search_params.items() if v != ''}
        caregivers = get_caregiver_by(session, **search_params)
        display_caregivers(caregivers)

# Update Caregiver Section
st.subheader('Update or Delete Caregiver')
all_caregivers = session.query(Caregiver).all()
selected_caregiver = st.selectbox('Select a caregiver to update or delete', options=all_caregivers, format_func=lambda x: f"ID:{x.caregiver_user_id}")

if selected_caregiver:
    if st.button('Edit This Caregiver'):
        st.session_state['caregiver_id_to_edit'] = selected_caregiver.caregiver_user_id

    # Caregiver Update Form
    if 'caregiver_id_to_edit' in st.session_state:
        with st.form("update_caregiver_form"):
            st.write('Edit Caregiver Details')
            update_data = {
                'photo': st.text_input('New Photo URL', value=selected_caregiver.photo),
                'gender': st.selectbox('New Gender', [e.value for e in GenderEnum], index=[e.value for e in GenderEnum].index(selected_caregiver.gender.value)),
                'caregiving_type': st.selectbox('New Caregiving Type', [e.value for e in CaregivingTypeEnum], index=[e.value for e in CaregivingTypeEnum].index(selected_caregiver.caregiving_type.value)),
                'hourly_rate': st.number_input('New Hourly Rate', min_value=0.00, value=float(selected_caregiver.hourly_rate), step=0.01, format='%f')
            }
            save_changes = st.form_submit_button('Save Changes')
            if save_changes:
                caregiver_to_update = session.query(Caregiver).filter_by(caregiver_user_id=st.session_state['caregiver_id_to_edit']).first()
                for key, value in update_data.items():
                    if key in ['gender', 'caregiving_type']:
                        value = getattr(GenderEnum if key == 'gender' else CaregivingTypeEnum, value)
                    setattr(caregiver_to_update, key, value)
                session.commit()
                st.success('Caregiver Updated')
                del st.session_state['caregiver_id_to_edit']
                time.sleep(1)
                st.rerun()

    # Caregiver Deletion
    if st.button('Delete This Caregiver'):
        caregiver_to_delete = session.query(Caregiver).filter_by(caregiver_user_id=selected_caregiver.caregiver_user_id).first()
        session.delete(caregiver_to_delete)
        session.commit()
        st.success('Caregiver Deleted')
        time.sleep(1)
        st.rerun()
else:
    st.write("No caregiver selected or caregiver does not exist.")