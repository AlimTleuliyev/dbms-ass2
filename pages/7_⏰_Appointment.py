# Import required libraries
import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Appointment, Caregiver, Member, Base
import pandas as pd
import datetime
import time

# Database Setup
engine = create_engine('sqlite:///dbms.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Streamlit UI Setup
st.title('Appointment Management System')

# Utility Functions
def create_appointment(session, **appointment_data):
    appointment = Appointment(**appointment_data)
    session.add(appointment)
    try:
        session.commit()
        return True, "Appointment Created Successfully"
    except Exception as e:
        session.rollback()
        return False, str(e)

def get_appointment_by(session, **kwargs):
    filters = {k: v for k, v in kwargs.items() if v}
    return session.query(Appointment).filter_by(**filters).all()

def display_appointments(appointments):
    appointment_df = pd.DataFrame([{c.name: getattr(a, c.name) for c in Appointment.__table__.columns} for a in appointments])
    st.dataframe(appointment_df, hide_index=True)

# Appointment Creation Form
with st.form('appointment_form'):
    st.write('Create a New Appointment')
    # Appointment input fields
    appointment_data = {
        'caregiver_user_id': st.selectbox('Caregiver ID', [x[0] for x in session.query(Caregiver.caregiver_user_id).all()]),
        'member_user_id': st.selectbox('Member ID', [x[0] for x in session.query(Member.member_user_id).all()]),
        'appointment_date': st.date_input('Appointment Date', datetime.date.today()),
        'appointment_time': st.time_input('Appointment Time', datetime.datetime.now().time()),
        'work_hours': st.number_input('Work Hours', min_value=1, max_value=12, value=1),
        'status': st.selectbox('Status', ['Pending', 'Confirmed', 'Declined'])
    }

    submitted = st.form_submit_button('Create Appointment')
    if submitted:
        success, message = create_appointment(session, **appointment_data)
        if success:
            st.success(message)
        else:
            st.error(message)

# Appointment Search Form
with st.form('appointment_search'):
    st.write('Search Appointments')
    search_params = {
        'appointment_id': st.text_input('By Appointment ID'),
        'caregiver_user_id': st.text_input('By Caregiver ID'),
        'member_user_id': st.text_input('By Member ID')
    }

    searched = st.form_submit_button('Search')
    if searched:
        appointments = get_appointment_by(session, **search_params)
        display_appointments(appointments)

# Update Appointment Section
st.subheader('Update or Delete Appointment')
all_appointments = session.query(Appointment).all()
selected_appointment = st.selectbox('Select an appointment to update or delete', options=all_appointments, format_func=lambda x: f"Appointment ID: {x.appointment_id}, Caregiver ID: {x.caregiver_user_id}")

if selected_appointment:
    if st.button('Edit This Appointment'):
        st.session_state['appointment_id_to_edit'] = selected_appointment.appointment_id

    # Appointment Update Form
    if 'appointment_id_to_edit' in st.session_state:
        with st.form("update_appointment_form"):
            st.write('Edit Appointment Details')
            update_data = {
                'appointment_date': st.date_input('New Appointment Date', selected_appointment.appointment_date),
                'appointment_time': st.time_input('New Appointment Time', selected_appointment.appointment_time),
                'work_hours': st.number_input('New Work Hours', min_value=1, max_value=12, value=selected_appointment.work_hours),
                'status': st.selectbox('New Status', ['Pending', 'Confirmed', 'Declined'], index=['Pending', 'Confirmed', 'Declined'].index(selected_appointment.status))
            }
            save_changes = st.form_submit_button('Save Changes')
            if save_changes:
                appointment_to_update = session.query(Appointment).filter_by(appointment_id=st.session_state['appointment_id_to_edit']).first()
                for key, value in update_data.items():
                    setattr(appointment_to_update, key, value)
                session.commit()
                st.success('Appointment Updated')
                del st.session_state['appointment_id_to_edit']
                time.sleep(1)
                st.rerun()

    # Appointment Deletion
    if st.button('Delete This Appointment'):
        appointment_to_delete = session.query(Appointment).filter_by(appointment_id=selected_appointment.appointment_id).first()
        session.delete(appointment_to_delete)
        session.commit()
        st.success('Appointment Deleted')
        time.sleep(1)
        st.rerun()
else:
    st.write("No appointment selected or appointment does not exist.")
