INSERT INTO "user" (email, given_name, surname, city, phone_number, profile_description, "password")
VALUES
    ('aida.karimova@nu.edu.kz', 'Aida', 'Karimova', 'Nur-Sultan', '+77011234567', 'Profile description of Aida', 'passwordAida123'),
    ('askar.askarov@nu.edu.kz', 'Askar', 'Askarov', 'Almaty', '+77011234568', 'Profile description of Daulet', 'passwordDaulet123'),
    ('gulnara.satybaldiyeva@nu.edu.kz', 'Gulnara', 'Satybaldiyeva', 'Shymkent', '+77011234569', 'Profile description of Gulnara', 'passwordGulnara123'),
    ('bolat.nurmagambetov@nu.edu.kz', 'Bolat', 'Nurmagambetov', 'Aktau', '+77011234570', 'Profile description of Azamat', 'passwordAzamat123'),
    ('madina.almukhanova@nu.edu.kz', 'Madina', 'Almukhanova', 'Taraz', '+77011234571', 'Profile description of Madina', 'passwordMadina123'),
    ('nursultan.kaliyev@nu.edu.kz', 'Nursultan', 'Kaliyev', 'Astana', '+77011234572', 'Profile description of Nursultan', 'passwordNursultan123'),
    ('zhansaya.abdullayeva@nu.edu.kz', 'Zhansaya', 'Abdullayeva', 'Pavlodar', '+77011234573', 'Profile description of Zhansaya', 'passwordZhansaya123'),
    ('timur.ergaliyev@nu.edu.kz', 'Timur', 'Ergaliyev', 'Kyzylorda', '+77011234574', 'Profile description of Timur', 'passwordTimur123'),
    ('ainur.zhumagaliyeva@nu.edu.kz', 'Ainur', 'Zhumagaliyeva', 'Karaganda', '+77011234575', 'Profile description of Ainur', 'passwordAinur123'),
    ('rakhat.mukhtarov@nu.edu.kz', 'Rakhat', 'Mukhtarov', 'Ust-Kamenogorsk', '+77011234576', 'Profile description of Rakhat', 'passwordRakhat123'),
    ('aliya.iskakova@nu.edu.kz', 'Aliya', 'Iskakova', 'Astana', '+77011234577', 'Profile description of Aliya', 'passwordAliya123'),
    ('daniyar.tolegenov@nu.edu.kz', 'Daniyar', 'Tolegenov', 'Taldykorgan', '+77011234578', 'Profile description of Daniyar', 'passwordDaniyar123'),
    ('laura.sultanova@nu.edu.kz', 'Laura', 'Sultanova', 'Petropavl', '+77011234579', 'Profile description of Laura', 'passwordLaura123'),
    ('bakytzhan.kozhakhmetov@nu.edu.kz', 'Bakytzhan', 'Kozhakhmetov', 'Atyrau', '+77011234580', 'Profile description of Bakytzhan', 'passwordBakytzhan123'),
    ('zhanar.duisenova@nu.edu.kz', 'Zhanar', 'Duisenova', 'Kostanay', '+77011234581', 'Profile description of Zhanar', 'passwordZhanar123'),
    ('erbolat.amanov@nu.edu.kz', 'Erbolat', 'Amanov', 'Astana', '+77021234567', 'Profile description of Erbolat', 'passwordErbolat123'),
    ('anara.sabitova@nu.edu.kz', 'Anara', 'Sabitova', 'Almaty', '+77021234568', 'Profile description of Anara', 'passwordAnara123'),
    ('bolat.bolatov@nu.edu.kz', 'Bolat', 'Bolatov', 'Shymkent', '+77021234569', 'Profile description of Yeldos', 'passwordYeldos123'),
    ('meruyert.tursynova@nu.edu.kz', 'Meruyert', 'Tursynova', 'Aktau', '+77021234570', 'Profile description of Meruyert', 'passwordMeruyert123'),
    ('yeldos.serikov@nu.edu.kz', 'Yeldos', 'Serikov', 'Astana', '+77021234571', 'Profile description of Bolat', 'passwordBolat123');


INSERT INTO "caregiver" (caregiver_user_id, photo, gender, caregiving_type, hourly_rate)
VALUES
    (1, 'photo_url_11.jpg', 'Female', 'ElderlyCare', 1000.00),
    (2, 'photo_url_12.jpg', 'Male', 'ElderlyCare', 1200.00),
    (3, 'photo_url_13.jpg', 'Female', 'SpecialNeedsCare', 1100.00),
    (4, 'photo_url_14.jpg', 'Male', 'NurseCare', 1300.00),
    (5, 'photo_url_15.jpg', 'Female', 'BabySitter', 950.00),
    (6, 'photo_url_16.jpg', 'Male', 'PetCare', 900.00),
    (7, 'photo_url_17.jpg', 'Female', 'Housekeeping', 850.00),
    (8, 'photo_url_18.jpg', 'Male', 'PersonalAssistant', 1400.00),
    (9, 'photo_url_19.jpg', 'Female', 'BabySitter', 1000.00),
    (10, 'photo_url_20.jpg', 'Male', 'ElderlyCare', 1200.00);


INSERT INTO "member" (member_user_id, house_rules)
VALUES
    (11, 'Please remove shoes when entering the house. No pets. No smoking inside. Be kind and respectful.'),
    (12, 'Maintain a quiet environment after 8 PM. No pets allowed in the bedrooms.'),
    (13, 'Always lock the front door when leaving. No loud music or TV after 9 PM.'),
    (14, 'Keep the kitchen clean after use. No pets. Respect privacy in designated areas.'),
    (15, 'No overnight guests allowed. No pets. Please communicate if running late or early.'),
    (16, 'Use coasters for drinks on wooden surfaces. No food in the living room.'),
    (17, 'Clean up spills immediately to avoid staining. Inform us of any damages as soon as they occur.'),
    (18, 'Respect our family’s privacy. Refrain from using the home office space.'),
    (19, 'Do not share our Wi-Fi password with non-residents. Ensure all windows are closed before leaving.'),
    (20, 'Please engage with our children in educational activities. No pets. No screen time for children under 5.');


INSERT INTO "address" (member_user_id, house_number, street, town)
VALUES
    (11, '101', 'Mangilik El', 'Astana'),
    (12, '202', 'Auezov', 'Taldykorgan'),
    (13, '303', 'Baytursynov', 'Petropavl'),
    (14, '404', 'Turan', 'Kozhakhmetov'),
    (15, '505', 'Lenin Avenue', 'Kostanay'),
    (16, '606', 'Turan', 'Astana'),
    (17, '707', 'Abai Avenue', 'Almaty'),
    (18, '808', 'Seyfullin', 'Shymkent'),
    (19, '909', 'Amanzhol', 'Aktau'),
    (20, '1010', 'Bogenbai Batyr', 'Astana');


INSERT INTO "job" (member_user_id, required_caregiving_type, other_requirements, date_posted)
VALUES
    (11, 'ElderlyCare', 'Experience with toddlers preferred, non-smoker, first aid certified.', '2023-11-01'),
    (12, 'ElderlyCare', 'Must be patient, compassionate, and gentle, previous experience required.', '2023-11-02'),
    (13, 'SpecialNeedsCare', 'Knowledge in sign language, flexible schedule.', '2023-11-03'),
    (14, 'NurseCare', 'Professional nursing qualifications, available for night shifts.', '2023-11-04'),
    (15, 'BabySitter', 'Good conversational skills, enjoys board games and reading.', '2023-11-05'),
    (16, 'PetCare', 'Experience with large breeds, available on weekends.', '2023-11-06'),
    (17, 'Housekeeping', 'Attention to detail, reliable and punctual, previous references.', '2023-11-07'),
    (18, 'PersonalAssistant', 'Organizational skills, proficiency in English, driver’s license.', '2023-11-08'),
    (19, 'BabySitter', 'Enjoys arts and crafts, can help with homework, energetic and gentle.', '2023-11-09'),
    (20, 'ElderlyCare', 'Experience with dementia patients, calm demeanor, references.', '2023-11-10');


INSERT INTO "job_application" (caregiver_user_id, job_id, date_applied)
VALUES
    (1, 1, '2023-11-11'),
    (2, 2, '2023-11-12'),
    (3, 3, '2023-11-13'),
    (4, 4, '2023-11-14'),
    (5, 5, '2023-11-15'),
    (6, 6, '2023-11-16'),
    (7, 7, '2023-11-17'),
    (8, 8, '2023-11-18'),
    (9, 9, '2023-11-19'),
    (10, 10, '2023-11-20');


INSERT INTO "appointment" (caregiver_user_id, member_user_id, appointment_date, appointment_time, work_hours, status)
VALUES
    (1, 13, '2023-11-25', '09:00:00', 4, 'Confirmed'),
    (2, 11, '2023-11-26', '10:00:00', 3, 'Declined'),
    (3, 12, '2023-11-27', '14:00:00', 5, 'Pending'),
    (4, 14, '2023-11-28', '08:00:00', 6, 'Confirmed'),
    (5, 15, '2023-11-29', '15:00:00', 4, 'Pending'),
    (1, 16, '2023-11-30', '13:00:00', 3, 'Declined'),
    (7, 17, '2023-12-01', '16:00:00', 2, 'Confirmed'),
    (8, 18, '2023-12-02', '11:00:00', 4, 'Pending'),
    (9, 19, '2023-12-03', '09:30:00', 5, 'Confirmed'),
    (10, 20, '2023-12-04', '12:00:00', 3, 'Declined'),
    (2, 12, '2023-12-05', '10:30:00', 2, 'Confirmed'),
	(3, 19, '2023-12-06', '14:00:00', 4, 'Declined'),
	(4, 18, '2023-12-07', '08:45:00', 3, 'Pending'),
	(5, 17, '2023-12-08', '16:00:00', 5, 'Confirmed'),
	(6, 16, '2023-12-09', '11:30:00', 6, 'Pending'),
	(7, 15, '2023-12-10', '09:00:00', 4, 'Declined'),
	(8, 14, '2023-12-11', '13:15:00', 3, 'Confirmed'),
	(9, 13, '2023-12-12', '17:00:00', 2, 'Pending'),
	(10, 12, '2023-12-13', '12:00:00', 4, 'Confirmed'),
	(1, 11, '2023-12-14', '15:30:00', 3, 'Declined');

