-- USER
CREATE TABLE "user" (
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(100) NOT NULL UNIQUE,
    given_name VARCHAR(100) NOT NULL,
    surname VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    phone_number VARCHAR(20) NOT NULL UNIQUE,
    profile_description TEXT NOT NULL,
    "password" VARCHAR(100) NOT NULL
);


-- CAREGIVER
CREATE TYPE gender_enum AS ENUM ('Male', 'Female');

CREATE TYPE caregiving_type_enum AS ENUM (
    'BabySitter',
    'ElderlyCare',
    'SpecialNeedsCare',
    'NurseCare',
    'CompanionCare',
    'PetCare',
    'Housekeeping',
    'PersonalAssistant'
);

CREATE TABLE "caregiver" (
    caregiver_user_id INT PRIMARY KEY REFERENCES "user" (user_id) ON DELETE CASCADE,
    photo VARCHAR(255) NOT NULL,
    gender gender_enum NOT NULL,
    caregiving_type caregiving_type_enum NOT NULL,
    hourly_rate DECIMAL(10, 2) NOT NULL CHECK (hourly_rate > 0)
);

CREATE INDEX idx_caregiver_caregiving_type ON "caregiver" (caregiving_type);
CREATE INDEX idx_caregiver_city ON "user" (city);


-- MEMBER
CREATE TABLE "member" (
    member_user_id INT PRIMARY KEY REFERENCES "user" (user_id) ON DELETE CASCADE,
	house_rules TEXT NOT NULL
);


-- ADDRESS
CREATE TABLE "address" (
    member_user_id INT PRIMARY KEY REFERENCES "member" (member_user_id) ON DELETE CASCADE,
    house_number VARCHAR(50) NOT NULL,
    street VARCHAR(50) NOT NULL,
    town VARCHAR(50) NOT NULL
);


-- JOB
CREATE TABLE "job" (
    job_id SERIAL PRIMARY KEY,
    member_user_id INT NOT NULL REFERENCES "member" (member_user_id) ON DELETE CASCADE,
    required_caregiving_type caregiving_type_enum NOT NULL,
    other_requirements TEXT,
    date_posted DATE NOT NULL
);

CREATE INDEX idx_job_member_user_id ON "job" (member_user_id);
CREATE INDEX idx_job_caregiving_type ON "job" (required_caregiving_type);


-- JOB APPLICATION
CREATE TABLE "job_application" (
    caregiver_user_id INT NOT NULL,
    job_id INT NOT NULL,
    date_applied DATE NOT NULL,
    PRIMARY KEY (caregiver_user_id, job_id),
    FOREIGN KEY (caregiver_user_id) REFERENCES "caregiver" (caregiver_user_id) ON DELETE CASCADE,
    FOREIGN KEY (job_id) REFERENCES "job" (job_id) ON DELETE CASCADE
);

CREATE INDEX idx_job_application_job_id ON "job_application" (job_id);


-- APPOINTMENT
CREATE TABLE "appointment" (
    appointment_id SERIAL PRIMARY KEY,
    caregiver_user_id INT NOT NULL REFERENCES "caregiver" (caregiver_user_id) ON DELETE CASCADE,
    member_user_id INT NOT NULL REFERENCES "member" (member_user_id) ON DELETE CASCADE,
    appointment_date DATE NOT NULL,
    appointment_time TIME NOT NULL,
    work_hours INT NOT NULL CHECK (work_hours > 0),
    status VARCHAR(20) NOT NULL CHECK (status IN ('Pending', 'Confirmed', 'Declined'))
);

CREATE INDEX idx_appointment_caregiver_user_id ON "appointment" (caregiver_user_id);
CREATE INDEX idx_appointment_member_user_id ON "appointment" (member_user_id);
