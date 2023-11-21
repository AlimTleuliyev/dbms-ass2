# Import required libraries
import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import JobApplication, Caregiver, Job, Base
import pandas as pd
import datetime
import time

# Database Setup
engine = create_engine('sqlite:///dbms.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Streamlit UI Setup
st.title('Job Application Management System')

# Utility Functions
def create_job_application(session, **job_application_data):
    job_application = JobApplication(**job_application_data)
    session.add(job_application)
    try:
        session.commit()
        return True, "Job Application Created Successfully"
    except Exception as e:
        session.rollback()
        return False, str(e)

def get_job_application_by(session, **kwargs):
    filters = {k: v for k, v in kwargs.items() if v}
    return session.query(JobApplication).filter_by(**filters).all()

def display_job_applications(job_applications):
    job_app_df = pd.DataFrame([{c.name: getattr(ja, c.name) for c in JobApplication.__table__.columns} for ja in job_applications])
    st.dataframe(job_app_df, hide_index=True)

# Job Application Creation Form
with st.form('job_application_form'):
    st.write('Create a New Job Application')
    # Job Application input fields
    job_application_data = {
        'caregiver_user_id': st.selectbox('Caregiver ID', [x[0] for x in session.query(Caregiver.caregiver_user_id).all()]),
        'job_id': st.selectbox('Job ID', [x[0] for x in session.query(Job.job_id).all()]),
        'date_applied': st.date_input('Date Applied', datetime.date.today())
    }

    submitted = st.form_submit_button('Create Job Application')
    if submitted:
        success, message = create_job_application(session, **job_application_data)
        if success:
            st.success(message)
        else:
            st.error(message)

# Job Application Search Form
with st.form('job_application_search'):
    st.write('Search Job Applications')
    search_params = {
        'caregiver_user_id': st.text_input('By Caregiver ID'),
        'job_id': st.text_input('By Job ID')
    }

    searched = st.form_submit_button('Search')
    if searched:
        job_applications = get_job_application_by(session, **search_params)
        display_job_applications(job_applications)

# Update Job Application Section
st.subheader('Update or Delete Job Application')
all_job_applications = session.query(JobApplication).all()
selected_job_application = st.selectbox('Select a job application to update or delete', options=all_job_applications, format_func=lambda x: f"Caregiver ID: {x.caregiver_user_id}, Job ID: {x.job_id}")

if selected_job_application:
    if st.button('Edit This Job Application'):
        st.session_state['job_application_id_to_edit'] = (selected_job_application.caregiver_user_id, selected_job_application.job_id)

    # Job Application Update Form
    if 'job_application_id_to_edit' in st.session_state:
        with st.form("update_job_application_form"):
            st.write('Edit Job Application Details')
            update_data = {
                'date_applied': st.date_input('New Date Applied', selected_job_application.date_applied)
            }
            save_changes = st.form_submit_button('Save Changes')
            if save_changes:
                caregiver_id, job_id = st.session_state['job_application_id_to_edit']
                job_application_to_update = session.query(JobApplication).filter_by(caregiver_user_id=caregiver_id, job_id=job_id).first()
                for key, value in update_data.items():
                    setattr(job_application_to_update, key, value)
                session.commit()
                st.success('Job Application Updated')
                del st.session_state['job_application_id_to_edit']
                time.sleep(1)
                st.rerun()

    # Job Application Deletion
    if st.button('Delete This Job Application'):
        caregiver_id, job_id = (selected_job_application.caregiver_user_id, selected_job_application.job_id)
        job_application_to_delete = session.query(JobApplication).filter_by(caregiver_user_id=caregiver_id, job_id=job_id).first()
        session.delete(job_application_to_delete)
        session.commit()
        st.success('Job Application Deleted')
        time.sleep(1)
        st.rerun()
else:
    st.write("No job application selected or job application does not exist.")
