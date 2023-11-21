# Import required libraries
import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Job, Member, CaregivingTypeEnum, Base
import pandas as pd
import datetime
import time

# Database Setup
engine = create_engine('sqlite:///dbms.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Streamlit UI Setup
st.title('Job Management System')

# Utility Functions
def create_job(session, **job_data):
    job = Job(**job_data)
    session.add(job)
    try:
        session.commit()
        return True, "Job Created Successfully"
    except Exception as e:
        session.rollback()
        return False, str(e)

def get_job_by(session, **kwargs):
    filters = {k: v for k, v in kwargs.items() if v}
    return session.query(Job).filter_by(**filters).all()

def display_jobs(jobs):
    job_df = pd.DataFrame([{c.name: getattr(j, c.name) for c in Job.__table__.columns} for j in jobs])
    st.dataframe(job_df, hide_index=True)

# Job Creation Form
with st.form('job_form'):
    st.write('Create a New Job')
    # Job input fields
    job_data = {
        'member_user_id': st.selectbox('Member ID', [x[0] for x in session.query(Member.member_user_id).all()]),
        'required_caregiving_type': st.selectbox('Required Caregiving Type', [t.name for t in CaregivingTypeEnum]),
        'other_requirements': st.text_area('Other Requirements'),
        'date_posted': st.date_input('Date Posted', datetime.date.today())
    }

    submitted = st.form_submit_button('Create Job')
    if submitted:
        success, message = create_job(session, **job_data)
        if success:
            st.success(message)
        else:
            st.error(message)

# Job Search Form
with st.form('job_search'):
    st.write('Search Jobs')
    search_params = {
        'job_id': st.text_input('By Job ID'),
        'member_user_id': st.text_input('By Member ID'),
        'required_caregiving_type': st.selectbox('By Caregiving Type', [''] + [t.name for t in CaregivingTypeEnum])
    }

    searched = st.form_submit_button('Search')
    if searched:
        jobs = get_job_by(session, **search_params)
        display_jobs(jobs)

# Update Job Section
st.subheader('Update or Delete Job')
all_jobs = session.query(Job).all()
selected_job = st.selectbox('Select a job to update or delete', options=all_jobs, format_func=lambda x: f"Job ID: {x.job_id}, Caregiving Type: {x.required_caregiving_type}")

if selected_job:
    if st.button('Edit This Job'):
        st.session_state['job_id_to_edit'] = selected_job.job_id

    # Job Update Form
    if 'job_id_to_edit' in st.session_state:
        with st.form("update_job_form"):
            st.write('Edit Job Details')
            update_data = {
                'required_caregiving_type': st.selectbox('New Caregiving Type', [t.name for t in CaregivingTypeEnum], index=[t.name for t in CaregivingTypeEnum].index(selected_job.required_caregiving_type)),
                'other_requirements': st.text_area('New Other Requirements', value=selected_job.other_requirements),
                'date_posted': st.date_input('New Date Posted', selected_job.date_posted)
            }
            save_changes = st.form_submit_button('Save Changes')
            if save_changes:
                job_to_update = session.query(Job).filter_by(job_id=st.session_state['job_id_to_edit']).first()
                for key, value in update_data.items():
                    setattr(job_to_update, key, value)
                session.commit()
                st.success('Job Updated')
                del st.session_state['job_id_to_edit']
                time.sleep(1)
                st.rerun()

    # Job Deletion
    if st.button('Delete This Job'):
        job_to_delete = session.query(Job).filter_by(job_id=selected_job.job_id).first()
        session.delete(job_to_delete)
        session.commit()
        st.success('Job Deleted')
        time.sleep(1)
        st.rerun()
else:
    st.write("No job selected or job does not exist.")
