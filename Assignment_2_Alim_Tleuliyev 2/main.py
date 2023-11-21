from sqlalchemy import create_engine, text

DATABASE_URI = 'postgresql+psycopg2://alimtleuliyev:qwerty@localhost:5432/alimtleuliyev'

engine = create_engine(DATABASE_URI)    

def execute(query, type):
    with engine.connect() as connection:
        try:
            result = connection.execute(query)
            if type == 'select':
                print(tuple(result.keys())) 
                for row in result:
                    print(row)
            elif type == 'update':
                print("Successfully updated")
            elif type == 'delete':
                print("Successfully deleted")
            else:
                raise Exception("Unknown type of query")
            connection.commit()
        except Exception as e:
            print(e)
            connection.rollback()

def execute_queries(title:str, queries: list[tuple[str, str, str]]):
    print(("-"*70 + '\n')*3)
    print(title+'\n')

    for query_title, query_statement, query_type in queries:
        print(query_title)
        execute(text(query_statement), query_type)
        print()
    
        
execute_queries(
    title = "3.1 Update the phone number of Askar Askarov to +77771010001.",
    queries= [
        (
            "Askar Askarovs number before:",
            """
            SELECT given_name, surname, phone_number
            FROM "user"
            WHERE given_name = 'Askar' AND surname = 'Askarov';
            """,
            "select"

        ),
        (
            "Updating...",
            """
            UPDATE "user" 
            SET phone_number = '+77771010001' 
            WHERE given_name = 'Askar' AND surname = 'Askarov';
            """,
            "update"
        ),
        (
            "Askar Askarovs number after:",
            """
            SELECT given_name, surname, phone_number
            FROM "user"
            WHERE given_name = 'Askar' AND surname = 'Askarov';
            """,
            "select"

        )
    ]
)


execute_queries(
    title="3.2 Add $0.5 commission fee to the Caregivers’ hourly rate if it's less than $9, or 10% if it's not.",
    queries = [
        (
            "Caregivers hourly rate before:",
            """
            SELECT c.caregiver_user_id, u.given_name, u.surname, c.hourly_rate
            FROM caregiver c
            LEFT JOIN "user" u ON c.caregiver_user_id = u.user_id
            """,
            "select"
        ),
        (
            "Updating...",
            """
            UPDATE caregiver
            SET hourly_rate = hourly_rate + CASE
                WHEN hourly_rate < 9 * 465 THEN 0.5 * 465
                ELSE hourly_rate * 0.1
            END
            """,
            "update"
        ),
        (
            "Caregivers hourly rate after:",
            """
            SELECT c.caregiver_user_id, u.given_name, u.surname, c.hourly_rate
            FROM caregiver c
            LEFT JOIN "user" u ON c.caregiver_user_id = u.user_id
            """,
            "select"
        )
    ]
)


execute_queries(
    title="4.1 Delete the jobs posted by Bolat Bolatov.",
    queries=[
        (
            "JOBS before deletion:",
            """
            SELECT j.job_id, u.given_name, u.surname
            FROM job j 
            LEFT JOIN "user" u ON j.member_user_id = u.user_id
            """,
            "select"
        ),
        (
            "Deleting...",
            """
            DELETE FROM job
            WHERE job_id IN (
                SELECT job_id
                FROM job
                LEFT JOIN "user" ON member_user_id = user_id
                WHERE given_name = 'Bolat' AND surname = 'Bolatov'
            )
            """,
            "delete"
        ),
        (
            "JOBS after deletion:",
            """
            SELECT j.job_id, u.given_name, u.surname
            FROM job j 
            LEFT JOIN "user" u ON j.member_user_id = u.user_id
            """,
            "select"
        )
    ]
)


execute_queries(
    title="4.2 Delete all members who live on Turan street.",
    queries=[
        (
            "MEMBERS BEFORE:",
            """
            SELECT m.member_user_id, u.given_name, u.surname, a.street
            FROM member m 
            LEFT JOIN "user" u ON m.member_user_id = u.user_id
            LEFT JOIN address a ON m.member_user_id = a.member_user_id
            """,
            "select"
        ),
        (
            "Deleting...",
            """
            DELETE FROM "user"
            WHERE user_id IN (
                SELECT m.member_user_id
                FROM member m
                NATURAL JOIN address a
                WHERE a.street = 'Turan'
            )
            """,
            "delete"
        ),
        (
            "MEMBERS AFTER:",
            """
            SELECT m.member_user_id, u.given_name, u.surname, a.street
            FROM member m 
            LEFT JOIN "user" u ON m.member_user_id = u.user_id
            LEFT JOIN address a ON m.member_user_id = a.member_user_id
            """,
            "select"
        )
    ]
)


execute_queries(
    title="5.1 Select caregiver and member names for the accepted appointments.",
    queries=[
        (
            "Selecting...",
            """
            SELECT c.given_name AS caregiver_name, m.given_name AS member_name
            FROM appointment a
            LEFT JOIN "user" c ON a.caregiver_user_id = c.user_id
            LEFT JOIN "user" m ON a.member_user_id = m.user_id
            WHERE a.status = 'Confirmed';
            """,
            "select"
        )
    ]
)

execute_queries(
    title="5.2 List job ids that contain ‘gentle’ in their other requirements.",
    queries=[
        (
            "Selecting...",
            r"""
            SELECT job_id
            FROM job
            WHERE other_requirements LIKE '%gentle%';
            """,
            "select"
        )
    ]
)

execute_queries(
    title="5.3 List the work hours of Baby Sitter positions.",
    queries=[
        (
            "Selecting...",
            """
            SELECT a.caregiver_user_id, u.given_name, u.surname, SUM(a.work_hours)
            FROM appointment a
            LEFT JOIN caregiver c ON a.caregiver_user_id = c.caregiver_user_id
            LEFT JOIN "user" u ON a.caregiver_user_id = u.user_id
            WHERE c.caregiving_type = 'BabySitter'
            GROUP BY a.caregiver_user_id, u.given_name, u.surname;
            """,
            "select"
        )
    ]
)

execute_queries(
    title="5.4 List the members who are looking for Elderly Care in Astana and have “No pets.” rule.",
    queries=[
        (
            "Selecting...",
            """
            SELECT u.given_name AS member_name 
            FROM member m
            LEFT JOIN "user" u ON m.member_user_id = u.user_id
            LEFT JOIN job j ON m.member_user_id = j.member_user_id
            LEFT JOIN address a ON m.member_user_id = a.member_user_id
            WHERE j.required_caregiving_type = 'ElderlyCare' and a.town = 'Astana' and m.house_rules LIKE '%No pets.%';
            """,
            "select"
        )
    ]
)


execute_queries(
    title="6.1 Count the number of applicants for each job posted by a member (multiple joins with aggregation)",
    queries=[
        (
            "Selecting...",
            """
            SELECT j.member_user_id, u.given_name, u.surname, j.job_id, COUNT(ja.caregiver_user_id) AS applicants_count
            FROM job j
            LEFT JOIN job_application ja ON j.job_id = ja.job_id
            LEFT JOIN "user" u ON j.member_user_id = u.user_id
            GROUP BY j.member_user_id, u.given_name, u.surname, j.job_id;
            """,
            "select"
        )
    ]
)


execute_queries(
    title="6.2 Total hours spent by care givers for all accepted appointments (multiple joins with aggregation)",
    queries=[
        (
            "Selecting...",
            """
            SELECT a.caregiver_user_id, u.given_name, u.surname, SUM(a.work_hours) AS total_hours
            FROM appointment a
            LEFT JOIN "user" u ON a.caregiver_user_id = u.user_id
            WHERE a.status = 'Confirmed'
            GROUP BY a.caregiver_user_id, u.given_name, u.surname;
            """,
            "select"
        )
    ]
)


execute_queries(
    title="6.3 Average pay of caregivers based on accepted appointments (join with aggregation)",
    queries=[
        (
            "Selecting...",
            """
            SELECT a.caregiver_user_id, u.given_name, u.surname, AVG(a.work_hours * c.hourly_rate) AS average_pay
            FROM appointment a
            LEFT JOIN caregiver c ON a.caregiver_user_id = c.caregiver_user_id
            LEFT JOIN "user" u ON a.caregiver_user_id = u.user_id
            WHERE a.status = 'Confirmed'
            GROUP BY a.caregiver_user_id, u.given_name, u.surname;
            """,
            "select"
        )
    ]
)


execute_queries(
    title="6.4 Caregivers who earn above average based on accepted appointments (multiple join with aggregation and nested query)",
    queries=[
        (
            "Selecting...",
            """
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
            """,
            "select"
        )
    ]
)


execute_queries(
    title="7.1 Calculate the total cost to pay for a caregiver for all accepted appointments.",
    queries=[
        (
            "Selecting...",
            """
            SELECT a.caregiver_user_id, u.given_name, u.surname, SUM(a.work_hours * c.hourly_rate) AS total_pay
            FROM appointment a
            LEFT JOIN caregiver c ON a.caregiver_user_id = c.caregiver_user_id
            LEFT JOIN "user" u ON a.caregiver_user_id = u.user_id
            WHERE a.status = 'Confirmed'
            GROUP BY a.caregiver_user_id, u.given_name, u.surname;
            """,
            "select"
        )
    ]
)


execute_queries(
    title="8.1 View all job applications and the applicants",
    queries=[
        (
            "Selecting...",
            """
            SELECT ja.job_id, ja.caregiver_user_id, u.given_name, u.surname
            FROM job_application ja
            LEFT JOIN "user" u ON ja.caregiver_user_id = u.user_id;
            """,
            "select"
        )
    ]
)

# Output:
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------

# 3.1 Update the phone number of Askar Askarov to +77771010001.

# Askar Askarovs number before:
# ('given_name', 'surname', 'phone_number')
# ('Askar', 'Askarov', '+77011234568')

# Updating...
# Successfully updated

# Askar Askarovs number after:
# ('given_name', 'surname', 'phone_number')
# ('Askar', 'Askarov', '+77771010001')

# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------

# 3.2 Add $0.5 commission fee to the Caregivers’ hourly rate if it's less than $9, or 10% if it's not.

# Caregivers hourly rate before:
# ('caregiver_user_id', 'given_name', 'surname', 'hourly_rate')
# (1, 'Aida', 'Karimova', Decimal('1000.00'))
# (2, 'Askar', 'Askarov', Decimal('1200.00'))
# (3, 'Gulnara', 'Satybaldiyeva', Decimal('1100.00'))
# (4, 'Bolat', 'Nurmagambetov', Decimal('1300.00'))
# (5, 'Madina', 'Almukhanova', Decimal('950.00'))
# (6, 'Nursultan', 'Kaliyev', Decimal('900.00'))
# (7, 'Zhansaya', 'Abdullayeva', Decimal('850.00'))
# (8, 'Timur', 'Ergaliyev', Decimal('1400.00'))
# (9, 'Ainur', 'Zhumagaliyeva', Decimal('1000.00'))
# (10, 'Rakhat', 'Mukhtarov', Decimal('1200.00'))

# Updating...
# Successfully updated

# Caregivers hourly rate after:
# ('caregiver_user_id', 'given_name', 'surname', 'hourly_rate')
# (1, 'Aida', 'Karimova', Decimal('1232.50'))
# (2, 'Askar', 'Askarov', Decimal('1432.50'))
# (3, 'Gulnara', 'Satybaldiyeva', Decimal('1332.50'))
# (4, 'Bolat', 'Nurmagambetov', Decimal('1532.50'))
# (5, 'Madina', 'Almukhanova', Decimal('1182.50'))
# (6, 'Nursultan', 'Kaliyev', Decimal('1132.50'))
# (7, 'Zhansaya', 'Abdullayeva', Decimal('1082.50'))
# (8, 'Timur', 'Ergaliyev', Decimal('1632.50'))
# (9, 'Ainur', 'Zhumagaliyeva', Decimal('1232.50'))
# (10, 'Rakhat', 'Mukhtarov', Decimal('1432.50'))

# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------

# 4.1 Delete the jobs posted by Bolat Bolatov.

# JOBS before deletion:
# ('job_id', 'given_name', 'surname')
# (1, 'Aliya', 'Iskakova')
# (2, 'Daniyar', 'Tolegenov')
# (3, 'Laura', 'Sultanova')
# (4, 'Bakytzhan', 'Kozhakhmetov')
# (5, 'Zhanar', 'Duisenova')
# (6, 'Erbolat', 'Amanov')
# (7, 'Anara', 'Sabitova')
# (8, 'Bolat', 'Bolatov')
# (9, 'Meruyert', 'Tursynova')
# (10, 'Yeldos', 'Serikov')

# Deleting...
# Successfully deleted

# JOBS after deletion:
# ('job_id', 'given_name', 'surname')
# (1, 'Aliya', 'Iskakova')
# (2, 'Daniyar', 'Tolegenov')
# (3, 'Laura', 'Sultanova')
# (4, 'Bakytzhan', 'Kozhakhmetov')
# (5, 'Zhanar', 'Duisenova')
# (6, 'Erbolat', 'Amanov')
# (7, 'Anara', 'Sabitova')
# (9, 'Meruyert', 'Tursynova')
# (10, 'Yeldos', 'Serikov')

# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------

# 4.2 Delete all members who live on Turan street.

# MEMBERS BEFORE:
# ('member_user_id', 'given_name', 'surname', 'street')
# (11, 'Aliya', 'Iskakova', 'Mangilik El')
# (12, 'Daniyar', 'Tolegenov', 'Auezov')
# (13, 'Laura', 'Sultanova', 'Baytursynov')
# (14, 'Bakytzhan', 'Kozhakhmetov', 'Turan')
# (15, 'Zhanar', 'Duisenova', 'Lenin Avenue')
# (16, 'Erbolat', 'Amanov', 'Turan')
# (17, 'Anara', 'Sabitova', 'Abai Avenue')
# (18, 'Bolat', 'Bolatov', 'Seyfullin')
# (19, 'Meruyert', 'Tursynova', 'Amanzhol')
# (20, 'Yeldos', 'Serikov', 'Bogenbai Batyr')

# Deleting...
# Successfully deleted

# MEMBERS AFTER:
# ('member_user_id', 'given_name', 'surname', 'street')
# (11, 'Aliya', 'Iskakova', 'Mangilik El')
# (12, 'Daniyar', 'Tolegenov', 'Auezov')
# (13, 'Laura', 'Sultanova', 'Baytursynov')
# (15, 'Zhanar', 'Duisenova', 'Lenin Avenue')
# (17, 'Anara', 'Sabitova', 'Abai Avenue')
# (18, 'Bolat', 'Bolatov', 'Seyfullin')
# (19, 'Meruyert', 'Tursynova', 'Amanzhol')
# (20, 'Yeldos', 'Serikov', 'Bogenbai Batyr')

# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------

# 5.1 Select caregiver and member names for the accepted appointments.

# Selecting...
# ('caregiver_name', 'member_name')
# ('Askar', 'Daniyar')
# ('Rakhat', 'Daniyar')
# ('Aida', 'Laura')
# ('Zhansaya', 'Anara')
# ('Madina', 'Anara')
# ('Ainur', 'Meruyert')

# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------

# 5.2 List job ids that contain ‘gentle’ in their other requirements.

# Selecting...
# ('job_id',)
# (2,)
# (9,)

# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------

# 5.3 List the work hours of Baby Sitter positions.

# Selecting...
# ('caregiver_user_id', 'given_name', 'surname', 'sum')
# (5, 'Madina', 'Almukhanova', 9)
# (9, 'Ainur', 'Zhumagaliyeva', 7)

# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------

# 5.4 List the members who are looking for Elderly Care in Astana and have “No pets.” rule.

# Selecting...
# ('member_name',)
# ('Aliya',)
# ('Yeldos',)

# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------

# 6.1 Count the number of applicants for each job posted by a member (multiple joins with aggregation)

# Selecting...
# ('member_user_id', 'given_name', 'surname', 'job_id', 'applicants_count')
# (20, 'Yeldos', 'Serikov', 10, 1)
# (17, 'Anara', 'Sabitova', 7, 1)
# (19, 'Meruyert', 'Tursynova', 9, 1)
# (13, 'Laura', 'Sultanova', 3, 1)
# (15, 'Zhanar', 'Duisenova', 5, 1)
# (11, 'Aliya', 'Iskakova', 1, 1)
# (12, 'Daniyar', 'Tolegenov', 2, 1)

# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------

# 6.2 Total hours spent by care givers for all accepted appointments (multiple joins with aggregation)

# Selecting...
# ('caregiver_user_id', 'given_name', 'surname', 'total_hours')
# (1, 'Aida', 'Karimova', 4)
# (2, 'Askar', 'Askarov', 2)
# (5, 'Madina', 'Almukhanova', 5)
# (7, 'Zhansaya', 'Abdullayeva', 2)
# (9, 'Ainur', 'Zhumagaliyeva', 5)
# (10, 'Rakhat', 'Mukhtarov', 4)

# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------

# 6.3 Average pay of caregivers based on accepted appointments (join with aggregation)

# Selecting...
# ('caregiver_user_id', 'given_name', 'surname', 'average_pay')
# (1, 'Aida', 'Karimova', Decimal('4930.0000000000000000'))
# (2, 'Askar', 'Askarov', Decimal('2865.0000000000000000'))
# (5, 'Madina', 'Almukhanova', Decimal('5912.5000000000000000'))
# (7, 'Zhansaya', 'Abdullayeva', Decimal('2165.0000000000000000'))
# (9, 'Ainur', 'Zhumagaliyeva', Decimal('6162.5000000000000000'))
# (10, 'Rakhat', 'Mukhtarov', Decimal('5730.0000000000000000'))

# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------

# 6.4 Caregivers who earn above average based on accepted appointments (multiple join with aggregation and nested query)

# Selecting...
# ('caregiver_user_id', 'given_name', 'surname', 'average_pay')
# (1, 'Aida', 'Karimova', Decimal('4930.0000000000000000'))
# (5, 'Madina', 'Almukhanova', Decimal('5912.5000000000000000'))
# (9, 'Ainur', 'Zhumagaliyeva', Decimal('6162.5000000000000000'))
# (10, 'Rakhat', 'Mukhtarov', Decimal('5730.0000000000000000'))

# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------

# 7.1 Calculate the total cost to pay for a caregiver for all accepted appointments.

# Selecting...
# ('caregiver_user_id', 'given_name', 'surname', 'total_pay')
# (1, 'Aida', 'Karimova', Decimal('4930.00'))
# (2, 'Askar', 'Askarov', Decimal('2865.00'))
# (5, 'Madina', 'Almukhanova', Decimal('5912.50'))
# (7, 'Zhansaya', 'Abdullayeva', Decimal('2165.00'))
# (9, 'Ainur', 'Zhumagaliyeva', Decimal('6162.50'))
# (10, 'Rakhat', 'Mukhtarov', Decimal('5730.00'))

# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------

# 8.1 View all job applications and the applicants

# Selecting...
# ('job_id', 'caregiver_user_id', 'given_name', 'surname')
# (1, 1, 'Aida', 'Karimova')
# (2, 2, 'Askar', 'Askarov')
# (3, 3, 'Gulnara', 'Satybaldiyeva')
# (5, 5, 'Madina', 'Almukhanova')
# (7, 7, 'Zhansaya', 'Abdullayeva')
# (9, 9, 'Ainur', 'Zhumagaliyeva')
# (10, 10, 'Rakhat', 'Mukhtarov')