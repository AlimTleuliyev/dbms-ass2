from sqlalchemy import create_engine, Column, Integer, String, Text, DECIMAL, Date, Time, ForeignKey, Enum, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum

# Define enums
class GenderEnum(enum.Enum):
    Male = 'Male'
    Female = 'Female'

class CaregivingTypeEnum(enum.Enum):
    BabySitter = 'BabySitter'
    ElderlyCare = 'ElderlyCare'
    SpecialNeedsCare = 'SpecialNeedsCare'
    NurseCare = 'NurseCare'
    CompanionCare = 'CompanionCare'
    PetCare = 'PetCare'
    Housekeeping = 'Housekeeping'
    PersonalAssistant = 'PersonalAssistant'

Base = declarative_base()

# Define models
class User(Base):
    __tablename__ = 'user'
    user_id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True, nullable=False)
    given_name = Column(String(100), nullable=False)
    surname = Column(String(100), nullable=False)
    city = Column(String(100), nullable=False)
    phone_number = Column(String(20), unique=True, nullable=False)
    profile_description = Column(Text, nullable=False)
    password = Column(String(100), nullable=False)

class Caregiver(Base):
    __tablename__ = 'caregiver'
    caregiver_user_id = Column(Integer, ForeignKey('user.user_id', ondelete='CASCADE'), primary_key=True)
    photo = Column(String(255), nullable=False)
    gender = Column(Enum(GenderEnum), nullable=False)
    caregiving_type = Column(Enum(CaregivingTypeEnum), nullable=False)
    hourly_rate = Column(DECIMAL(10, 2), CheckConstraint('hourly_rate > 0'), nullable=False)
    user = relationship("User")

class Member(Base):
    __tablename__ = 'member'
    member_user_id = Column(Integer, ForeignKey('user.user_id', ondelete='CASCADE'), primary_key=True)
    house_rules = Column(Text, nullable=False)
    user = relationship("User")

class Address(Base):
    __tablename__ = 'address'
    member_user_id = Column(Integer, ForeignKey('member.member_user_id', ondelete='CASCADE'), primary_key=True)
    house_number = Column(String(50), nullable=False)
    street = Column(String(50), nullable=False)
    town = Column(String(50), nullable=False)
    member = relationship("Member")

class Job(Base):
    __tablename__ = 'job'
    job_id = Column(Integer, primary_key=True)
    member_user_id = Column(Integer, ForeignKey('member.member_user_id', ondelete='CASCADE'), nullable=False)
    required_caregiving_type = Column(Enum(CaregivingTypeEnum), nullable=False)
    other_requirements = Column(Text)
    date_posted = Column(Date, nullable=False)
    member = relationship("Member")

class JobApplication(Base):
    __tablename__ = 'job_application'
    caregiver_user_id = Column(Integer, ForeignKey('caregiver.caregiver_user_id', ondelete='CASCADE'), primary_key=True)
    job_id = Column(Integer, ForeignKey('job.job_id', ondelete='CASCADE'), primary_key=True)
    date_applied = Column(Date, nullable=False)
    caregiver = relationship("Caregiver")
    job = relationship("Job")

class Appointment(Base):
    __tablename__ = 'appointment'
    appointment_id = Column(Integer, primary_key=True)
    caregiver_user_id = Column(Integer, ForeignKey('caregiver.caregiver_user_id', ondelete='CASCADE'), nullable=False)
    member_user_id = Column(Integer, ForeignKey('member.member_user_id', ondelete='CASCADE'), nullable=False)
    appointment_date = Column(Date, nullable=False)
    appointment_time = Column(Time, nullable=False)
    work_hours = Column(Integer, CheckConstraint('work_hours > 0'), nullable=False)
    status = Column(String(20), CheckConstraint("status IN ('Pending', 'Confirmed', 'Declined')"), nullable=False)
    caregiver = relationship("Caregiver")
    member = relationship("Member")

# Create the SQLite database
engine = create_engine('postgresql+psycopg2://alimtleuliyev:qwerty@localhost:5432/alimtleuliyev')
Base.metadata.create_all(engine)
