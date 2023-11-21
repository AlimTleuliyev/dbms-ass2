from sqlalchemy import create_engine, text

engine = create_engine('sqlite:///dbms.db')

def populate():
    with open('population.sql', 'r') as f:
        sql_commands = f.read().split(';')
        with engine.connect() as con:
            for command in sql_commands:
                con.execute(text(command.strip() + ';'))
            con.commit()