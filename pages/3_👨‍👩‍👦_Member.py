# member_page.py
# Import required libraries
import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from models import Member, User, Base
import pandas as pd
import time

# Database Setup
engine = create_engine('sqlite:///dbms.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Streamlit UI Setup
st.title('Member Management System')

# Utility Functions
def create_member(session, **member_data):
    # Ensure the associated user exists before creating a member
    associated_user = session.query(User).filter_by(user_id=member_data['member_user_id']).first()
    if associated_user:
        member = Member(**member_data)
        session.add(member)
        try:
            session.commit()
            return True, "Member Created Successfully"
        except Exception as e:
            session.rollback()
            return False, str(e)
    else:
        return False, "Associated User not found. Please create a User first."

def get_member_by(session, **kwargs):
    filters = {k: v for k, v in kwargs.items() if v}
    return session.query(Member).filter_by(**filters).all()

def display_members(members):
    member_df = pd.DataFrame([{c.name: getattr(m, c.name) for c in Member.__table__.columns} for m in members])
    st.dataframe(member_df, hide_index=True)

# Member Creation Form
with st.form('member_form'):
    st.write('Create a New Member')
    # Member input fields
    member_data = {
        'member_user_id': st.number_input('User ID', step=1, format='%d'),
        'house_rules': st.text_area('House Rules')
    }

    submitted = st.form_submit_button('Create Member')
    if submitted:
        success, message = create_member(session, **member_data)
        if success:
            st.success(message)
        else:
            st.error(message)

# Member Search Form
with st.form('member_search'):
    st.write('Search Members')
    search_params = {
        'member_user_id': st.text_input('By Member User ID'),
        'house_rules': st.text_input('By House Rules Contains')
    }

    searched = st.form_submit_button('Search')
    if searched:
        # If the fields are left empty, remove them from the search query
        search_params = {k: v for k, v in search_params.items() if v != ''}
        members = get_member_by(session, **search_params)
        display_members(members)

# Update Member Section
st.subheader('Update or Delete Member')
all_members = session.query(Member).all()
selected_member = st.selectbox('Select a member to update or delete', options=all_members, format_func=lambda m: f"ID:{m.member_user_id}")

if selected_member:
    if st.button('Edit This Member'):
        st.session_state['member_id_to_edit'] = selected_member.member_user_id

    # Member Update Form
    if 'member_id_to_edit' in st.session_state:
        with st.form("update_member_form"):
            st.write('Edit Member Details')
            update_data = {
                'house_rules': st.text_area('New House Rules', value=selected_member.house_rules)
            }
            save_changes = st.form_submit_button('Save Changes')
            if save_changes:
                member_to_update = session.query(Member).filter_by(member_user_id=st.session_state['member_id_to_edit']).first()
                for key, value in update_data.items():
                    setattr(member_to_update, key, value)
                session.commit()
                st.success('Member Updated')
                del st.session_state['member_id_to_edit']
                time.sleep(1)
                st.rerun()

    # Member Deletion
    if st.button('Delete This Member'):
        member_to_delete = session.query(Member).filter_by(member_user_id=selected_member.member_user_id).first()
        session.delete(member_to_delete)
        session.commit()
        st.success('Member Deleted')
        time.sleep(1)
        st.rerun()
else:
    st.write("No member selected or member does not exist.")