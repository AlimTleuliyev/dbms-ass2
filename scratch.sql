SELECT job_id
FROM job
LEFT JOIN "user" ON member_user_id = user_id
WHERE given_name = 'Bolat' AND surname = 'Bolatov'


SELECT * FROM "user" 
SELECT * FROM address
SELECT * FROM member


DELETE FROM "user"
WHERE user_id 

SELECT m.member_user_id
FROM member m
NATURAL JOIN address a
WHERE a.street = 'Turan'


SELECT c.given_name AS caregiver_name, m.given_name AS member_name
FROM appointment a
LEFT JOIN "user" c ON a.caregiver_user_id = c.user_id
LEFT JOIN "user" m ON a.member_user_id = m.user_id
WHERE a.status = 'Confirmed';

SELECT job_id
FROM job
WHERE other_requirements LIKE '% in %';

INSERT INTO job_application (caregiver_user_id, job_id, date_applied) VALUES (6, 11, '2023-11-11')
INSERT INTO job (member_user_id, required_caregiving_type, other_requirements, date_posted) 
VALUES
	(19, 'Elderly Care', 'Experience with dementia patients, calm demeanor, references.', '2023-11-10');


SELECT j.member_user_id, j.job_id, COUNT(ja.caregiver_user_id) AS applicants_count
FROM job j
LEFT JOIN job_application ja ON j.job_id = ja.job_id
GROUP BY j.member_user_id, j.job_id 
ORDER BY j.member_user_id, j.job_id;


SELECT a.caregiver_user_id, u.given_name, u.surname, SUM(a.work_hours) AS total_hours
FROM appointment a
LEFT JOIN "user" u ON a.caregiver_user_id = u.user_id
WHERE a.status = 'Confirmed'
GROUP BY a.caregiver_user_id, u.given_name, u.surname;
	
SELECT a.caregiver_user_id, u.given_name, u.surname, AVG(a.work_hours * c.hourly_rate) AS average_pay
FROM appointment a
LEFT JOIN caregiver c ON a.caregiver_user_id = c.caregiver_user_id
LEFT JOIN "user" u ON a.caregiver_user_id = u.user_id
WHERE a.status = 'Confirmed'
GROUP BY a.caregiver_user_id, u.given_name, u.surname;
	
	

SELECT t.caregiver_user_id, t.given_name, t.surname, t.average_pay
FROM (
	SELECT a.caregiver_user_id, u.given_name, u.surname, AVG(a.work_hours * c.hourly_rate) AS average_pay
	FROM appointment a
	LEFT JOIN caregiver c ON a.caregiver_user_id = c.caregiver_user_id
	LEFT JOIN "user" u ON a.caregiver_user_id = u.user_id
	WHERE a.status = 'Confirmed'
	GROUP BY a.caregiver_user_id, u.given_name, u.surname
) t
WHERE t.average_pay > (
	SELECT AVG(a.work_hours * c.hourly_rate) AS average_pay
	FROM appointment a
	LEFT JOIN caregiver c ON a.caregiver_user_id = c.caregiver_user_id
	WHERE a.status = 'Confirmed'
);

SELECT a.caregiver_user_id, u.given_name, u.surname, SUM(a.work_hours * c.hourly_rate) AS total_pay
FROM appointment a
LEFT JOIN caregiver c ON a.caregiver_user_id = c.caregiver_user_id
LEFT JOIN "user" u ON a.caregiver_user_id = u.user_id
WHERE a.status = 'Confirmed'
GROUP BY a.caregiver_user_id, u.given_name, u.surname;

SELECT ja.job_id, ja.caregiver_user_id, u.given_name, u.surname
FROM job_application ja
LEFT JOIN "user" u ON ja.caregiver_user_id = u.user_id;

SELECT *
FROM address

SELECT *
FROM caregiver

SELECT j.job_id, u.given_name, u.surname
FROM job j 
LEFT JOIN "user" u ON j.member_user_id = u.user_id

SELECT m.member_user_id, u.given_name, u.surname, a.street
FROM member m 
LEFT JOIN "user" u ON m.member_user_id = u.user_id
LEFT JOIN address a ON m.member_user_id = a.member_user_id

DO
$do$
DECLARE
   r RECORD;
BEGIN
   FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = current_schema()) LOOP
      EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(r.tablename) || ' CASCADE';
   END LOOP;
END
$do$;